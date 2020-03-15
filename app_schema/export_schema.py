import json
from app_schema.schema import schema
import subprocess
import sys
from graphql.utils import schema_printer
import os
import shutil

"""

Exports schema to frontend directory (securethebox-client)

Run this in the background: 
watch -n 10 pytest tests/app_schema/test_export_schema.py

"""


class AppSchema():
   def __init__(self):
      self.schema = schema_printer.print_schema(schema)
      self.currentDirectory = ""

   def setCurrentDirectory(self):
      try:
         self.currentDirectory = os.getcwd()
         return True
      except:
         return False

   def writeSchemaToFile(self):
      try:
         with open(self.currentDirectory+'/app_schema/schema.json', "w") as fp:
            fp.write(self.schema)
         return True
      except:
         return False

   def copyToFrontend(self,schemaPath):
      try:
         if shutil.which("travis") is None:
            print("Travis command does not exist!")
            return True
         else:
            subprocess.Popen([f"mv {self.currentDirectory}/app_schema/schema.json {schemaPath}"],shell=True).wait()
         return True
      except:
         return False
      