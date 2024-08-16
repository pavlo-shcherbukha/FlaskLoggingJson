# py-flask-rdbg Remote debug flask application on openshift

## About

This example shows  how to prepare deployment on openshift python flask application  deployment for local and remote debug using Visual Studio Code. 
## Folder assignment

- sh_app contains a simple python flask applicaiton
- openshift  contains deployments on openshift using RedHat UBI8-Python 3.9 image
- .vscode  contains file **launch.json** which contains configuration for debug: local and remote.


## Run on your laptop

1. clone git hub repo

```bash
  git clone https://github.com/pavlo-shcherbukha/py-flask-rdbg.git

```
2. prepare local environment

- create virtual environment

```bash
    py -m venv env

```
run     .\env\Scripts\activate.ps1 for checking 

- install dependency

```bash

  py -m pip install -r requirements.txt

```

3. run debug on your laptop

- Choose "run and debug" icon on the left side bar
- Choose in dropdown sh_app: Win Flask
- Start debugging using F5 or icon

4. running on openshift

4.1. Prepare openhsift environment

- run openshift sandbox as described here [create openshift sendbox](https://github.com/pavlo-shcherbukha/google-sheet-to-db#create-openshift-sendbox).  Personally I prefer this variant.

- install and run openshift crc platform [ A minimal OpenShift Container Platform 4 cluster and Podman container runtime to your local computer](https://crc.dev/crc/).

- use your corporate openshift if it possible.

4.2. Modify login.cmd  according to your openshift credentials

4.3. Create your github secret

- Modify  secret-github-basicauth.yaml  according to your githyb credentials

- create secret using 

```bash
 oc create -f secret-github-basicauth.yaml
```

4.4. Deploy  service 

The folders  openshift/ubi8_docker_deployment contain 2 cmd files:
- srvc-process.cmd  which creates the service;
- route-process.cmd which creates the route.  

Run this files

5. Prepare remote debug

5.1. Check environment variable on container

```yaml
            - name: APP_SCRIPT
              value: /opt/app-root/etc/xapp.sh
            - name: APP_DEBUG
              value: 'DEBUG_BRK'  
```

5.2. Port forward container debug port to the port on your laptop.

To forward container debug port to the port on your laptop you should run the  openshift command:

```bash
oc  port-forward py-ubi8docker-srvc-4-swgbk  5680:5678

```

5.3. Connect Visual Studit Code to debug

- Choose "run and debug" icon on the left side bar
- Choose in dropdown sh_app: Remote Attach
- Start debugging using F5 or icon


6 Run in normal mode, using Gunicorn

Delete or clear env variables

```yaml
            - name: APP_SCRIPT
              value: /opt/app-root/etc/xapp.sh
            - name: APP_DEBUG
              value: 'DEBUG_BRK'  
```

In this case your app will start using gunicorn parameters from this env variables

```yaml
            - name: GUNICORN_CMD_ARGS
              value: -k gevent --workers=1 --worker-connections=2000  --bind=0.0.0.0:8080 --access-logfile=-

```


7 Addition comment

This env variables are  using for different modes:

- FLASK_APP for remote debug mode
- APP_MODULE for running under gunicorn 

```yaml

            - name: FLASK_APP
              value: sh_app.webapp
            - name: APP_MODULE
              value: sh_app.webapp


```

