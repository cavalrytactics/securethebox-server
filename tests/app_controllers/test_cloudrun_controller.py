from app_controllers.cloudrun_controller import CloudRunController
import json
import os
import pytest

pytest.globalData = []

c = CloudRunController()

def loadGlobalData():
    with open(str(os.getcwd())+"/tests/globalData.json", "r") as f:
        pytest.globalData = json.load(f)

def test_loadGlobalData():
    loadGlobalData()
    with open(str(os.getcwd())+"/tests/globalData.json", "r") as f:
        pytest.globalData = json.load(f)

def test_setCurrentDirectory():
    loadGlobalData()
    assert c.setCurrentDirectory() == True

def test_setFileName():
    loadGlobalData()
    assert c.setFileName(pytest.globalData["googleCloudRunServiceAccountFile"]) == True

def test_setServiceAccountEmailAddress():
    loadGlobalData()
    assert c.setServiceAccountEmailAddress(pytest.globalData["googleCloudRunServiceAccountEmail"]) == True

def test_setProjectId():
    loadGlobalData()
    assert c.setProjectId(pytest.globalData["googleCloudRunProjectId"]) == True

def test_setImageName():
    loadGlobalData()
    assert c.setImageName(pytest.globalData["googleCloudRunImageName"]) == True

def test_setRegion():
    loadGlobalData()
    assert c.setRegion(pytest.globalData["googleCloudRunRegion"]) == True

def test_setPlatform():
    loadGlobalData()
    assert c.setPlatform(pytest.globalData["googleCloudRunPlatform"]) == True

def test_setDockerSources():
    loadGlobalData()
    assert c.setDockerSources() == True

def test_setAccount():
    loadGlobalData()
    c.setCurrentDirectory()
    c.setProjectId(pytest.globalData["googleCloudRunProjectId"])
    c.setServiceAccountEmailAddress(pytest.globalData["googleCloudRunServiceAccountEmail"])
    assert c.setAccount() == True

def test_buildImage():
    loadGlobalData()
    c.setProjectId(pytest.globalData["googleCloudRunProjectId"])
    c.setImageName(pytest.globalData["googleCloudRunImageName"])
    assert c.buildImage() == True

def test_pushImage():
    loadGlobalData()
    c.setProjectId(pytest.globalData["googleCloudRunProjectId"])
    c.setImageName(pytest.globalData["googleCloudRunImageName"])
    assert c.pushImage() == True

def test_deployImage():
    loadGlobalData()
    c.setCurrentDirectory()
    c.setProjectId(pytest.globalData["googleCloudRunProjectId"])
    c.setImageName(pytest.globalData["googleCloudRunImageName"])
    c.setRegion(pytest.globalData["googleCloudRunRegion"])
    assert c.deployImage() == True