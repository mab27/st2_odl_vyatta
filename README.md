
[![Build Status](https://travis-ci.org/mab27/st2_odl_vyatta.svg?branch=master)](https://travis-ci.org/mab27/st2_odl_vyatta)

# StackStorm automation pack for Brocade vyatta vRouter via OpenDayLight Controller

## Content of the pack:
- This pack contains simple actions and workflows to interact with the Brocade 5600 vRouter including: interfaces mgmt, routing, Firewalling, IPSec, via an OpenDayLight Controller.
- The ODL Controller used in this repo is the commercial distribution from Brocade: Brocade SDN Controller (BSC) version 4.1.
- Action runner for the different actions is ```python-script``` which generates REST calls to the ODL Controller (BSC).
- This pack has been written based on the Brocade Vyatta Network OS configuration manuals: 

## What is OpenDayLight (Brief introduction):
- Vendor-driven consortium for developing open-source SDN controller platform.
- It is developed in Java and the latest Release: Carbon (April 2017)
- It employs a model-driven approach to describe the network, the functions to be performed on it and the resulting state. This model-driven approach is fundamental to ODL project, YANG is a data modeling language used to model configuration and state data manipulated. This modeling engine acts as a middleware between the southbound plugins (OpenFlow, NETCONF, OVSDB etc ...) and the northbound plugin: RESTCONF API.
- The content of this pack acts as a so called “SDN app” in the ODL nomenclature, in the sense where it consumes the ODL Northbound API (RESTCONF) to manipulate configuration and obtain states from the network. And because ODL is by nature multivendor, this can allow for multivendor network automation.
- For more information check the following links:

## How to install this pack:
- Go to the packs directory in your StackStorm/BWC machine and Git clone this reposistory.
- Rename the folder to ```odl_vyatta```
- Install python virtual Environement
- Restart st2ctl service to register the actions/rules/etc...

```
cd /opt/stackstorm/packs
sudo git clone https://github.com/mab27/st2_odl_vyatta.git
sudo cp -r st2_odl_vyatta odl_vyatta
sudo rm -r st2_odl_vyatta
sudo cd odl_vyatta
sudo st2 run packs.setup_virtualenv packs=odl_vyatta
```
- Restart and check if the actions have been registered:
```
sudo st2ctl restart
st2 action list -p odl_vyatta
```
## Before using the pack:
- Check the status of the ODL Controller, if needed start it.
```
sudo service brcd-bsc {start|stop|restart|status|configure|clean [msg]}
```
- Check the status of the ODL Controller UI, if needed start it.
```
sudo service brcd-ui {start|stop|status|restart|configure}
```
- For general information on how to use the BSC : [Brocade SDN Controller User Guide, 4.0.0](http://www.brocade.com/content/html/en/sdn-controller/4.0.0/bsc-400-userguide/GUID-4FC280C8-B75D-4AED-9576-854687A8DE77-homepage.html)
- To understand the structure of the RESTConf calls (How YANG data-models are exposed via the REST API), use the embeded api-doc explorer. This tool is accessible on the controller UI at **{{ip_adress_of_bsc}}:8181/apidoc/explorer/index.html**. go to "Mounted Ressources" and click on the device you are interested in. You will obtain the full ist of CRUD operations available, to help you build your northbound calls based on  the southbound rpc you are looking for.

## Actions & Workflows:

- **mount** / **unmount**:

- **cfg_interface** 	/ 	**del_interface**
- **cfg_ip_route** 		/ 	**del_ip_route**
- **cfg_ebgp** 			/ 	**del_ebgp**
- **adv_ebgp_prefix** 	/ 	**del_ebgp_prefix**
- **cfg_ipsec** 		/ 	**del_ipsec**
- **cfg_fw_rule** 		/ 	**del_fw_rule**
- **cfg_fw_instance** 	/ 	**del_fw_instance**

- **show_interfaces**
- **show_ip_route**
- **show_bgp_sum**
- **show_bgp_neighbors**
- **show_vpn**
- **show_fw**

- **show_run_conf**		/ **show_startup_conf** 	/ **copy_cfg**


### Examples:

- Mount / Unmount a device to the ODL Controller:
```
st2 run odl_vyatta.mount mountName=vR001 deviceIP=192.168.0.10

st2 run odl_vyatta.unmount mountName=vR001 deviceIP=192.168.0.10
```

- Interface management:
```
st2 run odl_vyatta.cfg_interface deviceName=vR001 intfType=loopback intfNum=lo10 address=10.10.10.10/32

st2 run odl_vyatta.show_interfaces deviceName=vR001

```

- Static routing:
```
st2 run odl_vyatta.cfg_ip_route deviceName=vR001 subnet=20.20.20.0/24 nextHop=172.16.0.20

st2 run odl_vyatta.show_ip_route deviceName=vR001

st2 run odl_vyatta.del_ip_route deviceName=vR001 subnet=20.20.20.0/24 nextHop=172.16.0.20
```


- BGP Routing:
```
st2 run odl_vyatta.cfg_ebgp eastDeviceName=vR001 eastASN=65010 eastPeeringIP=192.168.0.10 westDeviceName=vR002 westPeeringIP=192.168.0.20 westASN=65020

```

- Firewall:
```

```

- IPSec:
```
st2 run odl_vyatta.cfg_ipsec_mistral eastDeviceName=vR001 westDeviceName=vR002 eastTunnelIP=172.16.0.10 westTunnelIP=172.16.0.20 eastPrefix=10.10.10.10/32 westPrefix=20.20.20.20/32

st2 run odl_vyatta.show_vpn deviceName=vR001

st2 run odl_vyatta.del_ipsec deviceName=vR001 
```

## Rules:

### Webhooks: 
- **webhook_cfg_interface**: From Webhook payload, fire the action to configure an interface.
- **webhook_del_interface**: From Webhook payload, fire the action to delete an  interface.

- **webhook_cfg_ip_route**: From Webhook payload, fire the action to configure an ip route.
- **webhook_del_ip_route**: From Webhook payload, fire the action to delete an ip route.

- **webhook_cfg_fw_rule**: From Webhook payload, fire the action to configure a FW rule.
- **webhook_del_fw_rule**: From Webhook payload, fire the action to delete a FW rule.
- **webhook_cfg_fw_instance**: From Webhook payload, fire the action to apply a FW instance.
- **webhook_del_fw_instance**: From Webhook payload, fire the action to remove a FW instance.

### What are Webhooks: 
- Systems that push data to the ST2 API when an event you are interested in occurs.
- Webhooks come handy is when you want to consume events from a 3rd party service which already offer webhooks integration - e.g. GitHub
- Webhooks aren't directly created --> they're created via rules.

The rules in this pack are written using one of the default triggers: ```core.st2.webhook``` --> This means that the rule will be watching for incoming events that are in the form of a custom webhook.

POST-ing data to a custom webhook will cause a trigger with the following attributes to be dispatched:
- **trigger** - Trigger name.
- **trigger.headers** - Dictionary containing the request headers.
- **trigger.body** - Dictionary containing the request body.

These allows the rule to check if the event matches any of its criteria, if yes, then the corresponding action/workflow will be fired.

### Pre-requisistes (Before trying rules):
- Make sure the rules are registered and available by list the available rules for the pack:
```
st2 rule list -p odl_vyatta
```
- If needed, restart the rules service:
```
sudo st2ctl restart --register-rules
```
- Obtain an authentication token. You'll need it to replace **$TOKEN** in the cURL commands below:
```
st2 auth login -p password
```

### Usefull commands to verify rules enforcement and actions/workflows executions:
- Check the latest rules enforced:
```
st2 rule-enforcement list -n 5
```
- Check the details of the emitted trigger  (obtain **trigger_id** from previous command):
```
st2 trigger-instance get **trigger_id**
```
- Check the latest actions/workflows executed:
```
st2 execution list -n 5
```

================
================
================
================
================


### Examples:

- Trigger the **cfg_fw_rule** rule:

First create a file ```body_cfg_rule_fw-1_1.json```:
```
{
    "task": "cfg_fw_rule",
    "deviceIP": "192.168.0.10",
    "rule_set_name": "fw-1",
    "rule_number": "1",
    "rule_filter": {
    	"action": "accept",
    	"state": "enable",
    	"protocol": "tcp",
    	"dst_addr": "172.60.10.0/24",
    	"dst_port": "80", 
    	"src_addr": "10.10.10.0/8"
    }
}
```
Then, send the call via cURL command:
```
curl -k -H "Content-Type:application/json" -H "X-Auth-Token:$TOKEN" -d @body_cfg_rule_fw-1_1.json http://localhost:9101/v1/webhooks/vrouter
```

- Trigger again the **cfg_fw_rule** rule:

First create a file ```body_cfg_rule_fw-1_2.json```:
```
{
    "task": "cfg_fw_rule",
    "deviceIP": "192.168.0.10",
    "rule_set_name": "fw-1",
    "rule_number": "2",
    "rule_filter": {
        "action": "accept",
        "state": "enable",
        "protocol": "tcp",
        "dst_addr": "172.60.10.0/24",
        "dst_port": "80", 
        "src_addr": "10.10.10.0/8"
    }
}
```
Then, send the call via cURL command:
```
curl -k -H "Content-Type:application/json" -H "X-Auth-Token:$TOKEN" -d @body_cfg_rule_fw-1_2.json http://localhost:9101/v1/webhooks/vrouter
```

- Trigger the **del_fw_rule** rule:

First create a file ```body_del_rule_fw-1_2.json```:
```
{
    "task": "cfg_fw_rule",
    "deviceIP": "192.168.0.10",
    "rule_set_name": "fw_1",
    "rule_number": "1"
}
```
Then, send the call via cURL command:
```
curl -k -H "Content-Type:application/json" -H "X-Auth-Token:$TOKEN" -d @body_del_rule_fw-1_2.json http://localhost:9101/v1/webhooks/vrouter
```


- Trigger the **apply_fw_instance** rule:

First create a file ```body_apply_instance_fw-1.json```:
```
{
    "task": "apply_fw_instance",
    "deviceIP": "192.168.0.10",
    "rule_set_name": "fw-1",
    "intfNum": "dp0p192p1",
    "direction": "out"
}
```
Then, send the call via cURL command:
```
curl -k -H "Content-Type:application/json" -H "X-Auth-Token:$TOKEN" -d @body_apply_instance_fw-1.json http://localhost:9101/v1/webhooks/vrouter
```
- Trigger the **remove_fw_instance** rule:

First create a file ```body_remove_instance_fw-1.json```:
```
{
    "task": "remove_fw_instance",
    "deviceIP": "192.168.0.10",
    "rule_set_name": "fw-1",
    "intfNum": "dp0p192p1",
    "direction": "out"
}
```
Then, send the call via cURL command:
```
curl -k -H "Content-Type:application/json" -H "X-Auth-Token:$TOKEN" -d @body_remove_instance_fw-1.json http://localhost:9101/v1/webhooks/vrouter
```

## ChatOps:
### What is Chatops:
- It is about humans talking to ChatBots (and the other way around).
- A more formal definition would be the concept of delegating responsibility of tasks/actions to an internal robot that also sits inline with your existing company.
- Simply put, ChatOps let you take operational and development workflows and expose them as commands that can be executed in a company chat room.
- The benefits are numerous: Shared CLI to help for incident management, enable team scaling by allowing automation consumable in a easy way by every team member (Makes everyone more powerfull) etc ...

### ChatOps in this pack:
- StackStorm facilitates the introduction of ChatOps in your organisation by diffeent integrations with pupular chat tools and bots.
- Any action/workflow you want to expose in a chatroom will have an action-alias, in the ```aliases``` folder.
- The demo in this pack has been realised using Slack as a chat tool and Hu-Bot as a bot. 

### Examples:
Before trying any conversation with your bot, check its online presence in the chatroom, the bot must appear on-line to be able to communicate with ST2.
And also type in the two following commands to restart the ChatOps service, this is often required every time you reconnect to you chatroom:
```
st2ctl reload --register-aliases
sudo service st2chatops restart
```
- Show the firewall config on a device, type this in the chatroom:
```
!show fw on 192.168.0.10 
```