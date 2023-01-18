""" Repository file """
import abc
from copy import copy
from typing import Type, List

from sqlalchemy import delete, select
from sqlalchemy.orm import sessionmaker

from abstract import Factory
from ..models import Base


class Repository(Factory):
    """ Repository abstract class """

    model: Base
    type_model: Type[Base]

    def __init__(self, type_model: Type[Base], pool: sessionmaker):
        """
        Initialize abstract repository class
        :param type_model: Which model will be used for operations
        :param pool: Sessions pool
        """
        self.type_model = type_model
        self.pool = pool

    async def get(self, ident: int | str) -> Type[Base]:
        """
        Get an ONE model from the database with PK
        :param ident: Key which need to find entry in database
        :return:
        """
        async with self.pool() as session:
            return await session.get(entity=self.model, ident=ident)

    async def get_by_where(self, whereclause) -> Type[Base] | None:
        """
        Get an ONE model from the database with whereclause
        :param whereclause: Clause by which entry will be found
        :return: Model if only one model was found, else None
        """
        statement = select(self.type_model).where(whereclause)
        async with self.pool() as session:
            return (await session.execute(statement)).one_or_none()

    async def get_many(self, whereclause, limit: int = 100, order_by=None) -> List[Type[Base]]:
        """
        Get many models from the database with whereclause
        :param whereclause: Where clause for finding models
        :param limit: (Optional) Limit count of results
        :param order_by: (Optional) Order by clause

        Example:
        >> Repository.get_many(Model.id == 1, limit=10, order_by=Model.id)

        :return: List of founded models
        """
        statement = select(self.model)\
            .where(whereclause)\
            .limit(limit)
        if order_by:
            statement = statement.order_by(order_by)

        async with self.pool() as session:
            return (await session.scalars(statement)).all()

    async def delete(self, whereclause) -> None:
        """
        Delete model from the database

        :param whereclause: (Optional) Which statement
        :return: Nothing
        """
        statement = delete(self.model).where(whereclause)

        async with self.pool() as session:
            await session.execute(statement)
            await session.commit()

    async def update(self, key, value) -> None:
        """
        Update data
        :param key: which key to update
        :param value: value to set
        :return: Nothing
        """
        async with self.pool() as session:
            self.model.__setattr__(name=key, value=value)
            await session.commit()

    @abc.abstractmethod
    async def new(self, *args, **kwargs) -> None:
        """
        This method is need to be implemented in child classes,
        it is responsible for adding a new model to the database
        :return: Nothing
        """
        ...

    def __call__(self, model: Base, *args, **kwargs):
        _con_repository = copy(self)
        _con_repository.model = model
        return _con_repository
