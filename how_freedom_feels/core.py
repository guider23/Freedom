import subprocess
import requests
import tempfile
import os
import platform
from typing import Optional


class FreedomConnect:
    DEFAULT_CONFIG_URL = "https://example.com/configs/wg0-client.txt"

    def __init__(
        self,
        config_url: Optional[str] = None,
        timeout: int = 10,
        interface_name: Optional[str] = None,
        persist: bool = False,
        verify_ssl: bool = True,
    ):
        self.config_url = config_url or self.DEFAULT_CONFIG_URL
        self.timeout = timeout
        self.interface_name = interface_name
        self.persist = persist
        self.verify_ssl = verify_ssl
        self.config_path = None
        self._is_windows = platform.system() == "Windows"

    def _get_wireguard_command(self) -> str:
        """Get the WireGuard command based on platform"""
        if self._is_windows:
            # On Windows, check for wireguard.exe (CLI) or use the service
            return "wireguard.exe"
        return "wg-quick"

    def _check_wg_installed(self) -> bool:
        if self._is_windows:
            # Check for wireguard.exe or wg.exe on Windows
            try:
                subprocess.run(
                    ["wg", "--version"],
                    capture_output=True,
                    check=True,
                    shell=True
                )
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    subprocess.run(
                        ["wireguard.exe", "/help"],
                        capture_output=True,
                        shell=True
                    )
                    return True
                except:
                    return False
        else:
            wg_command = self._get_wireguard_command()
            try:
                subprocess.run(
                    [wg_command, "--version"],
                    capture_output=True,
                    check=True
                )
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False

    def show_wg_warning(self):
        if not self._check_wg_installed():
            print("\n" + "="*60)
            print("WARNING: WireGuard may not be installed!")
            print("="*60)
            if self._is_windows:
                print("\nDownload WireGuard for Windows:")
                print("https://www.wireguard.com/install/")
            else:
                print("\nDownload WireGuard:")
                print("https://www.wireguard.com/install/")
            print("\nIf WireGuard is not installed, connection will fail.")
            print("="*60 + "\n")

    def download_config(self) -> str:
        try:
            headers = {
                'User-Agent': 'how-freedom-feels/0.1.7',
                'Accept': 'text/plain, */*'
            }
            response = requests.get(
                self.config_url,
                timeout=self.timeout,
                verify=self.verify_ssl,
                headers=headers
            )
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise Exception(f"Failed to download config from {self.config_url}: {e}")

    def _create_config_file(self, config_data: str) -> str:
        if self.persist and self.interface_name:
            config_dir = os.path.expanduser("~/.config/wireguard")
            os.makedirs(config_dir, exist_ok=True)
            config_path = os.path.join(config_dir, f"{self.interface_name}.conf")
            with open(config_path, "w") as f:
                f.write(config_data)
            return config_path
        else:
            # On Windows, use a consistent filename so we can disconnect later
            if self._is_windows:
                tunnel_name = self.interface_name or "freedom-vpn"
                temp_dir = tempfile.gettempdir()
                config_path = os.path.join(temp_dir, f"{tunnel_name}.conf")
                with open(config_path, "w") as f:
                    f.write(config_data)
                return config_path
            else:
                # On Linux/Mac, use temporary file
                tmp = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".conf",
                    mode="w"
                )
                tmp.write(config_data)
                tmp.close()
                return tmp.name

    def connect(self) -> bool:
        self.show_wg_warning()
        
        try:
            config_data = self.download_config()
            print(f"Downloaded config from {self.config_url}")

            self.config_path = self._create_config_file(config_data)
            print(f"Created config file at {self.config_path}")

            if self._is_windows:
                # On Windows, use wireguard.exe /installtunnelservice
                tunnel_name = self.interface_name or "freedom-vpn"
                subprocess.run(
                    ["wireguard.exe", "/installtunnelservice", self.config_path],
                    check=True,
                    capture_output=True,
                    text=True,
                    shell=True
                )
                print(f"Successfully installed and started VPN tunnel: {tunnel_name}")
                # Don't cleanup on Windows - the service needs the file to stay
            else:
                # On Linux/Mac, use wg-quick
                wg_command = self._get_wireguard_command()
                subprocess.run(
                    [wg_command, "up", self.config_path],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print("Successfully connected to VPN")
                # Cleanup temp file after connection on Linux/Mac
                if not self.persist and self.config_path:
                    self._cleanup()

            return True

        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to connect WireGuard: {e.stderr if e.stderr else str(e)}"
            if not self._is_windows:
                self._cleanup()
            raise Exception(error_msg)

        except Exception as e:
            if not self._is_windows:
                self._cleanup()
            raise

    def disconnect(self, interface: Optional[str] = None) -> bool:
        try:
            if self._is_windows:
                # On Windows, the tunnel name is the config filename without .conf
                if interface:
                    tunnel_name = interface
                elif self.config_path:
                    # Extract tunnel name from config path (filename without .conf)
                    tunnel_name = os.path.splitext(os.path.basename(self.config_path))[0]
                else:
                    tunnel_name = self.interface_name or "freedom-vpn"
                
                # On Windows, use wireguard.exe /uninstalltunnelservice
                subprocess.run(
                    ["wireguard.exe", "/uninstalltunnelservice", tunnel_name],
                    check=True,
                    capture_output=True,
                    text=True,
                    shell=True
                )
                print(f"Successfully disconnected VPN tunnel: {tunnel_name}")
            else:
                # On Linux/Mac, use wg-quick
                wg_command = self._get_wireguard_command()
                
                if interface:
                    target = interface
                elif self.interface_name:
                    target = self.interface_name
                elif self.config_path:
                    target = self.config_path
                else:
                    raise Exception("No interface specified for disconnection")

                subprocess.run(
                    [wg_command, "down", target],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(f"Successfully disconnected from VPN")

            self._cleanup()

            return True

        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to disconnect: {e.stderr if e.stderr else str(e)}"
            raise Exception(error_msg)

    def _cleanup(self):
        if not self.persist and self.config_path and os.path.exists(self.config_path):
            try:
                os.remove(self.config_path)
                print(f"Cleaned up config file")
            except OSError:
                pass

    def get_status(self) -> dict:
        try:
            wg_command = "wg"
            result = subprocess.run(
                [wg_command, "show"],
                capture_output=True,
                text=True,
                check=True,
                shell=self._is_windows  # Use shell on Windows
            )
            return {
                "connected": bool(result.stdout.strip()),
                "details": result.stdout
            }
        except subprocess.CalledProcessError:
            return {
                "connected": False,
                "details": None
            }
