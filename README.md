## Running the Project with Docker

This project includes a Docker setup for running the Python application in a reproducible environment. The Docker configuration is tailored for Python 3.10 and includes dependencies for audio playback (e.g., gTTS, mpg123).

### Project-Specific Docker Details

- **Python Version:** 3.10 (slim base image)
- **System Dependencies:**
  - `mpg123` (audio playback)
  - `gcc`, `libffi-dev`, `libsndfile1` (for building and running Python audio libraries)
- **Virtual Environment:** All Python dependencies are installed in a `.venv` directory inside the container.
- **Default Entrypoint:** Runs `add_words.py` by default (can be overridden).
- **User:** Runs as a non-root user (`appuser`) for security.

### Environment Variables
- No required environment variables are set by default in the Dockerfiles or Compose file.
- If your application requires environment variables, you can add them via a `.env` file and uncomment the `env_file` line in `docker-compose.yml`.

### Build and Run Instructions

1. **Build the Docker image and start the container:**
   ```sh
   docker compose up --build
   ```
   This will build the image and run the app, executing `python add_words.py` by default.

2. **Override the default command (optional):**
   To run a different script, use:
   ```sh
   docker compose run python-app python <your-script.py>
   ```

### Special Configuration
- No ports are exposed by default. If your application provides a web UI or API, uncomment and adjust the `ports` section in `docker-compose.yml`.
- No external services (databases, caches, etc.) are configured or required.
- No persistent volumes are defined; all data is ephemeral unless you add volumes.

### Ports
- **None exposed by default.**
  - If you add a web server or API, expose the relevant port in the `ports` section of `docker-compose.yml`.

---

_If you have additional configuration needs (such as environment variables or persistent storage), update the `docker-compose.yml` accordingly._
