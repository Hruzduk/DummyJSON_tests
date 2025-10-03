import pytest
import allure


@allure.feature('Product Search')
@pytest.mark.products
class TestProductSearch:
    @pytest.fixture(scope="class")
    def search_terms(self, products_data):
        """Get 5 different product titles for parametrized search test"""
        if not products_data:
            pytest.skip("No products data available")

        product_titles = []
        for product in products_data[:10]:
            if "title" in product and product["title"]:
                words = product["title"].split()
                if words:
                    search_word = words[0]
                    if search_word not in product_titles:
                        product_titles.append(search_word)

        if len(product_titles) < 5:
            product_titles.extend(["Apple", "Phone", "Laptop", "Samsung", "iPhone"])

        return product_titles[:5]

    @allure.story('Parametrized Search')
    @pytest.mark.parametrize("search_index", [0, 1, 2, 3, 4])
    def test_product_search_returns_results(self, api_client, search_terms, search_index):
        """Test product search with different search terms"""
        search_term = search_terms[search_index]

        response = api_client.get("/products/search", params={"q": search_term})
        assert response.status_code == 200, (
            f"Search failed for '{search_term}': {response.status_code}"
        )

        data = response.json()
        assert "products" in data, f"No 'products' field in search response for '{search_term}'"

        products = data["products"]

        if len(products) > 0:
            for product in products:
                assert "id" in product, f"Product doesn't have ID in search results for '{search_term}'"
                assert "title" in product, f"Product doesn't have title in search results for '{search_term}'"
                assert "price" in product, f"Product doesn't have price in search results for '{search_term}'"
                assert "description" in product, f"Product doesn't have description in search results for '{search_term}'"

                product_text = f"{product.get('title', '')} {product.get('description', '')} {product.get('brand', '')}".lower()
                assert search_term.lower() in product_text or any(
                    word in product_text for word in search_term.lower().split()
                ), f"Search term '{search_term}' not found in product: {product.get('title')}"

    @allure.story('Special Query')
    @allure.description('Test search with Apple keyword')
    def test_search_with_special_query(self, api_client):
        """Test search with specific query 'Apple' as mentioned in requirements"""
        response = api_client.get("/products/search", params={"q": "Apple"})
        assert response.status_code == 200, f"Search for 'Apple' failed: {response.status_code}"

        data = response.json()
        assert "products" in data, "No 'products' field in search response"
        assert "total" in data, "No 'total' field in search response"
        assert "skip" in data, "No 'skip' field in search response"
        assert "limit" in data, "No 'limit' field in search response"

        products = data["products"]
        if len(products) > 0:
            for product in products:
                product_text = f"{product.get('title', '')} {product.get('description', '')} {product.get('brand', '')}".lower()
                assert "apple" in product_text or "iphone" in product_text or "ipad" in product_text or "mac" in product_text, (
                    f"Product doesn't seem related to 'Apple': {product.get('title')}"
                )

    @allure.story('Edge Cases')
    @allure.description('Test behavior with empty search query')
    def test_empty_search_query(self, api_client):
        """Test behavior with empty search query"""
        response = api_client.get("/products/search", params={"q": ""})
        assert response.status_code == 200, f"Empty search failed: {response.status_code}"

        data = response.json()
        assert "products" in data, "No 'products' field in response"
        assert isinstance(data["products"], list), "Products should be a list"