import subprocess
from subprocess import check_output
import os
from os import path
import datetime
from google.cloud import tasks_v2
from google.api_core import exceptions
from google.protobuf import timestamp_pb2
from typing import Tuple, List
import json
"""
Enable API manually

IAM Permissions:
Cloud Tasks Admin
Cloud Tasks Enqueuer
Cloud Tasks Queue Admin
Cloud Tasks Service Agent
Cloud Tasks Task Deleter
*Enable Domain Wide Delegation (Allows Service Account Requests)
"""


class CloudTasksController():
    def __init__(self):
        self.currentDirectory = ""
        self.fileName = ""
        self.serviceAccountEmailAddress = ""
        self.projectId = ""
        self.location = ""
        self.taskName = None
        self.taskUrl = ""
        self.taskDelay = 0
        self.taskPayload = None

    def setCurrentDirectory(self) -> bool:
        try:
            self.currentDirectory = os.getcwd()
            return True
        except:
            return False

    def setFileName(self, fileName: str) -> bool:
        try:
            self.fileName = fileName
            return True
        except:
            return False

    def setServiceAccountEmailAddress(self, serviceAccountEmailAddress: str) -> bool:
        try:
            self.serviceAccountEmailAddress = serviceAccountEmailAddress
            return True
        except:
            return False

    def setProjectId(self, projectId: str) -> bool:
        try:
            self.projectId = projectId
            return True
        except:
            return False

    def setLocation(self, location: str) -> bool:
        try:
            self.location = location
            subprocess.Popen(
                [f"gcloud config set run/region {self.location} >> /dev/null 2>&1"], shell=True).wait()
            return True
        except:
            return False

    def setAccount(self) -> bool:
        try:
            subprocess.Popen(
                [f"gcloud auth activate-service-account --key-file {self.currentDirectory}/secrets/{self.fileName} >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen(
                [f"gcloud config set project {self.projectId} >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen(
                [f"gcloud config set account {self.serviceAccountEmailAddress} >> /dev/null 2>&1"], shell=True).wait()
            return True
        except:
            return False

    def setQueueId(self, queueId: str) -> bool:
        try:
            self.queueId = queueId+"-"+str(1)
            return True
        except:
            return False

    def incrementQueueId(self) -> bool:
        try:
            name = self.queueId.split("-")[0]
            number = self.queueId.split("-")[1]
            self.queueId = f"{name}-{number}" 
            return True
        except:
            return False

    def setTaskName(self, taskName: str) -> bool:
        try:
            self.taskName = taskName
            return True
        except:
            return False

    def setTaskDelay(self, taskDelay: str) -> bool:
        try:
            self.taskDelay = taskDelay
            return True
        except:
            return False

    def setTaskUrl(self, taskUrl: str) -> bool:
        try:
            self.taskUrl = taskUrl
            return True
        except:
            return False

    def setTaskPayload(self, taskPayload: str) -> bool:
        try:
            self.taskPayload = taskPayload
            return True
        except:
            return False

    def deleteTaskQueue(self) -> bool:
        try:
            subprocess.Popen(
                [f"echo y | gcloud tasks queues delete {self.queueId}"], shell=True).wait()
            return True
        except:
            return False

    def createTaskQueue(self) -> bool:
        try:
            client = tasks_v2.CloudTasksClient()
            parent = client.location_path(self.projectId, self.location)
            queuePath = client.queue_path(self.projectId, self.location, self.queueId)
            queue = {"name": queuePath} 
            try:
                client.create_queue(parent, queue)
                return True 
            except exceptions.GoogleAPICallError as error:
                if "Queue already exists" in str(error):
                    return True
        except:
            return False

    def pauseTaskQueue(self) -> bool:
        try:
            client = tasks_v2.CloudTasksClient()
            queuePath = client.queue_path(self.projectId, self.location, self.queueId)
            try:
                client.pause_queue(queuePath) 
                return True
            except exceptions.GoogleAPICallError as error:
                if "Queue does not exist" in str(error):
                    return True
                else:
                    return False
        except:
            return False

    def resumeTaskQueue(self) -> bool:
        try:
            client = tasks_v2.CloudTasksClient()
            queuePath = client.queue_path(self.projectId, self.location, self.queueId)
            try:
                client.resume_queue(queuePath) 
                return True
            except exceptions.GoogleAPICallError as error:
                if "Queue does not exist" in str(error):
                    return True
                else:
                    return False
        except:
            return False

    def purgeAllTasksInTaskQueue(self) -> bool:
        try:
            client = tasks_v2.CloudTasksClient()
            queuePath = client.queue_path(self.projectId, self.location, self.queueId)
            try:
                client.purge_queue(queuePath) 
                return True
            except exceptions.GoogleAPICallError as error:
                if "Queue does not exist" in str(error):
                    return True
                else:
                    return False
        except:
            return False
        # try:
        #     subprocess.Popen(
        #         [f"echo y | gcloud tasks queues purge {self.queueId}"], shell=True).wait()
        #     return True
        # except:
        #     return False

    def createTaskInQueue(self) -> Tuple[bool, str]:
        try:
            client = tasks_v2.CloudTasksClient()
            # Construct the fully qualified queue name.
            parent = client.queue_path(
                self.projectId, self.location, self.queueId)

            # Construct the request body.
            task = {
                'http_request': {  # Specify the type of request.
                    'http_method': 'POST',
                    'url': self.taskUrl
                }
            }

            if self.taskPayload is not None:
                # The API expects a payload of type bytes.
                converted_payload = self.taskPayload.encode()

                # Add the payload to the request.
                task['http_request']['body'] = converted_payload

            if self.taskDelay != 0:
                # Convert "seconds from now" into an rfc3339 datetime string.
                d = datetime.datetime.utcnow() + datetime.timedelta(seconds=self.taskDelay)

                # Create Timestamp protobuf.
                timestamp = timestamp_pb2.Timestamp()
                timestamp.FromDatetime(d)

                # Add the timestamp to the tasks.
                task['schedule_time'] = timestamp

            if self.taskName is not None:
                # Add the name to tasks.
                task['name'] = f"projects/{self.projectId}/locations/{self.location}/queues/{self.queueId}/tasks/{self.taskName}"

            # Use the client to build and send the task.
            try:
                response = client.create_task(parent, task)
                return True, response
            except exceptions.GoogleAPICallError as error:
                if "Requested entity already exists" in str(error):
                    return True, error
                if "The task cannot be created because a task with this name existed too recently" in error:
                    self.incrementQueueId()
                    self.createTaskInQueue() 
        except:
            print("Error in createTaskInQueue")
            return False, "failed"

    def listTasksInQueue(self) -> (bool):
        try:
            command = ["gcloud","tasks", "list", "--queue", f"{self.queueId}", "--format", "json"]
            output = check_output(command)
            taskListJson = json.loads(output)
            return True, taskListJson
        except:
            return False, []
