from collections.abc import AsyncIterator

import httpx
from dishka import Provider, Scope, provide


class HTTPProvider(Provider):
    component = "superhero-api"

    @provide(scope=Scope.APP)
    async def superhero_http_client(self) -> AsyncIterator[httpx.AsyncClient]:
        async with httpx.AsyncClient() as session:
            yield session
