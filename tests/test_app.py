from urllib.parse import quote


def test_get_activities(client):
    # Arrange: client fixture
    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success(client):
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"

    # Act
    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify participant shows up
    resp2 = client.get("/activities")
    assert email in resp2.json()[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange
    email = "michael@mergington.edu"  # already in Chess Club initial data
    activity = "Chess Club"

    # Act
    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 400


def test_unregister_success(client):
    # Arrange
    email = "daniel@mergington.edu"
    activity = "Chess Club"

    # Act
    resp = client.delete(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    resp2 = client.get("/activities")
    assert email not in resp2.json()[activity]["participants"]


def test_unregister_not_found(client):
    # Arrange
    email = "noone@mergington.edu"
    activity = "Chess Club"

    # Act
    resp = client.delete(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404
