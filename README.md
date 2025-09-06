# README: Hands

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