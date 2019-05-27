#!/bin/bash -e

# Input variables
export ST2_DOCKER_PATH=${ST2_DOCKER_PATH:-"/opt/opensds/orchestration"}
export ST2_WORKFLOW_PATH=${ST2_WORKFLOW_PATH:-"/opt/opensds/orchestration"}
export PACKS_PATH=${PACKS_PATH:-/opt/stackstorm/packs}

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
    cd $ST2_DOCKER_PATH/st2-docker
    docker-compose down
}

osds::st2::start() {
    cd $ST2_DOCKER_PATH/st2-docker
    docker-compose up -d
}

osds::st2::download() {
  (
    cd $ST2_DOCKER_PATH
    git clone https://github.com/stackstorm/st2-docker
    cd st2-docker
    make env
  )
}

osds::st2::install() {
    # validate before running
    if [ ! -d "$ST2_DOCKER_PATH/st2-docker" ]; then
        osds::st2::download
    fi

    # start st2 docker container
    cd $ST2_DOCKER_PATH/st2-docker
    docker-compose down
    osds::st2::start

    # install opensds workflows
    C_ID=`docker ps -a -q -f "name=st2-docker_stackstorm"`
    docker cp $ST2_WORKFLOW_PATH/opensds $C_ID:$PACKS_PATH/
    docker-compose exec stackstorm st2ctl reload --register-all
    docker-compose exec stackstorm st2 run packs.setup_virtualenv packs=opensds
}

osds::st2::cleanup() {
    cd $ST2_DOCKER_PATH/st2-docker
    docker-compose exec stackstorm st2 pack remove opensds
    docker-compose exec stackstorm rm -rf $PACKS_PATH/opensds
    docker-compose down
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
