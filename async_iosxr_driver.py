import asyncio

from scrapli.driver.core import AsyncIOSXRDriver

IOSXR_DEVICE1 = {
    "host": "10.30.111.171",
    "auth_username": "cisco",
    "auth_password": "cisco123!",
    "auth_strict_key": False,
    "port": 22,
    "transport": "asyncssh",
    "driver": AsyncIOSXRDriver,
}

IOSXR_DEVICE2 = {
    "host": "10.30.111.168",
    "auth_username": "cisco",
    "auth_password": "cisco123!",
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


