# RedisEntities

## How to install it?

You can install RedisEntites from this Github repository with `python3 setup.py install`,
or just install it directly from pypi with `pip3 install redis_entities`.

## What is it?

Redis Entities is a small library that allows you to map represent certain *entities* in Redis.
An *Entity* could be for example a Hashmap type and stores information about one User that currently requested a
password reset. Each Entity has a predefined Prefix used to differentiate the different types of Entities you create.
There are 4 different RedisEntities you can use:

- `RedisListEntity`
- `RedisSetEntity`
- `RedisHashmapEntity`
- `RedisSecureHashmapEntity`

`RedisSecureHahmapEntity` is a subclass of `RedisHashmapEntity` that provides Integrity protection to all of the
contained data in this hashmap.

## How does it work?

To create an own Entity, just subclass from one of the Provided RedisEntity Base classes.<br>
Note, that every Entity has to set the `redis_client` Class Attribute to an instance of `Redis` from `redis-py`, or
a class that supports all methods that `Redis` from `redis-py` does.


### RedisListEntity

```python3
import redis
from redis_entities import RedisListEntity
class JobQueueEntity(RedisListEntity):
    redis_client = redis.Redis(...)
    Prefix = "JobQueue"

MyRedisListEntity.lpush("Worker1", "command1")
assert MyRedisListEntity.length("Worker1") == 1
```
Supported Methods are:
- `lpush`
- `brpop`
- `get`
- `length`
- `clear`




### RedisSetEntity

```python3
import redis
from redis_entities import RedisSetEntity
class AccessTokensEntity(RedisSetEntity):
    redis_client = redis.Redis(...)
    Prefix = "AccessTokens"

AccessTokensEntity.add("User1", "Token1")
AccessTokensEntity.add("User2", "Token1")
assert AccessTokensEntity.exists("User1", "Token1") is True
```
Supported Methods are:
- `add`
- `delete`
- `clear`
- `exists`
- `list_all`
- `length`



### RedisHashmapEntity

```python3
import redis
from redis_entities import RedisHashmapEntity
class VerifyEmailTokens(RedisHashmapEntity):
    redis_client = redis.Redis(...)
    Prefix = "VerifyEmailTokens"
    Contents = (
        "MandatoryKey1",
        "MandatoryKey2"
    )
    Expire = 180

VerifyEmailTokens.store("test@example.com", MandatoryKey1="Value1", MandatoryKey2="Value2")
loaded_entity = VerifyEmailTokens.load("test@example.com")
assert loaded_entity.MandatoryKey1 == b"Value1"
assert loaded_entity.MandatoryKey1 == b"Value2"
assert VerifyEmailTokens.exists("test@example.com") is True
```

Supported Methods are:
- `store`
- `load`
- `exists`
- `length`
- `delete`
- `length`


### RedisSecureHashmapEntity

```python3
import redis
from redis_entities import RedisSecureHashmapEntity
class VerifyEmailTokens(RedisSecureHashmapEntity):
    redis_client = redis.Redis(...)
    Prefix = "VerifyEmailTokens"
    Contents = (
        "MandatoryKey1",
        "MandatoryKey2"
    )
    HMACKey = b"A" * 64
    Expire = 180

_, secret_information, = VerifyEmailTokens.store("test@example.com", MandatoryKey1="Value1", MandatoryKey2="Value2")
assert isinstance(secret_information, RedisSecureHashmapEntity.SecureIntegrityEntityInformation)
loaded_entity = VerifyEmailTokens.load("test@example.com")
assert loaded_entity.MandatoryKey1 == b"Value1"
assert loaded_entity.MandatoryKey1 == b"Value2"
```
Supported Methods are:
- the same as `RedisHashmapEntity`