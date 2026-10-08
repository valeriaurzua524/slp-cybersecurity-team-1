# Network Safety 
# Author: Elizabeth Arellano

import platform
import socket
import psutil

# User's Operating System - System() gives the Operating System and Release() gives the Version Number
print("Operating System & Version: ", platform.system(), platform.release())
print()

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
                    print("IPv4 Address: ", address.address)
                    print("Subnet Mask: ", address.netmask)
                    print()

# Active Interfaces:
# User's Active Network Interfaces

print("========== List of Active Interfaces ==========")
# Loop through each network interface and its status info
for name, stats in activeInterfaces.items():
    # Check if the interface is up and exclude the loopback interface
    if stats.isup and name != "lo0":
        print("Active Interface: ", name)
        print("Status: Up")
        print()
