import sys
sys.path.insert(0, './psyche-api')
sys.path.insert(0, './psyche-core')

from fastapi.testclient import TestClient
from main import app

with TestClient(app) as client:
    r = client.post('/recommend', json={'user_id': 'test', 'n': 5})
    print(r.status_code)
    print(r.json())
