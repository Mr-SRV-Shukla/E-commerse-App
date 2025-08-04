from functools import wraps
from django.core.cache import cache
from hashlib import md5

def cache_db_result(param_name, param_source='GET', timeout=60, include_user=False):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            # Extract param
            param_value = (
                request.POST.get(param_name, '') if param_source.upper() == 'POST'
                else request.GET.get(param_name, '')
            )
            print(param_value)
            # Build cache key
            key_parts = [func.__name__]
            if include_user and request.user.is_authenticated:
                key_parts.append(str(request.user.id))
            key_parts.append(md5(param_value.encode()).hexdigest())
            cache_key = ":".join(key_parts)

            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result

            # Cache miss - compute and store
            result = func(request, *args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result

        return wrapper
    return decorator
