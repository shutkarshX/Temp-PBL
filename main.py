"""Run a small, deterministic demonstration of OS process scheduling."""
from pathlib import Path
from os_platform.models import ServiceRequest
from os_platform.scheduler import FCFSScheduler
from os_platform.storage import save_requests

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "demo_requests.json"


def build_demo_requests() -> list[ServiceRequest]:
    # Synthetic IDs only; no real citizen data is used.
    return [
        ServiceRequest("REQ-001", "CIT-DEMO-01", "Certificate", "Demo birth-certificate request", arrival_time=0),
        ServiceRequest("REQ-002", "CIT-DEMO-02", "Identity", "Demo identity-record update", arrival_time=1),
        ServiceRequest("REQ-003", "CIT-DEMO-03", "Grievance", "Demo grievance submission", arrival_time=2),
        ServiceRequest("REQ-004", "CIT-DEMO-04", "Tax", "Demo tax-document request", arrival_time=3),
    ]


def main() -> None:
    requests = build_demo_requests()
    scheduler = FCFSScheduler()
    for request in requests:
        scheduler.submit(request)
    completed = scheduler.run_all()
    save_requests(DATA_FILE, completed)

    print("Integrated National Citizen Services Platform — OS Simulator")
    print("Educational demo only; no real government service is contacted.\n")
    print(f"{'Order':<7}{'Request':<12}{'Service':<14}{'Final state':<14}Result")
    print("-" * 80)
    for request in completed:
        print(f"{request.completion_order:<7}{request.request_id:<12}{request.service_type:<14}{request.state.value:<14}{request.result}")
    print(f"\nSaved {len(completed)} demo requests to: {DATA_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
