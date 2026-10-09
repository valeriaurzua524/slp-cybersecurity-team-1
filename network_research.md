Network Security / Device Exposure Research
Purpose: Short Research File with 3 - 5 Realistic Device/Network Exposure Checks that could be added to future versions of the Network Security Scanner.

1. Connection Type
Connection type is an important part to check because it helps users understand how their device is connected to a network and what security risks may apply to that connection. If our program identifies the user's connection type, it can provide recommendations specific to that connection.

Examples:
- Wi-Fi: Wireless connections can introduce risks such as connecting to fake Wi-Fi hotspots, using weak encryption, or joining untrusted public networks.
- Ethernet: Wired connections generally require physical access to the network, reducing some wireless-specific risks, although the network itself can still be unsafe. 

Possible implementation: Use Python's psutil to identify network interfaces and operating-system-specific tools to determine the connection type.

2. Default Gateway
Default gateway would be an important thing to add because it helps identify the router or network device your computer uses to communicate with networks outside its local network, including the internet.

Examples:
- Connecting to Public Wi-Fi. Your scanner could display the gateway so users understand which network device handles their traffic. 
- Unexpected Gateway Change. Your scanner could notice the gateway changing and recommend investigating

Possible Implementation: Use Python's subprocess module to read routing information through OS commands, such as route on macOS.

3. Listening Ports and Services
Listening ports and services would be important to add because they help identify which applications or services on the user's device are waiting for incoming network connections. Some services may create security risks if they are unnecessarily exposed to other devices or networks.

Examples:
- Unnecessary Open Ports. Your scanner could identify listening ports that users may not need and recommend reviewing or disabling the associated services.
- Exposed Services. Your scanner could detect services such as SSH or file sharing that may be accessible to other devices and recommend restricting access if necessary.

Possible Implementation: Use Python's psutil.net_connections() to identify listening ports and their associated services on the user's device. Additional checks may be needed to determine whether those services are actually accessible from the network.

4. Private vs. Public Local Address
Checking whether an IP address is private or public would be important because it helps users understand how their device is addressed on a network and whether its IP address is potentially reachable from outside the local network.

Examples:
- Private IP Address. Your scanner could identify private IP addresses and explain that these are commonly used within home, school, or workplace networks.
- Public IP Address. Your scanner could identify a globally routable IP address assigned to a device and recommend reviewing its network exposure and firewall settings.

Possible Implementation: Use Python's built-in ipaddress module to classify IP addresses and determine whether they belong to private, globally routable, loopback, or other special-purpose ranges.

5. Host Firewall Status
Checking the host firewall status would be important because firewalls help protect devices by controlling network traffic based on security rules. Knowing whether the firewall is enabled can help users identify potentially unsafe device configurations, especially when connected to public or untrusted networks.

Examples:
- Firewall Disabled. Your scanner could detect when the device's firewall is turned off and recommend enabling it when appropriate to help protect against unwanted incoming connections.
- Firewall Enabled. Your scanner could confirm that the firewall is enabled and inform users that their device has an additional layer of network protection, while noting that firewall settings still matter.

Possible Implementation: Use Python's subprocess module to run operating-system-specific commands that check firewall status.