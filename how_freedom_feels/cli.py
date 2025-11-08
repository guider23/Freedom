import click
import sys
from .core import FreedomConnect


@click.command()
@click.option("--connect", "-c", is_flag=True, help="Connect to VPN")
@click.option("--url", "-u", default=None, help="Custom config URL")
@click.option("--timeout", "-t", default=10, type=int, help="HTTP timeout in seconds")
@click.option("--interface", "-i", default=None, help="WireGuard interface name")
@click.option("--no-verify-ssl", is_flag=True, help="Skip SSL verification")
@click.option("--disconnect", "-d", is_flag=True, help="Disconnect from VPN")
@click.option("--status", "-s", is_flag=True, help="Show connection status")
def main(connect, url, timeout, interface, no_verify_ssl, disconnect, status):
    try:
        client = FreedomConnect(
            config_url=url,
            timeout=timeout,
            interface_name=interface,
            persist=False,
            verify_ssl=not no_verify_ssl
        )

        if status:
            status_info = client.get_status()
            if status_info["connected"]:
                click.echo("VPN is connected")
                if status_info["details"]:
                    click.echo("\nDetails:")
                    click.echo(status_info["details"])
            else:
                click.echo("VPN is not connected")
            sys.exit(0)

        elif disconnect:
            click.echo("Disconnecting from VPN...")
            client.disconnect(interface)
            sys.exit(0)

        elif connect:
            click.echo("Connecting to VPN...")
            if url:
                click.echo(f"Using custom config: {url}")
            else:
                click.echo("Using default config")
            
            client.connect()
            
            click.echo("\nConnected!")
            sys.exit(0)
        
        else:
            click.echo("Use --connect to connect, --disconnect to disconnect, or --status to check status")
            click.echo("Run 'freedom --help' for more options")
            sys.exit(0)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
