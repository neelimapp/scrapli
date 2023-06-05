from scrapli.driver.core import IOSXRDriver

MY_DEVICE = {
    "host": "10.30.111.168",
    "auth_username": "cisco",
    "auth_password": "cisco123!",
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
         
