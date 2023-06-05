# Scrapli

Are you a pro in CLI commands but tired of manually logging in to each network device and managing the network device configuration and operational data using the command line interface ? Then its time for you to explore Scrapli and automate CLI scraping !!!!

How about structured data then ? Yes, you can also scrape structured data through scrapli_netconf.  

## What is Scrapli?

Scrapli is a python library that helps you to connect multiple network devices via SSH or Telnet, synchronously or asynchronously for screen scraping. Wondering what is screen scraping? well, it is the process of collecting screen display data from the network device and dumping it on to another screen or file. 

## Why Scrapli?
- Firstly, it is an open-source project, hence it is free to use and you can add new device/transport support to it based on your requirement
- It is fast, flexible, lightweight and well tested
- It uses asynchio python package and not threads to handle multiple device connections asynchronously
- It has an active community and well-maintained documentation
- As scrapli is completely written in python, it is easy to install, write code, integrate with any other python frameworks, troubleshoot and debug the issues using python debug tools
- It provides asynchronous and synchronous support for both ssh and telnet transport protocols
- It provides multi-vendor support (Arista EOS, Cisco NX-OS, Cisco IOS-XE, Cisco IOS-XR, Juniper JunOS)
         
## How does it work?

### Setup virtual environment(Optional)

If you would like to isolate the dependencies of scrapli from the system, you can create a python virtual environment.

