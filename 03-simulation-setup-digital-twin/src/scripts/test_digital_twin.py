"""
Unit Tests for KUKA Digital Twin 12ms Synchronization Engine
Phase 1: Fundamentals | Lesson 03
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import numpy as np
import pytest
from digital_twin_sync import DigitalTwinEngine, VrcPacket


def test_initial_configuration():
    engine = DigitalTwinEngine(initial_joints_deg=(0.0, -90.0, 90.0, 0.0, 0.0, 0.0))
    assert engine.simulated_time == 0.0
    assert engine.cycle_count == 0
    assert np.allclose(engine.current_joints, [0.0, -90.0, 90.0, 0.0, 0.0, 0.0])


def test_12ms_cycle_integration():
    engine = DigitalTwinEngine(initial_joints_deg=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
    # 100 deg/s velocity over 1 cycle (12 ms) -> delta_q = 1.2 deg
    v = np.array([100.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    pkt = engine.step_interpolation(v)

    assert pkt.cycle_index == 1
    assert np.isclose(pkt.timestamp_sec, 0.012)
    assert np.isclose(pkt.joint_angles_deg[0], 1.2)


def test_jitter_compliance():
    engine = DigitalTwinEngine()
    acceptable_delays = [0.001, 0.002, 0.0015, 0.0022]
    metrics = engine.compute_communication_jitter(acceptable_delays)
    assert metrics["realtime_compliant"] is True
    assert metrics["mean_delay_ms"] < 12.0
