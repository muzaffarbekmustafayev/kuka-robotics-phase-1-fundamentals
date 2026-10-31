"""
===============================================================================
KUKA KR 6 R900-2 Workspace Envelope & Stopping Distance Safety Analyzer
Course: KUKA Industrial Robotics | Phase 1: Fundamentals (Lesson 01)
Academic Partners: Samarkand State University & Tomsk State University
Author: Muzaffarbek Mustafayev

All code, function signatures, docstrings, and comments are in English.
===============================================================================
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np


@dataclass(frozen=True)
class KR6R900Dimensions:
    """Mechanical link dimensions of KUKA KR 6 R900-2 (KR AGILUS-2) in millimeters."""
    d1_base_height: float = 400.0        # Ground to Axis 2 center (mm)
    a1_shoulder_offset: float = 25.0     # Axis 1 to Axis 2 horizontal offset (mm)
    a2_upper_arm: float = 455.0          # Axis 2 to Axis 3 length (mm)
    a3_elbow_offset: float = 35.0        # Axis 3 to Axis 4 horizontal offset (mm)
    d4_forearm: float = 420.0            # Axis 3 to Axis 5 wrist intersection (mm)
    d6_flange: float = 80.0              # Axis 5 to mechanical tool flange (mm)
    rated_payload_kg: float = 6.0        # Rated payload capacity (kg)
    nominal_reach_mm: float = 901.5      # Official maximum reach (mm)


@dataclass(frozen=True)
class AxisLimits:
    """Software joint limits (degrees) and max angular velocities (deg/s)."""
    q_min: Tuple[float, ...] = (-170.0, -190.0, -120.0, -185.0, -120.0, -350.0)
    q_max: Tuple[float, ...] = (170.0, 45.0, 156.0, 185.0, 120.0, 350.0)
    v_max_deg_s: Tuple[float, ...] = (360.0, 300.0, 360.0, 381.0, 388.0, 615.0)


class WorkspaceKinematics:
    """Computes geometric reach envelopes, forward kinematics, and workspace boundaries."""

    def __init__(self, dims: KR6R900Dimensions = KR6R900Dimensions()):
        self.dims = dims
        self.limits = AxisLimits()

    def compute_theoretical_reach(self) -> Dict[str, float]:
        """
        Calculates theoretical maximum and minimum reach based on link geometry.
        
        Theorem (Triangle Inequality Reach Bound):
        The maximum distance from the shoulder pivot to the wrist center is:
            R_wc_max = a2 + sqrt(a3^2 + d4^2)
        The maximum distance from base origin to mechanical flange is:
            R_flange_max = sqrt((a1 + a2 + a3)^2 + (d4 + d6)^2)
        """
        forearm_hypotenuse = np.sqrt(self.dims.a3_elbow_offset**2 + self.dims.d4_forearm**2)
        r_wc_max = self.dims.a2_upper_arm + forearm_hypotenuse
        r_wc_min = abs(self.dims.a2_upper_arm - forearm_hypotenuse)
        
        # Flange maximum reach in fully stretched horizontal configuration
        x_max_reach = self.dims.a1_shoulder_offset + self.dims.a2_upper_arm + self.dims.a3_elbow_offset
        z_reach_offset = self.dims.d4_forearm + self.dims.d6_flange
        r_flange_nominal = np.sqrt(x_max_reach**2 + z_reach_offset**2)

        return {
            "wrist_center_max_reach_mm": float(r_wc_max),
            "wrist_center_min_reach_mm": float(r_wc_min),
            "flange_nominal_reach_mm": float(r_flange_nominal),
            "catalog_reach_mm": self.dims.nominal_reach_mm,
        }

    def forward_kinematics_position(self, q_deg: np.ndarray) -> np.ndarray:
        """
        Computes 3D position [X, Y, Z] (mm) of mechanical flange using standard DH composition.
        
        Args:
            q_deg: Array of 6 joint angles in degrees.
        Returns:
            np.ndarray: [X, Y, Z] position of tool flange center in robot base frame.
        """
        q_rad = np.radians(q_deg)
        d = self.dims

        dh_table = [
            (q_rad[0], d.d1_base_height, d.a1_shoulder_offset, -np.pi / 2),
            (q_rad[1] - np.pi / 2, 0.0, d.a2_upper_arm, 0.0),
            (q_rad[2], 0.0, d.a3_elbow_offset, np.pi / 2),
            (q_rad[3], d.d4_forearm, 0.0, -np.pi / 2),
            (q_rad[4], 0.0, 0.0, np.pi / 2),
            (q_rad[5] + np.pi, d.d6_flange, 0.0, np.pi),
        ]

        T = np.eye(4)
        for theta, offset_d, length_a, alpha in dh_table:
            ct, st = np.cos(theta), np.sin(theta)
            ca, sa = np.cos(alpha), np.sin(alpha)
            Ai = np.array([
                [ct, -st * ca,  st * sa, length_a * ct],
                [st,  ct * ca, -ct * sa, length_a * st],
                [0.0,      sa,       ca,      offset_d],
                [0.0,     0.0,      0.0,           1.0]
            ])
            T = T @ Ai

        return T[:3, 3]

    def sample_workspace_monte_carlo(self, num_samples: int = 5000, random_seed: int = 42) -> np.ndarray:
        """
        Generates a Monte Carlo point cloud of reachable Cartesian positions within joint limits.
        
        Args:
            num_samples: Number of random joint configurations to evaluate.
            random_seed: Random seed for reproducible evaluation.
        Returns:
            np.ndarray: (num_samples, 3) matrix of reachable XYZ coordinates in mm.
        """
        np.random.seed(random_seed)
        q_min = np.array(self.limits.q_min)
        q_max = np.array(self.limits.q_max)

        random_joints = np.random.uniform(q_min, q_max, size=(num_samples, 6))
        points = np.zeros((num_samples, 3), dtype=np.float64)

        for i in range(num_samples):
            points[i] = self.forward_kinematics_position(random_joints[i])

        return points


class SafetyBrakingCalculus:
    """
    Computes emergency stopping distances and safety clearance zones under ISO 10218-1 & ISO 13849-1.
    """

    def __init__(self, t_reaction_sec: float = 0.030, a_brake_max_m_s2: float = 8.5):
        """
        Args:
            t_reaction_sec: Safety PLC / controller response and bus cycle latency (default 30 ms).
            a_brake_max_m_s2: Worst-case mechanical deceleration under full emergency braking.
        """
        self.t_reaction = t_reaction_sec
        self.a_brake = a_brake_max_m_s2

    def compute_stopping_distance(self, v_initial_m_s: float, stop_category: int = 1) -> Dict[str, float]:
        """
        Calculates stopping distance and stopping time for Stop Category 0 and Category 1.
        
        Formula:
            s_reaction = v_0 * t_reaction
            s_decel = v_0^2 / (2 * a_brake)
            s_total = s_reaction + s_decel
            t_total = t_reaction + (v_0 / a_brake)
        """
        # For Stop 0, mechanical friction brake engaging delay is modeled
        t_delay = self.t_reaction if stop_category == 1 else self.t_reaction + 0.020
        
        s_reaction = v_initial_m_s * t_delay
        s_decel = (v_initial_m_s**2) / (2.0 * self.a_brake)
        s_total = s_reaction + s_decel
        t_total = t_delay + (v_initial_m_s / self.a_brake)

        return {
            "initial_velocity_m_s": v_initial_m_s,
            "reaction_distance_mm": float(s_reaction * 1000.0),
            "braking_distance_mm": float(s_decel * 1000.0),
            "total_stopping_distance_mm": float(s_total * 1000.0),
            "total_stopping_time_ms": float(t_total * 1000.0),
            "stop_category": stop_category,
        }

    def compute_safety_fence_radius(self, max_reach_mm: float = 901.5, tool_length_mm: float = 150.0,
                                     max_velocity_m_s: float = 2.0, margin_mm: float = 200.0) -> float:
        """
        Calculates minimum safety perimeter distance according to ISO 13857 and ISO 10218-2.
        
        Formula:
            R_fence >= R_max + L_tool + s_stop(v_max) + Margin
        """
        stop_metrics = self.compute_stopping_distance(max_velocity_m_s, stop_category=1)
        r_fence = max_reach_mm + tool_length_mm + stop_metrics["total_stopping_distance_mm"] + margin_mm
        return float(r_fence)


def print_analytical_report():
    """Generates an industrial CLI report for KUKA KR 6 R900-2 workspace and safety metrics."""
    ws = WorkspaceKinematics()
    reach = ws.compute_theoretical_reach()
    safety = SafetyBrakingCalculus()

    print("=" * 78)
    print(" KUKA KR 6 R900-2 (KR AGILUS) WORKSPACE & SAFETY METRICS REPORT")
    print(" Course: KUKA Industrial Robotics | Phase 1 (Lesson 01)")
    print("=" * 78)
    print(f" Rated Payload:                {ws.dims.rated_payload_kg:.1f} kg")
    print(f" Catalog Maximum Reach:        {ws.dims.nominal_reach_mm:.1f} mm")
    print(f" Analytical Wrist Center Reach:{reach['wrist_center_max_reach_mm']:.2f} mm")
    print(f" Analytical Flange Reach:      {reach['flange_nominal_reach_mm']:.2f} mm")
    print(f" Inner Wrist Dead-Zone Radius: {reach['wrist_center_min_reach_mm']:.2f} mm")
    print("-" * 78)
    print(" EMERGENCY STOPPING DISTANCE CALCULATIONS (ISO 10218-1)")
    print("-" * 78)
    print(" Speed [m/s] | Mode        | Reaction [mm] | Braking [mm] | Total Stop [mm] | Time [ms]")
    print("-" * 78)

    test_velocities = [
        (0.25, "T1 (Reduced)", 1),
        (0.50, "Manual Test ", 1),
        (1.00, "Automatic 50%", 1),
        (2.00, "Automatic 100%", 1),
        (2.00, "Stop 0 (E-Stop)", 0),
    ]

    for v, mode_name, cat in test_velocities:
        m = safety.compute_stopping_distance(v, stop_category=cat)
        print(f" {v:11.2f} | {mode_name:11s} | {m['reaction_distance_mm']:13.1f} | "
              f"{m['braking_distance_mm']:12.1f} | {m['total_stopping_distance_mm']:15.1f} | "
              f"{m['total_stopping_time_ms']:9.1f}")

    fence_radius = safety.compute_safety_fence_radius(
        max_reach_mm=ws.dims.nominal_reach_mm,
        tool_length_mm=120.0,
        max_velocity_m_s=2.0,
        margin_mm=200.0,
    )
    print("-" * 78)
    print(f" Minimum Recommended Safety Enclosure Radius: {fence_radius:.1f} mm ({fence_radius/1000.0:.2f} m)")
    print("=" * 78)


if __name__ == "__main__":
    print_analytical_report()
