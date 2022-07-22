# RedisEntities

## How to install it?

You can install RedisEntites from this Github repository with `python3 setup.py install`,
or just install it directly from pypi with `pip3 install redis-entities`.

## What is it?

Redis Entities is a small library that allows you to map represent certain *entities* in Redis.
An *Entity* could be for example a Hashmap type and stores information about one User that currently requested a
password reset. Each Entity has a predefined Prefix used to differentiate the different types of Entities you create.
There are 3 different RedisEntities you can use:

- `RedisListEntity`
- `RedisSetEntity`
- `RedisHashmapEntity`

In addition there are a couple of mixins, which can be used to provide additional functionality to your entities.
There are 3 different Mixins you can use:

 - `HashedIdentifierMixin`: All identifiers are hashed before stored in Redis
 - `AuthenticatedEncryptionMixin`: All values are encrypted and authenticated before stored in Redis
 - `DeterministicAuthenticatedEncryptionMixin`: All values are encrypted and authenticated deterministically (the same value is encrypted to the same ciphertext) before stored in Redis

You can also combine multiple Mixins, except `AuthenticatedEncryptionMixin` and `DeterministicAuthenticatedEncryptionMixin`.

## How does it work?

To create an own Entity, just subclass from one of the Provided RedisEntity Base classes.<br>Note, that every Entity has to set the `RedisClient` Class Attribute to an instances of `Redis` from `redis-py`, or
a class that supports all methods that `Redis` from `redis-py` does.

Under the hood all keys are stored as strings, and all values are stored as bytes in Redis.


### RedisListEntity:

```python3
import redis
from redis_entities import RedisListEntity
from redis_entities.mixins import AuthenticatedEncryptionMixin
class JobQueueEntity(RedisListEntity, AuthenticatedEncryptionMixin):
    RedisClient = redis.Redis(...)
    Prefix = "JobQueue"
    AesKey = b"deaddeaddeaddeaddeaddeaddeaddead" # AES-128 in this case

JobQueueEntity.lpush("Worker1", "command1")
assert JobQueueEntity.length("Worker1") == 1
```
Supported Methods are:
- `lpush`
- `brpop`
- `lindex`
- `length`
- `clear`




### RedisSetEntity:

```python3
import redis
from redis_entities import RedisSetEntity
from redis_entities.mixins import DeterministicAuthenticatedEncryptionMixin
class AccessTokensEntity(RedisSetEntity, DeterministicAuthenticatedEncryptionMixin):
    RedisClient = redis.Redis(...)
    Prefix = "AccessTokens"
    Expire = 180
    AesKey = b"deaddeaddeaddeaddeaddeaddeaddeaddeaddeaddeaddeaddeaddeaddeaddead" # need to be twice the size of the key required by the underlying cipher (e.g. 64 bytes for AES-256)

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

NOTE: It is strongly recommended to use the `DeterministicAuthenticatedEncryptionMixin` instead of the `AuthenticatedEncryptionMixin` when you are working with `RedisSetEntity` , as most methods need to know the exact value that is stored in Redis. With the `DeterministicAuthenticatedEncryptionMixin` , the same plaintext results in the same ciphertext and thus makes this possible. 

### RedisHashmapEntity

```python3
import redis
from redis_entities import RedisHashmapEntity, 
from redis_entities.mixins import HashedIdentifierMixin, AuthenticatedEncryptionMixin
class VerifyEmailTokens(RedisHashmapEntity, HashedIdentifierMixin, AuthenticatedEncryptionMixin):
    RedisClient = redis.Redis(...)
    Prefix = "VerifyEmailTokens"
    Contents = (
        "MandatoryKey1",
        "MandatoryKey2"
    )
    Expire = 180
    HashName = "sha512_256"
    Salt = b"VerifyEmailTokens"
    AesKey = b"deaddeaddeaddeaddeaddeaddeaddead"

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

- `delete`

- `length`

  

