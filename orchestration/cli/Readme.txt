CLI for Orchestration


Steps to run CLI:

1. Deploy OpenSDS (https://github.com/opensds/opensds/wiki)
2. Deploy StackStorm with OpenSDS packs (https://github.com/opensds/orchestration/blob/master/docs/INSTALL.md)
3. Start Orchestrator (https://github.com/opensds/orchestration/blob/master/docs/INSTALL.md)
4. Update input parameters in util.py file (OPENSDS_IP, OPENSDS_TOKEN, ORCHESTRATOR_IP, etc.)

Example Usage:

$ python cli.py service list
$ python cli.py service add
$ python cli.py service get --id d8360a8a-6c5e-4533-a18a-b446db8caac8 

$ python cli.py instance get
$ python cli.py instance run --id 73207f47-5e99-4c24-8a73-2e7d6f92b107
