import base64
import json
import pytest

from src.mixins import AuthenticatedEncryptionMixin
from src.exceptions import DecryptionException


class TestEntity(AuthenticatedEncryptionMixin):
    Expire = 180
    AesKey = b"deaddeaddeaddeaddeaddeaddeaddead"


class TestEntityImmediateExpire(AuthenticatedEncryptionMixin):
    Expire = 0
    AesKey = b"deaddeaddeaddeaddeaddeaddeaddead"


def test_authenticated_encryption():
    assert TestEntity.encrypt_data("key", "value") != TestEntity.encrypt_data(
        "key", "value"
    )


def test_authenticated_encryption_modified_key():
    data = TestEntity.encrypt_data("key", "value")
    with pytest.raises(DecryptionException):
        TestEntity.decrypt_data("key2", data)


def test_authenticated_encryption_modified_value():
    data = TestEntity.encrypt_data("key", "value")
    data = json.loads(base64.b64decode(data))
    data["t"] = ""
    data = base64.b64encode(json.dumps(data).encode())
    with pytest.raises(DecryptionException):
        TestEntity.decrypt_data("key", data)


def test_authenticated_encryption_expiration():
    data = TestEntityImmediateExpire.encrypt_data("key", "value")
    with pytest.raises(DecryptionException):
        TestEntityImmediateExpire.decrypt_data("key", data)
