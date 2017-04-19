import requests
import warnings
from jinja2 import Template
# Libary import used for Key-Value store manipulation
from st2client.client import Client
from st2client.models import KeyValuePair

from st2actions.runners.pythonrunner import Action

class copyCfg(Action):
    def run(self, controllerIP, controllerUser, controllerPW, deviceName, source, target):
        
        # Preapring the request(s)
        ####################################################################### 
        headers = {
            "accept": "application/xml",
            "content-type": "application/xml",
        }
        
        url_base = "http://" + controllerIP + ":8181/restconf" + "/operations" +"/network-topology:network-topology/topology/topology-netconf/node/"
        url = url_base + deviceName + "/yang-ext:mount/ietf-netconf:copy-config"

        # Preapring the call's body (rely on Jinja2 template to build the body)
        #######################################################################
        f=open("/opt/stackstorm/packs/odl_vyatta/actions/templates/template_copy_config.j2")
        s=f.read()
        template=Template(s)
        body = template.render(source=source, target=target)
        print("\n")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("Sending REST call to ODL Controller (BSC):")
        print(" >>> Request:")
        print("     Method: POST")
        print("     URI:    " + url)
        print("     Body:    ")
        print body
        print("\n")
        
        # Sending the URL call(s) 
        #######################################################################        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cmd_response = requests.post(url, auth=(controllerUser, controllerPW), headers=headers, data=body, verify=False)
            cmd_response_code = cmd_response.status_code
            cmd_response_code = str(cmd_response_code)
            print(" >>> Response:")
            print("     Response code: " + cmd_response_code)
        try:
            data = json.loads(cmd_response.text)
            print("    Response body: ")
            print json.dumps(data, sort_keys=True, indent=6)
        except:
            print ("    Response body is empty")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
