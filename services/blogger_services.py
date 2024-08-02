from typing import Optional

from nameko.rpc import rpc


class BloggerService:
    name = "bloger_service"

    @rpc
    def get_blogger(self, blogger_id: int):
        pass

    @rpc
    def get_bloggers(self, **query_params: dict) -> list:
        pass

    @rpc
    def add_blogger(
        self, firstname: str, lastname: str, email: str, username: Optional[str]
    ):
        pass

    @rpc
    def delete_blogger(self, blogger_id: int):
        pass

    @rpc
    def update_blogger(self, blogger_id: int, **updated_params: dict):
        pass
