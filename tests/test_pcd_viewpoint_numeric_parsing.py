import numpy as np
import open3d as o3d

from oxspires_tools.point_cloud import read_pcd_with_viewpoint


class DummyCloud:
    def __init__(self):
        self.transform_matrix = None

    def transform(self, matrix):
        self.transform_matrix = np.asarray(matrix)
        return self


def test_read_pcd_with_viewpoint_parses_numeric_transform(tmp_path, monkeypatch):
    pcd_path = tmp_path / "cloud.pcd"
    pcd_path.write_bytes(b"VERSION .7\nVIEWPOINT 1 2 3 1 0 0 0\n")

    cloud = DummyCloud()
    monkeypatch.setattr(o3d.io, "read_point_cloud", lambda _: cloud)

    result = read_pcd_with_viewpoint(str(pcd_path))

    assert result is cloud
    np.testing.assert_allclose(
        cloud.transform_matrix,
        np.array(
            [
                [1.0, 0.0, 0.0, 1.0],
                [0.0, 1.0, 0.0, 2.0],
                [0.0, 0.0, 1.0, 3.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        ),
    )
