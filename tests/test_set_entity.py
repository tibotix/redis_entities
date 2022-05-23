import pytest


def test_set_entity_key_name(redis_set_entity):
    assert redis_set_entity.key_name("Identifier") == "TestPrefix:Identifier"


def test_set_entity_add(redis_client, redis_set_entity):
    assert redis_client.sismember("TestPrefix:Identifier", "value") is False
    redis_set_entity.add("Identifier", "value")
    assert redis_client.sismember("TestPrefix:Identifier", "value") is True


def test_set_entity_delete(redis_client, redis_set_entity):
    redis_set_entity.add("Identifier", "value")
    assert redis_client.sismember("TestPrefix:Identifier", "value") is True
    redis_set_entity.delete("Identifier", "value")
    assert redis_client.sismember("TestPrefix:Identifier", "value") is False


def test_set_entity_clear(redis_client, redis_set_entity):
    redis_set_entity.add("Identifier", "value", "value2")
    assert redis_client.sismember("TestPrefix:Identifier", "value") is True
    assert redis_client.sismember("TestPrefix:Identifier", "value2") is True
    redis_set_entity.clear("Identifier")
    assert redis_client.sismember("TestPrefix:Identifier", "value") is False
    assert redis_client.sismember("TestPrefix:Identifier", "value2") is False


def test_set_entity_exists(redis_set_entity):
    assert redis_set_entity.exists("Identifier", "value") is False
    redis_set_entity.add("Identifier", "value", "value2")
    assert redis_set_entity.exists("Identifier", "value") is True


def test_set_entity_list_all(redis_set_entity):
    values = ("Value", "Value2", "Value3")
    redis_set_entity.add("Identifier", *values)
    assert all(map(lambda x: x.decode() in values, redis_set_entity.list_all("Identifier")))


def test_set_entity_length(redis_set_entity):
    redis_set_entity.add("Identifier", "Value")
    redis_set_entity.add("Identifier2", "Value", "Value2")
    assert redis_set_entity.length("Identifier2") == 2
