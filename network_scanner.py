# Network scanner
# Original component: Elizabeth Arellano
# Integration/compatibility updates: Valeria

import platform
import socket
import psutil
import subprocess
import ipaddress


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

    # User-friendly operating system name
    display_os = os_name

    if os_name == "Darwin":
        display_os = "macOS"

        mac_version = platform.mac_ver()[0]

        if mac_version:
            os_version = mac_version

    interfaces = psutil.net_if_addrs()
    interface_stats = psutil.net_if_stats()

    active_interfaces = []

    primary_interface = None
    local_ip = None
    subnet_mask = None
    connection_type = "Unknown"

    # =========================================================
    # macOS
    # =========================================================

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

                        primary_interface = (
                            line
                            .split(":", 1)[1]
                            .strip()
                        )

                        break

        except (
            FileNotFoundError,
            subprocess.SubprocessError
        ):
            primary_interface = None

        # Identify whether primary interface is Wi-Fi or Ethernet
        if primary_interface is not None:

            try:

                result = subprocess.run(
                    [
                        "networksetup",
                        "-listallhardwareports"
                    ],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:

                    hardware_port = None

                    for line in result.stdout.splitlines():

                        line = line.strip()

                        if line.startswith(
                            "Hardware Port:"
                        ):

                            hardware_port = (
                                line
                                .split(":", 1)[1]
                                .strip()
                            )

                        elif line.startswith(
                            "Device:"
                        ):

                            device = (
                                line
                                .split(":", 1)[1]
                                .strip()
                            )

                            if device == primary_interface:

                                if hardware_port == "Wi-Fi":

                                    connection_type = (
                                        "Wi-Fi"
                                    )

                                elif (
                                    hardware_port is not None
                                    and "Ethernet"
                                    in hardware_port
                                ):

                                    connection_type = (
                                        "Ethernet"
                                    )

                                break

            except (
                FileNotFoundError,
                subprocess.SubprocessError
            ):
                connection_type = "Unknown"

    # =========================================================
    # Windows
    # =========================================================

    elif os_name == "Windows":

        try:

            result = subprocess.run(
                ["route", "print", "-4"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:

                default_routes = []

                for line in result.stdout.splitlines():

                    columns = line.split()

                    if (
                        len(columns) == 5
                        and columns[0] == "0.0.0.0"
                        and columns[1] == "0.0.0.0"
                    ):

                        try:

                            route_ip = columns[3]
                            metric = int(
                                columns[4]
                            )

                            default_routes.append(
                                (
                                    metric,
                                    route_ip
                                )
                            )

                        except ValueError:
                            continue

                # Lowest metric is usually preferred route
                for metric, route_ip in sorted(
                    default_routes
                ):

                    for name, addresses in (
                        interfaces.items()
                    ):

                        for address in addresses:

                            if (
                                address.family
                                == socket.AF_INET
                                and address.address
                                == route_ip
                            ):

                                primary_interface = (
                                    name
                                )

                                local_ip = (
                                    address.address
                                )

                                subnet_mask = (
                                    address.netmask
                                )

                                break

                        if (
                            primary_interface
                            is not None
                        ):
                            break

                    if (
                        primary_interface
                        is not None
                    ):
                        break

        except (
            FileNotFoundError,
            subprocess.SubprocessError
        ):
            primary_interface = None

        if primary_interface is not None:

            name_lower = (
                primary_interface.lower()
            )

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

    # =========================================================
    # Linux / other operating systems
    # =========================================================

    else:

        for name, stats in interface_stats.items():

            if not stats.isup:
                continue

            if name in (
                "lo0",
                "lo"
            ):
                continue

            if name not in interfaces:
                continue

            for address in interfaces[name]:

                if (
                    address.family
                    == socket.AF_INET
                ):

                    try:

                        ip_object = (
                            ipaddress.ip_address(
                                address.address
                            )
                        )

                    except ValueError:
                        continue

                    if ip_object.is_loopback:
                        continue

                    primary_interface = name
                    local_ip = (
                        address.address
                    )
                    subnet_mask = (
                        address.netmask
                    )

                    name_lower = (
                        name.lower()
                    )

                    if (
                        "wi-fi" in name_lower
                        or "wifi" in name_lower
                        or "wireless" in name_lower
                        or "wlan" in name_lower
                    ):

                        connection_type = (
                            "Wi-Fi"
                        )

                    elif (
                        "ethernet" in name_lower
                        or name_lower.startswith(
                            "eth"
                        )
                    ):

                        connection_type = (
                            "Ethernet"
                        )

                    break

            if primary_interface is not None:
                break

    # =========================================================
    # Collect active IPv4 interfaces
    # =========================================================

    for name, stats in interface_stats.items():

        if not stats.isup:
            continue

        if name in (
            "lo0",
            "lo"
        ):
            continue

        if name not in interfaces:
            continue

        for address in interfaces[name]:

            if (
                address.family
                != socket.AF_INET
            ):
                continue

            try:

                ip_object = (
                    ipaddress.ip_address(
                        address.address
                    )
                )

            except ValueError:
                continue

            if ip_object.is_loopback:
                continue

            interface_info = {
                "name": name,
                "ip_address": address.address,
                "subnet_mask": address.netmask,
                "status": "up",
            }

            active_interfaces.append(
                interface_info
            )

            # Fill primary interface IP details
            if name == primary_interface:

                local_ip = (
                    address.address
                )

                subnet_mask = (
                    address.netmask
                )

    # =========================================================
    # Final fallback
    # =========================================================

    if (
        primary_interface is None
        and active_interfaces
    ):

        primary_interface = (
            active_interfaces[0]["name"]
        )

        local_ip = (
            active_interfaces[0][
                "ip_address"
            ]
        )

        subnet_mask = (
            active_interfaces[0][
                "subnet_mask"
            ]
        )

        name_lower = (
            primary_interface.lower()
        )

        if (
            "wi-fi" in name_lower
            or "wifi" in name_lower
            or "wireless" in name_lower
            or "wlan" in name_lower
        ):

            connection_type = "Wi-Fi"

        elif (
            "ethernet" in name_lower
            or name_lower.startswith("eth")
        ):

            connection_type = "Ethernet"

    # =========================================================
    # Return results
    # =========================================================

    return {
        "operating_system": display_os,
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
        f"{results['operating_system']} "
        f"{results['os_version']}"
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

    print(
        "\nActive IPv4 Interfaces:"
    )

    if not results[
        "active_interfaces"
    ]:

        print(
            "No active IPv4 interfaces found."
        )

    else:

        for interface in results[
            "active_interfaces"
        ]:

            print(
                f"- {interface['name']}: "
                f"{interface['ip_address']} "
                f"({interface['subnet_mask']})"
            )


if __name__ == "__main__":
    main()