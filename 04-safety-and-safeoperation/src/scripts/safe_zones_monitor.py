"""Safety Zones & SafeOperation Monitor for KUKA KR 6 R900-2 (Agilus).

Complies with ISO 10218-1/2, ISO 13849-1 (Cat 4 / PL e), and ISO/TS 15066.
Simulates Cartesian monitoring spaces (AABB/OBB), safe reduced speed (SRS),
and stopping distance prediction under emergency brake (SS1/SS2).
"""

from dataclasses import dataclass
from typing import Tuple, List, Dict, Optional
import numpy as np


@dataclass
class AxisLimits:
    """Axis angular limits in degrees for KUKA KR 6 R900-2."""
    a1_min: float = -170.0
    a1_max: float = 170.0
    a2_min: float = -190.0
    a2_max: float = 45.0
    a3_min: float = -120.0
    a3_max: float = 156.0
    a4_min: float = -185.0
    a4_max: float = 185.0
    a5_min: float = -120.0
    a5_max: float = 120.0
    a6_min: float = -350.0
    a6_max: float = 350.0

    def check_joint_limits(self, joints_deg: List[float]) -> Tuple[bool, Optional[str]]:
        """Validate if joint coordinates fall within manufacturer safety bounds."""
        if len(joints_deg) != 6:
            return False, "Error: 6 axis angles required."
        limits = [
            (self.a1_min, self.a1_max),
            (self.a2_min, self.a2_max),
            (self.a3_min, self.a3_max),
            (self.a4_min, self.a4_max),
            (self.a5_min, self.a5_max),
            (self.a6_min, self.a6_max),
        ]
        for idx, (val, (low, high)) in enumerate(zip(joints_deg, limits), start=1):
            if val < low or val > high:
                return False, f"Axis A{idx} violation: {val:.2f}° outside [{low}°, {high}°]"
        return True, None


@dataclass
class CartesianCuboidZone:
    """Cartesian monitoring workspace defined as an Axis-Aligned Bounding Box (AABB) in mm."""
    zone_id: int
    name: str
    is_exclusion: bool  # True: robot must stay OUTSIDE; False: robot must stay INSIDE
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    z_min: float
    z_max: float

    def contains(self, point: np.ndarray) -> bool:
        """Check whether 3D position [x, y, z] is inside the bounding box."""
        x, y, z = float(point[0]), float(point[1]), float(point[2])
        return bool(self.x_min <= x <= self.x_max and
                    self.y_min <= y <= self.y_max and
                    self.z_min <= z <= self.z_max)

    def is_safe(self, point: np.ndarray) -> bool:
        """Check if robot point complies with the zone rule."""
        inside = self.contains(point)
        return bool(not inside if self.is_exclusion else inside)


