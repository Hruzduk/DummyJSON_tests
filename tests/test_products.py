import pytest
import allure


@allure.feature('Products')
@pytest.mark.products
@pytest.mark.smoke
class TestProducts:
    @allure.story('Product List')
    @allure.description('Verify minimum number of products returned')
    def test_products_list_returns_minimum_five_products(self, api_client):
        """Verify that at least 5 products are returned from /products endpoint"""
        response = api_client.get("/products")
        assert response.status_code == 200, f"Failed to get products: {response.status_code}"

        data = response.json()
        assert "products" in data, "No 'products' field in response"

        products = data["products"]
        assert len(products) >= 5, f"Expected at least 5 products, got {len(products)}"

    @allure.story('Product Validation')
    @allure.description('Verify each product has required fields: price, title, description')
    def test_each_product_has_required_fields(self, api_client):
        """Verify that each product has price, title, and description"""
        response = api_client.get("/products")
        assert response.status_code == 200, f"Failed to get products: {response.status_code}"

        data = response.json()
        products = data["products"]

        for index, product in enumerate(products[:10]):
            assert "price" in product, f"Product at index {index} doesn't have 'price' field"
            assert "title" in product, f"Product at index {index} doesn't have 'title' field"
            assert "description" in product, f"Product at index {index} doesn't have 'description' field"

            assert isinstance(product["price"], (int, float)), (
                f"Product {index}: price should be a number, got {type(product['price'])}"
            )
            assert product["price"] > 0, f"Product {index}: price should be positive"

            assert isinstance(product["title"], str), (
                f"Product {index}: title should be a string"
            )
            assert len(product["title"]) > 0, f"Product {index}: title should not be empty"

            assert isinstance(product["description"], str), (
                f"Product {index}: description should be a string"
            )
            assert len(product["description"]) > 0, (
                f"Product {index}: description should not be empty"
            )

    @allure.story('Product Schema')
    @allure.description('Verify products have complete schema with all expected fields')
    def test_products_have_additional_fields(self, api_client):
        """Verify that products have other expected fields"""
        response = api_client.get("/products", params={"limit": 1})
        assert response.status_code == 200

        product = response.json()["products"][0]

        expected_fields = [
            "id", "title", "description", "price", "discountPercentage",
            "rating", "stock", "brand", "category", "thumbnail", "images"
        ]

        for field in expected_fields:
            assert field in product, f"Product doesn't have '{field}' field"