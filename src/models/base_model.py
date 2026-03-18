import datetime
import re
from sqlalchemy import func, DateTime
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


def camel_to_snake(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def make_plural(word):
    word = camel_to_snake(word)
    if word.endswith('y'):
        return word[:-1] + 'ies'
    if word.endswith(('s', 'sh', 'ch', 'x', 'z')):
        return word + 'es'
    if word.endswith('fe'):
        return word[:-2] + 'ves'
    if word.endswith('f'):
        return word[:-1] + 'ves'

    return word + 's'


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return make_plural(cls.__name__)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
