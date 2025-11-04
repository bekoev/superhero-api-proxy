from collections.abc import AsyncIterator

import httpx
from dishka import Provider, Scope, provide


# TODO: Identify Superhero API-related client by a Dishka component
class HTTPProvider(Provider):
    @provide(scope=Scope.APP)
    async def superhero_http_client(self) -> AsyncIterator[httpx.AsyncClient]:
        async with httpx.AsyncClient() as session:
            yield session
