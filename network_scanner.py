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
    # Check which operating system the user has
    if os_name == "Darwin":
        # Run the macOS command to get the default network route
        result = subprocess.run(["route", "-n", "get", "default"], capture_output=True, text=True)

    # If operating system is Windows, use Windows routing command
    elif os_name == "Windows":
        # Run Windows command to get IPv4 routing information
        result = subprocess.run(["route", "print", "-4"], capture_output=True, text=True)

        # Check if the Windows command ran successfully
        if result.returncode == 0:
            # Empty list to store default routes
            default_routes = []

            # Go through each line of the routing command's output
            for line in result.stdout.splitlines():
                # Split each line into separate columns
                columns = line.split()

                # Find default IPv4 Routes
                if len(columns) == 5 and columns[0] == "0.0.0.0" and columns[1] == "0.0.0.0":
                    # Try to get the route's IP address and metric
                    try:
                        # Get the local IP address used by the route
                        route_ip = columns[3]
                        # Convert the metric into an int
                        metric = int(columns[4])
                        # Add metric and IP address to the list
                        default_routes.append((metric, route_ip))

                    # Skip the route if the metric is not a valid number
                    except ValueError:
                        continue

            # Check routes starting with lowest metric
            for metric, route_ip in sorted(default_routes):
                # Find the interface that has the matching IP address
                # Loop through each interface and its addresses
                for name, addresses in interfaces.items():
                    # Loop through each address belonging to the interface
                    for address in addresses:
                        # Check if the IPv4 address matches the route's IP 
                        if address.family == socket.AF_INET and address.address == route_ip:
                            # Save matching interface name
                            primary_interface = name
                            break

                    # Stop checking interfaces once a match is found
                    if primary_interface is not None:
                        break

                # Stop checking routes once a match is found
                if primary_interface is not None:
                    break

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
        # Run macOS command to list network hardware ports and devices
        result = subprocess.run(["networksetup", "-listallhardwareports"], capture_output=True, text=True)

        # Check if the command ran successfully
        if result.returncode == 0:
            # Create a variable to store the hardware port type
            hardware_port = None
            # Go through each line of the command's output
            for line in result.stdout.splitlines():
                # Remove extra spaces from the beginning and end of the line
                line = line.strip()
                # Check if the line contains a hardware port
                if line.startswith("Hardware Port: "):
                    # Save the hardware port name
                    hardware_port = line.split(":", 1)[1].strip()

                # Check if the line contains a device name
                if line.startswith("Device:"):
                    # Save device name
                    device = line.split(":", 1)[1].strip()

                    # Check if the device matches the primary interface
                    if device == primary_interface:
                        # If the hardware port is Wi-Fi, save the connection type
                        if hardware_port == "Wi-Fi":
                            connection_type = "Wi-Fi"
                        # If the hardware port contains Ethernet, save the connection type
                        elif hardware_port is not None and "Ethernet" in hardware_port:
                            connection_type = "Ethernet"
                        break

    # Identify connection type on Windows
    elif os_name == "Windows" and primary_interface is not None:
        # Check if the interface name contains "wi-fi"
        if "wi-fi" in primary_interface.lower():
            connection_type = "Wi-Fi"

        # Check if the interface name contains "ethernet"
        elif "ethernet" in primary_interface.lower():
            connection_type = "Ethernet"

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