import numpy as np

def homogeneous_transform(R: np.ndarray, p: np.ndarray) -> np.ndarray:
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = p
    return T

def invert_transform(T: np.ndarray) -> np.ndarray:
    R = T[:3, :3]
    p = T[:3, 3]
    T_inv = np.eye(4)
    T_inv[:3, :3] = R.T
    T_inv[:3, 3] = -R.T @ p
    return T_inv

def test_coordinate_chain():
    # Base offset relative to World
    T_W_B = homogeneous_transform(np.eye(3), np.array([500.0, 0.0, 0.0]))
    # Flange relative to World
    T_W_F = homogeneous_transform(np.eye(3), np.array([750.0, 200.0, 400.0]))
    # Tool relative to Flange
    T_F_T = homogeneous_transform(np.eye(3), np.array([0.0, 0.0, 150.0]))
    
    # TCP in Base frame
    T_B_T = invert_transform(T_W_B) @ T_W_F @ T_F_T
    print("Computed TCP in Base frame (X, Y, Z):", T_B_T[:3, 3])
    assert np.allclose(T_B_T[:3, 3], np.array([250.0, 200.0, 550.0]))
    print("[SUCCESS] Coordinate chain theorem verified!")

if __name__ == "__main__":
    test_coordinate_chain()
