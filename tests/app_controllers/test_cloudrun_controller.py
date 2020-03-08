from app_controllers.cloudrun_controller import CloudRunController
import json
import os
import pytest

pytest.globalData = []

c = CloudRunController()

def test_loadGlobalData():
    with open(str(os.getcwd())+"/tests/globalData.json", "r") as f:
        pytest.globalData = json.load(f)

def test_setCurrentDirectory():
    assert c.setCurrentDirectory() == True

def test_setFileName():
    assert c.setFileName(pytest.globalData["googleCloudRunServiceAccountFile"]) == True

def test_setServiceAccountEmailAddress():
    assert c.setServiceAccountEmailAddress(pytest.globalData["googleCloudRunServiceAccountEmail"]) == True

def test_setProjectId():
    assert c.setProjectId(pytest.globalData["googleCloudRunProjectId"]) == True

def test_setImageName():
    assert c.setImageName(pytest.globalData["googleCloudRunImageName"]) == True

def test_setRegion():
    assert c.setRegion(pytest.globalData["googleCloudRunRegion"]) == True

def test_setPlatform():
    assert c.setPlatform(pytest.globalData["googleCloudRunPlatform"]) == True

def test_setDockerSources():
    assert c.setDockerSources() == True

def test_setAccount():
    c.setCurrentDirectory()
    c.setProjectId(pytest.globalData["googleCloudRunProjectId"])
    c.setServiceAccountEmailAddress(pytest.globalData["googleCloudRunServiceAccountEmail"])
    assert c.setAccount() == True

def test_buildImage():
    c.setProjectId(pytest.globalData["googleCloudRunProjectId"])
    c.setImageName(pytest.globalData["googleCloudRunImageName"])
    assert c.buildImage() == True

def test_pushImage():
    c.setProjectId(pytest.globalData["googleCloudRunProjectId"])
    c.setImageName(pytest.globalData["googleCloudRunImageName"])
    assert c.pushImage() == True

def test_deployImage():
    c.setCurrentDirectory()
    c.setProjectId(pytest.globalData["googleCloudRunProjectId"])
    c.setImageName(pytest.globalData["googleCloudRunImageName"])
    c.setRegion(pytest.globalData["googleCloudRunRegion"])
    assert c.deployImage() == True