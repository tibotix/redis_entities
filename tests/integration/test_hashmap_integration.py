import pytest


def test_hashmap_integration(parametrized_redis_hashmap_entity):
    assert parametrized_redis_hashmap_entity.exists("Identifier1") is False
    parametrized_redis_hashmap_entity.store(
        "Identifier1", Key1=b"value1", Key2=b"value2"
    )
    assert parametrized_redis_hashmap_entity.exists("Identifier1") is True
    assert parametrized_redis_hashmap_entity.length("Identifier1") == 2

    loaded_values = parametrized_redis_hashmap_entity.load("Identifier1")
    assert loaded_values.Key1 == b"value1"
    assert loaded_values.Key2 == b"value2"

    parametrized_redis_hashmap_entity.delete("Identifier1")
    assert parametrized_redis_hashmap_entity.exists("Identifier1") is False
