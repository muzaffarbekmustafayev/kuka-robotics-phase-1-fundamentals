"""
Unit Tests for KUKA KR 6 R900-2 Workspace & Safety Calculus
Phase 1: Fundamentals | Lesson 01
Author: Muzaffarbek Mustafayev
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import numpy as np
import pytest
from workspace_analyzer import WorkspaceKinematics, SafetyBrakingCalculus, KR6R900Dimensions


@pytest.fixture
def kinematics() -> WorkspaceKinematics:
    return WorkspaceKinematics()


@pytest.fixture
def safety() -> SafetyBrakingCalculus:
    return SafetyBrakingCalculus(t_reaction_sec=0.030, a_brake_max_m_s2=8.5)


def test_reach_dimensions(kinematics: WorkspaceKinematics):
    reach = kinematics.compute_theoretical_reach()
    # Wrist center reach must be between 870 and 880 mm
    assert 870.0 < reach["wrist_center_max_reach_mm"] < 880.0
    # Minimum dead-zone must be positive and small
    assert 30.0 < reach["wrist_center_min_reach_mm"] < 40.0
    # Catalog nominal reach
    assert reach["catalog_reach_mm"] == 901.5


def test_forward_kinematics_home_pose(kinematics: WorkspaceKinematics):
    # Zero angle pose [0, 0, 0, 0, 0, 0]
    p_zero = kinematics.forward_kinematics_position(np.zeros(6))
    assert isinstance(p_zero, np.ndarray)
    assert p_zero.shape == (3,)
    # Z height should match base + links upright position
    assert np.isclose(p_zero[2], 890.0, atol=1.0)


def test_stopping_distance_monotonicity(safety: SafetyBrakingCalculus):
    # Stopping distance must increase strictly with initial speed
    m_slow = safety.compute_stopping_distance(0.25)
    m_fast = safety.compute_stopping_distance(2.00)
    
    assert m_slow["total_stopping_distance_mm"] < m_fast["total_stopping_distance_mm"]
    assert m_slow["braking_distance_mm"] < m_fast["braking_distance_mm"]
    assert m_slow["total_stopping_time_ms"] < m_fast["total_stopping_time_ms"]


def test_stop_category_comparison(safety: SafetyBrakingCalculus):
    # Stop 0 with friction brake engagement delay has greater reaction distance than Stop 1
    m_cat1 = safety.compute_stopping_distance(1.5, stop_category=1)
    m_cat0 = safety.compute_stopping_distance(1.5, stop_category=0)
    
    assert m_cat0["reaction_distance_mm"] > m_cat1["reaction_distance_mm"]
    assert m_cat0["total_stopping_distance_mm"] > m_cat1["total_stopping_distance_mm"]


def test_monte_carlo_envelope_bounded(kinematics: WorkspaceKinematics):
    # All sampled reachable points must strictly reside within maximum reach sphere
    samples = kinematics.sample_workspace_monte_carlo(num_samples=200, random_seed=123)
    shoulder_origin = np.array([25.0, 0.0, 400.0])
    
    distances_from_shoulder = np.linalg.norm(samples - shoulder_origin, axis=1)
    max_theoretical_envelope = 901.5 + 100.0  # adding safe margin
    
    assert np.all(distances_from_shoulder <= max_theoretical_envelope)
