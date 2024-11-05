

REST API for an Online Store

This project is a REST API for an online store built using Python and FastAPI. The API supports managing products, reserving and selling them, and generating sales reports.

### Installation

Clone the repository:
```git clone https://github.com/alextesshu/online_store_api.git```
```cd online_store_api```

Create and activate a virtual environment:
```python -m venv venv```
```venv\Scripts\activate```

Install dependencies:
```pip install -r requirements.txt```

### Running the Server

To start the server, use:
```uvicorn app.main:app --reload```

The application will be available at http://127.0.0.1:8000, and the Swagger documentation can be accessed at http://127.0.0.1:8000/docs.

### API Endpoints

    Get Product List
        GET /products/
        <!-- Returns a paginated list of available products with optional category filters. -->

        Query parameters:
            - skip (int): Number of products to skip.
            - limit (int): Number of products to return.

    Add a New Product
        POST /products/  
        <!-- Adds a new product to the database. -->
    
    Example request body:
    {
        "name": "New Product",
        "category_id": 1,
        "price": 199.99,
        "stock": 50
    }
    
    Update Product Price
        PATCH /products/{product_id}/price
        <!-- Updates the price of a product by its product_id. -->

    Delete a Product
        DELETE /products/{product_id}
        <!-- Description: Removes a product from the database by its ID. If the product does not exist, returns a 404 error. -->

    Reserve a Product
        POST /products/{product_id}/reserve
        <!-- Reserves a product, decreasing its stock. -->

    Cancel Product Reservation
        DELETE /products/{product_id}/cancel-reservation
        <!-- Cancels the reservation of a product, increasing its stock. -->

    Sell a Product
        POST /products/{product_id}/sell
        <!-- Processes the sale of a product, decreasing its stock. If the stock reaches zero, the product becomes unavailable (is_available = False). -->

    Start Promotion (Discount)
        PATCH /products/{product_id}/start-promotion
        <!-- Applies a discount to a specific product by updating its discount field and adjusting its price based on the discount percentage. -->

        Parameters:
            - product_id (path parameter): The ID of the product to apply the discount to.
            - discount (query parameter): A percentage (0-100) representing the discount to apply to the product.

    Sales Report Endpoint
        GET /products/sold/
        <!-- Retrieve a report of sold products, with optional filtering by date range and category. -->

        Parameters:
            - start_date (optional): The start date for filtering sold products.
            - end_date (optional): The end date for filtering sold products.
            - category_id (optional): The ID of the category to filter products by category.

        Response: A list of sold products that match the specified filters, each with details such as name, category, price, sale date, etc.


### Database Migrations

This project uses Alembic for database migrations. To manage database schema changes, follow these steps:
    - Initialize Alembic (if not already initialized):**
        ```alembic init alembic```

    - Create a Migration Script: Generate a new migration script based on changes in the models.
        ```alembic revision --autogenerate -m "Describe your change"```

    - Apply Migrations: To apply migrations to the database, run:
        ```alembic upgrade head```

    - Downgrade Migrations (if necessary): To revert the latest migration, use:
        ```alembic downgrade -1```
        

### Database Setup with Docker
    To set up a PostgreSQL database with Docker, use the following docker-compose.yml configuration:

    version: '3.8'

    services:
    postgres:
        image: postgres:16.0
        environment:
        POSTGRES_USER: postgres
        POSTGRES_PASSWORD: postgres
        POSTGRES_DB: test_store_db
        ports:
        - "5432:5432"
        volumes:
        - postgres_data:/var/lib/postgresql/data

    volumes:
    postgres_data:

Run Docker Compose to start the database:
    ```docker-compose up -d```

### Inserting Test Data

    To insert sample data into the database for testing, run:

```python tests/insert_test_data.py```

This script adds sample categories and subcategories to the database if they do not already exist.


### Running Tests

    To run the tests, use:
```pytest tests/test_api.py```
    This runs the tests in tests/test_api.py, which cover the core API functionality.

### Project Structure
    - app/main.py: Main application file where the FastAPI app is initialized.
    - app/db: Database models and initialization logic.
    - app/schemas: Pydantic schemas used for request validation and response formatting.
    - app/services: Contains business logic and operations related to products.
    - tests/: Folder with test files, including tests for the main API endpoints.

### Configuration Notes
    This project uses:

    - FastAPI for API handling.
    - SQLAlchemy for database management.
    - Alembic for database migrations.
    - Pydantic V2 for data validation.

### Additional Information
        Swagger: Full documentation is available at /docs.
        Error Handling: The API returns appropriate HTTP status codes, such as 404 for not found resources, 400 for invalid requests, and 200 for successful operations.
        DDD Structure: The project is structured according to Domain-Driven Design (DDD) principles, making it easier to maintain and extend.