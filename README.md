# Project Agent - Planning, Estimation, and Allocation

This project uses a crew of AI agents to generate project plans based on input project details. It provides a FastAPI backend and a simple HTML/JavaScript frontend for interaction.

## Project Structure

- **/backend**: Contains the FastAPI application and core logic.
  - `app_FastAPI.py`: The main FastAPI application file.
  - `/src`: Core Python modules for the AI crew, configuration, etc.
- **/config**: Contains YAML configuration files for agents and tasks.
  - `agents.yaml`: Defines the AI agents.
  - `tasks.yaml`: Defines the tasks for the AI crew.
- **/frontend**: Contains a simple HTML/JavaScript frontend.
  - `index.html`: The main interface file.
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
    *(Note: If you are in the `backend` directory, the path to requirements.txt is `../requirements.txt`)*

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

## Running the Frontend

1.  **Ensure the backend is running** (see "Running the Backend" above).
2.  **Open the `frontend/index.html` file in your web browser.**
    - You can typically do this by navigating to the project's root directory in your file explorer and double-clicking the `index.html` file located in the `frontend` folder.
    - Alternatively, from the command line, you might use a command like `open frontend/index.html` (on macOS) or `start frontend/index.html` (on Windows).

    The interface will allow you to input project details and see the streamed logs and results from the backend.

### Frontend Interface Screenshot

*(Placeholder: An image of the frontend interface would be displayed here.)*

The screenshot would show:
- Input fields for: Project Name/Type, Industry, Project Objectives, Team Members, and Project Requirements.
- A "Generate Project Plan" button.
- An area below the form where live logs from the AI agent crew are displayed.
- A separate area where the final structured project plan (JSON) is shown once the generation is complete.

## API Endpoint (Backend)

- **POST /stream**:
  - Accessed by the frontend at `http://localhost:8000/stream`.
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
