import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.models import Base

TEST_DB_URL = "sqlite+pysqlite:///:memory:"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
Base.metadata.create_all(bind=engine)

@pytest.fixture
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        # hand the client to the test
        yield c
        # --- teardown happens when the 'with' block exits ---

# def test_create_user(client):
#     r = client.post("/api/users",
# json={"name":"Paul","email":"pl@atu.ie","age":25,"student_id":"S1234567"})
#     assert r.status_code == 201

def put_user_pass(client):
    r = client.put("/api/users{1}",
json={"id":1, "name":"Paul","email":"pl@atu.ie","age":25,"student_id":"S1234567"})
    assert r.status_code == 200

# @app.patch("/api/users/{user_id}", response_model=UserRead)
# def partial_edit_user(user_id: int, payload: UserPartialUpdate, db: Session = Depends(get_db)):
#     # Get only fields that were sent (exclude unset means fields missing from request are ignored)
#     new_details = payload.model_dump(exclude_unset=True)
    
#     if not new_details:
#         raise HTTPException(status_code=400, detail="No fields provided to update")
#     user = db.get(UserDB, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     try:
#         stmt = update(UserDB).where(UserDB.id == user_id).values(**new_details)
#         db.execute(stmt)
#         db.commit()
#     except IntegrityError:
#         db.rollback()
#         raise HTTPException(status_code=409, detail="Conflict updating user")

#     updated_user = db.get(UserDB, user_id)
#     return updated_user