Install virtualenv package using pip. pip is a package installer for Python. Here I am using Python 3.8.5 version.
```
pip install virtualenv
```
Using virtualenv package, create a python virtual environment.
Refer [creation of python virtual environments](https://docs.python.org/3/library/venv.html).
```
virtualenv scrapli_venv
```
Now activate the virtual environment.
```
source ~/scrapli_venv/bin/activate
```
### Install Scrapli and its plugins

In the “scrapli_venv” virtual environment, install **scrapli**. At the moment of producing this tutorial, latest version of scrapli is 2022.1.30.
```
pip install scrapli
```
Install **scrapli_netconf**. It is a netconf driver built on top of scrapli to automate devices while connecting them through Netconf(over SSH).
```
pip install scrapli_netconf
```
Install **scrapli[asyncssh]**. It is a scrapli plugin which speed up the automation process by executing the tasks asynchronously.
```
pip install scrapli[asyncssh]
```

Once you have all the required packages installed, go ahead and write the code to retrieve, configure or validate device data.

### Write a few lines of code to automate your network

## scrapli

### 1. generic_driver.py

```
from scrapli.driver import GenericDriver

MY_DEVICE = {
    "host": "10.30.11.1",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_strict_key": False,
    "port": 22,
}


def main():

    # `GenericDriver` is a good place to start if your 
    # platform is not supported by a "core" platform drivers
   
    # IMPORTANT: paging is NOT disabled w/ GenericDriver driver!
   
    conn = GenericDriver(**MY_DEVICE)
   
    conn.open()
    
    # Disable paging
    conn.send_command("terminal length 0")
    
    print("Prompt:\n")
    print(conn.channel.get_prompt() + "\n\n")

    print("Hostname:\n")
    print(conn.send_command("show run | i hostname").result + "\n\n")

    print("Version:\n")
    print(conn.send_command("show version").result + "\n\n")
   
    conn.close()


if __name__ == "__main__":
    main()

```
Here generic driver of scrapli is used to connect to the device via SSH. Generic driver doesn't disable paging, hence it is disabled explicitly using the CLI command. The above code open the connection to the device, disable paging, retrieve the prompt, hostname, version, and close the connection.

Execute **generic_driver.py** file and retrieve the results.

```
python generic_driver.py
```
### Output
```
Prompt:

RP/0/RP0/CPU0:R2_Red_Pine#

Hostname:

Sun Jun  4 21:30:03.851 PDT
Building configuration...
hostname R2_Red_Pine


Version:

Sun Jun  4 21:30:04.180 PDT
Cisco IOS XR Software, Version 7.9.1
Copyright (c) 2013-2023 by Cisco Systems, Inc.

Build Information:
 Built By     : ingunawa
 Built On     : Sun Apr  2 01:04:35 PDT 2023
 Built Host   : iox-ucs-047
 Workspace    : /auto/srcarchive15/prod/7.9.1/ncs5500/ws
 Version      : 7.9.1
 Location     : /opt/cisco/XR/packages/
 Label        : 7.9.1-iso

cisco NCS-5500 () processor
System uptime is 4 weeks 2 days 18 hours 1 minute
```
The output shows the prompt, hostname and version details of the device as per the request.

### 2. iosxr_driver.py

```
from scrapli.driver.core import IOSXRDriver

MY_DEVICE = {
    "host": "10.30.11.1",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_strict_key": False,
    "port": 22,
}


def main():

    # Context manager is a great way to use scrapli, 
    # it will auto open/close the connection for you
    
    # Platform drivers will auto-magically 
    # handle disabling paging for you
    
    with IOSXRDriver(**MY_DEVICE) as conn:
        result = conn.send_command("show interfaces summary")

    print(result.result)


if __name__ == "__main__":
    main()
    
```
Here core IOS-XR driver of scrapli is used to connect to the device via SSH. Core driver does disable the paging. Context manager helps open and close the device connection while connecting to it, hence explicit open and close instructions are not given in the code. 

Execute **iosxr_driver.py** file and retrieve the results.
```
python iosxr_driver.py
```
### Output
```
Interface Type          Total    UP       Down     Admin Down
--------------          -----    --       ----     ----------
ALL TYPES               56       3        0        53
--------------
IFT_HUNDREDGE           6        0        0        6
IFT_ETHERNET            1        1        0        0
IFT_NULL                1        1        0        0
IFT_TENGETHERNET        48       1        0        47

```
The output shows interfaces summary information as per the request.

### 3. sync_iosxr_driver.py

```
from scrapli.driver.core import IOSXRDriver

IOSXR_DEVICE1 = {
    "host": "10.30.11.1",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_strict_key": False,
    "port": 22,
}

IOSXR_DEVICE2 = {
    "host": "10.30.11.2",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_strict_key": False,
    "port": 22,
}

DEVICES = [IOSXR_DEVICE1, IOSXR_DEVICE2]


def gather_version(device):
    """Simple function to open a connection and get some data"""
    conn = IOSXRDriver(**device)
    conn.open()
    prompt_result = conn.get_prompt()
    version_result = conn.send_command("show version")
    conn.close()
    return prompt_result, version_result


def main():
    """Function to gather config details, and print results"""
    for device in DEVICES:
        output = gather_version(device)
        print(f"device prompt: {output[0]}")
        print(f"device show version: {output[1].result}")


if __name__ == "__main__":
    main()
    
```
Here the configurations of 2 devices are retrieved in a synchronous manner i.e one after another.

Execute **sync_iosxr_driver.py** file and retrieve the results.
```
time python sync_iosxr_driver.py
```
### Output
```
device prompt: RP/0/RP0/CPU0:R1_Macrocarpa#
device show version: Mon Jun  5 04:37:58.281 UTC
Cisco IOS XR Software, Version 7.10.1.26I
Copyright (c) 2013-2023 by Cisco Systems, Inc.

Build Information:
 Built By     : deenayak
 Built On     : Wed May 24 02:03:06 PDT 2023
 Built Host   : iox-ucs-002
 Workspace    : /auto/iox-ucs-002-san2/prod/7.10.1.26I.SIT_IMAGE/ncs5500/ws
 Version      : 7.10.1.26I
 Location     : /opt/cisco/XR/packages/
 Label        : 7.10.1.26I

cisco NCS-5500 () processor
System uptime is 1 day 12 hours 29 minutes

device prompt: RP/0/RP0/CPU0:R2_Red_Pine#
device show version: Sun Jun  4 21:40:55.670 PDT
Cisco IOS XR Software, Version 7.9.1
Copyright (c) 2013-2023 by Cisco Systems, Inc.

Build Information:
 Built By     : ingunawa
 Built On     : Sun Apr  2 01:04:35 PDT 2023
 Built Host   : iox-ucs-047
 Workspace    : /auto/srcarchive15/prod/7.9.1/ncs5500/ws
 Version      : 7.9.1
 Location     : /opt/cisco/XR/packages/
 Label        : 7.9.1-iso

cisco NCS-5500 () processor
System uptime is 4 weeks 2 days 18 hours 12 minutes

real	0m4.028s
user	0m0.238s
sys	0m0.140s

```
The output shows prompt and version details of the 2 devices and it took 4 seconds to retrieve this information in a synchronous way.

### 4. async_iosxr_driver.py

```
import asyncio

from scrapli.driver.core import AsyncIOSXRDriver

IOSXR_DEVICE1 = {
    "host": "10.30.11.1",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_strict_key": False,
    "port": 22,
    "transport": "asyncssh",
    "driver": AsyncIOSXRDriver,
    
}

IOSXR_DEVICE2 = {
    "host": "10.30.11.2",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_strict_key": False,
    "port": 22,
    "transport": "asyncssh",
    "driver": AsyncIOSXRDriver,
}

DEVICES = [IOSXR_DEVICE1, IOSXR_DEVICE2]


async def gather_version(device):
    """Simple function to open a connection and get some data"""
    driver = device.pop("driver")
    conn = driver(**device)
    await conn.open()
    prompt_result = await conn.get_prompt()
    version_result = await conn.send_command("show version")
    await conn.close()
    return prompt_result, version_result


async def main():
    """Function to gather coroutines, await them and print results"""
    coroutines = [gather_version(device) for device in DEVICES]
    results = await asyncio.gather(*coroutines)
    for result in results:
        print(f"device prompt: {result[0]}")
        print(f"device show version: {result[1].result}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

```
Here the configurations of 2 devices are retrieved in an asynchronous way i.e in parallel. In this case we use AsyncIOSXRDriver to connect the devices via asyncssh transport. The functions in this code are executed asynchronously, hence we await on every operation of the device. 

Execute **async_iosxr_driver.py** file and retrieve the results.
```
time python async_iosxr_driver.py
```
### Output
```
device prompt: RP/0/RP0/CPU0:R1_Macrocarpa#
device show version: Mon Jun  5 04:39:37.260 UTC
Cisco IOS XR Software, Version 7.10.1.26I
Copyright (c) 2013-2023 by Cisco Systems, Inc.

Build Information:
 Built By     : deenayak
 Built On     : Wed May 24 02:03:06 PDT 2023
 Built Host   : iox-ucs-002
 Workspace    : /auto/iox-ucs-002-san2/prod/7.10.1.26I.SIT_IMAGE/ncs5500/ws
 Version      : 7.10.1.26I
 Location     : /opt/cisco/XR/packages/
 Label        : 7.10.1.26I

cisco NCS-5500 () processor
System uptime is 1 day 12 hours 30 minutes

device prompt: RP/0/RP0/CPU0:R2_Red_Pine#
device show version: Sun Jun  4 21:42:32.574 PDT
Cisco IOS XR Software, Version 7.9.1
Copyright (c) 2013-2023 by Cisco Systems, Inc.

Build Information:
 Built By     : ingunawa
 Built On     : Sun Apr  2 01:04:35 PDT 2023
 Built Host   : iox-ucs-047
 Workspace    : /auto/srcarchive15/prod/7.9.1/ncs5500/ws
 Version      : 7.9.1
 Location     : /opt/cisco/XR/packages/
 Label        : 7.9.1-iso

cisco NCS-5500 () processor
System uptime is 4 weeks 2 days 18 hours 14 minutes

real	0m1.966s
user	0m0.363s
sys	0m0.074s
```
The output shows prompt and version details of the 2 devices and it took 1.9 seconds to retrieve this information asynchronously.

## scrapli_netconf

### 5. get_config.py

```
from scrapli_netconf.driver import NetconfDriver

my_device = {
    "host": "10.30.11.1",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_strict_key": False,
    "port": 830,
}

def main():
    with NetconfDriver(**my_device) as conn:
         response = conn.get_config(source="running")
    print(response.result)

if __name__ == "__main__":
    main()
    
```
Here NetconfDriver is used to connect the device via Netconf over SSH to retrieve running configuration.

Execute **get_config.py** file and retrieve the results.
```
python get_config.py
```
### Output 
```
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101">
  <data>
    <netconf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-man-xml-ttyagent-cfg">
      <agent>
        <tty>
          <enable/>
        </tty>
      </agent>
    </netconf>
    <call-home xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-call-home-cfg">
      <active/>
      <contact-smart-licensing>true</contact-smart-licensing>
      <profiles>
        <profile>
          <profile-name>CiscoTAC-1</profile-name>
          <active/>
          <methods>
            <method>
              <method>email</method>
              <enable>false</enable>
            </method>
            <method>
              <method>http</method>
              <enable>true</enable>
            </method>
          </methods>
        </profile>
      </profiles>
    </call-home>
   <data>
  <rpc-reply>
```
The output shows running configuration of the device as per the request.

### 6. edit_config.py

```
from scrapli_netconf import NetconfDriver

IOSXR_DEVICE = {
    "host": "10.30.11.1",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_strict_key": False,
    "port": 830,
}

EDIT_INTERFACE = """
<config>
  <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
    <interface-configuration>
      <active>act</active>
      <interface-name>GigabitEthernet0/0/0/0</interface-name>
      <description>skfasjdlkfjdsf</description>
      <ipv4-network xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg">
        <addresses>
          <primary>
            <address>10.10.0.1</address>
            <netmask>255.255.255.0</netmask>
          </primary>
        </addresses>
      </ipv4-network>
    </interface-configuration>
  </interface-configurations>
</config>
"""


def main():
    """Edit config"""
    # create scrapli_netconf connection just like with scrapli, open the connection
    conn = NetconfDriver(**IOSXR_DEVICE)
    conn.open()
    
    print("LOCK")
    # lock the candidate config before starting because why not
    result = conn.lock(target="candidate")
    print(result.result)

    print("EDIT")
    config = EDIT_INTERFACE
    result = conn.edit_config(config=config, target="candidate")
    print(result.result)

    print("COMMIT")
    # commit config changes
    conn.commit()
    print(result.result)

    print("UNLOCK")
    # unlock the candidate now that we're done
    result = conn.unlock(target="candidate")
    print(result.result)

    # close the session
    conn.close()


if __name__ == "__main__":
    main()

```
Here we are connecting to the device via NETCONF to edit and commit the candidate configuration.

Execute **edit_config.py** file and retrieve the results.
```
python edit_config.py
```
### Output
```
LOCK
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101">
  <ok/>
</rpc-reply>

EDIT
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="102">
  <ok/>
</rpc-reply>

COMMIT
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="102">
  <ok/>
</rpc-reply>

UNLOCK
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="104">
  <ok/>
</rpc-reply>

```
The output returns rpc replies as ok, which means the edit operations are completed successfully.

### 7. async_edit_config.py

```
import asyncio

from scrapli_netconf import AsyncNetconfDriver

IOSXR_DEVICE1 = {
    "host": "10.30.11.1",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_strict_key": False,
    "port": 830,
    "transport": "asyncssh",
}

IOSXR_DEVICE2 = {
    "host": "10.30.11.2",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_strict_key": False,
    "port": 830,
    "transport": "asyncssh",
}

DEVICES = [IOSXR_DEVICE1, IOSXR_DEVICE2]

EDIT_INTERFACE = """
<config>
  <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
    <interface-configuration>
      <active>act</active>
      <interface-name>GigabitEthernet0/0/0/0</interface-name>
      <description>skfasjdlkfjdsf</description>
      <ipv4-network xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg">
        <addresses>
          <primary>
            <address>10.10.0.1</address>
            <netmask>255.255.255.0</netmask>
          </primary>
        </addresses>
      </ipv4-network>
    </interface-configuration>
  </interface-configurations>
</config>
"""


async def main():
    """Edit config """
    
    for device in DEVICES:
        # create scrapli_netconf connection just like with scrapli, open the connection
        conn = AsyncNetconfDriver(**device)
        await conn.open()
        
        print("LOCK")
        # lock the candidate config before starting because why not
        result = await conn.lock(target="candidate")
        print(result.result)
        
        print("EDIT")
        config = EDIT_INTERFACE
        result = await conn.edit_config(config=config, target="candidate")
        print(result.result)

        print("COMMIT")
        # commit config changes
        result = await conn.commit()
        print(result.result)

        print("UNLOCK")
        # unlock the candidate now that we're done
        result = await conn.unlock(target="candidate")
        print(result.result)

        # close the session
        await conn.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

```
Here we are connecting to 2 devices via NETCONF to edit and commit the candidate configuration asynchronously.

Execute **async_edit_config.py** file and retrieve the results.
```
python async_edit_config.py
```
### Output
```
LOCK
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101">
  <ok/>
</rpc-reply>

EDIT
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="102">
  <ok/>
</rpc-reply>

COMMIT
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="103">
  <ok/>
</rpc-reply>

UNLOCK
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="104">
  <ok/>
</rpc-reply>

LOCK
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101">
  <ok/>
</rpc-reply>

EDIT
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="102">
  <ok/>
</rpc-reply>

COMMIT
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="103">
  <ok/>
</rpc-reply>

UNLOCK
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="104">
  <ok/>
</rpc-reply>
```
The output returns rpc replies as ok, which means the asynchronously edit operations on 2 devices completed successfully.

## What are the flavours of Scrapli ?
- [scrapli_netconf](https://scrapli.github.io/scrapli_netconf/) 
- [nornir_scrapli](https://scrapli.github.io/nornir_scrapli/)
- [scrapli_community](https://scrapli.github.io/scrapli_community/)
- [scrapli_replay](https://scrapli.github.io/scrapli_replay/)
- [scrapli_cfg](https://scrapli.github.io/scrapli_cfg/)
- [scrapli_stubs](https://github.com/scrapli/scrapli_stubs)
- [scrapli_asynchssh](https://github.com/scrapli/scrapli_asyncssh)
- [scrapli_ssh2](https://github.com/scrapli/scrapli_ssh2)
- [scrapli_paramiko](https://github.com/scrapli/scrapli_paramiko)
- [scrapligo](https://github.com/scrapli/scrapligo)
- [srlinux-scrapli](https://github.com/srl-labs/srlinux-scrapli) 

# What did I learn ?
Scrapli is a screen scraping python library that provides a way to automate your network tasks efficiently by connecting multiple network devices via SSH, NETCONF or Telnet, synchronously or asynchronously. Being an open-sourced project written in python makes it easy for the user to debug and troubleshoot. Above all, it's time-efficient, free, and easy to use. Write simple lines of python code to execute your network tasks on a lot of your network devices with CLI scraping!!


# Resources

- [Scrapli Documentation](https://carlmontanari.github.io/scrapli/)
- [Scrapli GitHub repository](https://github.com/carlmontanari/scrapli)

#
*Stay tuned to learn about another network automation tool in our next post.*
*Please do comment below, your questions, and what you would like to learn about network automation!!*
