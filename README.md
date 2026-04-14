# fastapi-plane

A small FastAPI CRUD-style API for managing an in-memory list of planes, with optional Docker support and a GitHub Actions pipeline to provision Azure App Service infrastructure (Bicep) and deploy the app.

## Features

- **FastAPI** API with basic endpoints:
  - `GET /` health/home response
  - `GET /planes` list planes
  - `POST /planes` add a plane
  - `GET /planes/{plane_id}` get a plane by id
  - `PUT /planes/{plane_id}` update a plane
  - `DELETE /planes/{plane_id}` delete a plane
- **In-memory storage** (data resets on restart)
- **Production server** via **Gunicorn + Uvicorn worker**
- **Dockerfile** exposing port **3100**
- **Azure deployment**:
  - IaC using **Bicep** (`infra/main.bicep`)
  - CI/CD via **GitHub Actions** (`.github/workflows/azure-deploy.yml`)

---

## Requirements

- Python (workflow uses **3.12**)
- Pip
- (Optional) Docker
- (Optional) Azure CLI + an Azure subscription for deployment

---

## Local development

### 1) Install dependencies

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 2) Run the app

Run with Uvicorn (recommended for local dev):

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 3100
```

Then open:

- `http://localhost:3100/`
- `http://localhost:3100/docs` (Swagger UI)

---

## API usage

### Plane model

Example JSON body for `POST /planes`:

```json
{
  "id": 1,
  "model": "A320",
  "manufacturer": "Airbus",
  "first_flight": 1987,
  "published": true
}
```

### Example requests

Create a plane:

```bash
curl -X POST "http://localhost:3100/planes" \
  -H "Content-Type: application/json" \
  -d '{"id":1,"model":"A320","manufacturer":"Airbus","first_flight":1987,"published":true}'
```

List planes:

```bash
curl "http://localhost:3100/planes"
```

---

## Run with Docker

Build:

```bash
docker build -t fastapi-plane .
```

Run:

```bash
docker run --rm -p 3100:3100 fastapi-plane
```

Open:

- `http://localhost:3100/docs`

---

## Gunicorn configuration

The repo includes `gunicorn.conf.py` with settings intended to be friendly to smaller Azure App Service SKUs (caps worker count using `WEB_CONCURRENCY`).

The Dockerfile starts:

```bash
gunicorn --bind 0.0.0.0:3100 main:app --worker-class uvicorn.workers.UvicornWorker
```

Note: if your actual ASGI app module is `app.py` (it is in this repo), you may prefer `app:app` in your runtime command. The Azure Bicep template uses:

```text
gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn.conf.py app:app
```

---

## Azure (IaC + GitHub Actions) deployment

This repository includes an end-to-end workflow that:

1. Builds a deployable ZIP artifact
2. Deploys Azure infrastructure with Bicep into a target resource group
3. Deploys the ZIP artifact to Azure App Service

### Files

- Workflow: `.github/workflows/azure-deploy.yml`
- Bicep template: `infra/main.bicep`
- Optional local parameters: `infra/main.parameters.json`
- Notes: `Build-Deploy.md`

### Configure GitHub Secrets

Create these **repository secrets**:

- `AZURE_CREDENTIALS`  
  From:  
  `az ad sp create-for-rbac --name <name> --role contributor --scopes /subscriptions/<subscription-id>/resourceGroups/<resource-group> --sdk-auth`
- `AZURE_SUBSCRIPTION_ID`
- `AZURE_RESOURCE_GROUP`

### Configure GitHub Variables

Create these **repository variables**:

- `APP_SERVICE_NAME` (must be globally unique)
- `AZURE_REGION` (example: `eastus`)

### Trigger

The workflow runs on:

- Push to `main`
- Manual run via `workflow_dispatch`

---

## Project structure (high level)

- `app.py` — FastAPI app and routes
- `requirements.txt` — Python dependencies
- `Dockerfile` — container build (port 3100)
- `gunicorn.conf.py` — Gunicorn config
- `infra/` — Azure Bicep template and parameters
- `.github/workflows/` — GitHub Actions CI/CD workflow

---

## Notes / limitations

- This app uses an in-memory list (`planedb`), so it is **not persistent**.
- ID handling is simplistic (e.g., `GET /planes/{plane_id}` uses list indexing assumptions). For production you’d typically add a database and proper lookup/validation.

---

## License

Add your preferred license (MIT/Apache-2.0/etc.) in a `LICENSE` file.
