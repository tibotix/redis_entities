import pytest

from src.mixins import HashedIdentifierMixin


def test_hashed_identifier_mixin():
    assert (
        HashedIdentifierMixin._hash_identifier("test")
        == "3d37fe58435e0d87323dee4a2c1b339ef954de63716ee79f5747f94d974f913f"
    )
    assert (
        HashedIdentifierMixin._hash_identifier(b"test")
        == "3d37fe58435e0d87323dee4a2c1b339ef954de63716ee79f5747f94d974f913f"
    )
