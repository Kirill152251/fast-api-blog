from sqlalchemy.orm import Session


def is_exist(db: Session, pk: int, model) -> bool:
    return db.query(model.id).filter_by(id=pk).first() is not None
