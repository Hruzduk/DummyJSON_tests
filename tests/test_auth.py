import pytest
import allure


@allure.feature('Authentication')
@pytest.mark.auth
@pytest.mark.smoke
class TestAuthentication:
    @allure.story('User Login')
    @allure.description('Test user login with valid credentials and token generation')
    def test_user_login_and_get_token(self, api_client, test_user_credentials):
        """Test user login and token generation"""
        response = api_client.post(
            "/auth/login",
            json=test_user_credentials
        )

        assert response.status_code == 200, f"Login failed: {response.status_code} - {response.text}"

        data = response.json()
        assert "accessToken" in data, "No access token in response"
        assert "refreshToken" in data, "No refresh token in response"
        assert "id" in data, "No user ID in response"
        assert "username" in data, "No username in response"
        assert "email" in data, "No email in response"
        assert "firstName" in data, "No firstName in response"
        assert "lastName" in data, "No lastName in response"

        assert data["username"] == test_user_credentials["username"], "Username mismatch"

        access_token = data["accessToken"]
        assert access_token, "Access token is empty"
        assert len(access_token) > 10, "Access token seems too short"

    @allure.story('Profile Access')
    @allure.description('Verify authorized user can access their profile')
    def test_authorized_user_can_access_profile(self, authenticated_client):
        """Test that authorized user can access their profile via /user/me"""
        response = authenticated_client.get("/user/me")

        assert response.status_code == 200, (
            f"Failed to get user profile: {response.status_code} - {response.text}"
        )

        data = response.json()
        assert "id" in data, "No user ID in profile response"
        assert "username" in data, "No username in profile response"
        assert "email" in data, "No email in profile response"
        assert "firstName" in data, "No firstName in profile response"
        assert "lastName" in data, "No lastName in profile response"

        assert data["username"] == "emilys", "Username doesn't match expected value"
        assert data["email"] == "emily.johnson@x.dummyjson.com", "Email doesn't match expected value"

    @allure.story('Access Control')
    @allure.description('Verify unauthorized user cannot access protected endpoints')
    def test_unauthorized_user_cannot_access_profile(self, api_client):
        """Test that unauthorized user cannot access /user/me"""
        clean_client = APIClient()
        response = clean_client.get("/user/me")

        assert response.status_code == 401, (
            f"Expected 401 for unauthorized access, got {response.status_code}"
        )


from conftest import APIClient