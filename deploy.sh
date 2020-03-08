pytest -vs tests/app_schema/
pytest -vs tests/app_controllers/test_travis_controller.py
pytest -vs tests/app_controllers/test_clouddns_controller.py
pytest -vs tests/app_controllers/test_cloudrun_controller.py
pytest -vs tests/app_controllers/test_kubernetes_controller.py

if [ $? -eq 0 ]; then
    git add .
    cz commit
    git push
else
    echo FAILED
fi

