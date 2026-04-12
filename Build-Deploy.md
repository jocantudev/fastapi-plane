Create a comprehensive GitHub Actions deployment pipeline for my application, including the following key stages.

## Build Stage
- Build the App using FastAPI
- Generate the artifact from the build that can be deployed.

## Infrastructure as a Code (IaC) Deployment
- Use Bicep templates to provision necessary Azure resources (e.g.  Azure App Service)
- Ensure the correct Azure Resource Group is targeted.

## Application Deployment
- After successfully deploying the infrastructure, deploy the built Application artifact to the Azure App Service..
- Specifythe the required Azure credentials and enviroment variables.
- Deploy the application to a specific region.

## Additional Notes
- Think step-by-step