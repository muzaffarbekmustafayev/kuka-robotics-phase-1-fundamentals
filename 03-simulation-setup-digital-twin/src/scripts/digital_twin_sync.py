"""
===============================================================================
KUKA Digital Twin Synchronization & VRC Real-Time Packet Engine
Phase 1: Fundamentals | Lesson 03: Simulation Setup & Digital Twin
Author: Muzaffarbek Mustafayev (SamDU & TSU)
===============================================================================
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np


@dataclass(frozen=True)
class VrcPacket:
    """Represents a single deterministic interpolator cycle packet from KUKA VRC."""
    timestamp_sec: float
    cycle_index: int
    joint_angles_deg: Tuple[float, float, float, float, float, float]
    joint_velocities_deg_s: Tuple[float, float, float, float, float, float]


class DigitalTwinEngine:
    """
    Simulates real-time synchronization between KUKA OfficeLite VRC and KUKA.Sim Pro.
    
    Theorem (Discrete Trajectory Interpolation):
        q(t_k) = q(t_{k-1}) + int_{t_{k-1}}^{t_k} \dot{q}(t) dt
        Under 12ms deterministic KSS cycle: \Delta t = 0.012 s
    """

    CYCLE_TIME_SEC = 0.012  # Standard KSS interpolation cycle (12 ms)

    def __init__(self, initial_joints_deg: Tuple[float, ...] = (0.0, -90.0, 90.0, 0.0, 0.0, 0.0)):
        self.current_joints = np.array(initial_joints_deg, dtype=np.float64)
        self.packet_history: List[VrcPacket] = []
        self.simulated_time = 0.0
        self.cycle_count = 0

    def step_interpolation(self, target_velocities_deg_s: np.ndarray) -> VrcPacket:
        """
        Executes one 12ms deterministic VRC control step.
        """
        # Linear Euler integration of joint angles over 12 ms
        delta_q = target_velocities_deg_s * self.CYCLE_TIME_SEC
        self.current_joints += delta_q
        self.simulated_time += self.CYCLE_TIME_SEC
        self.cycle_count += 1

        packet = VrcPacket(
            timestamp_sec=self.simulated_time,
            cycle_index=self.cycle_count,
            joint_angles_deg=tuple(self.current_joints),
            joint_velocities_deg_s=tuple(target_velocities_deg_s)
        )
        self.packet_history.append(packet)
        return packet

    def compute_communication_jitter(self, simulated_delays_sec: List[float]) -> Dict[str, float]:
        """
        Calculates network latency jitter and max synchronization error under VRC streaming.
        """
        delays = np.array(simulated_delays_sec)
        mean_delay = float(np.mean(delays))
        jitter = float(np.std(delays))
        max_lag_cycles = int(np.ceil(np.max(delays) / self.CYCLE_TIME_SEC))

        return {
            "mean_delay_ms": mean_delay * 1000.0,
            "jitter_ms": jitter * 1000.0,
            "max_lag_cycles": max_lag_cycles,
            "realtime_compliant": jitter < (self.CYCLE_TIME_SEC / 2.0)
        }


def main():
    print("=" * 78)
    print(" KUKA DIGITAL TWIN 12ms VRC INTERPOLATION & JITTER BENCHMARK")
    print("=" * 78)

    engine = DigitalTwinEngine()
    print(" Initial Home Joints (deg):", engine.current_joints)

    # Simulate 50 steps of joint acceleration (Axis 1 turning at 30 deg/s)
    v_target = np.array([30.0, 10.0, -5.0, 0.0, 0.0, 0.0])
    for _ in range(50):
        pkt = engine.step_interpolation(v_target)

    print(f" Executed 50 VRC cycles ({engine.simulated_time:.3f} s):")
    print(" Final Joint Angles (deg):", np.round(pkt.joint_angles_deg, 3))

    # Evaluate simulated Ethernet latency jitter
    delays = [0.002, 0.003, 0.001, 0.004, 0.002, 0.005, 0.002]
    metrics = engine.compute_communication_jitter(delays)
    print("\nVRC Communication Metrics:")
    print(f" Mean Latency:  {metrics['mean_delay_ms']:.2f} ms")
    print(f" Latency Jitter:{metrics['jitter_ms']:.2f} ms")
    print(f" Real-time Compliant (KSS < 6ms jitter): {metrics['realtime_compliant']}")
    print("=" * 78)


if __name__ == "__main__":
    main()
