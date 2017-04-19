import requests
import warnings
from jinja2 import Template
# Libary import used for Key-Value store manipulation
from st2client.client import Client
from st2client.models import KeyValuePair

from st2actions.runners.pythonrunner import Action

class cfgIpsec(Action):
    def run(self, controllerIP, controllerUser, controllerPW, deviceName, peerIP, localIP, localPrefix, remotePrefix, ikeGroup, ikeProposal, ikeVersion, ikeEncryption, ikeHashAlg, ikeLifetime, espGroup, espProposal, espEncryption, espHashAlg, espLifetime, psk, tunnelID):
        
        # Preapring the request(s)
        ####################################################################### 
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }
        
        url_base = "http://" + controllerIP + ":8181/restconf" + "/config" +"/network-topology:network-topology/topology/topology-netconf/node/"
        url = url_base + deviceName + "/yang-ext:mount/vyatta-security-v1:security/vyatta-security-vpn-ipsec-v1:vpn/"

        # Preapring the call's body (rely on Jinja2 template to build the body)
        #######################################################################
        f=open("/opt/stackstorm/packs/odl_vyatta/actions/templates/template_ipsec.j2")
        s=f.read()
        template=Template(s)
        body = template.render(peerIP=peerIP, localIP=localIP, localPrefix=localPrefix, remotePrefix=remotePrefix, ikeGroup=ikeGroup, ikeProposal=ikeProposal, ikeVersion=ikeVersion, ikeEncryption=ikeEncryption, ikeHashAlg=ikeHashAlg, ikeLifetime=ikeLifetime, espGroup=espGroup, espProposal=espProposal, espEncryption=espEncryption, espHashAlg=espHashAlg, espLifetime=espLifetime, psk=psk, tunnelID=tunnelID)
        print("\n")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("Sending REST call to ODL Controller (BSC):")
        print(" >>> Request:")
        print("     Method: PUT")
        print("     URI:    " + url)
        print("     Body:    ")
        print body
        print("\n")
        
        # Sending the URL call(s) 
        #######################################################################        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cmd_response = requests.put(url, auth=(controllerUser, controllerPW), headers=headers, data=body, verify=False)
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
