@description('Azure region for all resources.')
param location string = resourceGroup().location

@description('Globally unique App Service name.')
param appServiceName string

@description('App Service plan name.')
param appServicePlanName string = '${appServiceName}-plan'

@description('Pricing tier for App Service plan.')
param skuName string = 'B1'

resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: skuName
    tier: 'Basic'
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

resource webApp 'Microsoft.Web/sites@2023-12-01' = {
  name: appServiceName
  location: location
  kind: 'app,linux'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.12'
      appCommandLine: 'gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn.conf.py app:app'
      ftpsState: 'Disabled'
      alwaysOn: true
      appSettings: [
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
        {
          name: 'WEBSITES_PORT'
          value: '3100'
        }
        {
          name: 'WEB_CONCURRENCY'
          value: '2'
        }
      ]
    }
  }
}

output appServiceName string = webApp.name
output appServicePlanId string = appServicePlan.id
