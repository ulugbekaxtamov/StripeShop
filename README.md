# StripeShop

## Getting Started

These instructions will help you run a copy of the project on your local machine for development and testing.

### Prerequisites

Install the following tools:

- Docker
- Docker Compose

### Installation and Launch

1. **Cloning the repository**:
    ```
    git clone https://github.com/ulugbekaxtamov/StripeShop.git
    ```

2. **Navigate to the project directory**:
    ```
    cd StripeShop
    ```

3. **Create `.env` files using examples**:
    ```
    cat example.env > .env
    ```
    - Please fill in the `STRIPE_PUBLIC_TOKEN` and `STRIPE_SECRET_TOKEN` values in the `.env` file.

4. **Run Docker Compose**:
    ```
    docker-compose up --build
    ```

### API Documentation

Access the Swagger documentation for API details at:

```
http://127.0.0.1:8000/redoc/
```

```
http://127.0.0.1:8000/swagger/
```

### Project Structure

```

├── README.md # This file
├── docker-compose.yaml # Docker Compose configuration for development
├── Dockerfile # Dockerfile for the main server
├── requirements.txt # Python dependencies
├── .env # Environment variables
├── main/ # Main Django project folder
│ ├── settings.py # Import Base class here
│ └── ...
├── base/ # Manage soft deletion and default fields
│ ├── apps.py
│ ├── models.py # Base class imported here
│ └── ...
├── products/ # Products app
├── user/ # User management app
......
```