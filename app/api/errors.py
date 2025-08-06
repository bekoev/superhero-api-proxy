from fastapi import HTTPException, status


class HeroNotFoundError(HTTPException):
    def __init__(self, name: str):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f"Hero {name} not found"


class MultipleHeroesFoundError(HTTPException):
    def __init__(self, message: str):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = message
