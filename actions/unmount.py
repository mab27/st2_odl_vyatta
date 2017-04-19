import requests
import warnings
from jinja2 import Template
# Libary import used for Key-Value store manipulation
from st2client.models import KeyValuePair
from st2client.client import Client

from st2actions.runners.pythonrunner import Action

class unmount(Action):
    def run(self, controllerIP, controllerUser, controllerPW, mountName):
              
        # Preapring the request(s)
        ####################################################################### 
        headers = {
            "accept": "application/xml",
            "content-type": "application/xml",
        }
        
        url_base = "http://" + controllerIP + ":8181/restconf" + "/config" +"/network-topology:network-topology/topology/topology-netconf/node/"
        url = url_base + mountName
        print("\n")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("Sending REST call to ODL Controller (BSC):")
        print(" >>> Request:")
        print("     Method: PUT")
        print("     URI:    " + url)
        print("\n")

        # Sending the URL call(s) 
        #######################################################################        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cmd_response = requests.delete(url, auth=(controllerUser, controllerPW), headers=headers, verify=False)
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