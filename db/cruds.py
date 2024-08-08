from typing import TypeVar, Type, Optional

from sqlalchemy import select, Select

from .engine import Session
from .exceptions import NotFound

T = TypeVar("T", bound="BaseCRUD")


class _Select(Select):
    def __init__(self, stmt: Select, *entities):
        super().__init__(*entities)
        self.stmt = stmt

    def all(self) -> list[T]:
        with Session() as session:
            return session.scalars(self.stmt).all()

    def one(self) -> T:
        with Session() as session:
            return session.scalars(self.stmt).one()

    def one_or_none(self) -> Optional[T]:
        with Session() as session:
            return session.scalars(self.stmt).one_or_none()

    def first(self) -> Optional[T]:
        with Session() as session:
            return session.scalars(self.stmt).first()


class CRUD:
    __LOOKUP_EXPRESSIONS = {"__lt__": "lt", "__gt__": "gt", "__eq__": "exact"}

    @classmethod
    def __get_columns(cls, exclude: Optional[set[str]] = None) -> list[str]:
        if exclude is None:
            exclude = set()
        return [c.key for c in cls.__table__.columns if c.key not in exclude]

    @classmethod
    def get(
        cls: Type[T],
        pk: int,
        _session: Optional[Session] = None,
        raise_not_found: bool = False,
    ) -> T:
        close_session = False
        if _session is None:
            _session = Session()
            close_session = True
        obj = _session.get(cls, pk)
        if close_session:
            _session.close()
        if not obj and raise_not_found:
            raise NotFound(f"{cls.__tablename__} Not Found!")
        return obj

    @classmethod
    def __construct_filter(cls, select_statement: Select, **filters) -> Select:
        selected_entity = select_statement.froms[0]
        columns = cls.__get_columns({"id"})
        where_clauses = list()
        for filter_, filter_value in filters.items():
            filter_lookup_split = filter_.split("__")
            field = filter_lookup_split[0]
            if field not in columns:
                raise AttributeError(
                    f"{selected_entity.name.title()} has no attribute {field}"
                )
            #  todo: implement filtering with different lookup expressions

            if len(filter_lookup_split) > 1:
                lookup_expression = cls.__LOOKUP_EXPRESSIONS.get(filter_lookup_split[1])
                if lookup_expression is None:
                    raise NotImplementedError(
                        f"{filter_lookup_split[1]} filter not supported"
                    )
            else:
                lookup_expression = "__eq__"
            column = getattr(selected_entity.c, field)
            operator = getattr(column, lookup_expression)
            where_clauses.append(operator(filter_value))
        return select_statement.where(*where_clauses)

    @classmethod
    def filter(cls: Type[T], **filters) -> _Select:
        applied_filter = cls.__construct_filter(select(cls), **filters)

        return _Select(applied_filter)

    @classmethod
    def update(cls: Type[T], pk: int, **update_info) -> T:
        with Session() as session:
            obj = cls.get(pk, session, True)
            for field, value in update_info.items():
                if field not in cls.__get_columns({"id"}):
                    raise AttributeError(
                        f"{cls.__tablename__.title()} has no attribute {field}"
                    )
                setattr(obj, field, value)
                session.commit()
                session.refresh(obj)
                return obj

    @classmethod
    def delete(cls: Type[T], pk: int) -> None:
        with Session() as session:
            obj = cls.get(pk, session)
            if obj:
                session.delete(obj)
                session.commit()

    @classmethod
    def insert(cls: Type[T], **attrs) -> T:
        for attr in attrs:
            if attr not in cls.__get_columns({"id"}):
                raise AttributeError(
                    f"{cls.__tablename__.title()} has no attribute {attr}"
                )
        with Session() as session:
            obj = cls(**attrs)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj
