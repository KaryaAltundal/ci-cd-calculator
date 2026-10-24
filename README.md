# CI/CD Calculator

A small FastAPI service used to practise a complete CI/CD pipeline: every push to `main` runs the tests, creates a version tag, builds a Docker image, pushes it to Docker Hub and triggers a Jenkins job.

The API itself is intentionally simple. The point of the project is the automation around it.

## API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check, returns `{"status": "healthy"}` |
| GET | `/sum?a=10&b=5` | Returns `{"result": 15}` |
| GET | `/subtract?a=10&b=5` | Returns `{"result": 5}` |

FastAPI also serves interactive documentation at `/docs`.

## Run locally

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

The service is then available at http://127.0.0.1:8000.

## Run the tests

```bash
python -m pytest
```

The tests use FastAPI's `TestClient` and cover all three endpoints (`tests/test_app.py`).

## Run with Docker

```bash
docker build -t calculator-api .
docker run -p 8000:8000 calculator-api
```

## CI/CD pipeline

The workflow in `.github/workflows/docker-build-push.yml` runs on every push to `main`:

1. **Check out** the code and install the dependencies.
2. **Run the tests** with pytest. The pipeline stops here if a test fails.
3. **Bump the version** and push a new Git tag (patch bump, for example `v1.0.3`) using `github-tag-action`.
4. **Log in to Docker Hub** and **build and push** the image with two tags: `latest` and the new version tag.
5. **Trigger a Jenkins job** through its remote build API and pass the image tag as a parameter (`IMAGE_TAG`), so Jenkins can deploy exactly that version.

Credentials are never stored in the repository. The workflow reads them from GitHub Actions secrets:

- `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`
- `JENKINS_URL`, `JENKINS_JOB_NAME`, `JENKINS_USER`, `JENKINS_TOKEN`

The Jenkins job itself is configured on the Jenkins server and is not part of this repository.

## Tech stack

Python 3.13, FastAPI, Uvicorn, pytest, httpx, Docker, GitHub Actions, Jenkins

## Project structure

```
app.py                                  FastAPI application
tests/test_app.py                       API tests
Dockerfile                              Container image
requirements.txt                        Python dependencies
.github/workflows/docker-build-push.yml CI/CD workflow
```
