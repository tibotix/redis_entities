import pytest
from src.parameters import timestamp2b
from src.exceptions import IntegrityException


def test_redis_hashmap_entity_key_name(redis_hashmap_entity):
    assert (
        redis_hashmap_entity.key_name("Identifier")
        == "TestPrefix:Identifier"
    )


def test_redis_hashmap_enforce_valid_entity(redis_hashmap_entity):
    redis_hashmap_entity.store('Identifier', Key1='Value1', Key2='Value2')
    redis_hashmap_entity.store('Identifier', Key1='Value1', Key2='Value2', extra=0)
    with pytest.raises(AttributeError):
        redis_hashmap_entity.store('Identifier', Key1='Value1')
    with pytest.raises(AttributeError):
        redis_hashmap_entity.load('Identifierdoesnotexist')


def test_redis_hashmap_store(redis_client, redis_hashmap_entity):
    reg = redis_hashmap_entity.store("Identifier", Key1='Value1', Key2='Value2')

    loaded_obj = redis_client.hgetall("TestPrefix:Identifier")
    assert loaded_obj.get(b"Key1") == reg.Key1 == b"Value1"
    assert loaded_obj.get(b"Key2") == reg.Key2 == b"Value2"
    assert redis_client.ttl("TestPrefix:Identifier") > 0

    with pytest.raises(AttributeError):
        redis_hashmap_entity.store("Identifier", Key1="Value1")


def test_redis_hashmap_exists(redis_hashmap_entity):
    assert redis_hashmap_entity.exists("Identifier") is False

    redis_hashmap_entity.store(
        "Identifier", Key1="Value1", Key2="Value2"
    )
    assert redis_hashmap_entity.exists("Identifier") is True


def test_redis_hashmap_load(redis_client, redis_hashmap_entity):
    redis_hashmap_entity.store(
        "Identifier", Key1="Value1", Key2="Value2"
    )
    reg = redis_hashmap_entity.load("Identifier")
    loaded_obj = redis_client.hgetall("TestPrefix:Identifier")
    assert loaded_obj.get(b"Key1") == reg.Key1 == b"Value1"
    assert loaded_obj.get(b"Key2") == reg.Key2 == b"Value2"
    assert redis_client.ttl(b"TestPrefix:Identifier") > 0


def test_hashmap_length(redis_hashmap_entity):
    redis_hashmap_entity.store("Identifier", Key1="Value1", Key2="Value2")
    assert redis_hashmap_entity.length("Identifier") == 2

    redis_hashmap_entity.store("Identifier2", Key1="Value1", Key2="Value2", extra=0)
    assert redis_hashmap_entity.length("Identifier2") == 3


def test_redis_hashmap_delete(redis_hashmap_entity):
    redis_hashmap_entity.store(
        "Identifier", Key1="Value1", Key2="Value2"
    )
    assert redis_hashmap_entity.exists("Identifier") is True
    redis_hashmap_entity.delete("Identifier")
    assert redis_hashmap_entity.exists("Identifier") is False


def test_redis_secure_hashmap(redis_client, redis_secure_hashmap_entity):
    entity, secure_entity, = redis_secure_hashmap_entity.store(
        "Identifier", Key1="Value1", Key2="Value2"
    )
    identifier_hash = entity.identifier
    identifier_plain = secure_entity.identifier
    assert identifier_plain == "Identifier"
    assert len(secure_entity.salt) == 0

    assert redis_client.exists("TestPrefix:" + identifier_hash) == 1
    obj = redis_client.hgetall("TestPrefix:" + identifier_hash)
    assert obj.get(b"ExpireInterval") == timestamp2b(
        redis_secure_hashmap_entity.Expire
    )
    assert obj.get(b"Key1") == b"Value1"

    loaded_obj = redis_secure_hashmap_entity.load(identifier_plain)
    assert not hasattr(loaded_obj, "ExpireInterval")
    assert not hasattr(loaded_obj, "CreationTimestamp")
    assert not hasattr(loaded_obj, "HMAC")
    assert loaded_obj.Key1 == b"Value1"

    assert redis_secure_hashmap_entity.exists(identifier_plain) is True

    redis_secure_hashmap_entity.delete(identifier_plain)
    assert redis_secure_hashmap_entity.exists(identifier_plain) is False
    assert redis_client.exists("TestPrefix:" + identifier_hash) == 0


def test_redis_secure_hashmap_manipulated(redis_client, redis_secure_hashmap_entity):
    entity, secure_entity = redis_secure_hashmap_entity.store(
        "Identifier", Key1="Value1", Key2="Value2"
    )
    identifier_hash = entity.identifier
    identifier_plain = secure_entity.identifier
    redis_client.hset(
        "TestPrefix:" + identifier_hash, key="Key1", value="ModifiedValue1"
    )
    with pytest.raises(IntegrityException):
        redis_secure_hashmap_entity.load(identifier_plain)
