from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):

    def save(self, session: Session):
        try:
            session.add(self)
            session.commit()
            return True
        except SQLAlchemyError as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(error)
            ) from error


    def delete(self, session: Session):
        try:
            session.delete(self)
            session.commit()
            return True
        except SQLAlchemyError as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(error)
            ) from error


    def update(self, session: Session, **kwargs):
        try:
            for k, v in kwargs.items():
                setattr(self, k, v)
            session.commit()
        except SQLAlchemyError as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(error)
            ) from error

