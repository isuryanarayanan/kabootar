import pytest
from fastapi.testclient import TestClient
from kabootar.main import create_application
from kabootar.db import db

client = TestClient(create_application())

def test_root():
    print(db.list_collection_names())