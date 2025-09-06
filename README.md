# README: Hands

> [!Important]
> This is a 0 release of the library. It is not yet stable and may change in the future!
> Use at your own risk but very welcome!

## Goal
Testing is hard and often starts to make hard choices between different frameworks, protocols, and logging mechanisms.
We believe that testing should be easy and flexible, allowing users to choose the best tools for their specific needs.
It should further more be easy to get into the pipeline and CI/CD workflows, why we host this library on PyPI and make it installable via pip.

> [!Note]
> The `Robot Framework` offers us a great way of reporting. 
> Hands will use this output format to provide a common ground for reporting across different testing frameworks.

The `hands` package aims to provide a modular and extensible framework for managing and interacting with various devices and services. It is designed to be flexible, allowing users to integrate different communication protocols, testing frameworks, and logging mechanisms seamlessly.


## Usage (cli)

```bash
pip install hands
```

## Structure

> [!Important]
> This is a monorepo structure where each finger represents a separate package. The `thumb` package serves as the core, importing functionalities from other packages. This design allows for modular development and testing of each component.

```
hand/
├── pyproject.toml        # (root manager for workspace, e.g. poetry or uv)
├── left_palm/            # pytest project
│   ├── pyproject.toml
│   └── left_palm/
│       ├── __init__.py
│       └── runner.py
│   └── tests/
│       └── test_runner.py
│
├── right_palm/           # robot framework
│   ├── pyproject.toml
│   └── right_palm/
│       ├── __init__.py
│       └── robot_runner.py
│   └── tests/
│       └── acceptance.robot
│
├── thumb/                # core device handling
│   ├── pyproject.toml
│   └── thumb/
│       ├── __init__.py
│       └── device.py     # imports left_palm or right_palm
│   └── tests/
│       └── test_device.py
│
├── index_finger/         # assertions + logging
│   ├── pyproject.toml
│   └── index_finger/
│       ├── __init__.py
│       └── asserts.py
│       └── logging.py
│   └── tests/
│       └── test_asserts.py
│
├── middle_finger/        # communication interface
│   ├── pyproject.toml
│   └── middle_finger/
│       ├── __init__.py
│       ├── mqtt.py
│       ├── grpc.py
│       └── grafana.py
│   └── tests/
│       └── test_mqtt.py
│
└── README.md
```