#coding=utf-8
import os
import time
import paramiko
import datetime
import configparser
from monitor_model import system_disk_monitor, system_uptime

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
cf = configparser.ConfigParser()
cf.read(PATH('monitor.config'))
SERVER_PASS = cf.get('config', 'SERVER_PASS')

def get_system_condition():
    result = {}

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.199.208', 22, 'pi', SERVER_PASS)
    stdin, stdout, stder = ssh.exec_command('df')
    occupation_result_list = stdout.read().decode(encoding="utf-8",
                                                  errors="strict").split('\n')
    stdin, stdout, stder = ssh.exec_command('uptime')
    uptime_result_list = stdout.read().decode(encoding="utf-8",
                                              errors="strict").split('\n')
    ssh.close()
    result = {}

    result['occupation'] = {}
    var_occupation_list = occupation_result_list[1].strip().split(' ')
    temp_var_occupation_list = {}
    temp_var_occupation_list = temp_var_occupation_list.fromkeys(
        var_occupation_list)
    temp_var_occupation_list.pop('')
    var_occupation_list = list(temp_var_occupation_list.keys())
    result['occupation']['size'] = round(
        (float(var_occupation_list[1]) / 1000000), 2)
    result['occupation']['used'] = round(
        (float(var_occupation_list[2]) / 1000000), 2)

    result['uptime'] = {}
    try:
        result['uptime']['user'] = int(
            uptime_result_list[0].strip().split(' ')[7])
    except:
        result['uptime']['user'] = int(
            uptime_result_list[0].strip().split(' ')[6])
    result['uptime']['average'] = float(
        uptime_result_list[0].strip().split(' ')[-1])
    print(result)

    query1 = system_disk_monitor(
        size=result['occupation']['size'],
        used=result['occupation']['used'],
        update_time=datetime.datetime.now())

    query2 = system_uptime(average=result['uptime']['average'],
                           user=result['uptime']['user'],
                           update_time=datetime.datetime.now())
    query1.save()
    query2.save()
	
get_system_condition()