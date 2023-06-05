import asyncio

from scrapli_netconf import AsyncNetconfDriver

IOSXR_DEVICE1 = {
    "host": "10.30.111.171",
    "auth_username": "cisco",
    "auth_password": "cisco123!",
    "auth_strict_key": False,
    "port": 830,
    "transport": "asyncssh",
}

IOSXR_DEVICE2 = {
    "host": "10.30.111.168",
    "auth_username": "cisco",
    "auth_password": "cisco123!",
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
