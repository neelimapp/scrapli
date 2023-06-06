
from scrapli.driver.core import IOSXRDriver

IOSXR_DEVICE1 = {
    "host": "198.18.134.1",
    "auth_username": "cisco",
    "auth_password": "cisco123",
    "auth_strict_key": False,
    "port": 22,
}

IOSXR_DEVICE2 = {
    "host": "198.18.134.1",
    "auth_username": "cisco",
    "auth_password": "cisco123",
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
    """Function to gather coroutines, await them and print results"""
    for device in DEVICES:
        output = gather_version(device)
        print(f"device prompt: {output[0]}")
        print(f"device show version: {output[1].result}")


if __name__ == "__main__":
    main()


