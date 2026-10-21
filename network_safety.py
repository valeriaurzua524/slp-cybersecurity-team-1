# Network Safety 
# Author: Elizabeth Arellano

import platform
import socket
import psutil

# Function to get the user's network information
def get_network_info():

    # User's Operating System - System() gives the Operating System and Release() gives the Version Number
    os_name = platform.system()
    os_version = platform.release()

    # Dictionary to store the user's network information
    network_info = {
        "operating_system": os_name,
        "os_version": os_version,
        "local_ip": None,
        "subnet_mask": None,
        "active_interfaces": []
    }

    # User's Local IP Address

    # Get all network interfaces and their assigned addresses
    interfaces = psutil.net_if_addrs()

    # Get the status info for all network interfaces
    activeInterfaces = psutil.net_if_stats()

    # Loop through each interface name and its list of addresses
    for name, addresses in interfaces.items():
        # Loop through each address belonging to the current interface
        for address in addresses:
            # Check if the address is IPv4 and exclude the loopback interface (lo0)
            if address.family == socket.AF_INET and name != "lo0":
                print("Interface Name: ", name)
                print("Local IP Address: ", address.address)
                network_info["local_ip"] = address.address

    # Basic Interface Information

    # Loop through each network interface and its status information
    for name, stats in activeInterfaces.items():
        # Check if the interface is up and is not the loopback interface
        if stats.isup and name != "lo0":
            # Check if the interface exists in the address dictionary
            if name in interfaces:
                # Loop through the addresses belonging to that specific interface
                for address in interfaces[name]:
                    # Check if the current address is an IPv4 address
                    if address.family == socket.AF_INET:
                        print("Subnet Mask: ", address.netmask)
                        print()
                        network_info["subnet_mask"] = address.netmask

    # Active Interfaces:
    # User's Active Network Interfaces

    print("========== List of Active Interfaces ==========")
    # Loop through each network interface and its status info
    for name, stats in activeInterfaces.items():
        # Check if the interface is up and exclude the loopback interface
        if stats.isup and name != "lo0":

            # Check if the interface exists in the address dictionary
            if name in interfaces:

                # Loop through the addresses belonging to the interface
                for address in interfaces[name]:

                    # Only display interfaces that have an IPv4 address
                    if address.family == socket.AF_INET:
                        print("Active Interface: ", name)
                        print("Status: Up")
                        print()
                        network_info["active_interfaces"].append(name)

    # Return the collected information
    return network_info


# Call the function
results = get_network_info()

# Display operating system information
print("Operating System & Version: ", results["operating_system"], results["os_version"])
