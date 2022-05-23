import pytest


def test_list_entity_key_name(redis_list_entity):
    assert redis_list_entity.key_name("Identifier") == "TestPrefix:Identifier"


def test_list_entity_lpush(redis_client, redis_list_entity):
    assert redis_client.exists("TestPrefix:Identifier") == 0
    redis_list_entity.lpush("Identifier", "value1", "value2")
    assert redis_client.exists("TestPrefix:Identifier") == 1


def test_list_entity_brpop(redis_client, redis_list_entity):
    redis_list_entity.lpush("Identifier", "value1")
    assert redis_list_entity.brpop("Identifier") == (b"TestPrefix:Identifier", b"value1")


def test_list_entity_get(redis_client, redis_list_entity):
    redis_list_entity.lpush("Identifier", "value1", "value2")
    assert redis_list_entity.get("Identifier", 1) == b"value1"


def test_list_entity_length(redis_client, redis_list_entity):
    redis_list_entity.lpush("Identifier", "value1", "value2")
    assert redis_list_entity.length("Identifier") == 2


def test_list_entity_clear(redis_client, redis_list_entity):
    assert redis_list_entity.length("Identifier") == 0
    redis_list_entity.lpush("Identifier", "value1", "value2", "value3")
    assert redis_list_entity.length("Identifier") == 3
    redis_list_entity.clear("Identifier")
    assert redis_list_entity.length("Identifier") == 0
