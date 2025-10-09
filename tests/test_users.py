#test_users.py
import pytest

#import users to clear the list
from app.main import users

#Payload to pass as default object
def user_payload(uid=1, name="Paul", email="pl@atu.ie", age=25, sid="S1234567"):
    return {"user_id": uid, "name": name, "email": email, "age": age, "student_id":sid}


def test_create_user_ok(client):
    #Clear the list before posting a user and checking the assert is 201
    users.clear()
    result = client.post("/api/users", json=user_payload())
    assert result.status_code == 201
    data = result.json()
    assert data["user_id"] == 1
    assert data["name"] == "Paul"

def test_duplicate_user_id_conflict(client):
    #Two users with same id are posted, first works but second throws 409
    users.clear()
    client.post("/api/users", json=user_payload(uid=2))
    result = client.post("/api/users", json=user_payload(uid=2))
    assert result.status_code == 409 # duplicate id -> conflict
    assert "exists" in result.json()["detail"].lower()

@pytest.mark.parametrize("bad_sid", ["BAD123", "s1234567", "S123", "S12345678"])
def test_bad_student_id_422(client, bad_sid):
      #Parameterized test where bad sids are passed and 422 is asserted
    users.clear()
    result = client.post("/api/users", json=user_payload(uid=3, sid=bad_sid))
    assert result.status_code == 422 # pydantic validation error

@pytest.mark.parametrize("bad_email", ["fakeEmai", "FakeEmail1", "@email"])
def test_bad_email_422(client, bad_email):
    #Parameterized test where bad emails are passed and 422 is asserted
    users.clear()
    result = client.post("/api/users", json=user_payload(uid=3, email=bad_email))
    assert result.status_code == 422 # pydantic validation error

def test_get_user_404(client):
    #Test a get when no user is posted
    users.clear()
    result = client.get("/api/users/999")
    assert result.status_code == 404

def test_delete_then_404(client):
    #Posts user before deleting for a status 204
    client.post("/api/users", json=user_payload(uid=10))
    result1 = client.delete("/api/users/10")
    assert result1.status_code == 204
    #Second delete should assert 404 as user no longer exists
    result2 = client.delete("/api/users/10")
    assert result2.status_code == 404

def test_put_200(client):
    #Posts user before attempting to edit a user that does exist
    users.clear()
    client.post("/api/users", json=user_payload())
    result = client.put("/api/users/1",json=user_payload(name="Jim"))
    assert result.status_code == 200

def test_put_404(client):
    #Posts user before attempting to edit a user that doesn't exist
    users.clear()
    client.post("/api/users", json=user_payload())
    result = client.put("/api/users/2",json=user_payload(name="Joe"))
    assert result.status_code == 404
    assert result.json()["detail"] == "User not found"
