# Integrated National Citizen Services Platform — OS Simulator

An educational simulator for demonstrating Operating System concepts through synthetic citizen-service requests. It does **not** connect to real government systems.

## Current baseline
- Request/process model with NEW, READY, RUNNING, WAITING, and TERMINATED states.
- FCFS scheduling with deterministic processing order.
- JSON persistence for demo requests.
- Unit tests for scheduler behavior and storage.

`WAITING` is defined as a process state but the initial sequential baseline does not yet simulate blocking/wakeup. Synchronization, concurrent processing, deadlock experiments, role-based access, and additional schedulers are not implemented in this baseline.

## Requirements
- Python 3.10+ (standard library only)

## Run
```bash
python main.py
```

## Test
```bash
python -m unittest discover -s tests -v
```

## Repository note
This code is currently hosted in [shutkarshX/Temp-PBL](https://github.com/shutkarshX/Temp-PBL). The repository name is temporary/generic and should be renamed to a project-specific name when repository administration is available.

Only synthetic IDs and demo records are used. Do not enter real citizen personal information.
