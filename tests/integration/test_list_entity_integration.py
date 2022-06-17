import pytest


def test_list_integration(parametrized_redis_list_entity):
    parametrized_redis_list_entity.lpush("Identifier1", "value1", "value2")
    # list contains: <HEAD> value2 , value1 <END>
    assert parametrized_redis_list_entity.length("Identifier1") == 2
    assert parametrized_redis_list_entity.length("Identifier2") == 0
    assert parametrized_redis_list_entity.lindex("Identifier1", 0) == b"value2"
    assert parametrized_redis_list_entity.brpop("Identifier1") == (
        parametrized_redis_list_entity.build_identifier("Identifier1").encode(),
        b"value1",
    )
    assert parametrized_redis_list_entity.length("Identifier1") == 1
    parametrized_redis_list_entity.clear("Identifier1")
    assert parametrized_redis_list_entity.length("Identifier1") == 0
