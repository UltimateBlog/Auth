from typing import TypeVar

from sqlalchemy import select, Result

from .engine import Session

T = TypeVar("T", bound="BaseCRUD")


class BaseCRUD:
    @classmethod
    def get(cls: [T], pk: int) -> T:
        with Session() as session:
            return session.get(cls, pk)

    @classmethod
    def filter(cls: T, **filters) -> Result:
        # implement filtering with different lookup expression
        with Session() as session:
            return session.execute(
                select(cls).where(
                    *(
                        getattr(cls, field) == filter_value
                        for field, filter_value in filters.items()
                    )
                )
            )

    @classmethod
    def update(cls: T, pk: int, **update_info) -> T:
        pass

    @classmethod
    def delete(cls: T, pk: int) -> None:
        pass

    @classmethod
    def insert(cls: T, object_info: dict) -> T:
        pass
