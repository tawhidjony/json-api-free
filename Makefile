# Makefile for CRUD API Project
# Usage: make <target>

.PHONY: help install run dev test clean migrate upgrade downgrade revision create-tables drop-tables reset-db

# Default target
help:
	@echo "Available commands:"
	@echo "  install        - Install project dependencies"
	@echo "  run            - Run the FastAPI server"
	@echo "  dev            - Run the server in development mode with auto-reload"
	@echo "  test           - Run tests (if available)"
	@echo "  clean          - Clean Python cache files"
	@echo "  migrate        - Create a new migration"
	@echo "  upgrade        - Apply all pending migrations"
	@echo "  downgrade        - Rollback the last migration"
	@echo "  create-tables  - Create all database tables"
	@echo "  drop-tables    - Drop all database tables"
	@echo "  reset-db       - Reset database (drop and recreate tables)"
	@echo "  status         - Show migration status"
	@echo "  history        - Show migration history"
	@echo "  fix-migration  - Fix common migration issues"
	@echo "  test-cors      - Test CORS configuration"
	@echo "  test-external-cors - Test CORS with external origin"
	@echo "  test-external-cors-script - Test CORS with external origin (Python script)"
	@echo "  serve-cors-test - Serve CORS test HTML file"

# Install dependencies
install:
	@echo "Installing project dependencies..."
	pip install -r requirements.txt

# Run the server
run:
	@echo "Starting FastAPI server..."
	python runserver.py

# Run in development mode
dev:
	@echo "Starting FastAPI server in development mode..."
	python runserver.py --reload

# Clean Python cache
clean:
	@echo "Cleaning Python cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	@echo "Cache cleaned!"

# Alembic migration commands
migrate:
	@echo "Creating new migration..."
	@read -p "Enter migration message: " message; \
	. .venv/bin/activate && alembic revision --autogenerate -m "$$message"

upgrade:
	@echo "Applying all pending migrations..."
	. .venv/bin/activate && alembic upgrade head

downgrade:
	@echo "Rolling back the last migration..."
	. .venv/bin/activate && alembic downgrade -1

status:
	@echo "Migration status:"
	. .venv/bin/activate && alembic current
	@echo ""
	@echo "Pending migrations:"
	. .venv/bin/activate && alembic heads

history:
	@echo "Migration history:"
	. .venv/bin/activate && alembic history --verbose

# Fix common migration issues
fix-migration:
	@echo "Fixing common migration issues..."
	@echo "1. Checking for enum type conflicts..."
	@echo "2. Ensuring proper column defaults..."
	@echo "3. Migration file has been updated to handle enum types properly"
	@echo "Now try running: make upgrade"

# Database management
create-tables:
	@echo "Creating database tables..."
	. .venv/bin/activate && alembic upgrade head

drop-tables:
	@echo "Dropping all database tables..."
	. .venv/bin/activate && alembic downgrade base

reset-db:
	@echo "Resetting database..."
	. .venv/bin/activate && alembic downgrade base
	. .venv/bin/activate && alembic upgrade head
	@echo "Database reset complete!"

# Test commands (placeholder - add your test framework)
test:
	@echo "Running tests..."
	@echo "No tests configured yet. Add your test framework to requirements.txt"
	@echo "Common options: pytest, unittest"

# Development utilities
format:
	@echo "Formatting code with black..."
	@if command -v black >/dev/null 2>&1; then \
		black .; \
	else \
		echo "black not found. Install with: pip install black"; \
	fi

lint:
	@echo "Linting code with flake8..."
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 .; \
	else \
		echo "flake8 not found. Install with: pip install flake8"; \
	fi

# Database URL check
check-db:
	@echo "Checking database configuration..."
	@if [ -z "$$DATABASE_URL" ]; then \
		echo "Warning: DATABASE_URL environment variable not set"; \
		echo "Please set it in your .env file or environment"; \
	else \
		echo "Database URL is configured"; \
	fi

# Environment setup
setup-env:
	@echo "Setting up environment..."
	@if [ ! -f .env ]; then \
		echo "Creating .env file from template..."; \
		echo "DATABASE_URL=postgresql://user:password@localhost:5432/dbname" > .env; \
		echo "HOST=0.0.0.0" >> .env; \
		echo "PORT=8000" >> .env; \
		echo "RELOAD=false" >> .env; \
		echo ".env file created. Please update with your actual values."; \
	else \
		echo ".env file already exists"; \
	fi

# Quick start for new developers
quickstart: setup-env install check-db
	@echo "Quick start complete!"
	@echo "Next steps:"
	@echo "1. Update .env file with your database credentials"
	@echo "2. Run 'make create-tables' to create database tables"
	@echo "3. Run 'make dev' to start the development server"
	@echo "4. Visit http://localhost:8000/docs for API documentation"

# CORS testing
test-cors:
	@echo "Testing CORS configuration..."
	@echo "1. Starting server in background..."
	@make dev &
	@sleep 3
	@echo "2. Testing CORS endpoint..."
	@curl -s http://localhost:8000/cors-test | python -m json.tool
	@echo "3. Testing CORS headers..."
	@curl -s -H "Origin: http://localhost:3000" -v http://localhost:8000/health 2>&1 | grep -E "(Access-Control|Origin)"
	@echo "4. Stopping server..."
	@pkill -f "python runserver.py"
	@echo "CORS test completed!"

test-external-cors:
	@echo "Testing CORS with external origin..."
	@echo "1. Starting server in background..."
	@make dev &
	@sleep 3
	@echo "2. Testing external origin CORS..."
	@curl -s -H "Origin: https://json-api-free.onrender.com" -v http://localhost:8000/health 2>&1 | grep -E "(Access-Control|Origin)"
	@echo "3. Stopping server..."
	@pkill -f "python runserver.py"
	@echo "External CORS test completed!"

test-external-cors-script:
	@echo "Testing CORS with external origin using Python script..."
	@echo "1. Starting server in background..."
	@make dev &
	@sleep 3
	@echo "2. Running external CORS test script..."
	@. .venv/bin/activate && python test-external-cors.py
	@echo "3. Stopping server..."
	@pkill -f "python runserver.py"
	@echo "External CORS script test completed!"

serve-cors-test:
	@echo "Serving CORS test HTML file..."
	@echo "Open http://localhost:8080/cors-test.html in your browser"
	@echo "Make sure your FastAPI server is running on port 8000"
	@python -m http.server 8080
