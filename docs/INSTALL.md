# Installation

This document describe how to set up Orchestration/Workflow Manager for OpenSDS project.

* In this document Workflow Manager used is [StackStorm](https://stackstorm.com/).
* A Docker instance of StackStorm will be created from the StackStorms [repository](https://github.com/StackStorm/st2-docker)
* A StackStorm Pack with OpenSDS specific workflows and actions will be mounted into it.
* A Docker instance of Orchestration Manager will be started.
* A limited set of Workflows/Actions are available in [Orchestration](https://github.com/opensds/orchestration/tree/master/contrib/st2/opensds) reposity for OpenSDS.
* An example usage of these Workflows is listed below.

#### Install OpenSDS

Installation steps for OpenSDS is listed in the WIKI page of [OpenSDS](https://github.com/opensds/opensds/wiki).
The recommended OpenSDS Local Cluster Installation may be followed for initial testing of Orchestration.


#### Install Orchestration 
* Clone [OpenSDS Orchestration](https://github.com/opensds/orchestration)  project and install the Orchestration manager
    ```sh
    $ git clone https://github.com/opensds/orchestration
    $ cd orchestration
    $ pip install -r requirements.txt
    $ python setup.py install
    ```
* Install StackStorm
	The stackstorm [docker installer](https://github.com/StackStorm/st2-docker) repo is cloned, build as below.
    ```sh
    $ git clone https://github.com/stackstorm/st2-docker
    $ cd st2-docker
    $ make env
    ```
* Start docker container using docker-compose, copy opensds pack and register opensds pack
    ```sh
    $ docker-compose up -d
    $ docker cp <orchestration project>/contrib/st2/opensds <st2 container id>:/opt/stackstorm/packs/
	$ docker-compose exec stackstorm /bin/bash
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
* Run [OpenSDS Orchestration](https://github.com/opensds/orchestration) the Orchestration manager. (StackStorm End-point and Password are required for Orchestration Manager)
    ```sh
    $ cd <OpenSDS Orchestration Directory>
    $ ./orchestration/connectionmanager/credcreator.py set "St2" "<ST2 Endpoint IP>" "st2admin" "<ST2 Password>"
    $ ./orchestration/server.py
    ```

#### Installer script
The file [install.sh](https://github.com/opensds/orchestration/install.sh) may be used for automated installation of StackStorm and Workflows.

```sh
$  ./install.sh
```
And, default paths for st2-docker or opensds pack may be modified as below, if needed.

```sh
$ ST2_DOCKER_PATH="/opt/opensds/orchestration" ST2_WORKFLOW_PATH="/opt/opensds/orchestration/contrib/st2" ./scripts/install.sh
```

* Known issue
  * Creation of virtual environment for opensds (command: st2 run packs.setup_virtualenv packs=opensds) fails with [Exception: Failed to install requirement "six>=1.9.0,<2.0": Collecting six<2.0,>=1.9.0]. This can be ignored for now.
  * After cleanup, mistral services may not be running. Restart postgres, and bring up stackstorm containers
    ```sh
    $docker-compose down && docker-compose up -d postgres && docker-compose up -d
    ```

#### Example usage
OpenSDS Orchestration Dashboard OR CURL may be used for testing

For the examples below OpenSDS is installed on VM and both StackStorm and Orchestration manager are running on Host. Please replace '<>' with respective values.

* Get token from StackStorm with username st2admin, and password as input arguments
    ```sh
    $ curl -X POST -k -u st2admin:'<password>' https://localhost/auth/v1/tokens
    ```
* Provision Volume Workflow using StackStorm with input arguments
    ```sh
    $ curl -k -X POST \
        https://localhost/api/v1/executions \
        -H  'content-type: application/json' \
        -H  'X-Auth-Token: <stackstorm token>' \
        -d '{"action": "opensds.provision-volume", "user": null, "parameters": {"i_paddr": "<ip>", "port": "50040", "size": 1, "tenant_id": "<id>", "name": "test000", "auth_token": "<opensds token>", "host_id": "<host_id>"}}'
    ```

* Create Volume using StackStorm Action with input arguments
    ```sh
    $ curl -k -X POST   \
    https://localhost/api/v1/executions   \
    -H  'content-type: application/json'   \
    -H  'X-Auth-Token: <stackstorm token>'   \
    -d '{"action": "opensds.create-volume", "user": nul, "parameters": {"ip_addr": "<ip>", "port": "50040", "size": 1, "tenant_id": "<id>", "name": "test001", "auth_token": "<opensds token>"}}'
    ```
