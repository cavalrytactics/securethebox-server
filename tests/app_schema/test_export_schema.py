from app_schema.export_schema import AppSchema
import json
import os
import pytest

c = AppSchema()

def test_setCurrentDirectory():
    assert c.setCurrentDirectory() == True

def test_writeSchemaToFile():
    assert c.writeSchemaToFile() == True

def test_copyToFrontend():
    assert c.copyToFrontend("../securethebox-client/src/graphql/schema.graphql") == True