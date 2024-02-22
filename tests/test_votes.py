import pytest
from app import models

@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote_on_post(authorized_client, test_posts, test_user):
    data = {
        "post_id": test_posts[3].id,
        "direction": 1,
    }
    assert test_user['id'] != test_posts[3].owner_id
    res = authorized_client.post("/vote/", json=data)
    assert res.status_code == 201

def test_vote_on_post_unauthorized(client, test_posts):
    data = {
        "post_id": test_posts[3].id,
        "direction": 1,
    }
    res = client.post("/vote/", json=data)
    assert res.status_code == 401

def test_vote_on_post_not_exist(authorized_client, test_posts):
    non_existent_post_id = 999999
    data = {
        "post_id": non_existent_post_id,
        "direction": 1,
    }
    res = authorized_client.post("/votes/", json=data)
    assert res.status_code == 404

def test_vote_on_post_already_voted(authorized_client, test_posts, test_vote):
    data = {
        "post_id": test_posts[3].id,
        "direction": 1,
    }
    res = authorized_client.post("/vote/", json=data)
    assert res.status_code == 409

def test_delete_vote(authorized_client, test_posts, test_vote):
    data = {
        "post_id": test_posts[3].id,
        "direction": 0,
    }
    res = authorized_client.post("/vote/", json=data)
    assert res.status_code == 201

def test_delete_vote_not_exist(authorized_client, test_posts):
    data = {
        "post_id": test_posts[3].id,
        "direction": 0,
    }
    res = authorized_client.post("/vote/", json=data)
    assert res.status_code == 404