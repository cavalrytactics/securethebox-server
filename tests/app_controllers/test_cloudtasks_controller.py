from app_controllers.cloudtasks_controller import CloudTasksController
import json
import os
import pytest

pytest.globalData = []

c = CloudTasksController()

def loadGlobalData():
    with open(str(os.getcwd())+"/tests/globalData.json", "r") as f:
        pytest.globalData = json.load(f)

def test_loadGlobalData():
    with open(str(os.getcwd())+"/tests/globalData.json", "r") as f:
        pytest.globalData = json.load(f)

def test_setCurrentDirectory():
    loadGlobalData()
    assert c.setCurrentDirectory() == True

def test_setFileName():
    loadGlobalData()
    assert c.setFileName(pytest.globalData["googleCloudTasksServiceAccountFile"]) == True

def test_setServiceAccountEmailAddress():
    loadGlobalData()
    assert c.setServiceAccountEmailAddress(pytest.globalData["googleCloudTasksServiceAccountEmail"]) == True

def test_setProjectId():
    loadGlobalData()
    assert c.setProjectId(pytest.globalData["googleCloudTasksProjectId"]) == True

def test_setLocation():
    loadGlobalData()
    assert c.setLocation(pytest.globalData["googleCloudTasksLocation"]) == True

def test_setAccount():
    loadGlobalData()
    c.setCurrentDirectory()
    c.setProjectId(pytest.globalData["googleCloudTasksProjectId"])
    c.setServiceAccountEmailAddress(pytest.globalData["googleCloudTasksServiceAccountEmail"])
    assert c.setAccount() == True

def test_setQueueId():
    loadGlobalData()
    for queueId in pytest.globalData["googleCloudTasksQueueIds"]:
        assert c.setQueueId(queueId) == True

# def test_deleteTaskQueue():
#     loadGlobalData()
#     for queueId in pytest.globalData["googleCloudTasksQueueIds"]:
#         c.setQueueId(queueId)
#         assert c.deleteTaskQueue() == True

def test_createTaskQueue():
    loadGlobalData()
    for queueId in pytest.globalData["googleCloudTasksQueueIds"]:
        c.setQueueId(queueId)
        assert c.createTaskQueue() == True

def test_setTaskName():
    loadGlobalData() 
    for task in pytest.globalData["googleCloudTasksQueueTaskNames"]:
        assert c.setTaskName(task) == True 

def test_setTaskDelay():
    loadGlobalData() 
    assert c.setTaskDelay(pytest.globalData["googleCloudTasksQueueDelay"]) == True

def test_setTaskPayload():
    loadGlobalData() 
    assert c.setTaskPayload(pytest.globalData["googleCloudTasksQueuePayload"]) == True

def test_createTaskInQueue():
    loadGlobalData()
    for queueId in pytest.globalData["googleCloudTasksQueueIds"]:
        c.setQueueId(queueId)
        c.setLocation(pytest.globalData["googleCloudTasksLocation"])
        c.setTaskUrl(pytest.globalData["googleCloudTasksQueueUrl"])
        for task in pytest.globalData["googleCloudTasksQueueTaskNames"]:
            c.setTaskName(task)
            c.setTaskDelay(pytest.globalData["googleCloudTasksQueueDelay"])
            c.setTaskPayload(pytest.globalData["googleCloudTasksQueuePayload"])
            value, response = c.createTaskInQueue()
            assert value == True

# def test_pauseTaskQueue():
#     loadGlobalData()
#     for queueId in pytest.globalData["googleCloudTasksQueueIds"]:
#         c.setQueueId(queueId)
#         assert c.pauseTaskQueue() == True

# def test_resumeTaskQueue():
#     loadGlobalData()
#     for queueId in pytest.globalData["googleCloudTasksQueueIds"]:
#         c.setQueueId(queueId)
#         assert c.resumeTaskQueue() == True
# def test_purgeAllTasksInTaskQueue():
#     loadGlobalData()

