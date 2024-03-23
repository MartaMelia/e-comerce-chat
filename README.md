
# E-COMERCE CHAT


## Architecture Description

The project is structured into a modular fashion to ensure separation of concerns and ease of navigation. Below is the architecture of the project, detailing the purpose and contents of each directory:

### `.venv`
This directory contains the virtual environment where all the dependencies required for the project are installed. This helps in keeping the project dependencies isolated from the global Python environment.

### `src`
The source code of the project is contained within this directory.

#### `config`
Holds the configuration files and scripts for the project, including `configuration.py` which likely contains settings and constants used throughout the application.

#### `data`
Contains data files used by the project. For example, `raw_data.csv` might include input data that the project processes.

#### `routers`
This directory holds the router definitions for the project, likely used for handling HTTP requests if the project includes a web server component.

- `prompts.py`: Likely contains functions related to generating prompts for the chat.
- `public.py`: Possibly includes functions that serve publicly available data or endpoints.
- `request.py`: Handles incoming requests to the server.

### `vectors/vector (ID)`
This uniquely identified directory (`f13ca344-4ca8-4d83-a096-2c77b4f6da07`) seems to be related to data indexing or a specific vectorization process used in the project.

- `data_level0.bin`, `header.bin`, `length.bin`, `link_lists.bin`: Binary files that might be used for storing vector data.
- `index_metadata.pickle`: A serialized file containing metadata about the index.
- `chroma.sqlite3`: A SQLite3 database file, potentially storing indexed data or lookup tables.

#### `main.py`
The main entry point of the application, which runs the core logic.

### Project Root Files

- `.gitignore`: Specifies intentionally untracked files to ignore by Git.
- `config.yml`: Contains configuration settings for the project.
- `README.md`: The Markdown file where the project documentation is provided.
- `requirements.txt`: Lists all Python dependencies necessary to run the project.


## `configuration.py`

### Overview
The `configuration.py` script is an integral component of the application that initializes the application's configurations and sets up the data and vector embedding required for the project's operation.

### Functionality
- **Configuration Loading**: Uses `box` and `yaml` to parse `config.yml`, allowing for easy access to configuration values.
- **Data Initialization (`_init_data`)**: Prepares directories for data storage, downloads data, and invokes data processing.
- **Data Filtering (`_data_filter`)**: Cleans the CSV data using `pandas`, and maintains necessary columns.
- **Vector Initialization (`_init_vector`)**: Initializes vector storage and embeddings, and persists them for efficient retrieval.

### Interaction with Other Components
- Works with `langchain` for document loading and `Chroma` for vector storage.
- Downloads data with `requests`.
- Uses Google AI embeddings for vector initialization.

### Usage
Invoke `configure` at the application's startup to ensure all settings and dependencies are correctly set up.

```python
# Example usage
if __name__ == "__main__":
    configure()
```

## `prompts.py`

### Overview
`prompts.py` contains predefined templates for generating responses in an e-commerce consulting context. The script is designed to provide detailed explanations and tailored advice to customers, leveraging product data from a structured CSV file.

### Functionality
The script defines a template, `assistant_prompt`, which structures the response for the e-commerce assistant. It ensures that each product suggestion is formatted with the following details:
- Title
- Price
- Detailed Explanation
- Product URL
- Product Image

The prompt enforces a standardized response that includes five specific product suggestions, using relevant data extracted from predefined columns in the dataset.

## `request.py`

### Overview
`request.py` is responsible for defining the schema of requests that the e-commerce assistant can handle. It utilizes Pydantic, which is a data validation and settings management library, to enforce type annotations and data validation for incoming requests to the application.

### Functionality
The script creates a `BaseModel` class named `AssistantRequest`, which serves as a data model for the user's request. This model ensures that all incoming data fits the expected structure, with proper data types and fields.

### AssistantRequest Model
- **question**: A string field that contains the customer's question or inquiry. This field is mandatory for a request to be valid.


## `public.py`

### Overview
`public.py` defines the API routes for the e-commerce chat application. It uses FastAPI to create an `APIRouter` that handles incoming POST requests to the `/assistant` endpoint. The script integrates the chatbot logic, vector retrieval, and response generation into the API.

### Functionality
- **APIRouter Setup**: Initializes the API router and defines the POST endpoint `/assistant` for assistant interactions.
- **Configuration Loading**: Loads settings from `config.yml` to configure the chatbot and vector store.
- **Image Link Cleaning**: A utility function `_clean_image_links` is provided to validate and clean image URLs in the chatbot's responses.
- **Assistant Endpoint**: The main API endpoint that accepts an `AssistantRequest`, processes it, and returns the generated answer. It utilizes several components:
  - `GoogleGenerativeAIEmbeddings`: For generating vector embeddings of the input.
  - `Chroma`: A vector store for efficient document retrieval.
  - `ChatGoogleGenerativeAI`: A large language model for generating responses.
  - Document Chains: Combines documents from the vector store with prompts to generate a coherent response.

### Endpoint Description
- **POST `/assistant`**: Accepts a JSON object with a `question` field. It processes the question using a retrieval chain and returns a structured and cleaned response.

### Example Usage
```python
import requests

# Define the API endpoint
url = 'http://<host>:<port>/assistant'

# Example request data
request_data = {
    "question": "Can you recommend some eco-friendly notebooks?"
}

# Sending a POST request to the API endpoint
response = requests.post(url, json=request_data)
print(response.json())
```

## `main.py`

### Overview
`main.py` orchestrates the launching of the FastAPI web application. It includes the setup of routing, middleware for Cross-Origin Resource Sharing (CORS), custom OpenAPI schema generation, and runs the server instance.

### Features
- **FastAPI App Initialization**: Sets up the FastAPI app and includes the router from `public.py`.
- **CORS Middleware Configuration**: Configures allowed origins and headers to handle cross-origin requests, essential for frontend communication.
- **Custom OpenAPI Schema**: Overrides the default OpenAPI schema generation to provide custom API documentation.
- **Root Endpoint**: Provides a simple health check endpoint that returns `{"health: OK"}`.

### Launching the Application
The application is started by invoking the `configure` function to load configurations and then running the `uvicorn` ASGI server with the FastAPI application instance.

### Custom Swagger UI
Provides a custom Swagger UI for the API documentation accessible via the `/docs` endpoint.

### Usage
Run the `main.py` script to start the server:

```bash
python main.py
