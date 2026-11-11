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

    # Get primary network interface from the macOS routing table
    result = subprocess.run(["route", "-n", "get", "default"], capture_output=True, text=True)

    # Find the interface used for the default route
    # .returncode - attribute provided by the subprocess result object (exit status)
    if result.returncode == 0:
        # Go through every line of text returned by the terminal command
        for line in result.stdout.splitlines():
            # After removing extra spaces, does this line start with interface?
            if line.strip().startswith("interface:"):
                # Take text after :, remove any extra spaces, save in primary_interface
                primary_interface = line.split(":", 1)[1].strip()
                break

    # Identify whether the primary interface uses Wi-Fi or Ethernet
    if os_name == "Darwin" and primary_interface is not None:
        result = subprocess.run(["networksetup", "-listallhardwareports"], capture_output=True, text=True)

        if result.returncode == 0:
            hardware_port = None
            for line in result.stdout.splitlines():
                line = line.strip()
                if line.startswith("Hardware Port: "):
                    hardware_port = line.split(":", 1)[1].strip()

                if line.startswith("Device:"):
                    device = line.split(":", 1)[1].strip()

                    if device == primary_interface:
                        if hardware_port == "Wi-Fi":
                            connection_type = "Wi-Fi"
                        elif hardware_port is not None and "Ethernet" in hardware_port:
                            connection_type = "Ethernet"
                        break

    # Find active interfaces that have IPv4 addresses
    for name, stats in interface_stats.items():

        if not stats.isup:
            continue

        if name in ("lo0", "lo"):
            continue

        if name not in interfaces:
            continue

        for address in interfaces[name]:

            if address.family == socket.AF_INET:

                interface_info = {
                    "name": name,
                    "ip_address": address.address,
                    "subnet_mask": address.netmask,
                    "status": "up",
                }

                active_interfaces.append(interface_info)

                # Get the IP address and subnet mask of the primary interface
                if name == primary_interface:
                    # Only save the IP address and subnet mask if they belong to that specific interface
                    local_ip = address.address
                    subnet_mask = address.netmask

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