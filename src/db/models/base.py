"""Base model."""
from sqlalchemy import Integer, MetaData
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

metadata = MetaData(
    naming_convention={
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_%(constraint_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s',
    }
)


@as_declarative(metadata=metadata)
class Base:
    """Abstract model with declarative base functionality."""

    @classmethod
    @declared_attr
    def __tablename__(cls):
        """Hooks __tablename__ attribute based on model name.

        You can skip specifying this attribute in models, then name for table
        will be got from the model's name.
        """
        return cls.__name__.lower()

    __allow_unmapped__ = False

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True
    )
