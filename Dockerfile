FROM python:3.13-slim

WORKDIR /app
RUN pip install uv

# Copy the entire project first so hatchling can find README.md and src/
COPY . .

# Install production dependencies (not editable, no dev dependencies)
RUN uv pip install --system .

CMD ["uvicorn", "--factory", "platformmind.api.app:create_app", "--host", "0.0.0.0", "--port", "8000"]
