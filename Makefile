.PHONY: help install test clean venv activate

help:
	@echo "TWM - Terminal Window Management"
	@echo ""
	@echo "Available commands:"
	@echo "  make venv      - Create virtual environment"
	@echo "  make install   - Install TWM in development mode"
	@echo "  make test      - Run test suite"
	@echo "  make clean     - Remove build artifacts"
	@echo "  make activate  - Show activation command"
	@echo ""
	@echo "Quick start:"
	@echo "  make venv && source venv/bin/activate && make install"

venv:
	@echo "Creating virtual environment..."
	python3 -m venv venv
	@echo "Virtual environment created!"
	@echo "Activate with: source venv/bin/activate"

install:
	@echo "Installing TWM..."
	pip install -e .
	@echo "Installation complete!"
	@echo "Try: twm --help"

test:
	@echo "Running tests..."
	pip install pytest
	pytest tests/ -v

clean:
	@echo "Cleaning up..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf venv/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	@echo "Clean complete!"

activate:
	@echo "To activate the virtual environment, run:"
	@echo "  source venv/bin/activate"
