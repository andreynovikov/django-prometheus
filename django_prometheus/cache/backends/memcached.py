from django import VERSION as DJANGO_VERSION
from django.core.cache.backends import memcached

from django_prometheus.cache.metrics import (
    django_cache_get_total,
    django_cache_hits_total,
    django_cache_misses_total,
)


class MemcachedPrometheusCacheMixin:
    def get(self, key, default=None, version=None):
        django_cache_get_total.labels(backend="memcached").inc()
        cached = super().get(key, default=None, version=version)
        if cached is not None:
            django_cache_hits_total.labels(backend="memcached").inc()
        else:
            django_cache_misses_total.labels(backend="memcached").inc()
        return cached or default


class MemcachedCache(MemcachedPrometheusCacheMixin, memcached.MemcachedCache):
    """Inherit memcached to add metrics about hit/miss ratio"""

    pass


if DJANGO_VERSION >= (3, 2):

    class PyLibMCCache(MemcachedPrometheusCacheMixin, memcached.PyLibMCCache):
        """Inherit memcached to add metrics about hit/miss ratio"""

        pass

    class PyMemcacheCache(MemcachedPrometheusCacheMixin, memcached.PyMemcacheCache):
        """Inherit memcached to add metrics about hit/miss ratio"""

        pass
