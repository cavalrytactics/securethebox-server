import json
from app_schema.schema import schema
import subprocess
import sys
from graphql.utils import schema_printer
import os
import shutil

class GenerateMutation():
   def __init__(self):
      self.model = ""
      self.currentDirectory = ""
      self.fields = []
      self.inputData = {}

   def setCurrentDirectory(self):
      try:
         self.currentDirectory = os.getcwd()
         return True
      except:
         return False
