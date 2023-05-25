import json
import requests

from abc import ABC, abstractproperty
from enum import Enum

class RequestType(Enum):
    GET  = 1
    POST = 2

class PepwaveException(Exception):
    def __init__(self, message):
        super().__init__(message)

class PepwaveRequest(ABC):
    @abstractproperty
    def data(self) -> dict:
        pass

    @abstractproperty
    def endpoint(self):
        pass

    @abstractproperty
    def requestType(self):
        pass
    

class LoginRequest(PepwaveRequest):
    def __init__(self, username: str = "admin", password: str = "password"):
        self._endpoint = "/api/login"
        self._reqType  = RequestType.POST
        self.username  = username
        self.password  = password

    @property
    def data(self) -> dict:
        return {
            'username': self.username,
            'password': self.password,
        }

    @property
    def endpoint(self) -> str:
        return self._endpoint
    
    @property
    def requestType(self):
        return self._reqType

class LogoutRequest(PepwaveRequest):
    def __init__(self):
        self._endpoint = "/api/logout"
        self._reqType  = RequestType.POST

    @property
    def data(self) -> dict:
        return {}
    
    @property
    def endpoint(self) -> str:
        return self._endpoint
    
    @property
    def requestType(self):
        return self._reqType

class StatusWanConnection(PepwaveRequest):
    def __init__(self):
        self._endpoint = "/api/status.wan.connection"
        self._reqType  = RequestType.GET

    @property
    def data(self) -> dict:
        return {}
    
    @property
    def endpoint(self) -> str:
        return self._endpoint
    
    @property
    def requestType(self):
        return self._reqType

class Pepwave:
    def __init__(self, ipaddress):
        self.host      = f'http://{ipaddress}'
        self.session   = requests.Session()
        self.connected = False
        self.headers   = {'Accept': 'application/json'}

    def doRequest(self, pr: PepwaveRequest):
        url = f'{self.host}{pr.endpoint}'
        resp = None

        if not isinstance(pr, LoginRequest) and self.connected == False:
            raise PepwaveException("Not authenticated, login first")

        match pr.requestType:
            case RequestType.GET:
                resp = self.session.get(url, headers=self.headers)
                
            case RequestType.POST:
                resp = self.session.post(url, headers=self.headers, data=pr.data)
        
        if resp == None or resp.status_code != 200 or resp.json()['stat'] != 'ok':
            # TODO: Handle error
            raise PepwaveException("Error performing request")
        
        if isinstance(pr, LoginRequest):
            self.connected = True

        if isinstance(pr, LogoutRequest):
            self.connected = False

        return json.dumps(resp.json())

