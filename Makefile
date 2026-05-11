.RECIPEPREFIX := >
.PHONY: setup test run-cli run-ui docker-build docker-run

setup:
>python3 -m venv .venv
>. .venv/bin/activate && pip install -r requirements.txt

test:
>pytest -q

run-cli:
>python3 src/phishing_detector.py samples/phishing_combined.txt

run-ui:
>python3 src/web_app.py

docker-build:
>docker build -t upwind-phishing-detector:1.0 .

docker-run:
>docker run --rm -p 5000:5000 upwind-phishing-detector:1.0
