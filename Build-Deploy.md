# GitHub Actions Build and Azure Deployment

This repository now includes a complete CI/CD pipeline that:

1. Builds and packages the FastAPI app into a deployable artifact.
2. Provisions Azure infrastructure using Bicep in a specific resource group.
3. Deploys the built artifact to Azure App Service.

## Files Added

- `.github/workflows/azure-deploy.yml`
- `infra/main.bicep`
- `infra/main.parameters.json` (optional local reference values)

## Step 1: Configure GitHub Secrets

Set these repository secrets:

- `AZURE_CREDENTIALS`:
	JSON output from `az ad sp create-for-rbac --name <name> --role contributor --scopes /subscriptions/<subscription-id>/resourceGroups/<resource-group> --sdk-auth`
- `AZURE_SUBSCRIPTION_ID`:
	Azure subscription ID
- `AZURE_RESOURCE_GROUP`:
	Target resource group name used by the IaC deployment stage

## Step 2: Configure GitHub Variables

Set these repository variables:

- `APP_SERVICE_NAME`: globally unique Azure Web App name
- `APP_SERVICE_PLAN_NAME`: App Service Plan name
- `AZURE_REGION`: deployment region (example: `eastus`)

## Step 3: Build Stage

Job: `build`

- Checks out source code
- Sets up Python 3.12
- Installs dependencies from `requirements.txt`
- Creates deployable zip artifact (`fastapi-app.zip`)
- Uploads artifact as `fastapi-package`

## Step 4: IaC Deployment Stage

Job: `deploy_infra` (depends on `build`)

- Logs into Azure using `AZURE_CREDENTIALS`
- Validates required secret/variable values
- Deploys `infra/main.bicep` with `azure/arm-deploy`
- Explicitly targets the resource group from `AZURE_RESOURCE_GROUP`
- Outputs the App Service name for downstream deployment

The Bicep template provisions:

- Linux App Service Plan
- Linux Web App configured for FastAPI/Gunicorn

## Step 5: Application Deployment Stage

Job: `deploy_app` (depends on `deploy_infra`)

- Downloads the build artifact
- Logs into Azure
- Deploys artifact to Azure App Service with `azure/webapps-deploy`

## Triggering the Pipeline

The workflow runs on:

- Pushes to `main`
- Manual trigger via `workflow_dispatch`

## Notes

- Keep the App Service app name globally unique.
- Confirm your service principal has Contributor access to the target resource group.
- If desired, you can customize SKU and runtime values in `infra/main.bicep`.