# Facility Feed Service

This project implements a facility feed service that retrieves data from a database, generates JSON feed files (with optional gzip compression), and uploads them to a storage solution (local or S3). The project is designed with maintainability and future adaptability in mind.

## Table of Contents

- [Setup Instructions](#setup-instructions)
- [How to Run Locally](#how-to-run-locally)
- [Running Tests](#run-tests)
- [Linting](#linting)
- [Explanation of Approach](#explanation-of-approach)
- [Technologies Used](#technologies-used)

## Setup Instructions

### Prerequisites
- [Python 3.11 or higher](https://www.python.org/downloads/)
- [Docker & Docker-Compose(for local development)](https://www.docker.com/get-started)
- Poetry (for dependency management)
- PostgreSQL/MySQL (for database access)
- AWS Account with access to S3, ECR, ECS and IAM (for deployment)

1. **Clone the Repository**  
   Clone the repository to your local machine:
   ```bash
   git clone https://github.com/huzaifaahmed01/facility-feed-service.git
   cd facility-feed-service
   ```

2. **Install Dependencies**  
   Install the required dependencies using Poetry:
   ```bash
   poetry install
   ```

3. **Set Up Environment Variables**
    Copy the example environment file and fill in the required values:
   ```
    cp .env.example .env
   ```

4. **Database Setup**  
   Ensure you have a PostgreSQL or MySQL database running. Update the `.env` file with your database connection details.
    
    ```env
    DB_ENGINE=postgresql # or mysql
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=your_database_name
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    ```

    Run **db-init.sql** to create the required tables in your database. You can use a database client or run the SQL script directly in your database.


5. **AWS Credentials**
    If you are using S3 for storage, ensure your AWS credentials are set up in the `.env` file:
    ```env
    AWS_ACCESS_KEY_ID=your_access_key_id
    AWS_SECRET_ACCESS_KEY=your_secret_access_key
    AWS_REGION=your_aws_region
    S3_BUCKET_NAME=your_s3_bucket_name
    ```
6. **Other Environment Variables**
    Ensure the following environment variables are set in your `.env` file:
    ```env
    CHUNK_SIZE=1000 # Number of records per chunk
    FEED_TYPE=your_feed_type # e.g., 'facility'
    FEED_NAME=your_feed_name # e.g., 'facility_feed','reservewithgoogle.entity 
    ```

7. **Docker Setup (Optional)**
    If you prefer to run the service in a Docker container, ensure Docker is installed and running. You can build and run the Docker container using:
    ```bash
    docker build -t facility-feed-service .
    ```
    
## How to Run Locally

### Run the Service
To run the service locally, use the following command:
```bash
poetry run python main.py
```
This will start the service and begin processing the data.

### Run with Docker
To run the service in a Docker container, use the following command:
```bash
docker run -d --env-file .env facility-feed-service
```

### Run Tests
To run the tests, use the following command:
```bash
poetry run pytest tests/
```

### Linting
To check the code for linting issues, use the following command:
```bash
poetry run pylint app/ tests/
```

## Explanation of Approach

### Modular and Maintainable Design
- **Separation of Concerns:**
The project is structured into clear modules: db, feed, repositories, storage, and utils. Each module encapsulates its functionality, making the codebase easier to maintain and extend.

- **Interface-Driven Development:**
Key components (e.g., feed generators and storage adapters) implement well-defined interfaces. This approach allows you to easily swap implementations (e.g., replacing local storage with S3) without modifying the core logic.

- **Asynchronous Operations:**
The service leverages Python's asyncio along with async libraries such as asyncpg, aiomysql, and aioboto3 to ensure non-blocking I/O operations. This makes the service scalable and efficient under load.

- **Use of Design Patterns:**
The project employs design patterns such as the Factory pattern for creating feed generators and storage adapters, and the Repository pattern for database interactions. This enhances code organization and promotes reusability.

- **Support for future extensions:**
The modular design allows for easy addition of new feed types or storage solutions. For example, if you want to add support for a new database engine or a different storage service, you can create a new repository or storage adapter without affecting existing code.

### Robustness and Error Handling
- **Connection Pooling and Retry Logic:**
Database connection classes include connection pooling with retry logic (using exponential backoff) to handle transient errors gracefully.

- **Resilient File Operations:**
The storage adapters (both local and S3) include error handling, logging, and cleanup (e.g., deleting files after a successful upload) to maintain a consistent state.

### Code Quality and Testing
- **Dependency Management:**
The project uses Poetry for dependency management, ensuring that all required packages are installed and versioned correctly.

- **Unit and Integration Tests:**
The project is accompanied by a comprehensive test suite using pytest and pytest-asyncio, ensuring that each component works as expected.

- **Linting with pylint:**
Code quality is maintained through regular linting with pylint, which enforces a consistent code style and highlights potential issues early.

- **PEP8 Compliance:**
The code adheres to PEP8 standards, ensuring readability and maintainability.

- **Type Hinting:**
The codebase uses type hinting to improve code clarity and assist with static analysis, making it easier to understand the expected types of variables and function parameters.

- **Documentation:**
The code is well-documented with docstrings, providing clear explanations of the purpose and usage of each class and method. This documentation aids in understanding the codebase and serves as a reference for future developers.

## Technologies Used
- Python 3.11 or higher.
- Poetry for dependency management and packaging.
- Asyncio for asynchronous programming.
- asyncpg & aiomysql for asynchronous database operations.
- aioboto3 for asynchronous S3 interactions.
- pytest & pytest-asyncio for testing.
- pylint for linting and code quality.
- Logging using Python's built-in logging module.
- Docker for containerization
- PostgreSQL or MySQL for database access.
- AWS S3, ECR, ECS for cloud storage and deployment.

## Future Improvements
- **Support for Additional Storage Solutions:**
Implement support for other cloud storage providers (e.g., Google Cloud Storage, Azure Blob Storage) to enhance flexibility.
- **Enhanced Monitoring and Alerting:**
Integrate monitoring and alerting solutions (e.g., Prometheus, Grafana, or AWS CloudWatch) to track service performance and health.
- **Improved Error Handling:**
Implement more granular error handling and logging to capture specific error types and provide better insights into failures.