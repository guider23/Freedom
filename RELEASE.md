# GitHub Release Instructions

This folder contains all files ready for GitHub release.

## Files Included

- `README.md` - Main documentation
- `EC2_SETUP_FOR_BEGINNERS.md` - Server setup guide
- `LICENSE` - MIT License
- `how_freedom_feels/` - Source code
- `examples/` - Usage examples
- `requirements.txt` - Dependencies
- `.gitignore` - Git ignore rules

## How to Create a GitHub Release

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial release v0.1.0"
git branch -M main
git remote add origin https://github.com/guider23/how-freedom-feels.git
git push -u origin main
```

### 2. Create a Release on GitHub

1. Go to https://github.com/guider23/how-freedom-feels
2. Click "Releases" → "Create a new release"
3. Create a new tag: `v0.1.0`
4. Release title: `v0.1.0 - Initial Release`
5. Description:

```markdown
## How Freedom Feels v0.1.0

A lightweight VPN connection manager to bypass network restrictions.

### Features
- Connect to VPN with custom config URLs
- Default server support (AWS/Linode/Google Cloud)
- Simple CLI interface
- Python API support

### Installation

```bash
pip install how-freedom-feels
```

### Quick Start

```bash
# Connect
freedom --connect

# Connect to custom server
freedom --connect --url https://your-domain.com/config.conf

# Disconnect
freedom --disconnect
```

### Requirements
- Python 3.7+
- WireGuard installed

### Documentation
- [README.md](README.md) - Full documentation
- [EC2_SETUP_FOR_BEGINNERS.md](EC2_SETUP_FOR_BEGINNERS.md) - Set up your own server

### What's Changed
- Initial release
```

6. Click "Publish release"

### 3. Optional: Attach Release Assets

You can attach the built wheel file:
- Build first: `python -m build`
- Attach `dist/how_freedom_feels-0.1.0-py3-none-any.whl`

## Repository Setup

### Create .gitignore

Already included in this folder.

### Add Topics

On GitHub, add these topics to your repository:
- vpn
- wireguard
- python
- cli
- network-tools
- bypass

### Add Description

Repository description:
```
A lightweight VPN connection manager to bypass network restrictions using custom config URLs
```

### Enable Features

- Issues: Yes
- Projects: Optional
- Wiki: Optional
- Discussions: Optional

## Maintaining Releases

### For New Versions

1. Update version in code
2. Update CHANGELOG.md (create one)
3. Commit changes
4. Create new tag: `git tag v0.2.0`
5. Push: `git push origin v0.2.0`
6. Create release on GitHub

### Version Numbering

Follow semantic versioning:
- `0.1.0` - Initial release
- `0.1.1` - Bug fixes
- `0.2.0` - New features
- `1.0.0` - Stable release

## Files Structure

```
github_release/
├── README.md
├── EC2_SETUP_FOR_BEGINNERS.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── how_freedom_feels/
│   ├── __init__.py
│   ├── core.py
│   └── cli.py
└── examples/
    └── basic_usage.py
```

This is the clean version ready for public release!
