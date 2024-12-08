from typing import Optional, Any
from ..core import cache

class Cache:
    def __init__(self, key: str, ex: Optional[int] = None) -> None:
        self.key = key
        self.ex = ex

        self.cache = cache

    def get(self) -> Any:
        return self.cache.get(self.key)

    def set(self, value: Any) -> None:
        self.cache.set(self.key, value, ex=self.ex)

    def delete(self) -> None:
        self.cache.delete(self.key)

class CacheProvider(Cache):
    def __init__(self, *args) -> None:
        super().__init__('provider:' + ':'.join(args))

class CacheHistoryMonitor(Cache):
    def __init__(self, *args) -> None:
        super().__init__('history:monitor:' + ':'.join(map(str, args)), ex=1800)

class CacheWebhookMonitor(Cache):
    def __init__(self, *args) -> None:
        super().__init__('webhook:monitor:' + ':'.join(map(str, args)))

    def set(self, value: bool) -> None:
        return super().set(int(value))

    def get_all_webhook_active(self) -> list:
        keys = self.cache.keys('webhook:monitor:*')
        if not keys:
            return []

        return [int(key.split(':')[-1]) for key in keys if self.cache.get(key) not in [None, f'{int(False)}']]
    
    def delete_all_monitor_webhook(self) -> None:
        keys = self.cache.keys('webhook:monitor:*')
        for key in keys:
            self.cache.set(key, int(False))

class CacheWebhookUser(Cache):
    def __init__(self, *args) -> None:
        super().__init__('webhook:user:' + ':'.join(map(str, args)))

    def set(self) -> None:
        intents = self.get() if self.get() else 0
        return super().set(int(intents) + 1)

    def is_intents_webhook_limit(self) -> bool:
        return int(self.get() if self.get() else 0) == 3