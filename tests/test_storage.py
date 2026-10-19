import tempfile
import unittest
from pathlib import Path
from os_platform.models import ProcessState, ServiceRequest
from os_platform.storage import load_requests, save_requests


class TestJSONStorage(unittest.TestCase):
    def test_save_and_load_round_trip(self):
        request = ServiceRequest("REQ-9", "CIT-DEMO-9", "Tax", "Synthetic test", state=ProcessState.TERMINATED, completion_order=1, result="Done")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "requests.json"
            save_requests(path, [request])
            loaded = load_requests(path)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].request_id, request.request_id)
        self.assertEqual(loaded[0].state, ProcessState.TERMINATED)
        self.assertEqual(loaded[0].result, "Done")

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(load_requests(Path(tmp) / "missing.json"), [])

    def test_invalid_top_level_json_shape_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "requests.json"
            path.write_text('{"not": "a list"}', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_requests(path)
