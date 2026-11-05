import requests, json, sys, numpy
from .DeviceParameters import DEVICE_IP, PORT, ApiKey
from .SensorParameters import SensorParams

TCHANNELS = ['', 't50k', 't4k', 'tmagnet', '', 'tstill', 'tmixing', '', 'tfse']
SENSORNAME = ['', '', '', '', '', '', 'R10482340', '', '']
PCHANNELS = ["can", "p2", "p3", "p4", "tank", "p6"]

class DR:

    def __init__(self, ErrorRaise=False, timeout=2):
        #req=requests.get(f'https://{DEVICE_IP}:{PORT}/system?key={ApiKey}', timeout=timeout)
        self.DEVICE_IP=DEVICE_IP
        self.PORT=PORT
        self.ApiKey=ApiKey
        self.timeout=timeout

        try:
            req = requests.get(
                f'https://{self.DEVICE_IP}:{self.PORT}/system?key={self.ApiKey}',
                timeout=self.timeout,
                verify=__file__.rsplit('\\', 1)[0] + '\\certificate.pem'
            )
            if req.status_code==200:
                print(req.json()['data']['system_name'], req.json()['data']['system_version'])
        except Exception as E:
            if ErrorRaise:
                raise f"Initial HTTP request failed. {E}"
            print(f">>>>>> {E}")

    def Get(self, node):
        req=requests.get(f"https://{self.DEVICE_IP}:{self.PORT}/{node}?key={self.ApiKey}", timeout=self.timeout, verify=__file__.rsplit('\\', 1)[0] + '\\certificate.pem')
        return req

    def Post(self, node, data):
        req = requests.post(f"https://{self.DEVICE_IP}:{self.PORT}/{node}?key={self.ApiKey}", json=data, timeout=self.timeout, verify=__file__.rsplit('\\', 1)[0] + '\\certificate.pem')
        return req

    def Id(self):
        req=requests.get(f'https://{DEVICE_IP}:{PORT}/system?key={ApiKey}', timeout=self.timeout, verify=__file__.rsplit('\\', 1)[0] + '\\certificate.pem')
        return req.json()['data']['system_name'], req.json()['data']['system_version']

    def GetT(self, name):
        if name not in TCHANNELS:
            return "Invalid channel"
        
        req=self.Get(f"values/mapper/bf/temperatures/{name}")
        if req.status_code != 200:
            return f"Comm failed. Status Code {req.status_code}"
         
        out=float(req.json()['data'][f'mapper.bf.temperatures.{name}']['content']['latest_value']['value'])
        if out>0:
            return out
        try:
            out=numpy.polyval(SensorParams[SENSORNAME[TCHANNELS.index(name)]], numpy.log10(self.GetTR(name)))
            if out>0:
                return f"*{format(out, '.3e')}"
            out=self.GetT("t_still")
            if out>0:
                return out
        except:
            pass
        return numpy.nan
        
    def GetTCh(self, Chn):
        return self.GetT(TCHANNELS[Chn])

    def GetTRCh(self, Chn):
        req=self.Get(f"values/mapper/temperature_control/sensors/t{Chn}/resistance")
        if req.status_code != 200:
            return f"Comm failed. Status Code {req.status_code}"
         
        try:
            out=float(req.json()['data'][f'mapper.temperature_control.sensors.t{Chn}.resistance']['content']['latest_value']['value'])
            if out>0:
                return out
        except:
            return float('NaN')
        
    def GetTR(self, name):
        return self.GetTRCh(TCHANNELS.index(name))

    def GetPCh(self, Chn):
        if Chn not in range(1, 7):
            return "Invalid channel"
        
        req=self.Get(f"values/mapper/bf/pressures/p{Chn}")
        if req.status_code != 200:
            return f"Comm failed. Status Code {req.status_code}"
        
        try: 
            out=float(req.json()['data'][f'mapper.bf.pressures.p{Chn}']['content']['latest_value']['value'])
            if out>0:
                return out
        except:
            return float('NaN')
        

    def GetFlow(self):
        req=self.Get(f"values/mapper/bf/flow")
        if req.status_code != 200:
            return f"Comm failed. Status Code {req.status_code}"
        
        try:
            out=float(req.json()['data']['mapper.bf.flow']['content']['latest_value']['value'])
            if out>0:
                return out
        except:
            return float('NaN')

        
    def GetPulseTubeStatus(self):
        req=self.Get(f"values/mapper/bf/pulsetube")
        if req.status_code != 200:
            return f"Comm failed. Status Code {req.status_code}"

        return int(req.json()['data']['mapper.bf.pulsetube']['content']['latest_value']['value'])
    
    @property
    def T_4K(self):
        return self.GetT('t4k')
    
    @property
    def T_mxc(self):
        return self.GetT('tmixing')