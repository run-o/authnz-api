class TestGetUserData:

    def test_requires_authentication(self, client):
        response = client.get(
            "/user_data/by_email",
            params={"email": "notloggedint@test.com"},
            headers=None,
        )
        assert response.status_code == 401
        assert response.json() == {
            "detail": "Not authenticated"
        }
        
    def test_cannot_access_other_user_data(self, client, logged_in_user_token_header,
                                           create_user, create_user_data):
        create_user(email="otheruser@email.com")
        create_user_data(email="otheruser@email.com", data="some data")
                
        auth_header = logged_in_user_token_header("loggedinuser@email.com")
        response = client.get(
            "/user_data/by_email",
            params={"email": "otheruser@email.com"},
            headers=auth_header,
        )
        assert response.status_code == 404
        assert response.json() == {
            "detail": "No user data found for email otheruser@email.com."
        }
        
    def test_return_own_user_data(self, client, logged_in_user_token_header,
                                  create_user, create_user_data):
        create_user(email="loggedinuser@email.com")
        create_user_data(email="loggedinuser@email.com", data="some data")
        
        auth_header = logged_in_user_token_header("loggedinuser@email.com")
        response = client.get(
            "/user_data/by_email",
            params={"email": "loggedinuser@email.com"},
            headers=auth_header,
        )
        assert response.status_code == 200
        res_json = response.json()
        assert len(res_json) == 1
        assert res_json[0]['personal_data'] == "some data"


class TestCreateUserData:

    def test_requires_authentication(self, client):
        response = client.post(
            "/user_data/",
            json={
                "user_id": "some_user_id",
                "personal_data": "some data"
            },
            headers=None,
        )
        assert response.status_code == 401
        assert response.json() == {
            "detail": "Not authenticated"
        }
        
    def test_cannot_create_other_user_data(self, client, logged_in_user_token_header,
                                           create_user, create_user_data):
        other_user = create_user(email="otheruser@email.com")
                
        auth_header = logged_in_user_token_header("loggedinuser@email.com")
        response = client.post(
            "/user_data/",
            json={
                "user_id": str(other_user.user_id),
                "personal_data": "some data"
            },
            headers=auth_header,
        )
        assert response.status_code == 403
        assert response.json() == {
            "detail": f"Cannot create data for user {other_user.user_id}."
        }
        
    def test_can_create_own_data(self, client, logged_in_user_token_header,
                                  create_user, create_user_data):
        user = create_user(email="loggedinuser@email.com")     
        auth_header = logged_in_user_token_header("loggedinuser@email.com")
        response = client.post(
            "/user_data/",
            json={
                "user_id": str(user.user_id),
                "personal_data": "some data"
            },
            headers=auth_header,
        )
        assert response.status_code == 200
        res_json = response.json()
        assert res_json['personal_data'] == "some data"