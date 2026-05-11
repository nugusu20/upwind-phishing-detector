.RECIPEPREFIX := >
.PHONY: setup test run-cli run-ui docker-build docker-run assignment2-build assignment2-run assignment2-ui

setup:
>python3 -m venv .venv
>.venv/bin/pip install -r requirements.txt

test:
>.venv/bin/pytest -q

run-cli:
>.venv/bin/python src/phishing_detector.py samples/phishing_combined.txt

run-ui:
>.venv/bin/python src/web_app.py

docker-build:
>docker build -t upwind-phishing-detector:1.0 .

docker-run:
>docker run --rm -p 5000:5000 upwind-phishing-detector:1.0

assignment2-build:
>docker build -t upwind-malware-sandbox:1.0 assignment2_sandbox

assignment2-run:
>docker run --rm --network none -v "$$PWD/assignment2_sandbox/logs:/logs" -v "$$PWD/assignment2_sandbox/reports:/reports" upwind-malware-sandbox:1.0

assignment2-ui:
>.venv/bin/python assignment2_sandbox/sandbox_ui.py
