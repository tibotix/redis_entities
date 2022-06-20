import pytest


def test_deterministic_set_integration(parametrized_redis_deterministic_set_entity):
    assert (
        parametrized_redis_deterministic_set_entity.exists("Identifier1", "value1")
        is False
    )
    parametrized_redis_deterministic_set_entity.add("Identifier1", "value1", "value2")
    assert (
        parametrized_redis_deterministic_set_entity.exists("Identifier1", "value1")
        is True
    )
    assert parametrized_redis_deterministic_set_entity.length("Identifier1") == 2
    parametrized_redis_deterministic_set_entity.delete("Identifier1", "value1")
    assert (
        parametrized_redis_deterministic_set_entity.exists("Identifier1", "value1")
        is False
    )
    assert parametrized_redis_deterministic_set_entity.length("Identifier1") == 1
    assert (
        parametrized_redis_deterministic_set_entity.exists("Identifier1", "value2")
        is True
    )
    parametrized_redis_deterministic_set_entity.clear("Identifier1")
    assert (
        parametrized_redis_deterministic_set_entity.exists("Identifier1", "value2")
        is False
    )


def test_nondeterministic_set_integration(
    parametrized_redis_nondeterministic_set_entity,
):
    assert (
        parametrized_redis_nondeterministic_set_entity.exists("Identifier1", "value1")
        is False
    )
    parametrized_redis_nondeterministic_set_entity.add(
        "Identifier1", "value1", "value2"
    )
    assert (
        parametrized_redis_nondeterministic_set_entity.exists("Identifier1", "value1")
        is False
    )
    assert parametrized_redis_nondeterministic_set_entity.length("Identifier1") == 2
    parametrized_redis_nondeterministic_set_entity.delete("Identifier1", "value1")
    assert (
        parametrized_redis_nondeterministic_set_entity.exists("Identifier1", "value1")
        is False
    )
    assert parametrized_redis_nondeterministic_set_entity.length("Identifier1") == 2
    assert (
        parametrized_redis_nondeterministic_set_entity.exists("Identifier1", "value2")
        is False
    )
    parametrized_redis_nondeterministic_set_entity.clear("Identifier1")
    assert (
        parametrized_redis_nondeterministic_set_entity.exists("Identifier1", "value2")
        is False
    )
    assert parametrized_redis_nondeterministic_set_entity.length("Identifier1") == 0
