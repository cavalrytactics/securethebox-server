# Run tests
pytest -vs -x tests/app_schema/
pytest -vs -x tests/app_controllers/test_travis_controller.py
pytest -vs -x tests/app_controllers/test_clouddns_controller.py
pytest -vs -x tests/app_controllers/test_cloudrun_controller.py
pytest -vs -x tests/app_controllers/test_kubernetes_controller.py