# How Freedom Feels
# I know WireGuard does the job, but I wanted something simple so my classmates could connect to my VM. Explaining IP forwarding gets tricky when everyone’s still busy with binary trees, so I built my own VPN client.
![SUntitled](https://github.com/user-attachments/assets/9e2f57fc-699a-4fb6-89f3-e508b8daec62)

So my college decided to block literally everything. YouTube? Blocked. Reddit? Blocked. Even Stack Overflow sometimes (yes, really). 

## TL;DR - Just Want It Working?

```bash
(You should have installed wireguard.exe beforehand) don't expect me to do everything
pip install how-freedom-feels
freedom --connect
```

That's it. If it works, you're done. If not, keep reading.

## The Problem (aka My College IT (AI&DS) Department Goes Too Far)

Not only did they block half the internet, they also blacklisted every VPN domain they could find. NordVPN? Blocked. ExpressVPN? Blocked. Even the small obscure ones. You can't even reach their websites to download configs. Big brain move by the IT department, honestly.

## The Solution (aka How I Got My Internet Back)

Here's the thing - they can't blacklist domains that don't exist yet. So I made this tool that grabs VPN configs from random cloud servers (AWS, Linode, Google Cloud - wherever I feel like hosting that week). 

By default, it connects to my servers. But fair warning: sometimes I forget to pay the AWS bill or just turn off the EC2 instance for fun. If it doesn't work, don't panic - just spin up your own server and use `--url` to point to it.

## Installation & Quick Start

### Install

```bash
pip install how-freedom-feels
```

### Connect

```bash
freedom --connect
```

### Want to Use Your Own Server?

```bash
freedom --connect --url https://your-domain.com/wg0.conf
```

## What You Actually Need (Requirements)

First, you need WireGuard. Yeah, you actually have to install something. I know, shocking.

- WireGuard: https://www.wireguard.com/install/ (just click and install, it's not rocket science)
- Python 3.7+ (if you're in college and don't have Python installed, we need to talk)

**Note:** If you get an error about WireGuard not being installed, install it first, then run `pip install how-freedom-feels` again.

## Want to Edit This and Use Your Own Domain?

Feel free to fork this, clone the source, and change the default domain to yours LOL. Just edit `how_freedom_feels/core.py` and change `DEFAULT_CONFIG_URL` to whatever you want.

```python
class FreedomConnect:
    DEFAULT_CONFIG_URL = "https://your-domain.com/your-config.conf"  # Change this!
```

Then build and use it locally, or publish your own version. I don't care, it's MIT licensed.

## Installation

```bash
pip install how-freedom-feels
```

That's it. No 47-step process, no "make sure to configure your DNS" nonsense. Just install and go.

## Quick Start (For the Impatient)

```bash
# Connect to my server (if it's running, no promises)
freedom --connect

# Connect to your own server (recommended because trust issues)
freedom --connect --url https://your-domain.com/wg0.conf

# Disconnect (when you're done procrastinating)
freedom --disconnect

# Check if you're actually connected
freedom --status
```

## Usage

### Connect with default config

```bash
freedom --connect
```

### Connect with custom domain/URL

```bash
freedom --connect --url https://your-domain.com/config.conf
```

### Connect with custom parameters

```bash
freedom --connect --url https://your-domain.com/config.conf --timeout 30
```

### Disconnect

```bash
freedom --disconnect
```

### Check status

```bash
freedom --status
```

### Python API

```python
from how_freedom_feels import FreedomConnect

# Connect with default config
client = FreedomConnect()
client.connect()

# Connect with custom URL
client = FreedomConnect(config_url="https://your-domain.com/config.conf")
client.connect()

# Connect with custom parameters
client = FreedomConnect(
    config_url="https://your-domain.com/config.conf",
    timeout=30,
    interface_name="wg0",
    persist=True
)
client.connect()

# Disconnect
client.disconnect()
```

## What It Does

- Installs in 2 seconds with pip (because your time is valuable)
- Connects to my servers by default (or yours, I'm not your boss)
- Actually cleans up after itself (looking at you, other VPN tools)
- Works from command line OR Python (flexibility, wow)
- Doesn't leave config files lying around like breadcrumbs

## What You Actually Need

- Python 3.7 or newer (seriously, if you're on Python 2.7, what year is it?)
- WireGuard installed (https://www.wireguard.com/install/)
- `wg-quick` in your PATH (the installer does this, don't panic)

## All the Flags and Stuff

- `--connect, -c`: Actually connect to the VPN (novel concept)
- `--disconnect, -d`: Turn it off when you're done
- `--status, -s`: Check if it's working (spoiler: it probably is)
- `--url, -u`: Point to your own server (trust no one, not even me)
- `--timeout, -t`: How long to wait before giving up (default: 10 seconds)
- `--interface, -i`: Custom interface name (if you're feeling fancy)
- `--no-verify-ssl`: Skip SSL checks (not recommended but hey, you do you)

## Setting Up Your Own Server

You'll need to set up your own WireGuard server on AWS, Linode, Google Cloud, or any VPS provider. 

**Quick steps:**
1. Spin up a Linux server (Ubuntu recommended)
2. Install WireGuard: `sudo apt install wireguard`
3. Generate keys and create configs
4. Host your config file on a web server
5. Use `freedom --connect --url https://your-server.com/config.conf`

For detailed instructions, check out [EC2_SETUP_FOR_BEGINNERS.md](EC2_SETUP_FOR_BEGINNERS.md) in the GitHub repository or search for "WireGuard server setup" guides online.

## How This Actually Works

1. Downloads a WireGuard config from wherever you told it to
2. Saves it temporarily (don't worry, it deletes it after)
3. Runs `wg-quick` to connect
4. Cleans up like a responsible program

## Why Your College Can't Block This

Here's the secret: network admins blacklist known VPN domains. They've got NordVPN.com, ExpressVPN.com, all the big names. But your random AWS EC2 instance at `ec2-54-123-45-67.compute.amazonaws.com`? Yeah, that's not on their list. You're welcome.

## License

MIT License


A dedicated work by Kaniska LOL 🥰

