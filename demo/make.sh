#!/bin/bash

set -e

function ExitWhenError()
{
	result=$?
	if [ $result != 0 ];then
		exit $result
	fi
}

function GenProto()
{
    if [ $# = 0 ];then
        cd tools
        python genprotoloadsrc.py
        cd -
        mkdir -p src/protocol/temp
        cd src/protocol/temp
        python ../make.py
        ExitWhenError
        cd -
    elif [ $# == 1 ];then
        if [ "clean" = "$1" ];then
            rm -rf src/protocol/temp/*
        fi
    fi
}

function MakeLib()
{
    MAKE_CMD="make -j4"
    if [ $# = 1 ];then
        cd src/$1
        $MAKE_CMD
        ExitWhenError
        cd -
    elif [ $# == 2 ];then
        if [ "clean" = "$2" ];then
            cd src/$1
            make clean
            cd -
        elif [ "release" = "$2" ];then
            cd src/$1
            $MAKE_CMD BUILD=release
            cd -
        fi
    fi
}

function MakeAppProject()
{
    MAKE_CMD="make -j4"
    if [ $# = 2 ];then
        $MAKE_CMD TARGETNAME=$1 INCCOMM=$2
        ExitWhenError
    elif [ $# == 3 ];then
        if [ "clean" = "$3" ];then
            make clean TARGETNAME=$1
        else
            $MAKE_CMD BUILD=$3 TARGETNAME=$1 INCCOMM=$2
            ExitWhenError
        fi

    fi
}

date
starttime=`date +'%Y-%m-%d %H:%M:%S'`
GenProto $@
MakeLib lib $@
MakeLib app/app_common_src $@
MakeAppProject gamesvr yes $@ # yes 需要逻辑层协议 no 不需要逻辑层协议
MakeAppProject gatesvr no $@
MakeAppProject zbusd no $@
MakeAppProject console no $@
endtime=`date +'%Y-%m-%d %H:%M:%S'`
start_seconds=$(date --date="$starttime" +%s);
end_seconds=$(date --date="$endtime" +%s);
echo "编译耗时： "$((end_seconds-start_seconds))"s"
date
echo finished!