# Google App Engine C2 HTTP Forwarder

This Google App Engine application can be used to forward traffic fronted from the Google App Engine domain to a C2 server running on a GCP compute instance VM.

This is a POC application only and has a few potential indicators that could be use to identify 

# Basic configuration

Setup a project in GCP with a VPC (the `default` one is fine) and at least one compute instance running a C2 server with a HTTP listener. In more complex setups you can use a multi host setup with a HTTP proxy (Apache, Nginx, etc) that filters and then forwards HTTP traffic to the C2s HTTP listener on another host to provide some seperation and protection for the C2 server. Take note of the IP address of the C2 server (or proxy server in a multi host setup), as we will need to set this in the app configuration before we deploy it.

I created a single instance which was running in the same region as the App Engine app I was intending to create.

Setup a Serverless VPC connector in your VPC with an unused IP address range in the same region as your App Engine App and VM instance. This is done in the console [here](https://console.cloud.google.com/networking/connectors/list). This is required to allow traffic from the App Engine App to the private IP address of your C2 instance - so you dont need to directly expose the HTTP interface of the C2/proxy to the Internet. Take note of the name of the connector as we need it when we configure the app before deployment.


Setup a firewall rule for the VPC which allows traffic from the VPC connectors private IP address range to the HTTP endpoint listeners port on the destination C2 host (or proxy in the multi host configuration).


Follow the [instructions](https://cloud.google.com/appengine/docs/standard/python3/building-app/creating-gcp-project) to create a Python GCP project. I created a `Standard` app in the `us-central` region. 

As referenced in the instructions, you will also need to [install and configure](https://cloud.google.com/sdk/docs/install) the GCloud CLI if you have not done so already. 

Before I did my first deploy, I had to specifically set the target project by ID in the CLI. You can get the project ID from a few places, I used the [welcome page](https://console.cloud.google.com/welcome/new). You will also need the project ID for app configuration.

```
gcloud config set project <project-id>
```


Now you need to configure a few settings in `app.yml` before deploying the app.

First, set the private IP address of the GCP C2 compute instance target VM in the following location. Add a port designation to the address as well (e.g. `10.11.1.1:8080`) if the listener is not running on port 80.

```
env_variables:
  DESTINATION: "<C2_INTERNAL_IP>"
```

Now we need to configure the app to use the Serverless VPC connector we created. Modify the following line, replacing the `<PROJECT_ID>`, `<REGION>` and `<CONNECTOR_NAME>` placeholders with the appropriate values.

```
vpc_access_connector:
  name: projects/<PROJECT_ID>/locations/<REGION>/connectors/<CONNECTOR_NAME>
  egress_setting: private-ranges-only
```

Finally, with those updates complete, run the following using this repositories root directory as the PWD.

```
gcloud app deploy
```

All being well, you should be able to then see the status of the deployed application at the [App Engine Dashboard](https://console.cloud.google.com/appengine).

The C2 HTTP endpoint should then be accessible at a URL similar to `https://<project-id>.<region-id>.r.appspot.com/` (the specific URL will be in the output of the previous command and in the App Engine Dashboard)
