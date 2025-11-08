from how_freedom_feels import FreedomConnect


def example_default_connection():
    print("Example 1: Connect with default config")
    client = FreedomConnect()
    client.connect()


def example_custom_url():
    print("Example 2: Connect with custom URL")
    client = FreedomConnect(
        config_url="https://your-domain.com/custom-config.conf"
    )
    client.connect()


def example_custom_parameters():
    print("Example 3: Connect with custom parameters")
    client = FreedomConnect(
        config_url="https://your-domain.com/config.conf",
        timeout=30,
        interface_name="wg0",
        persist=True,
        verify_ssl=True
    )
    client.connect()


def example_disconnect():
    print("Example 4: Disconnect")
    client = FreedomConnect()
    client.disconnect()


def example_status_check():
    print("Example 5: Check status")
    client = FreedomConnect()
    status = client.get_status()
    if status["connected"]:
        print("VPN is connected!")
        print(f"Details: {status['details']}")
    else:
        print("VPN is not connected")


def example_with_error_handling():
    print("Example 6: With error handling")
    client = FreedomConnect()
    
    try:
        client.connect()
        print("Successfully connected!")
    except Exception as e:
        print(f"Connection failed: {e}")


if __name__ == "__main__":
    example_with_error_handling()
