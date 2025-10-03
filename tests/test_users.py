import pytest
import allure


@allure.feature('Users')
@pytest.mark.users
@pytest.mark.smoke
class TestUsers:
    @allure.story('User Search')
    @allure.description('Verify specific user exists with email emily.johnson@x.dummyjson.com')
    def test_user_with_specific_email_exists(self, api_client):
        """Verify that at least one user with email 'emily.johnson@x.dummyjson.com' is returned"""
        target_email = "emily.johnson@x.dummyjson.com"

        response = api_client.get("/users")
        assert response.status_code == 200, f"Failed to get users: {response.status_code}"

        data = response.json()
        assert "users" in data, "No 'users' field in response"

        users = data["users"]
        assert len(users) > 0, "No users returned"

        users_with_target_email = [
            user for user in users
            if user.get("email") == target_email
        ]

        assert len(users_with_target_email) >= 1, (
            f"No user found with email '{target_email}'. "
            f"Found emails: {[u.get('email') for u in users[:5]]}"
        )

        user = users_with_target_email[0]
        assert "id" in user, "User doesn't have an ID"
        assert "username" in user, "User doesn't have a username"
        assert "firstName" in user, "User doesn't have a firstName"
        assert "lastName" in user, "User doesn't have a lastName"