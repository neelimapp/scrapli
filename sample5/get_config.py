from scrapli_netconf.driver import NetconfDriver

my_device = {
    "host": "198.18.134.1",
    "auth_username": "cisco",
    "auth_password": "cisco123",
    "auth_strict_key": False,
    "port": 830,
}

def main():
    with NetconfDriver(**my_device) as conn:
         response = conn.get_config(source="running")
    print(response.result)

if __name__ == "__main__":
    main()
