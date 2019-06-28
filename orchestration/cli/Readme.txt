CLI for Orchestration


Steps to run CLI:

1. Deploy OpenSDS (https://github.com/opensds/opensds/wiki)
2. Deploy StackStorm with OpenSDS packs (https://github.com/opensds/orchestration/blob/master/docs/INSTALL.md)
3. Start Orchestrator (https://github.com/opensds/orchestration/blob/master/docs/INSTALL.md)
4. Update input parameters in util.py file (OPENSDS_IP, ORCHESTRATOR_IP, etc.)


Usage Help:

usage: orchctl [-h] [-a ADDRESS] [-u USER] [-p PASSWORD] [-t PROJECT_ID]
               [--orch_ip ORCH_IP] [--orch_port ORCH_PORT]
               {service,instance,workflow,task,info} ...

    CLI for OpenSDS Orchestration Manager

    Example:
    ./orchctl --help
    ./orchctl info
    ./orchctl service list
    ./orchctl service add --data '{"name":"volume provision","description":"Volume Service","tenant_id":"94b280022d0c4401bcf3b0ea85870519","user_id":"558057c4256545bd8a307c37464003c9","input":"","constraint":"","group":"provisioning","workflows":[{"definition_source":"opensds.provision-volume","wfe_type":"st2"},{"definition_source":"opensds.snapshot-volume","wfe_type":"st2"}]}'
    ./orchctl service get --id d8360a8a-6c5e-4533-a18a-b446db8caac8
    ./orchctl instance list
    ./orchctl instance get --id 2723347b-9af8-451a-a7f8-62d40b10ad6f
    ./orchctl instance delete --id 2723347b-9af8-451a-a7f8-62d40b10ad6f
    ./orchctl instance run --data '{"service_id":"08e8a8a3-7a78-43d3-9ab1-45fe7a60d4eb","action":"opensds.provision-volume","name":"Volume Provision name","description":"Volume Provision description","user_id":"558057c4256545bd8a307c37464003c9","parameters":{"ip_addr":"127.0.0.1","port":"50040","tenant_id":"94b280022d0c4401bcf3b0ea85870519","size":1,"name":"test"}}'

positional arguments:
  {service,instance,workflow,task,info}
    service             Registers/Shows services in Orchestrator
    instance            Executes/Shows/Deletes workflow instances
    workflow            Shows workflow definitions in Orchestrator
    task                Status of the task in Orchestrator
    info                Shows configs, tenant_id, user_id, token of Orchestrator

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        ip address of opensds hotpot
  -u USER, --user USER  username for opensds hotpot
  -p PASSWORD, --password PASSWORD
                        password for opensds hotpot
  -t PROJECT_ID, --project_id PROJECT_ID
                        project_id for opensds hotpot
  --orch_ip ORCH_IP     Orchestration server ip address
  --orch_port ORCH_PORT
                        Orchestration server port
