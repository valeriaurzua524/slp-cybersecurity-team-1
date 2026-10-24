from website_scanner import website_scanner
from recommendations import recommendations
from report_generator import generate_report, save_report
from network_scanner import get_network_info
from wifi_safety import check_firewall_status


def run_website_scan(url):
    """
    Runs the complete website security pipeline.
    """

    scan_results = website_scanner(url)

    final_results = recommendations(scan_results)

    return final_results


def run_network_scan():
    """
    Runs the local network + firewall checks.
    """

    network_info = get_network_info()
    firewall_info = check_firewall_status()

    return {
        "network_info": network_info,
        "firewall": firewall_info,
    }


def main():
    while True:
        print("\nCYBERSECURITY VULNERABILITY & NETWORK SAFETY SCANNER")
        print("---------------------------------------------------")
        print("1. Scan Website")
        print("2. Check Network")
        print("3. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":

            url = input("\nEnter a website to scan: ")

            results = run_website_scan(url)

            print("\nFINAL WEBSITE RESULTS:")
            print(results)

            report = generate_report(results)

            print("\n")
            print(report)

            save_report(report)

        elif choice == "2":

            results = run_network_scan()

            print("\nNETWORK RESULTS")
            print("---------------")

            network = results["network_info"]
            firewall = results["firewall"]

            print(
                f"Operating System: "
                f"{network['operating_system']} "
                f"{network['os_version']}"
            )

            print(
                f"Primary Interface: "
                f"{network['primary_interface']}"
            )

            print(
                f"Local IP: "
                f"{network['local_ip']}"
            )

            print(
                f"Subnet Mask: "
                f"{network['subnet_mask']}"
            )

            print("\nFirewall Check:")

            print(
                f"Supported: "
                f"{firewall['supported']}"
            )

            print(
                f"Firewall Enabled: "
                f"{firewall['firewall_enabled']}"
            )

            print(
                f"Message: "
                f"{firewall['message']}"
            )

        elif choice == "3":
            print("\nExiting scanner.")
            break

        else:
            print("\nInvalid option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()