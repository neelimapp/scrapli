from scrapli.driver import GenericDriver

MY_DEVICE = {
    "host": "198.18.134.1",
    "auth_username": "cisco",
    "auth_password": "cisco123",
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
