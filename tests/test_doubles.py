"""Test Doubles — TODO: Stub / Mock / Fake"""
from unittest.mock import Mock
from src.calc import calculate_discount
from src.email_service import send_welcome_email
from src.store import FakeDB, User


# --- Stub: TODO ---
def get_user_stub(user_id: int) -> dict:
    return {"id": user_id, "name": "Test", "tier": "vip"}

def test_with_stub():
    user = get_user_stub(1)
    assert calculate_discount(1000, user["tier"], None) == 150


# --- Mock: TODO ---
def test_send_email_mock():
    mock_service = Mock()
    mock_service.send.return_value = True
    result = send_welcome_email("student@up.ac.th", email_service=mock_service)
    assert result is True
    mock_service.send.assert_called_once_with(to="student@up.ac.th", subject="Welcome to Campus Eats", body="Hello!")


# --- Fake: TODO ---
def test_fake_db():
    db = FakeDB()
    user = User(id=1, name="Mint", tier="member")
    db.save(user)
    assert db.get(1).name == "Mint"
