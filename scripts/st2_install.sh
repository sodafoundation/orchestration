#!/bin/bash -e

# Input variables
export ST2_DOCKER_SRC_PATH="/opt/opensds/orchestration"
export ST2_WORKFLOW_SRC_PATH="/opt/opensds/orchestration/contrib/st2/opensds"
export HOST_USER=demo_user
export HOST_PASSWORD=demo_password
export PACKS_PATH=/opt/stackstorm/packs/
export HOST_IP=100.64.40.36


osds::st2::show_help() {
    cat  << ST2_INSTALL_SCRIPT_HELP
Usage:
    $(basename $0) [-h|--help]
Flags:
    -h, --help     Print this information.s
    -u, --up       Start StackStorm Docker daemon.
    -d, --down     Ends StackStorm Docker daemon.
    -i, --install  Download and install StackStorm and opensds packs.
    -r, --remove   Remove opensds packs.

ST2_INSTALL_SCRIPT_HELP
}

osds::st2::stop() {
    cd $ST2_DOCKER_SRC_PATH/st2-docker
    docker-compose down
}

osds::st2::start() {
    cd $ST2_DOCKER_SRC_PATH/st2-docker
    docker-compose down
    docker-compose up -d
}

osds::st2::download() {
  (
    cd $ST2_DOCKER_SRC_PATH
    git clone https://github.com/stackstorm/st2-docker
    cd st2-docker
    make env
  )
}

osds::st2::install() {
    set -x xtrace

    # validate before running
    if [ ! -d "$ST2_DOCKER_SRC_PATH/st2-docker" ]; then
        osds::st2::download
    fi

    # start st2 docker container
    osds::st2::start

    # install opensds workflows
    cd $ST2_DOCKER_SRC_PATH/st2-docker

    docker-compose exec stackstorm sshpass -p $HOST_PASSWORD \
        scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -r \
        $HOST_USER@$HOST_IP:$ST2_WORKFLOW_SRC_PATH $PACKS_PATH
    docker-compose exec stackstorm st2ctl reload --register-all
    docker-compose exec stackstorm st2 action list -p opensds
    docker-compose exec stackstorm st2 run packs.setup_virtualenv packs=opensds
    docker-compose exec stackstorm st2ctl status
}

osds::st2::cleanup() {
    cd $ST2_DOCKER_SRC_PATH/st2-docker
    osds::st2::start
    docker-compose exec stackstorm st2 pack remove opensds
    docker-compose exec stackstorm rm -rf $PACKS_PATH/opensds
}

osds::st2::uninstall(){
    : # do nothing
}

osds::st2::uninstall_purge(){
    : # do nothing
}

if [ $# -eq 0 ]
  then
    osds::st2::show_help
    exit
fi

case $1 in
    -h|-\?|--help)
        osds::st2::show_help
        ;;
    -i|--install)
        osds::st2::install
        ;;
    -u|--up)
        osds::st2::start
        ;;
    -d|--down)
        osds::st2::stop
        ;;
    -r|--remove)
        osds::st2::cleanup
        ;;
    -|--)
        printf 'WARN: Missing option after: %s\n' "$1" >&2
        osds::st2::show_help
        ;;
    -?*)
        printf 'WARN: Unknown option (ignored): %s\n' "$1" >&2
        osds::st2::show_help
        ;;
esac
