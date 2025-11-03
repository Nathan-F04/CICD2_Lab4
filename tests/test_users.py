
def test_put_user_pass(client):
    client.post("/api/users", json={"name":"Paul","email":"pl@atu.ie","age":25,"student_id":"S1234567"})
    r = client.put("/api/users/1", json={"id":1, "name":"Pal","email":"pl@atu.ie","age":25,"student_id":"S1234567"})
    assert r.status_code == 200

def test_patch_user_pass(client):
    client.post("/api/users", json={"name":"Paul","email":"psy@atu.ie","age":25,"student_id":"S1234565"})
    r = client.patch("/api/users/1", json={"name":"Matt","email":"pal@atu.ie","age":25,"student_id":"S1234566"})
    assert r.status_code == 200

def test_put_project_pass(client):
    client.post("/api/users", json={"name":"Paul","email":"joe@atu.ie","age":25,"student_id":"S1234564"})
    client.post("/api/users/1/projects", json={"name":"Project1"})
    r = client.put("/api/users/project_put/1", json={"id":1,"name":"ProjectDiff","owner_id":1})
    assert r.status_code == 200

def test_patch_project_pass(client):
    client.post("/api/users", json={"name":"Paul","email":"jim@atu.ie","age":25,"student_id":"S1234563"})
    client.post("/api/users/1/projects", json={"name":"Project2"})
    r = client.patch("/api/users/project_patch/1", json={"name":"ProjectDiff"})
    assert r.status_code == 200
