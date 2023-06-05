from scrapli_netconf import NetconfDriver

IOSXR_DEVICE = {
    "host": "10.30.111.171",
    "auth_username": "cisco",
    "auth_password": "cisco123!",
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
    """Edit config example"""
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