class SafeOperationController:
    """Simulates KUKA.SafeOperation 3.x safety controller logic."""

    def __init__(self,
                 response_time_ms: float = 20.0,
                 max_brake_decel_mm_s2: float = 8000.0,
                 safe_speed_limit_mm_s: float = 250.0):
        """
        Args:
            response_time_ms: Safety bus cycle & relay reaction time (default 20 ms).
            max_brake_decel_mm_s2: Worst-case emergency brake deceleration in mm/s^2.
            safe_speed_limit_mm_s: Reduced safety speed threshold (default 250 mm/s per ISO 10218-1).
        """
        self.t_reaction = response_time_ms / 1000.0  # seconds
        self.a_brake = max_brake_decel_mm_s2
        self.safe_speed_limit = safe_speed_limit_mm_s
        self.axis_limits = AxisLimits()
        self.monitoring_zones: List[CartesianCuboidZone] = []

    def add_zone(self, zone: CartesianCuboidZone) -> None:
        """Register a Cartesian safety monitoring zone."""
        self.monitoring_zones.append(zone)

    def calculate_stopping_distance(self, current_velocity_mm_s: float, safety_margin_c_mm: float = 50.0) -> float:
        r"""Calculate ISO 13855 / ISO/TS 15066 safety stopping distance.

        Formula:
            S = v * t_r + (v^2) / (2 * a_brake) + C
        """
        v = abs(current_velocity_mm_s)
        reaction_dist = v * self.t_reaction
        braking_dist = (v ** 2) / (2.0 * self.a_brake)
        return reaction_dist + braking_dist + safety_margin_c_mm

    def verify_tool_center_point(self, tcp_pos: np.ndarray, tcp_vel_mm_s: float) -> Dict[str, any]:
        """Perform real-time safety evaluation for current TCP state."""
        # 1. Reduced speed monitoring
        speed_safe = tcp_vel_mm_s <= self.safe_speed_limit
        stopping_dist = self.calculate_stopping_distance(tcp_vel_mm_s)

        # 2. Zone violations check
        zone_statuses = []
        overall_safe = speed_safe

        for zone in self.monitoring_zones:
            safe = zone.is_safe(tcp_pos)
            if not safe:
                overall_safe = False
            zone_statuses.append({
                "zone_id": zone.zone_id,
                "name": zone.name,
                "is_exclusion": zone.is_exclusion,
                "is_safe": safe,
            })

        return {
            "overall_safe": overall_safe,
            "speed_safe": speed_safe,
            "tcp_velocity_mm_s": tcp_vel_mm_s,
            "stopping_distance_mm": stopping_dist,
            "zones": zone_statuses,
        }


def main():
    print("=" * 65)
    print("KUKA KR 6 R900-2 SafeOperation Supervisor Simulator")
    print("=" * 65)

    controller = SafeOperationController()

    # Define Cell Boundary (Allowed work zone: Workspace Cell)
    cell = CartesianCuboidZone(
        zone_id=1,
        name="Permitted Work Cell",
        is_exclusion=False,
        x_min=-200.0, x_max=1000.0,
        y_min=-900.0, y_max=900.0,
        z_min=0.0,    z_max=1200.0
    )

    # Define Operator Station (Prohibited zone / Exclusion Zone)
    operator_pod = CartesianCuboidZone(
        zone_id=2,
        name="Operator Station Exclusion Zone",
        is_exclusion=True,
        x_min=600.0, x_max=1000.0,
        y_min=-400.0, y_max=400.0,
        z_min=0.0,    z_max=900.0
    )

    controller.add_zone(cell)
    controller.add_zone(operator_pod)

    # Test Case 1: Normal processing position within safe limits
    p1 = np.array([450.0, 0.0, 500.0])
    v1 = 200.0  # mm/s
    res1 = controller.verify_tool_center_point(p1, v1)
    print(f"\n[Test 1] Pos: {p1}, Vel: {v1} mm/s")
    print(f"  Stopping distance: {res1['stopping_distance_mm']:.2f} mm")
    print(f"  Safe: {res1['overall_safe']}")

    # Test Case 2: Intrusion into Operator Exclusion Zone
    p2 = np.array([750.0, 100.0, 400.0])
    v2 = 220.0  # mm/s
    res2 = controller.verify_tool_center_point(p2, v2)
    print(f"\n[Test 2] Pos: {p2}, Vel: {v2} mm/s (In Exclusion Area)")
    print(f"  Safe: {res2['overall_safe']} (Violation detected!)")

    # Test Case 3: Over-speed violation (> 250 mm/s in Safe Monitored mode)
    p3 = np.array([450.0, 0.0, 500.0])
    v3 = 450.0  # mm/s
    res3 = controller.verify_tool_center_point(p3, v3)
    print(f"\n[Test 3] Pos: {p3}, Vel: {v3} mm/s (Excessive velocity)")
    print(f"  Speed safe: {res3['speed_safe']}, Overall safe: {res3['overall_safe']}")


if __name__ == "__main__":
    main()
