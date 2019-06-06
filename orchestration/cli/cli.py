import argparse
from service import add_services, list_services, get_services
from instance import get_instances, run_instance
from task import get_task, get_workflows
from utils import get_info

def service_api(args=''):
    switcher = {
        "add": add_services,
        "list": list_services,
        "get": get_services,
    }
    # Get the function from switcher dictionary
    func = switcher.get(args.operation, lambda: "Invalid operation")
    # Execute the function
    if args.operation == 'get':
        if args.id == None:
            print("ERROR: Needs --id set for service get")
            return
        func(args.id)
        return
    ret = func()
    if ret != None:
        print(ret)
    func()


def instance_api(args):
    switcher = {
        "run": run_instance,
        "get": get_instances,
    }
    # Get the function from switcher dictionary
    func = switcher.get(args.operation, lambda: "Invalid operation")
    # Execute the function
    ret = func()
    if ret != None:
        print(ret)
    func()


def workflow_api(args):
    switcher = {
        "get": get_workflows,
    }
    # Get the function from switcher dictionary
    func = switcher.get(args.operation, lambda: "Invalid operation")
    # Execute the function
    ret = func()
    if ret != None:
        print(ret)
    func()


def task_api(args):
    switcher = {
        "get": get_task
    }
    # Get the function from switcher dictionary
    func = switcher.get(args.operation, lambda: "Invalid operation")
    # Execute the function
    ret = func()
    if ret != None:
        print(ret)
    func()


def cli():
    parser = argparse.ArgumentParser(description="CLI for OpenSDS Orchestration Manager")
    parser.add_argument('-i', '--info', help="Prints information about orchestrator")

    subparsers = parser.add_subparsers(help='subcommands: [serivce, instance, workflow, or task]')

    parser_service = subparsers.add_parser('service', help='service takes operation: [get, list add]')
    parser_service.add_argument('operation', help='operation takes operation: [get, list add]')
    parser_service.add_argument('--id', help='ID help')
    parser_service.set_defaults(func=service_api)

    parser_instance = subparsers.add_parser('instance', help='instance takes operation: [get, run]')
    parser_instance.add_argument('operation', help='operation takes operation: [get, run]')
    parser_instance.set_defaults(func=instance_api)

    parser_workflow = subparsers.add_parser('workflow', help='workflow takes operation: [get]')
    parser_workflow.add_argument('operation', help='operation takes operation: [get]')
    parser_workflow.set_defaults(func=workflow_api)

    parser_task = subparsers.add_parser('task', help='task takes operation: [get]')
    parser_task.add_argument('operation', help='operation takes operation: [get]')
    parser_task.add_argument('--id', help='Execution ID help')
    parser_task.set_defaults(func=task_api)

    args = parser.parse_args()
    # if args.info == true:
    #     get_info()
    
    args.func(args)


if __name__ == '__main__':
    cli()