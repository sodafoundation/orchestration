#!/bin/bash -e


PROJ_DIR=${PROJ_DIR:-`pwd`}

if [ ! -d $PROJ_DIR/contrib/st2/opensds ]
then
    echo "ERROR: Invoke install script from project directory OR"
    echo "Set environment variable PROJ_DIR to project directory"
    exit
fi

# Input arguments
export ST2_DOCKER_PATH=${ST2_DOCKER_PATH:-$PROJ_DIR/contrib/st2}
export ST2_WORKFLOW_PATH=${ST2_WORKFLOW_PATH:-/opt/opensds/orchestration}

if [ ! -d $ST2_DOCKER_PATH ]
then
    echo "ERROR: Invalid path for StackStorm Docker"
    exit
fi

mkdir -p $ST2_WORKFLOW_PATH

if [ ! -d $ST2_WORKFLOW_PATH ]
then
    echo "ERROR: Failed to create opensds workflow directory : $ST2_WORKFLOW_PATH"
    exit
fi

# Copy opensds workflow to folder that will be mounted as named volume
cp -r $PROJ_DIR/contrib/st2/opensds $ST2_WORKFLOW_PATH

# Install StackStorm
$PROJ_DIR/scripts/st2_install.sh -i

# TODO: Install orchestration manager for OpenSDS
