# Network scanner
# Original component: Elizabeth Arellano
# Integration/compatibility updates: Valeria

import platform
import socket
import psutil

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

                # Use the first non-loopback IPv4 interface
                # as the primary interface for now
                if primary_interface is None:
                    primary_interface = name
                    local_ip = address.address
                    subnet_mask = address.netmask

    return {
        "operating_system": os_name,
        "os_version": os_version,
        "primary_interface": primary_interface,
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