def test_tags_crud(client):
    # Create
    r = client.post("/tags/", json={"name": "work"})
    assert r.status_code == 200, r.text
    tag = r.json()
    assert tag["name"] == "work"

    # Get
    r = client.get(f"/tags/{tag['id']}")
    assert r.status_code == 200

    # List with pagination
    r = client.get("/tags?limit=10&offset=0")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

    # Update
    r = client.patch(f"/tags/{tag['id']}", json={"name": "personal"})
    assert r.status_code == 200
    assert r.json()["name"] == "personal"

    # Delete
    r = client.delete(f"/tags/{tag['id']}")
    assert r.status_code == 204


def test_stickies_crud(client):
    # Create two tags
    t1 = client.post("/tags/", json={"name": "t1"}).json()
    t2 = client.post("/tags/", json={"name": "t2"}).json()

    # Create sticky with tags
    payload = {
        "title": "note",
        "content": "content",
        "url": None,
        "tag_ids": [t1["id"], t2["id"]],
    }
    r = client.post("/stickies/", json=payload)
    assert r.status_code == 200, r.text
    sticky = r.json()
    assert sticky["title"] == "note"
    assert len(sticky["tags"]) == 2

    # Like
    r = client.post(f"/stickies/{sticky['id']}/like")
    assert r.status_code == 200
    assert r.json()["like_count"] == 1

    # Get by id
    r = client.get(f"/stickies/{sticky['id']}")
    assert r.status_code == 200

    # List with pagination
    r = client.get("/stickies?limit=5&offset=0")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

    # Update fields and tags
    r = client.patch(
        f"/stickies/{sticky['id']}",
        json={"title": "updated", "tag_ids": [t1["id"]]},
    )
    assert r.status_code == 200
    s2 = r.json()
    assert s2["title"] == "updated"
    assert len(s2["tags"]) == 1

    # Delete
    r = client.delete(f"/stickies/{sticky['id']}")
    assert r.status_code == 204


def test_create_sticky_with_missing_tag_returns_422(client):
    r = client.post(
        "/stickies/",
        json={"title": "x", "content": "y", "url": None, "tag_ids": [99999]},
    )
    assert r.status_code == 422
