# README: Hands

> [!Important]
> This is a 0 release of the library. It is not yet stable and may change in the future!
> Use at your own risk but very welcome!

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