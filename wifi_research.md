Main focus: figuring out what makes a Wi-Fi connection safer or riskier and which checks are realistic for our final project 

Your deliverable: Research the Wi-Fi/public-network side of the project and figure out which checks we can realistically 
support.

    Please research things like: 
        ● how to determine the current SSID 
        ● whether the Wi-Fi is open or secured 
        ● Wi-Fi encryption/security type 
        ● connection type 
        ● local/default gateway 
        ● which Wi-Fi/security checks work on macOS vs. Windows 
        ● whether any checks need extra permissions 


SSID - service set identifier, public name of the wifi network youre currently connected to. check the wifi connection for name, if any.

open wifi doesnt need a password, while secured network does, usually displaying a lock icon. secured wifi networks use encryption. checking the encryption type is in the "network properties" of your device. 

wired equivalency protocol (WEP): original wireless standard with many vulnerabilities --> wifi protected access (WPA) built on and addressed WEP security flaws. WPA2 is faster and more secured (still widely used even after the release of WPA3).

encryption happens at many layers, not only wifi networks, as a baseline for all client devices.

unsecured wireless networks create risks with the possiblity of being compromised by threat actors trying to steal data (intercepting radio waves with wifi traffic). they can also be a vulnerability point to gain access to broader enterprise networks. viruses, ransomware or other malware can be spread to devices connected.

types of connection include:
    - wireless local area networks (WLAN): uses a wireless router to connect to a wired internet and broadcast radio signals for a room or building.
    - wireless metropolitan area network (WMAN): larger area covered than WLAN.
    - wireless personal area network (WPAN) - bluetooth: covers about 10 meters, mostly for individual devices of the user (keyboard, phone, headphones).
    - wireless WAN (WWAN) - wireless data: large geographic reach using cell towers (4G LTE and 5G).
    - mobile/portable hotspot: shares cellular data connection (5G) from a phone for a temporary wifi network for other devices.

local/default gateway is the main exit point for traffic destined for remote networks. allows for local networks to access the internet. it is a router or network device that serves as an access point to other networks. has a unique IP address reachable by all devices on the local network. functions as the "next-hop" for all non-local traffic when they cannot deliver directly to its destination.
    begins with device configuration and reaches successful packet delivery to remote networks.

wifi security checks on:
    - windows --> quick protocol checks (WPA2/WPA3), MAC address randomization (to prevent tracking on public networks), local firewalls
    - mac --> native packet capture (sniffing, monitor mode), passive signal/channel scanning (scan tool), in addition to what windows provides

extra permissions:
    - windows --> location to find SSID, advanced security and packet checks requires running the device as admin
    - mac --> locations, advanced security and packet checks requires sudo



3–5 Wi-Fi safety/security checks that seem realistic for our final scanner. 
    For each one, write: 
        ● what the check is 
        ● why it matters 
        ● whether it seems realistic for us to implement 
        ● whether it works differently on Mac vs. Windows


1. open or secure network
● what the check is: check security of a wifi connection - ensure there is the lock icon for a password and encryption.
● why it matters: unsecured wireless networks create risks with the possiblity of being compromised by threat actors trying to steal data (intercepting radio waves with wifi traffic).
● whether it seems realistic for us to implement: it doesnt seem difficult to implement but may require permission from the user to look into their device and see possible network connections.
● whether it works differently on Mac vs. Windows: different commands.

2. encryption/security type
● what the check is: check and rate which security protocol is used by the network.
● why it matters: older security types have many vulnerabilities that newer ones address.
● whether it seems realistic for us to implement: yes, build off the first check.
● whether it works differently on Mac vs. Windows: different commands.

3. firewall status
● what the check is: check if the device's built-in firewall is turned on.
● why it matters: it can block unwanted connections from a shared network.
● whether it seems realistic for us to implement: yes, reading the status doesn't need admin rights.
● whether it works differently on Mac vs. Windows: different commands.

