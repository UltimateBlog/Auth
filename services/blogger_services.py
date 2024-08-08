from typing import Optional

from nameko.rpc import rpc

from db import Blogger
from db.utils import convert_object_to_dict


class BloggerService:
    name = "blogger_service"

    @rpc
    def get_blogger(self, blogger_id: int, raise_: bool = False) -> Optional[dict]:
        return convert_object_to_dict(Blogger.get(blogger_id, raise_not_found=raise_))

    @rpc
    def get_bloggers(self, **filters: dict) -> list[dict]:
        return convert_object_to_dict(Blogger.filter(**filters).all(), multi=True)

    @rpc
    def add_blogger(
        self,
        firstname: str,
        lastname: str,
        email: str,
        password: str,
        username: Optional[str],
    ) -> dict:
        return convert_object_to_dict(
            Blogger.insert(
                firstname=firstname,
                lastname=lastname,
                email=email,
                password=password,
                username=username,
            )
        )

    @rpc
    def delete_blogger(self, blogger_id: int) -> None:
        Blogger.delete(blogger_id)

    @rpc
    def update_blogger(self, blogger_id: int, **updated_params: dict) -> dict:
        return convert_object_to_dict(Blogger.update(blogger_id, **updated_params))
