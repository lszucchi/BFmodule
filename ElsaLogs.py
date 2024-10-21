import pandas as pd
import numpy as np
from datetime import datetime
from time import sleep
from os.path import isfile, expanduser
from os import makedirs
import sys
from BFmodule import DR, TCHANNELS, PCHANNELS

def WriteLog(msg, path, mode='a', end='\n', output=True):
    makedirs(path.rsplit('/', 1)[0], exist_ok=True)
    with open(path, mode) as logfile:
        logfile.write(msg+end)
    if output:
        print(f'{msg}{end}', end='')

def InitLog(path):
    date=datetime.now().strftime('%y%m%d')
    tlog=f"{path}/TLog {date}.csv"
    plog=f"{path}/PLog {date}.csv"
    slog=f"{path}/SLog {date}.csv"
    if not isfile(tlog):
        WriteLog(f"Time,{','.join(TCHANNELS)}", tlog, 'w')
    if not isfile(plog):
        WriteLog(f"Time,{','.join(PCHANNELS)}", plog, 'w')
    return date, tlog, plog

def Logging(path, period):
    date=None
    tlog=None
    plog=None
    Elsa=DR()
    while(True):
        while datetime.now().time().second%period:
            sleep(0.5)
        if date!=datetime.now().strftime('%y%m%d') or not isfile(plog) or not isfile(tlog):
            date, tlog, plog=InitLog(path)
        time=datetime.now().strftime('%H:%M:%S')
        
        WriteLog(f"{time}", tlog, end='')
        for name in TCHANNELS:
            if name:
                temp=Elsa.GetT(name)
                try:
                    WriteLog(f",{format(temp, '07.3f') if temp > 0.1 else format(temp*1e3, '06.3f')+'e-3'}", tlog, end='')
                except:
                    WriteLog(f",{temp}", tlog, end='')
        WriteLog('', tlog)
        
        WriteLog(f"{time},{','.join([format(Elsa.GetPCh(k), '.3e') for k in range(1, 7)])},{format(Elsa.GetFlow(), '.2f')}", plog)
        sleep(1)
    return 1

        
Logging(expanduser('~/Documents/ElsaLogs'), 60)

    
