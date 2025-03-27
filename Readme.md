# Facility Feed Service

This is a Python-based service for managing facility feeds.

## Requirements
- Python 3.8 or higher
- Docker (optional, for containerized deployment)

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/facility-feed-service.git
    cd facility-feed-service
    ```

2. Create a virtual environment and install dependencies:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python app.py
    ```

## Docker Instructions

1. Build the Docker image:
    ```bash
    docker build -t facility-feed-service .
    ```

2. Run the Docker container:
    ```bash
    docker run -p 8000:8000 facility-feed-service
    ```

3. Access the service at `http://localhost:8000`.

## Testing

Run the tests using:
```bash
pytest
```

## License

This project is licensed under the MIT License.  