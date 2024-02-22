from typing import List
from app import schemas
import pytest

# def test_get_all_posts(authorized_client, test_posts):
#     res = authorized_client.get("/posts/")
#     def validate_post(post):
#         return schemas.PostResponse(**post)
    
#     posts_map = map(validate_post, res.json())
#     posts_list = list(posts_map)

#     assert res.status_code == 200
#     assert posts_list[0].id == test_posts[0].id
#     assert posts_list[0].title == test_posts[0].title
#     assert posts_list[0].content == test_posts[0].content
#     assert posts_list[0].owner_id == test_posts[0].owner_id

# def test_get_all_posts_unauthorized(client, test_posts):
#     res = client.get("/posts/")
#     assert res.status_code == 401

# def test_get_one_post_unauthorized(client, test_posts):
#     res = client.get(f"/posts/{test_posts[0].id}")
#     assert res.status_code == 401

# def test_get_one_post_not_exist(authorized_client, test_posts):
#     res = authorized_client.get(f"/posts/8888")
#     assert res.status_code == 404

# def test_get_one_post(authorized_client, test_posts):
#     res = authorized_client.get(f"/posts/{test_posts[0].id}")
#     print(res.json())
#     post = schemas.PostResponse(**res.json())
#     assert res.status_code == 200
#     assert post.id == test_posts[0].id
#     assert post.title == test_posts[0].title
#     assert post.content == test_posts[0].content
#     assert post.owner_id == test_posts[0].owner_id


# @pytest.mark.parametrize("title, content, published",[
#     ("awesome new title", "awesome new content", True),
#     ("favorite pizza", "i love pepperoni", False),
#     ("tallest skyscrappers", "wahoo", True),
# ])
# def test_create_post(authorized_client, test_user, title, content, published):
#     res = authorized_client.post("/posts/", json={
#         "title": title,
#         "content": content,
#         "published": published
#     })
#     created_post = schemas.PostOut(**res.json())
#     assert res.status_code == 201
#     assert created_post.title == title
#     assert created_post.content == content
#     assert created_post.published == published
#     assert created_post.owner_id == test_user['id']


# def test_create_post_published_default(authorized_client, test_user):
#     res = authorized_client.post("/posts/", json={
#         "title": "arbitrary title",
#         "content": "whatever"
#     })

#     created_post = schemas.PostOut(**res.json())
#     print(created_post)
#     assert res.status_code == 201
#     assert created_post.title == "arbitrary title"
#     assert created_post.content == "whatever"
#     assert created_post.published == True
#     assert created_post.owner_id == test_user['id']


# def test_create_post_unauthorized(client):
#     res = client.post("/posts/", json={
#         "title": "arbitrary title",
#         "content": "whatever"
#     })
#     assert res.status_code == 401
    
# def test_delete_post_unauthorized(client, test_posts):
#     res = client.delete(f"/posts/{test_posts[0].id}")
#     assert res.status_code == 401

# def test_delete_post_success(authorized_client, test_posts, test_user):
#     assert test_posts[0].owner_id == test_user['id']
#     res = authorized_client.delete(f"/posts/{test_posts[0].id}")
#     assert res.status_code == 204

# def test_delete_post_not_exist(authorized_client, test_posts):
#     non_existent_post_id = 999999999
#     res = authorized_client.delete(f"/posts/{non_existent_post_id}")
#     assert res.status_code == 404

# def test_delete_post_forbidden(authorized_client, test_posts):
#     res = authorized_client.delete(f"/posts/{test_posts[3].id}")
#     assert res.status_code == 403


def test_update_post(authorized_client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
    }

    assert test_user['id'] == test_posts[0].owner_id
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostOut(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_post_forbidden(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
    } 
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_update_post_unauthorized(client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401

def test_update_post_not_exist(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
    }
    non_existent_post_id = 999999
    res = authorized_client.put(f"/posts/{non_existent_post_id}", json=data)
    assert res.status_code == 404