# Network scanner
# Original component: Elizabeth Arellano
# Integration/compatibility updates: Valeria

import platform
import socket
import psutil
import subprocess


def get_network_info():
    """
    Collects basic network information from the user's device.

    Returns a dictionary with:
    - operating system
    - OS version
    - primary local IPv4 address
    - subnet mask
    - primary interface
    - connection type
    - active IPv4 interfaces
    """

    os_name = platform.system()
    os_version = platform.release()

    interfaces = psutil.net_if_addrs()
    interface_stats = psutil.net_if_stats()

    active_interfaces = []

    primary_interface = None
    local_ip = None
    subnet_mask = None
    connection_type = "Unknown"

    # -------------------------------------------------
    # macOS primary interface + connection type detection
    # -------------------------------------------------
    if os_name == "Darwin":

        try:
            # Find the interface used for the default route
            result = subprocess.run(
                ["route", "-n", "get", "default"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if line.strip().startswith("interface:"):
                        primary_interface = line.split(":", 1)[1].strip()
                        break

        except Exception:
            primary_interface = None

        # Identify whether the primary interface uses Wi-Fi or Ethernet
        if primary_interface is not None:

            try:
                result = subprocess.run(
                    ["networksetup", "-listallhardwareports"],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    hardware_port = None

                    for line in result.stdout.splitlines():
                        line = line.strip()

                        if line.startswith("Hardware Port:"):
                            hardware_port = line.split(":", 1)[1].strip()

                        elif line.startswith("Device:"):
                            device = line.split(":", 1)[1].strip()

                            if device == primary_interface:

                                if hardware_port == "Wi-Fi":
                                    connection_type = "Wi-Fi"

                                elif (
                                    hardware_port is not None
                                    and "Ethernet" in hardware_port
                                ):
                                    connection_type = "Ethernet"

                                break

            except Exception:
                connection_type = "Unknown"

    # -------------------------------------------------
    # Cross-platform fallback
    # Windows / Linux / other operating systems
    # -------------------------------------------------
    else:

        for name, stats in interface_stats.items():

            if not stats.isup:
                continue

            if name in ("lo0", "lo"):
                continue

            if name not in interfaces:
                continue

            for address in interfaces[name]:

                if address.family == socket.AF_INET:

                    if not address.address.startswith("127."):

                        primary_interface = name
                        local_ip = address.address
                        subnet_mask = address.netmask

                        # Try to identify connection type from interface name
                        name_lower = name.lower()

                        if (
                            "wi-fi" in name_lower
                            or "wifi" in name_lower
                            or "wireless" in name_lower
                            or "wlan" in name_lower
                        ):
                            connection_type = "Wi-Fi"

                        elif (
                            "ethernet" in name_lower
                            or "eth" in name_lower
                            or "en" in name_lower
                        ):
                            connection_type = "Ethernet"

                        break

            if primary_interface is not None:
                break

    # -------------------------------------------------
    # Collect all active IPv4 interfaces
    # -------------------------------------------------
    for name, stats in interface_stats.items():

        if not stats.isup:
            continue

        if name in ("lo0", "lo"):
            continue

        if name not in interfaces:
            continue

        for address in interfaces[name]:

            if address.family == socket.AF_INET:

                if address.address.startswith("127."):
                    continue

                interface_info = {
                    "name": name,
                    "ip_address": address.address,
                    "subnet_mask": address.netmask,
                    "status": "up",
                }

                active_interfaces.append(interface_info)

                # On macOS, fill IP information for the detected
                # primary interface
                if (
                    os_name == "Darwin"
                    and name == primary_interface
                ):
                    local_ip = address.address
                    subnet_mask = address.netmask

    # -------------------------------------------------
    # Final fallback in case primary interface was
    # not detected by the earlier logic
    # -------------------------------------------------
    if primary_interface is None and active_interfaces:

        primary_interface = active_interfaces[0]["name"]
        local_ip = active_interfaces[0]["ip_address"]
        subnet_mask = active_interfaces[0]["subnet_mask"]

        name_lower = primary_interface.lower()

        if (
            "wi-fi" in name_lower
            or "wifi" in name_lower
            or "wireless" in name_lower
            or "wlan" in name_lower
        ):
            connection_type = "Wi-Fi"

        elif (
            "ethernet" in name_lower
            or "eth" in name_lower
        ):
            connection_type = "Ethernet"

    return {
        "operating_system": os_name,
        "os_version": os_version,
        "primary_interface": primary_interface,
        "connection_type": connection_type,
        "local_ip": local_ip,
        "subnet_mask": subnet_mask,
        "active_interfaces": active_interfaces,
    }


def main():
    """
    Used only for testing this file by itself.
    """

    results = get_network_info()

    print("\nNETWORK INFORMATION")
    print("-------------------")

    print(
        f"Operating System: "
        f"{results['operating_system']} {results['os_version']}"
    )

    print(
        f"Primary Interface: "
        f"{results['primary_interface']}"
    )

    print(
        f"Connection Type: "
        f"{results['connection_type']}"
    )

    print(
        f"Local IP: "
        f"{results['local_ip']}"
    )

    print(
        f"Subnet Mask: "
        f"{results['subnet_mask']}"
    )

    print("\nActive IPv4 Interfaces:")

    if not results["active_interfaces"]:
        print("No active IPv4 interfaces found.")

    else:
        for interface in results["active_interfaces"]:
            print(
                f"- {interface['name']}: "
                f"{interface['ip_address']} "
                f"({interface['subnet_mask']})"
            )


if __name__ == "__main__":
    main()