#!/bin/sh

# Run database setup
alembic upgrade head

# Run any other build commands you need
# e.g., migrations, static file generation, etc.
echo "Running other build commands..."

# Example: running a migration script


# Any other commands...
pip install -r requirements.txt

# Finally, start the FastAPI application (if needed during build)
uvicorn app.main:app --reload
