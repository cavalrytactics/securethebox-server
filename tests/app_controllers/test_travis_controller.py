from app_controllers.travis_controller import TravisController
import json
import os
import pytest

pytest.globalData = []

c = TravisController()

def test_loadGlobalData():
    with open(str(os.getcwd())+"/tests/globalData.json", "r") as f:
        pytest.globalData = json.load(f)

def test_tarSecretFiles():
    c.setCurrentDirectory()
    c.setFileName("secrets.tar")
    assert c.tarSecretFiles(pytest.globalData["unencryptedFileNames"]) == True

def test_setTravisEncryptFile():
    c.setCurrentDirectory()
    c.setFileName("secrets.tar")
    assert c.setTravisEncryptFile() == True

def test_setTravisUnencryptFile():
    c.setCurrentDirectory()
    c.setFileName("secrets.tar")
    assert c.setTravisUnencryptFile() == True