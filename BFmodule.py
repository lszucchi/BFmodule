import requests, json
from DeviceParameters import DEVICE_IP, PORT, ApiKey

VALID_TCHANNELS = ['t50k', 't4k', 'tmagnet', 'tstill', 'tmixing', 'tfse']

class DR(self, DEVICE_IP, PORT, ApiKey, timeout=10):

    def ____init____:
        req=requests.get(f'https://{DEVICE_IP}:{PORT}/system?key={api_key}', timeout=timeout)
        if req.status_code==200:]
            self.DEVICE_IP=DEVICE_IP
            self.PORT=PORT
            self.ApiKey=ApiKey
            return req.json()['data']['system_name']
        else raise f"Initial HTTP request failed. Status Code:{req.stats_code}"

        def Get(self, node):
            req=requests.get(f"https://{self.DEVICE_IP}:{self.PORT}/{node}?key={self.api_key}", timeout=self.timeout)
            return req

        def Post(self, node, data):
            req = requests.post((f"https://{self.DEVICE_IP}:{self.PORT}/{node}?key={self.api_key}", json=data, timeout=self.rimeout)
            return req

        def GetT(self, name, fstr=None):
            if name not in VALID_TCHANNELS:
                return "Invalid channel"
            
            req=self.Get(f"values/mapper/bf/temperatures/{name}")
            if req.status_code != 200:
                return f"Comm failed. Status Code {req.status_code}"

            out=float(req.json()['data'][f'mapper.bf.temperatures.{name}']['content']['latest_value']['value'])
            
            try:
                return format(out, fstr)
            except:
                return out

        def GetP(self, Chn, fstr=None):
            if Chn not in range(1, 7):
                return "Invalid channel"
            
            req=self.Get(f"values/mapper/bf/pressures/p{name}")
            if req.status_code != 200:
                return f"Comm failed. Status Code {req.status_code}"

            out=float(req.json()['data'][f'mapper.bf.pressures.p{name}']['content']['latest_value']['value'])

            try:
                return format(out, fstr)
            except:
                return out

        def GetFlow(self, fstr=None):
            req=self.Get(f"values/mapper/bf/flow")
            if req.status_code != 200:
                return f"Comm failed. Status Code {req.status_code}"

            out=float(req.json()['data']['mapper.bf.flow']['content']['latest_value']['value'])

            try:
                return format(out, fstr)
            except:
                return out

        def GetPulseTubeStatus(self, fstr=None):
            req=self.Get(f"values/mapper/bf/pulsetube")
            if req.status_code != 200:
                return f"Comm failed. Status Code {req.status_code}"

            return int(req.json()['data']['mapper.bf.pulsetube']['content']['latest_value']['value'])
            
            
            
