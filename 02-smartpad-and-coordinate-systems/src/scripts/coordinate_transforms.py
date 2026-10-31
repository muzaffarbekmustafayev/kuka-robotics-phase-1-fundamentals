"""
===============================================================================
KUKA Coordinate Transformations & Jogging Mechanics Analyzer
Phase 1: Fundamentals | Lesson 02: smartPAD and Coordinate Systems
Author: Muzaffarbek Mustafayev (SamDU & TSU)
===============================================================================
"""

from dataclasses import dataclass
from typing import Dict, Tuple
import numpy as np


@dataclass(frozen=True)
class KukaFrame:
    """Represents a spatial 6D pose in KUKA FRAME convention: X, Y, Z (mm) and A, B, C (deg)."""
    x: float
    y: float
    z: float
    a: float  # Rotation around Z (deg)
    b: float  # Rotation around Y' (deg)
    c: float  # Rotation around X'' (deg)

    def to_homogeneous_matrix(self) -> np.ndarray:
        """Converts KUKA [X, Y, Z, A, B, C] frame into 4x4 homogeneous transformation matrix."""
        rad_a, rad_b, rad_c = np.radians([self.a, self.b, self.c])
        cA, sA = np.cos(rad_a), np.sin(rad_a)
        cB, sB = np.cos(rad_b), np.sin(rad_b)
        cC, sC = np.cos(rad_c), np.sin(rad_c)

        Rz = np.array([[cA, -sA, 0.0], [sA, cA, 0.0], [0.0, 0.0, 1.0]])
        Ry = np.array([[cB, 0.0, sB], [0.0, 1.0, 0.0], [-sB, 0.0, cB]])
        Rx = np.array([[1.0, 0.0, 0.0], [0.0, cC, -sC], [0.0, sC, cC]])

        R = Rz @ Ry @ Rx
        T = np.eye(4)
        T[:3, :3] = R
        T[:3, 3] = [self.x, self.y, self.z]
        return T

    @classmethod
    def from_homogeneous_matrix(cls, T: np.ndarray) -> "KukaFrame":
        """Extracts KUKA [X, Y, Z, A, B, C] frame from a 4x4 homogeneous matrix."""
        x, y, z = T[:3, 3]
        R = T[:3, :3]

        B = np.arctan2(-R[2, 0], np.sqrt(R[0, 0]**2 + R[1, 0]**2))
        if not np.isclose(np.cos(B), 0.0):
            A = np.arctan2(R[1, 0], R[0, 0])
            C = np.arctan2(R[2, 1], R[2, 2])
        else:
            C = 0.0
            A = np.arctan2(-R[0, 1], R[1, 1])

        return cls(x=float(x), y=float(y), z=float(z),
                   a=float(np.degrees(A)), b=float(np.degrees(B)), c=float(np.degrees(C)))


class CoordinateSystemManager:
    """
    Manages coordinate transformations between WORLD, BASE, FLANGE, and TOOL systems.
    
    Theorem (Kinematic Tree Transformation):
        T_BASE_TOOL = (T_WORLD_BASE)^-1 * T_WORLD_FLANGE * T_FLANGE_TOOL
    """

    def __init__(self, world_to_base: KukaFrame, flange_to_tool: KukaFrame):
        self.T_W_B = world_to_base.to_homogeneous_matrix()
        self.T_F_T = flange_to_tool.to_homogeneous_matrix()

    def compute_tcp_in_base(self, world_to_flange: KukaFrame) -> KukaFrame:
        """Calculates the current Tool Center Point (TCP) pose relative to BASE frame."""
        T_W_F = world_to_flange.to_homogeneous_matrix()
        T_B_W = np.linalg.inv(self.T_W_B)
        T_B_T = T_B_W @ T_W_F @ self.T_F_T
        return KukaFrame.from_homogeneous_matrix(T_B_T)

    def simulate_tool_jog(self, current_flange_in_world: KukaFrame, delta_tool_xyz: np.ndarray) -> KukaFrame:
        """
        Simulates smartPAD TOOL jogging: moves TCP along its own local tool axes.
        
        Formula:
            T_W_F_new = T_W_F_old * (T_F_T * Delta_T * T_F_T^-1)
        """
        T_W_F = current_flange_in_world.to_homogeneous_matrix()
        delta_T = np.eye(4)
        delta_T[:3, 3] = delta_tool_xyz

        T_W_T_old = T_W_F @ self.T_F_T
        T_W_T_new = T_W_T_old @ delta_T
        T_W_F_new = T_W_T_new @ np.linalg.inv(self.T_F_T)

        return KukaFrame.from_homogeneous_matrix(T_W_F_new)


def main():
    print("=" * 78)
    print(" KUKA KR 6 R900-2 COORDINATE SYSTEMS & JOGGING TRANSFORMATION DEMO")
    print("=" * 78)

    # 1. Setup Base and Tool frames
    base_frame = KukaFrame(x=200.0, y=100.0, z=0.0, a=0.0, b=0.0, c=0.0)
    tool_frame = KukaFrame(x=0.0, y=0.0, z=150.0, a=0.0, b=0.0, c=0.0)  # 150mm pointer tool
    flange_in_world = KukaFrame(x=600.0, y=300.0, z=500.0, a=45.0, b=0.0, c=0.0)

    mgr = CoordinateSystemManager(world_to_base=base_frame, flange_to_tool=tool_frame)

    # 2. Compute TCP in Base
    tcp_base = mgr.compute_tcp_in_base(flange_in_world)
    print(f" BASE Frame:        X={base_frame.x:.1f}, Y={base_frame.y:.1f}, Z={base_frame.z:.1f}")
    print(f" TOOL Frame:        X={tool_frame.x:.1f}, Y={tool_frame.y:.1f}, Z={tool_frame.z:.1f}")
    print(f" FLANGE (in World): X={flange_in_world.x:.1f}, Y={flange_in_world.y:.1f}, Z={flange_in_world.z:.1f}, A={flange_in_world.a:.1f}°")
    print(f" Computed TCP in BASE Frame:")
    print(f"   --> X={tcp_base.x:.2f} mm, Y={tcp_base.y:.2f} mm, Z={tcp_base.z:.2f} mm, A={tcp_base.a:.2f}°")

    # 3. Simulate smartPAD Tool Jogging (+50mm along tool Z-axis)
    flange_jogged = mgr.simulate_tool_jog(flange_in_world, delta_tool_xyz=np.array([0.0, 0.0, 50.0]))
    tcp_jogged = mgr.compute_tcp_in_base(flange_jogged)
    print("\n After smartPAD Jogging +50mm along local Tool +Z axis:")
    print(f"   --> New TCP in BASE: X={tcp_jogged.x:.2f} mm, Y={tcp_jogged.y:.2f} mm, Z={tcp_jogged.z:.2f} mm")
    print("=" * 78)


if __name__ == "__main__":
    main()
