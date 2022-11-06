from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unexistant_post(authorized_client, test_posts):
    res = authorized_client.get("/posts/999")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize("title, content, published", [
    ("title1", "content1", True),
    ("title2", "content2", True),
    ("title3", "content3", False),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content":
                                                  content, "published": published})
    post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert post.title == title
    assert post.content == content
    assert post.published == published
    assert post.owner_id == test_user['id']


def test_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "title1", "content":
                                                  "content1"})
    post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert post.published == True


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "title1", "content":
                                       "content1"})
    assert res.status_code == 401


def test_unauthorized_post_delete(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_post_delete(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_post_delete_unexistant(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/999")
    assert res.status_code == 404


def test_delete_post_other_user(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_posts):
    data = {"title": "title1",
            "content": "content1",
            "id": test_posts[0].id}
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert post.title == data['title']
    assert post.content == data['content']


def test_other_user_post_update(authorized_client, test_user, test_user1, test_posts):
    data = {"title": "title1",
            "content": "content1",
            "id": test_posts[3].id}
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_post_update(client, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_post_update_unexistant(authorized_client, test_posts):
    data = {"title": "title1",
            "content": "content1",
            "id": test_posts[3].id}
    res = authorized_client.put(f"/posts/999", json=data)
    assert res.status_code == 404
