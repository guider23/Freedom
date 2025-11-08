# Configuration

Before using this tool, you need to set up your default config URL.

## Setting Your Default Server

Edit `how_freedom_feels/core.py` and change the `DEFAULT_CONFIG_URL`:

```python
class FreedomConnect:
    DEFAULT_CONFIG_URL = "https://your-domain.com/config.conf"
```

Replace `https://your-domain.com/config.conf` with the URL to your WireGuard config file.

## Alternative: Always Use --url

You can skip editing the code and always use the `--url` flag:

```bash
freedom --connect --url https://your-server.com/wg0.conf
```

## Security Note

**Do not commit your real config URL to public repositories!**

The default URL in this repository is set to `https://example.com/config.conf` as a placeholder. You must replace it with your own server before using.

## Setting Up Your Server

See [EC2_SETUP_FOR_BEGINNERS.md](EC2_SETUP_FOR_BEGINNERS.md) for instructions on setting up your own WireGuard server.
