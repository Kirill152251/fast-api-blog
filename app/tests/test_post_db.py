import copy

import pytest
from sqlalchemy import select

from app.db import crud_post as crud
from app.db import schemas
from app.db.models import Post


def test_create_post(db, post_dto):
    post = crud.create_post(db, post_dto)
    assert post != None
    posts = db.scalars(select(Post)).all()
    assert len(posts) == 1
    assert post_dto.author_id == posts[0].author_id
    assert post_dto.group_id == posts[0].group_id
    assert post_dto.text == posts[0].text

def test_get_post(db, create_post_in_db):
    post = crud.get_post_by_id(db, create_post_in_db.id)
    assert post != None
    assert to_dict(post) == to_dict(create_post_in_db)

def test_get_non_existent_post(db, create_post_in_db):
    post = crud.get_post_by_id(db, create_post_in_db.id+1)
    assert post == None

def test_get_all_posts(db, create_two_posts):
    posts = copy.deepcopy(crud.get_all_posts(db))
    assert len(posts) == 2
    for (actually, expected) in zip(posts, create_two_posts):
        assert to_dict(actually) == to_dict(expected)

def test_delete_post(db, create_post_in_db: Post):
    assert len(get_posts(db)) == 1
    post = crud.delete_post(db, create_post_in_db.id)
    assert post != None
    assert len(get_posts(db)) == 0

def test_delete_non_existent_post(db, create_post_in_db: Post):
    assert len(get_posts(db)) == 1
    post = crud.delete_post(db, create_post_in_db.id+1)
    assert post == None
    assert len(get_posts(db)) == 1

def get_posts(db):
    return db.scalars(select(Post)).all()

def to_dict(post: Post): 
    return schemas.PostGet.model_validate(
        post, from_attributes=True
    ).model_dump()
