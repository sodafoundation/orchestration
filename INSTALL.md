# Installation

This document describe how to set up Orchestration/Workflow Manager for OpenSDS project.

* In this document Workflow Manager used is [StackStorm](https://stackstorm.com/).
* A Docker instance of StackStorm will be created from the StackStorms [repository](https://github.com/StackStorm/st2-docker)
* A StackStorm Pack with OpenSDS specific workflows and actions will be loaded into it.
* A limited set of Workflows/Actions are available in [Orchestration](https://github.com/opensds/orchestration/tree/master/contrib/st2/opensds) reposity for OpenSDS.
* An example usage of these Workflows is listed below.

#### Install OpenSDS

Installation steps for OpenSDS is listed in the WIKI page of [OpenSDS](https://github.com/opensds/opensds/wiki).
The recommended OpenSDS Local Cluster Installation may be followed for initial testing of Orchestration.


#### Install Orchestration 
* Install StackStorm
	The stackstorm [docker installer](https://github.com/StackStorm/st2-docker) repo is cloned, build as below.
    ```sh
    $ git clone https://github.com/stackstorm/st2-docker
    $ cd st2-docker
    $ make env
    ```
* Start docker container using docker-compose
    ```sh
    $ docker-compose up -d  # For starting container
    $ docker-compose down   # For stopping container
    ```
* Copy [opensds folder](https://github.com/opensds/orchestration/tree/master/contrib/st2/opensds) to packs folder of stackstorm docker instance.
	```sh
	$ docker-compose exec stackstorm /bin/bash
	# scp -r <host opensds path> /opt/stackstorm/packs/
	# st2ctl reload --register-all
	```
* Register virtual environment while installing opensds first time.
	```sh
	# st2 run packs.setup_virtualenv packs=opensds
	```
* Check status of StackStorm installation. It should list all services and PIDs as below.
	```sh
	# st2ctl status
    ##### st2 components status #####
    st2actionrunner PID: 96
    st2actionrunner PID: 102
    st2actionrunner PID: 110
    st2actionrunner PID: 115
    st2api PID: 58
    st2api PID: 268
    st2stream PID: 61
    st2stream PID: 261
    st2auth PID: 47
    st2auth PID: 249
    st2garbagecollector PID: 45
    st2notifier PID: 51
    st2resultstracker PID: 49
    st2rulesengine PID: 56
    st2sensorcontainer PID: 42
    st2chatops is not running.
    st2timersengine PID: 60
    st2workflowengine PID: 52
    st2scheduler PID: 54
    mistral-server PID: 340
    mistral.api PID: 335
	```

#### Installer script
The file script/st2_installer.sh may be used for automated installation of StackStorm and Workflows.
This script needs to be updated with input variables of,
* Source paths of StackStorm Installer and Workflow
* Host IP and user credentials

Example input variables:
```sh
# Input variables
export ST2_DOCKER_SRC_PATH="/opt/opensds/orchestration"
export ST2_WORKFLOW_SRC_PATH="/opt/opensds/orchestration/contrib/st2/opensds"
export HOST_USER=demo_user
export HOST_PASSWORD=demo_password
export PACKS_PATH=/opt/stackstorm/packs/
export HOST_IP=100.64.0.1
```

* Known issue
  * Creation of virtual environment for opensds (command: st2 run packs.setup_virtualenv packs=opensds) fails with [Exception: Failed to install requirement "six>=1.9.0,<2.0": Collecting six<2.0,>=1.9.0]. This can be ignored for now.
  * After cleanup, mistral services may not be running. Restart postgres, and bring up stackstorm containers [```docker-compose down && docker-compose up -d postgres && docker-compose up -d```]

#### Example usage	
OpenSDS Orchestration Dashboard OR CURL may be used for testing

For the examples below OpenSDS is installed on VM with IP: 100.64.41.214 and StackStorm docker image is running on Host IP: 100.64.40.36

* Provision Volume Workflow with input arguments
 ```sh
    $ curl -k -X POST \
        https://100.64.40.36/api/v1/executions \
        -H  'content-type: application/json' \
        -H  'X-Auth-Token: c2f427ce9b3d43889ec61eb623160c5d' \
        -d '{"action": "opensds.provision-volume", "user": null, "parameters": {"ipaddr": "100.64.41.214", "port": "50040", "size": 1, "projectid": "7e515a1edee94f9688efda14b6fb677e", "name": "test200", "token": "gAAAAABcy_WakGraN1iQy8R87ueVwdNYDJP2n9a2J_o7bnptqwFjJLxKMzvJoPVt4ofi74V7kLBCMJzZQ41kcwhWQEOv3v8ne9Z2FrhOOiYPY358Y1-F3gdRTY8oOKlyiqgcAJ9wT5sF5RzqAKwAyinRd3KEkGjsFsjxfFkJSlpRFdJmW_XQ8hwjch539Nwo3RgLaCXX1W0z", "hostinfo": {"host":"ubuntu","initiator":"iqn.1993-08.org.debian:01:437bac3717c8","ip":"100.64.40.36"}}}'  
 ```

* Create Volume Action with input arguments
```sh
    $ curl -k -X POST   \
    https://100.64.40.36/api/v1/executions   \
    -H  'content-type: application/json'   \
    -H  'X-Auth-Token: c2f427ce9b3d43889ec61eb623160c5d'   \
    -d '{"action": "opensds.create-volume", "user": nul, "parameters": {"ipaddr": "100.64.41.214", "port": "50040", "size": 1, "projectid": "7e515a1edee94f9688efda14b6fb677e", "name": "test101", "token": "gAAAAABcy_WakGraN1iQy8R87ueVwdNYDJP2n9a2J_o7bnptqwFjJLxKMzvJoPVt4ofi74V7kLBCMJzZQ41kcwhWQEOv3v8ne9Z2FrhOOiYPY358Y1-F3gdRTY8oOKlyiqgcAJ9wT5sF5RzqAKwAyinRd3KEkGjsFsjxfFkJSlpRFdJmW_XQ8hwjch539Nwo3RgLaCXX1W0z"}}'
```
