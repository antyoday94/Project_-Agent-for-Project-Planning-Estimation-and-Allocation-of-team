# Project Agent - Planning, Estimation, and Allocation

This project uses a crew of AI agents to generate project plans based on input project details. It provides a FastAPI backend for interaction.

## Project Structure

- **/backend**: Contains the FastAPI application and core logic.
  - `app_FastAPI.py`: The main FastAPI application file.
  - `/src`: Core Python modules for the AI crew, configuration, etc.
- **/config**: Contains YAML configuration files for agents and tasks.
  - `agents.yaml`: Defines the AI agents.
  - `tasks.yaml`: Defines the tasks for the AI crew.
- **/frontend**: Placeholder for a frontend application. Currently empty.
- `requirements.txt`: Python dependencies for the backend.
- `setup.py`: Python project setup file.

## Running the Backend

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Install dependencies:**
    Make sure you have Python 3.8+ installed. It's recommended to use a virtual environment.
    ```bash
    pip install -r ../requirements.txt
    ```
    *(Note: If you are in the \`backend\` directory, the path to requirements.txt is \`../requirements.txt\`)*

3.  **Run the FastAPI application:**
    You can run the application directly using Python:
    ```bash
    python app_FastAPI.py
    ```
    Or using Uvicorn for more control (e.g., auto-reload):
    ```bash
    uvicorn app_FastAPI:app --reload --host 0.0.0.0 --port 8000
    ```

    The API will then be available at `http://localhost:8000`.

## API Endpoint

- **POST /stream**:
  - Accepts a JSON body with project details:
    ```json
    {
      "project": "string",
      "industry": "string",
      "project_objectives": "string",
      "team_members": "string",
      "project_requirements": "string"
    }
    ```
  - Streams back logs and the final project plan as Server-Sent Events (SSE).
```
