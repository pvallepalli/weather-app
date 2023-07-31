# Weather App
The Weather App is a web application built using Flask, which allows users to search weather information for the coming week.

## Features
- Search for weather information for a location
- View the weather forecast for the next 7 days.
- Save and display the last 5 recently searched locations.
- Unit tests for code quality and reliability.

## Running the app locally
To run the Weather App locally, follow these steps:

1. Clone the repository
   ```
   git clone https://github.com/your-username/weather-app.git
   cd weather-app
   ```
2. Install dependencies
   ```
   pip install -r requirements.txt 
   ```

3. Obtain API keys

   Obtain a Google Maps API key and set the environment variable GMAPS_API_KEY
   ```
   export GMAPS_API_KEY="<Google maps api key>"
   ```

4. Run the application
   ```
   python app.py
   ```

5. Usage
Open your web browser and navigate to http://127.0.0.1:5000/

   To search for weather information in a different location, enter the location name in the search box and click the "Search" button. The application will display the weather forecast for the next 7 days, including the maximum and minimum temperatures, UV index, sunrise and sunset times.
You can also view the last 5 recently searched locations at the bottom of the page.
Running Tests

6. To run the unit tests, use the following command:

   ```
   python -m unittest discover tests/
   ```

## Deploying the app to Azure
We will use Azure App Service for hosting the webapp and Azure DevOps Pipeline to automate the build, test, and deployment processes, ensuring a streamlined and efficient deployment workflow.
- Easy Deployment: Azure App Service allows us to deploy the Weather App with minimal configuration. We can deploy the app directly from our CI/CD pipeline, making the deployment process quick and efficient.
- Automatic Scaling: Azure App Service automatically scales the application based on demand, ensuring optimal performance even during traffic spikes.
- Built-in Monitoring: Azure App Service provides built-in monitoring, making it easier to troubleshoot and optimize the application.

## Setting Up the Azure DevOps Pipeline
We chose Azure DevOps Pipeline as our CI/CD tool to automate the build, test, and deployment processes. Here's how we set up the pipeline:

Version Control: The Weather App code can hosted in Azure Repo's in Azure DevOps, and Azure DevOps Pipeline is configured to use this repository as the source.

Build Stage: The build stage of the pipeline installs the required dependencies, and runs unit tests to ensure code quality.

Artifact Publishing: After a successful build, the pipeline publishes the built artifacts, making them available for the deployment stage.

Deploy Stage: The release stage of the pipeline is responsible for deploying the application to Azure App Service. We use the Azure Web App Deployment task to deploy the app from the published artifacts.

Environment Variables: The pipeline uses environment variable `GMAPS_API_KEY` to securely pass API key to the pipeline. 

Trigger Configuration: The pipeline is configured to automatically trigger on code pushes to the master branch, ensuring continuous integration and deployment.

## Deploying the Weather App
With the Azure DevOps Pipeline and Azure App Service in place, the deployment process of the Weather App becomes straightforward. When a new code changes are pushed, it will trigger the pipeline and run unit tests, package it and deploy it to dev environment. 
