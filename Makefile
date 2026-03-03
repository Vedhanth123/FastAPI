start:
	uv run fastapi dev app/main.py

test:
	uv run pytest

clean:
	rm -rf __pycache__ .pytest_cache