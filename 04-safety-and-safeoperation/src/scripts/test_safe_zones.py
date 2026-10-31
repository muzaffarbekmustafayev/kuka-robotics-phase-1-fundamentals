"""Unit tests for SafeOperation zone and stopping distance calculations."""

import sys
from pathlib import Path
import numpy as np
import pytest

# Ensure local module is importable
sys.path.append(str(Path(__file__).parent))

from safe_zones_monitor import AxisLimits, CartesianCuboidZone, SafeOperationController


def test_axis_limits():
    limits = AxisLimits()
    # Safe configuration: Home position [0, -90, 90, 0, 0, 0]
    valid, err = limits.check_joint_limits([0.0, -90.0, 90.0, 0.0, 0.0, 0.0])
    assert valid is True
    assert err is None

    # Violation configuration: A1 beyond 170 deg
    invalid, err = limits.check_joint_limits([185.0, -90.0, 90.0, 0.0, 0.0, 0.0])
    assert invalid is False
    assert "Axis A1 violation" in err


def test_cuboid_zone_inclusion_exclusion():
    # Allowed work cell
    allowed_box = CartesianCuboidZone(
        zone_id=1, name="Allowed", is_exclusion=False,
        x_min=0.0, x_max=500.0, y_min=-500.0, y_max=500.0, z_min=0.0, z_max=800.0
    )
    p_inside = np.array([250.0, 0.0, 400.0])
    p_outside = np.array([600.0, 0.0, 400.0])
    assert allowed_box.is_safe(p_inside)
    assert not allowed_box.is_safe(p_outside)

    # Exclusion zone (keep out)
    prohibited_box = CartesianCuboidZone(
        zone_id=2, name="Forbidden", is_exclusion=True,
        x_min=100.0, x_max=200.0, y_min=100.0, y_max=200.0, z_min=0.0, z_max=500.0
    )
    p_in_hazard = np.array([150.0, 150.0, 250.0])
    p_out_hazard = np.array([50.0, 50.0, 250.0])
    assert not prohibited_box.is_safe(p_in_hazard)
    assert prohibited_box.is_safe(p_out_hazard)


def test_stopping_distance_formula():
    controller = SafeOperationController(
        response_time_ms=20.0,
        max_brake_decel_mm_s2=8000.0,
        safe_speed_limit_mm_s=250.0
    )
    v = 250.0  # mm/s
    margin = 50.0  # mm
    # S = 250 * 0.02 + 250^2 / (2 * 8000) + 50 = 5.0 + 3.90625 + 50.0 = 58.90625 mm
    expected = (250.0 * 0.02) + (250.0 ** 2 / 16000.0) + margin
    s = controller.calculate_stopping_distance(v, safety_margin_c_mm=margin)
    assert np.isclose(s, expected, atol=1e-3)


def test_controller_speed_and_zone_supervision():
    controller = SafeOperationController(safe_speed_limit_mm_s=250.0)
    zone = CartesianCuboidZone(
        zone_id=1, name="Workspace", is_exclusion=False,
        x_min=0.0, x_max=1000.0, y_min=-500.0, y_max=500.0, z_min=0.0, z_max=1000.0
    )
    controller.add_zone(zone)

    # 1. Nominal safe motion
    res1 = controller.verify_tool_center_point(np.array([400.0, 0.0, 300.0]), 200.0)
    assert res1["overall_safe"] is True
    assert res1["speed_safe"] is True

    # 2. Velocity violation
    res2 = controller.verify_tool_center_point(np.array([400.0, 0.0, 300.0]), 350.0)
    assert res2["speed_safe"] is False
    assert res2["overall_safe"] is False

    # 3. Spatial boundary violation
    res3 = controller.verify_tool_center_point(np.array([1200.0, 0.0, 300.0]), 150.0)
    assert res3["speed_safe"] is True
    assert res3["overall_safe"] is False
