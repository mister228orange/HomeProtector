from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

REDIS_URL = "redis://localhost:6379/0"

broker = ListQueueBroker(url=REDIS_URL).with_result_backend(
    RedisAsyncResultBackend(REDIS_URL)
)
