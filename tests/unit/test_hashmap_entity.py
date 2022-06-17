import pytest


def test_redis_hashmap_entity_identifier(redis_hashmap_entity):
    assert redis_hashmap_entity.build_identifier("Identifier") == "TestPrefix:Identifier"


def test_redis_hashmap_enforce_valid_entity(redis_hashmap_entity):
    redis_hashmap_entity.store("Identifier", Key1="Value1", Key2="Value2")
    redis_hashmap_entity.store("Identifier", Key1="Value1", Key2="Value2", extra="0")
    with pytest.raises(AttributeError):
        redis_hashmap_entity.store("Identifier", Key1="Value1")
    with pytest.raises(AttributeError):
        redis_hashmap_entity.load("Identifierdoesnotexist")


def test_redis_hashmap_store(redis_client, redis_hashmap_entity):
    reg = redis_hashmap_entity.store("Identifier", Key1="Value1", Key2="Value2")

    loaded_obj = redis_client.hgetall("TestPrefix:Identifier")
    assert loaded_obj.get(b"Key1") == reg.Key1 == b"Value1"
    assert loaded_obj.get(b"Key2") == reg.Key2 == b"Value2"
    assert redis_client.ttl("TestPrefix:Identifier") > 0

    with pytest.raises(AttributeError):
        redis_hashmap_entity.store("Identifier", Key1="Value1")


def test_redis_hashmap_exists(redis_hashmap_entity):
    assert redis_hashmap_entity.exists("Identifier") is False

    redis_hashmap_entity.store("Identifier", Key1="Value1", Key2="Value2")
    assert redis_hashmap_entity.exists("Identifier") is True


def test_redis_hashmap_load(redis_client, redis_hashmap_entity):
    redis_hashmap_entity.store("Identifier", Key1="Value1", Key2="Value2")
    reg = redis_hashmap_entity.load("Identifier")
    loaded_obj = redis_client.hgetall("TestPrefix:Identifier")
    assert loaded_obj.get(b"Key1") == reg.Key1 == b"Value1"
    assert loaded_obj.get(b"Key2") == reg.Key2 == b"Value2"
    assert redis_client.ttl(b"TestPrefix:Identifier") > 0


def test_hashmap_length(redis_hashmap_entity):
    redis_hashmap_entity.store("Identifier", Key1="Value1", Key2="Value2")
    assert redis_hashmap_entity.length("Identifier") == 2

    redis_hashmap_entity.store("Identifier2", Key1="Value1", Key2="Value2", extra="0")
    assert redis_hashmap_entity.length("Identifier2") == 3


def test_redis_hashmap_delete(redis_hashmap_entity):
    redis_hashmap_entity.store("Identifier", Key1="Value1", Key2="Value2")
    assert redis_hashmap_entity.exists("Identifier") is True
    redis_hashmap_entity.delete("Identifier")
    assert redis_hashmap_entity.exists("Identifier") is False

