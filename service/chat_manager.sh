#!/bin/bash

BASE_PATH=$(cd `dirname $0`; pwd)
app_path=${BASE_PATH}"/chat_server.py"
log_dir=${BASE_PATH}"/../logs"
temp_dir=${BASE_PATH}"/../temp"
if [ ! -e $log_dir ]
then
  mkdir $log_dir
  echo "create logs dir $log_dir"
fi
if [ ! -e $temp_dir ]
then
  mkdir $temp_dir
  echo "create temp dir $temp_dir"
fi

date=$(date "+%Y-%m-%d  %H:%M:%S")
today=$(date "+%Y-%m-%d")
log_file=$log_dir/app_$today.log
ID=`ps -ef | grep chat_server | grep python | awk '{print $2}'`
input=$1
if [ ! -n "$input" ]
 then
  echo -e "\033[43;35m please append start|stop|restart|check \033[0m \n"
else
 case $input in
 start)
  if [ -z "$ID" ]
  then
   nohup /root/anaconda3/envs/chatllm/bin/python $app_path &>> $log_file &
   echo "start app successful"
   echo "$date start app successful" >> $log_file
  else
   echo "app already started"
  fi
 ;;
 stop)
  if [ -z "$ID" ]
   then
   echo "$date NO MATCH APP STARTED" >> $log_file
   echo "NO MATCH APP STARTED"
  else
   kill -9 $ID & >> $log_file
   echo "$date stop app successful" >> $log_file
   echo "stop app successful"
  fi
 ;;
 restart)
  if [ -z "$ID" ]

 then
   nohup /root/anaconda3/envs/chatllm/bin/python $app_path &>> $log_file &
   echo "restart app successful"
   echo "$date restart app successful" >> $log_file
  else
   kill -9 $ID & >> $log_file
   nohup /root/anaconda3/envs/chatllm/bin/python $app_path &>> $log_file &
   echo "stop old app and restart restart new app successful"
   echo "$date stop old app and restart new app successful" >> $log_file
  fi
 ;;
 check)
  if [ -z "$ID" ]
  then
   echo "APP is stopped"
  else
   echo "APP is running and process ID is $ID"
  fi
 ;;
 *)
  echo -e "\033[43;35m please append start|stop|restart|check \033[0m \n"
 esac
 find $log_dir -name "app_*.log" -type f -mtime +7 -delete
fi