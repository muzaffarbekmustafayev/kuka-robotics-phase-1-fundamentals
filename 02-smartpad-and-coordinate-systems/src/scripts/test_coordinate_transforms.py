"""
Unit Tests for KUKA Coordinate Transformations & smartPAD Jogging
Phase 1: Fundamentals | Lesson 02
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import numpy as np
import pytest
from coordinate_transforms import KukaFrame, CoordinateSystemManager


def test_kuka_frame_conversion_roundtrip():
    original = KukaFrame(x=350.5, y=-120.0, z=600.2, a=45.0, b=-30.0, c=60.0)
    T = original.to_homogeneous_matrix()
    recovered = KukaFrame.from_homogeneous_matrix(T)

    assert np.isclose(original.x, recovered.x, atol=1e-4)
    assert np.isclose(original.y, recovered.y, atol=1e-4)
    assert np.isclose(original.z, recovered.z, atol=1e-4)
    assert np.isclose(original.a, recovered.a, atol=1e-4)
    assert np.isclose(original.b, recovered.b, atol=1e-4)
    assert np.isclose(original.c, recovered.c, atol=1e-4)


def test_base_tool_kinematic_chain():
    base = KukaFrame(x=100.0, y=0.0, z=0.0, a=0.0, b=0.0, c=0.0)
    tool = KukaFrame(x=0.0, y=0.0, z=100.0, a=0.0, b=0.0, c=0.0)
    flange_in_world = KukaFrame(x=500.0, y=200.0, z=400.0, a=0.0, b=0.0, c=0.0)

    mgr = CoordinateSystemManager(world_to_base=base, flange_to_tool=tool)
    tcp_base = mgr.compute_tcp_in_base(flange_in_world)

    # X in base should be 500 - 100 = 400
    assert np.isclose(tcp_base.x, 400.0)
    assert np.isclose(tcp_base.y, 200.0)
    # Z in base should be 400 + 100 = 500
    assert np.isclose(tcp_base.z, 500.0)


def test_tool_jog_along_z():
    base = KukaFrame(x=0.0, y=0.0, z=0.0, a=0.0, b=0.0, c=0.0)
    tool = KukaFrame(x=0.0, y=0.0, z=50.0, a=0.0, b=0.0, c=0.0)
    flange = KukaFrame(x=400.0, y=0.0, z=300.0, a=0.0, b=0.0, c=0.0)

    mgr = CoordinateSystemManager(world_to_base=base, flange_to_tool=tool)
    flange_jogged = mgr.simulate_tool_jog(flange, delta_tool_xyz=np.array([0.0, 0.0, 30.0]))
    tcp_jogged = mgr.compute_tcp_in_base(flange_jogged)

    # Initial TCP Z was 300 + 50 = 350. After +30mm jog along Z, it should be 380
    assert np.isclose(tcp_jogged.z, 380.0)
