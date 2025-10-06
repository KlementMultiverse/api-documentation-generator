.PHONY: install run demo test docker-build docker-run analyze clean

install:
	pip install -r requirements.txt

demo:
	python analyzer.py demo

analyze:
	@echo "Usage: make analyze FILE=path/to/logfile.log"
	@if [ -z "$(FILE)" ]; then \
		echo "Example: make analyze FILE=sample_logs/error.log"; \
		python analyzer.py demo; \
	else \
		python analyzer.py analyze $(FILE); \
	fi

test:
	pytest tests/ -v

docker-build:
	docker-compose build

docker-run:
	docker-compose up

docker-demo:
	docker build -t log-analyzer . && docker run --rm log-analyzer python analyzer.py demo

deploy-local:
	make docker-run

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
	find . -type f -name '*.pyc' -delete 2>/dev/null
	rm -rf reports/
