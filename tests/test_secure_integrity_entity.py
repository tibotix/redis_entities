import pytest

from src.secure_integrity_entity import SecureIntegrityEntity
from src.exceptions import IntegrityException

HMAC_KEY = b"\x8f\x85\x9en\xe8\xd6\xe2\xc4\xd3\xa7\xb2iD\xe6U~n.o\xe2\xc0\x94\xd2\xffn\xa2\x8d\x19\xcc\xd1\x80\xf7"
SALT = b"randomsalt"


def test_secure_integrity_entity_create():
    secure_entity = SecureIntegrityEntity.create(
        HMAC_KEY, 10, "Identifier", "some_extra", "data", salt=SALT
    )
    assert secure_entity.identifier == "Identifier"
    assert (
        secure_entity.identifier_hash.hex()
        == "8b8afa2bb31ae40afa1bf4f0a8ddcf638bc4fd0538f65e2372d6d9fc9f6497d8"  # pragma: allowlist secret
    )
    assert secure_entity.salt == SALT


def test_secure_integrity_entity_verify_mac():
    with pytest.raises(IntegrityException):
        SecureIntegrityEntity.verify_mac(
            HMAC_KEY, 10000, 10, b"identifierhash", b"mac", b"extra", salt=b"salt"
        )


def test_secure_integrity_entity_manipulated():
    secure_entity = SecureIntegrityEntity.create(
        HMAC_KEY, 10, "Identifier", "some_extra|", "data", salt=SALT
    )

    with pytest.raises(IntegrityException):
        SecureIntegrityEntity.verify_mac(
            HMAC_KEY, secure_entity.creation_timestamp, 10, secure_entity.identifier_hash, secure_entity.mac,
            "some_", "extra|data", salt=secure_entity.salt
        )