import json
from core.redis import redis_client


class CacheService:
    @staticmethod
    async def cached(cache_key_name: str, model_id: int, repo, schema):
        cache_key = f"{cache_key_name}:{model_id}"
        cached = await redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        model = await repo.get_by_id(model_id)

        model_schema = schema.model_validate(model)

        await redis_client.set(
            cache_key,
            model_schema.model_dump_json(),
            ex=300
        )
        return model_schema
