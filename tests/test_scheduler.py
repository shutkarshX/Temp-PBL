import unittest
from os_platform.models import ProcessState, ServiceRequest
from os_platform.scheduler import FCFSScheduler


def req(request_id: str, state: ProcessState = ProcessState.NEW) -> ServiceRequest:
    return ServiceRequest(request_id, "CIT-TEST", "Certificate", "Synthetic test request", state=state)


class TestFCFSScheduler(unittest.TestCase):
    def test_submit_moves_new_to_ready(self):
        scheduler = FCFSScheduler()
        request = req("REQ-1")
        scheduler.submit(request)
        self.assertEqual(request.state, ProcessState.READY)

    def test_fcfs_preserves_submission_order(self):
        scheduler = FCFSScheduler()
        requests = [req(f"REQ-{i}") for i in range(1, 4)]
        for request in requests:
            scheduler.submit(request)
        result = scheduler.run_all()
        self.assertEqual([r.request_id for r in result], ["REQ-1", "REQ-2", "REQ-3"])

    def test_completed_requests_are_terminated(self):
        scheduler = FCFSScheduler()
        request = req("REQ-1")
        scheduler.submit(request)
        scheduler.run_next()
        self.assertEqual(request.state, ProcessState.TERMINATED)

    def test_completion_order_is_sequential(self):
        scheduler = FCFSScheduler()
        for i in range(3):
            scheduler.submit(req(f"REQ-{i}"))
        self.assertEqual([r.completion_order for r in scheduler.run_all()], [1, 2, 3])

    def test_result_is_recorded(self):
        scheduler = FCFSScheduler()
        request = req("REQ-1")
        scheduler.submit(request)
        scheduler.run_next()
        self.assertIn("Certificate", request.result)

    def test_cannot_submit_non_new_request(self):
        scheduler = FCFSScheduler()
        with self.assertRaises(ValueError):
            scheduler.submit(req("REQ-1", ProcessState.READY))

    def test_empty_scheduler_returns_none(self):
        self.assertIsNone(FCFSScheduler().run_next())

    def test_run_all_on_empty_scheduler_is_empty(self):
        self.assertEqual(FCFSScheduler().run_all(), [])
