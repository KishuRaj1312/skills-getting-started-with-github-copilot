def test_get_activities(client):
    resp = client.get('/activities')
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert 'Chess Club' in data


def test_signup_and_duplicate(client):
    email = 'newstudent@mergington.edu'
    # Ensure not in participants
    resp = client.get('/activities')
    assert email not in resp.json()['Chess Club']['participants']

    # Signup
    post = client.post(f"/activities/Chess Club/signup?email={email}")
    assert post.status_code == 200
    assert 'Signed up' in post.json()['message']

    # Now present
    resp2 = client.get('/activities')
    assert email in resp2.json()['Chess Club']['participants']

    # Duplicate signup should 400
    dup = client.post(f"/activities/Chess Club/signup?email={email}")
    assert dup.status_code == 400


def test_signup_nonexistent_activity(client):
    post = client.post('/activities/NoSuchActivity/signup?email=test@x.com')
    assert post.status_code == 404


def test_remove_participant(client):
    # Ensure known participant exists
    resp = client.get('/activities')
    participants = resp.json()['Chess Club']['participants']
    assert 'daniel@mergington.edu' in participants

    # Remove
    delr = client.delete('/activities/Chess Club/participants?email=daniel@mergington.edu')
    assert delr.status_code == 200
    assert 'Removed daniel@mergington.edu' in delr.json()['message']

    # Confirm removed
    after = client.get('/activities').json()['Chess Club']['participants']
    assert 'daniel@mergington.edu' not in after

    # Removing non-existing participant returns 404
    del2 = client.delete('/activities/Chess Club/participants?email=noone@nowhere.edu')
    assert del2.status_code == 404


def test_remove_nonexistent_activity(client):
    delr = client.delete('/activities/NoSuchActivity/participants?email=test@x.com')
    assert delr.status_code == 404
