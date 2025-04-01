# Recommendation System

This project is a recommendation system built with FastAPI. Follow the instructions below to set up the development environment and start the server.

## Prerequisites

-   Python 3.8 or higher installed on your system.
-   `uv` installed for managing Python virtual environments. You can install it following the instructions here https://docs.astral.sh/uv/getting-started/installation/.

## Setup Instructions

1. **Clone the Repository**  
   Clone this repository to your local machine:

```bash
git clone git@github.com:23210287thongtruong/recommendation-system.git
cd recommendation-system
```

2. **Install Dependencies**  
   Sync and install the required dependencies:

```bash
uv sync
```

3. **Start the Development Server**  
   Run the FastAPI development server:

```bash
fastapi dev main.py
```

4. **Test the API Endpoints**  
   Once the server is running, you can test the API endpoints by navigating to:

```
http://127.0.0.1:8000/docs
```

This will open the interactive Swagger UI for testing the API.

## Contributing

Feel free to fork this repository and submit pull requests. Make sure to follow the coding standards and include tests for any new features.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
