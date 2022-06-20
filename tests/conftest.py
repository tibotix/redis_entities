import pytest
from fakeredis import FakeRedis
from src import RedisHashmapEntity, RedisListEntity, RedisSetEntity
from src.mixins import (
    HashedIdentifierMixin,
    AuthenticatedEncryptionMixin,
    DeterministicAuthenticatedEncryptionMixin,
)

fake_redis_client = FakeRedis()


class TestHashedIdentifierMixin(HashedIdentifierMixin):
    HashName = "sha512_256"


class TestSaltedHashedIdentifierMixin(HashedIdentifierMixin):
    HashName = "sha512_256"
    Salt = b"salt"


class TestAuthenticatedEncryptionMixin(AuthenticatedEncryptionMixin):
    AesKey = b"deaddeaddeaddeaddeaddeaddeaddead"


class TestDeterministicAuthenticatedEncryptionMixin(
    DeterministicAuthenticatedEncryptionMixin
):
    AesKey = b"deaddeaddeaddeaddeaddeaddeaddeaddeaddeaddeaddeaddeaddeaddeaddead"


mixin_combinations = [
    (),
    (TestHashedIdentifierMixin,),
    (TestSaltedHashedIdentifierMixin,),
    (TestAuthenticatedEncryptionMixin,),
    (TestDeterministicAuthenticatedEncryptionMixin,),
    (
        TestHashedIdentifierMixin,
        TestAuthenticatedEncryptionMixin,
    ),
    (
        TestHashedIdentifierMixin,
        TestDeterministicAuthenticatedEncryptionMixin,
    ),
]
mixin_combination_ids = [
    "No Mixin",
    "HashedIdentifierMixin",
    "SaltedHashedIdentifierMixin",
    "AuthenticatedEncryptionMixin",
    "DeterministicAuthenticatedEncryptionMixin",
    "HashedIdentifierMixin+AuthenticatedEncryptionMixin",
    "HashedIdentifierMixin+DeterministicAuthenticatedEncryptionMixin",
]
nondeterministic_mixin_combinations = [
    combination
    for combination in mixin_combinations
    if TestAuthenticatedEncryptionMixin in combination
]
deterministic_mixin_combinations = [
    combination
    for combination in mixin_combinations
    if TestAuthenticatedEncryptionMixin not in combination
]
nondeterministic_mixin_combination_ids = [
    mixin_combination_ids[mixin_combinations.index(combination)]
    for combination in nondeterministic_mixin_combinations
]
deterministic_mixin_combination_ids = [
    mixin_combination_ids[mixin_combinations.index(combination)]
    for combination in deterministic_mixin_combinations
]


@pytest.fixture
def redis_client():
    for key in fake_redis_client.scan_iter("*"):
        fake_redis_client.delete(key)
    return fake_redis_client


@pytest.fixture
def hashed_identifier_mixin():
    return TestHashedIdentifierMixin


@pytest.fixture
def salted_hashed_identifier_mixin():
    return TestSaltedHashedIdentifierMixin


@pytest.fixture
def aead_encryption_mixin():
    return TestAuthenticatedEncryptionMixin


@pytest.fixture
def deterministic_aead_encryption_mixin():
    return TestDeterministicAuthenticatedEncryptionMixin


@pytest.fixture
def redis_hashmap_entity(redis_client):
    contents = ["Key1", "Key2"]
    return type(
        "TestHashmapEntity",
        (RedisHashmapEntity,),
        {
            "RedisClient": redis_client,
            "Prefix": "TestPrefix",
            "Contents": contents,
            "Expire": 180,
        },
    )


@pytest.fixture(params=mixin_combinations, ids=mixin_combination_ids)
def parametrized_redis_hashmap_entity(request, redis_hashmap_entity):
    return type(
        "TestParametrizedHashmapEntity", (redis_hashmap_entity, *request.param), {}
    )


@pytest.fixture
def redis_list_entity(redis_client):
    return type(
        "TestListEntity",
        (RedisListEntity,),
        {
            "RedisClient": redis_client,
            "Prefix": "TestPrefix",
            "Expire": 180,
        },
    )


@pytest.fixture(params=mixin_combinations, ids=mixin_combination_ids)
def parametrized_redis_list_entity(request, redis_list_entity):
    return type("TestParametrizedListEntity", (redis_list_entity, *request.param), {})


@pytest.fixture
def redis_set_entity(redis_client):
    return type(
        "TestSetEntity",
        (RedisSetEntity,),
        {
            "RedisClient": redis_client,
            "Prefix": "TestPrefix",
            "Expire": 180,
        },
    )


@pytest.fixture(params=mixin_combinations, ids=mixin_combination_ids)
def parametrized_redis_set_entity(request, redis_set_entity):
    return type("TestParametrizedSetEntity", (redis_set_entity, *request.param), {})


@pytest.fixture(
    params=nondeterministic_mixin_combinations,
    ids=nondeterministic_mixin_combination_ids,
)
def parametrized_redis_nondeterministic_set_entity(request, redis_set_entity):
    return type("TestParametrizedSetEntity", (redis_set_entity, *request.param), {})


@pytest.fixture(
    params=deterministic_mixin_combinations, ids=deterministic_mixin_combination_ids
)
def parametrized_redis_deterministic_set_entity(request, redis_set_entity):
    return type("TestParametrizedSetEntity", (redis_set_entity, *request.param), {})
