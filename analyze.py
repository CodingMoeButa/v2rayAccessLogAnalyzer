#!/usr/bin/python3
#coding=utf-8
import sys
import time
import requests
import json
import csv

APPCODE = ''

path_log = sys.argv[1]
path_csv = sys.argv[2]
headers = {"Authorization":"APPCODE "+APPCODE}
sessions = []

fin = open(path_log, 'r')
lines = fin.readlines()
fin.close()
count = 0
for line in lines:
    count += 1
    print(count, end=' ')
    timestamp_current = time.mktime(time.strptime(line.split(' ')[0] + ' ' + line.split(' ')[1], '%Y/%m/%d %H:%M:%S'))
    ip_addr = line.split(' ')[2].removeprefix('tcp:').removeprefix('udp:').removesuffix(':0').removeprefix('[').removesuffix(']')
    for session in sessions[::-1]:
        if session['ip_addr']==ip_addr and timestamp_current-session['timestamp_end']<=30*60:
            sessions[sessions.index(session)]['timestamp_end'] = timestamp_current
            break
    else:
        sessions.append({
            'id':len(sessions),
            'timestamp_begin':timestamp_current,
            'timestamp_end':timestamp_current,
            'ip_addr':ip_addr
        })
print()

for i in range(len(sessions)):
    timestamp_begin = sessions[i]['timestamp_begin']
    timestamp_end = sessions[i]['timestamp_end']
    ip_addr = sessions[i]['ip_addr']
    time_begin = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(timestamp_begin))
    time_end = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(timestamp_end))
    sessions[i]['time_begin'] = time_begin
    sessions[i]['time_end'] = time_end
    try:
        response = requests.get('http://ipquery.market.alicloudapi.com/query?ip='+ip_addr, headers=headers)
        text = response.content.decode('unicode-escape')
        json_obj = json.loads(text, strict=False)
        status = json_obj['ret']
        if status==200:
            country = json_obj['data']['country']
            region = json_obj['data']['prov']
            city = json_obj['data']['city']
            district = json_obj['data']['area']
            isp = json_obj['data']['isp']
        else:
            country = region = city = district = isp = ''
    except Exception as e:
        print(e)
        country = region = city = district = isp = ''
    sessions[i]['country'] = country
    sessions[i]['region'] = region
    sessions[i]['city'] = city
    sessions[i]['district'] = district
    sessions[i]['isp'] = isp
    print(i, time_begin, time_end, ip_addr, country, region, city, district, isp)

fout = open(path_csv, 'w', newline='')
writer = csv.writer(fout)
for session in sessions:
    row = [
        session['id'],
        session['time_begin'],
        session['time_end'],
        session['ip_addr'],
        session['country'],
        session['region'], 
        session['city'],
        session['district'],
        session['isp']
    ]
    writer.writerow(row)
fout.close()