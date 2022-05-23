import pytest
from fakeredis import FakeRedis
from src import RedisHashmapEntity, RedisSecureHashmapEntity, RedisListEntity, RedisSetEntity


fake_redis_client = FakeRedis()


@pytest.fixture
def redis_client():
    for key in fake_redis_client.scan_iter("*"):
        fake_redis_client.delete(key)
    return fake_redis_client


@pytest.fixture
def redis_hashmap_entity(redis_client):
    contents = ['Key1', 'Key2']
    return type("TestHashmapEntity", (RedisHashmapEntity,), {'redis_client': redis_client, 'Prefix': 'TestPrefix',
                                                             'Contents': contents, 'Expire': 180})


@pytest.fixture
def redis_secure_hashmap_entity(redis_client):
    contents = ['Key1', 'Key2']
    hmac_key = b"deaddeaddeaddeaddeaddeaddeaddeaddeaddeaddeaddeaddeaddeaddeaddead"
    return type("TestSecureHashmapEntity", (RedisSecureHashmapEntity,), {
        'redis_client': redis_client, 'Prefix': 'TestPrefix',
        'Contents': contents, 'Expire': 180,
        'IntegrityHMACKey': hmac_key})


@pytest.fixture
def redis_list_entity(redis_client):
    return type("TestListEntity", (RedisListEntity,), {'redis_client': redis_client, 'Prefix': 'TestPrefix', })


@pytest.fixture
def redis_set_entity(redis_client):
    return type("TestSetEntity", (RedisSetEntity,), {'redis_client': redis_client, 'Prefix': 'TestPrefix', })

