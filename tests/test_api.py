import pytest
from workflowapi import workflowapi
from flask import Flask
import json

def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200
    expected = "Welcome to workflow-graphs"
    assert expected == res.get_data(as_text=True)
  