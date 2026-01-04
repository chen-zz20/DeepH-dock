.PHONY: build test clean

build: clean
	uv build --wheel -o dist .

test:
	pytest -v tests/

clean:
	rm -rf dist/ build/ *.egg-info

