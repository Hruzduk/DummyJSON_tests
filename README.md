# DummyJSON API Test Framework

![Daily Tests](https://github.com/Hruzduk/DummyJSON_tests/workflows/Daily%20API%20Tests/badge.svg)
[![Allure Report](https://img.shields.io/badge/Allure%20Report-View-orange)](https://hruzduk.github.io/DummyJSON_tests/)

Automated test framework for DummyJSON API using Python, Pytest, and Allure reporting.

## Features

- ✅ API testing for DummyJSON endpoints
- 📊 Allure reports with detailed test results
- 🔄 Daily automated test runs (10:00 AM Kyiv time)
- 🚀 GitHub Actions CI/CD integration
- 📈 Test history tracking

## Test Coverage

### Test Scenarios
1. **User Verification** - Verify user with email `emily.johnson@x.dummyjson.com`
2. **Authentication** - Login and token verification via `/user/me`
3. **Products Validation** - Verify minimum 5 products with required fields
4. **Product Search** - Parametrized search tests for different products

### Test Structure
```
tests/
├── conftest.py           # Fixtures and API client
├── test_auth.py          # Authentication tests
├── test_users.py         # User endpoint tests
├── test_products.py      # Product validation tests
└── test_product_search.py # Search functionality tests
```

## Installation

```bash
# Clone repository
git clone git@github.com:Hruzduk/DummyJSON_tests.git
cd DummyJSON_tests

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running Tests

### Local Execution
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test markers
pytest -m smoke
pytest -m auth

# Generate Allure report
pytest --alluredir=allure-results
allure serve allure-results
```

### PyCharm Configurations
Available run configurations:
- **All Tests** - Run all tests with timing
- **Smoke Tests** - Run critical tests only
- **Tests with HTML Report** - Generate HTML report

## CI/CD Pipeline

### GitHub Actions
Tests run automatically:
- **Daily**: 10:00 AM Kyiv time (08:00 UTC)
- **On Push**: To main/master branch
- **On PR**: Pull requests to main/master
- **Manual**: Via Actions tab

### Allure Reports
View test results at: `https://hruzduk.github.io/DummyJSON_tests/`

### Setup GitHub Pages
1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: `gh-pages` / `root`
4. Save

## Test Reports

### Allure Features
- Test execution history
- Detailed test steps
- Request/response logging
- Test categorization by features
- Execution trends

### Accessing Reports
- **Latest**: GitHub Pages URL
- **Local**: `allure serve allure-results`
- **CI**: Check Actions artifacts

## Project Dependencies

```txt
pytest==8.3.3
requests==2.32.3
pytest-html==4.1.1
allure-pytest==2.13.5
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit pull request

## Author

**Maksym Hrach** - [Hruzduk](https://github.com/Hruzduk)