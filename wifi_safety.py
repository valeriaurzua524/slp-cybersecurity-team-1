# checks whether the device's built-in firewall is turned on.
# currently tested on: windows 11 pro
# other systems will return "not supported"

# Original component: Ayla
# Integration/compatibility updates: Valeria

import platform
import subprocess


def check_firewall_status():

    operating_system = platform.system()

    # only supports windows
    if operating_system != "Windows":
        return {
            "operating_system": operating_system,
            "supported": False,
            "firewall_enabled": None,
            "message": "currently, firewall check only supports Windows."
        }

    # may fail
    try:
        result = subprocess.run(
            ["netsh", "advfirewall", "show", "allprofiles", "state"],
            capture_output=True,
            text=True,
            timeout=10,
        )

    except Exception:
        return {
            "operating_system": operating_system,
            "supported": True,
            "firewall_enabled": None,
            "message": "could not run the firewall command."
        }

    # collect ON/OFF value from each state line
    states = []

    for line in result.stdout.splitlines():
        line = line.strip()

        if line.startswith("State"):
            states.append(line.split()[-1])

    # if no state lines were found
    if len(states) == 0:
        return {
            "operating_system": operating_system,
            "supported": True,
            "firewall_enabled": None,
            "message": "could not read the firewall status."
        }

    # true only if every profile is ON
    firewall_enabled = all(
        state == "ON"
        for state in states
    )

    if firewall_enabled:
        message = "firewall is on."
    else:
        message = (
            "firewall is off for at least one network type. "
            "turn it on, especially on public wi-fi."
        )

    return {
        "operating_system": operating_system,
        "supported": True,
        "firewall_enabled": firewall_enabled,
        "message": message
    }


# only runs when this file is executed directly
# run "python3 wifi_safety.py"
if __name__ == "__main__":

    result = check_firewall_status()

    print("--- firewall check ---")
    print(f"operating system: {result['operating_system']}")
    print(f"supported: {result['supported']}")
    print(f"firewall enabled: {result['firewall_enabled']}")
    print(f"message: {result['message']}")