import requests
import warnings
import json
# Libary import used for Key-Value store manipulation
from st2client.client import Client
from st2client.models import KeyValuePair

from st2actions.runners.pythonrunner import Action

class shIpRoute(Action):
    def run(self, controllerIP, controllerUser, controllerPW, deviceName):
        
        # Preapring the request(s)
        ####################################################################### 
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }
        
        url_base = "http://" + controllerIP + ":8181/restconf" + "/operational" +"/network-topology:network-topology/topology/topology-netconf/node/"
        url = url_base + deviceName + "/yang-ext:mount/vyatta-protocols-v1:protocols/"
        print("\n")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("Sending REST call to ODL Controller (BSC):")
        print(" >>> Request:")
        print("     Method: GET")
        print("     URI:    " + url)
        print("\n")

        # Sending the URL call(s) 
        #######################################################################         
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cmd_response = requests.get(url, auth=(controllerUser, controllerPW), headers=headers, verify=False)
            cmd_response_code = str(cmd_response.status_code)
            print(" >>> Response:")
            print("     Response code: " + cmd_response_code)
            cmd_response_code = int(cmd_response.status_code)
            if cmd_response_code != 200:
                return (False, cmd_response_code)
            else:
                try:
                    data = json.loads(cmd_response.text)
                    print("     Response body: ")
                    print json.dumps(data, sort_keys=True, indent=4)
                except:
                    print ("     Response body: empty")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
