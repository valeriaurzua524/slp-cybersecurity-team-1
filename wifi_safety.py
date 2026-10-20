# checks whether the device's built-in firewall is turned on.
# currently tested on: windows 11 pro
    # other systems will return "not supported"

import platform
import subprocess

def check_firewall_status():

    # only supports windows
    if platform.system() != "Windows":
        return {
            "firewall_enabled": None,
            "message": "currently, firewall check only supports Windows."
        }

    # may fail
    try: 
        result = subprocess.run(
            ["netsh", "advfirewall", "show", "allprofiles", "state"],
            capture_output = True,
            text = True,
            timeout = 10,   # give up after ten seconds
        )
    except Exception:
        return {
            "firewall_enabled": None,
            "message": "could not run the firewall command.",
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
            "firewall_enabled": None,
            "message": "could not read the firewall status."
        }

    # true only if every profile is ON
    firewall_enabled = all(state == "ON" for state in states)

    if firewall_enabled:
        message = "firewall is on."
    else:
        message = "firewall is off for at least one network type. turn it on, especially on public wi-fi."
    return {"firewall_enabled": firewall_enabled, "message": message}

# only runs when this file is executed directly
# run "python wifi_safety.py" 
if __name__ == "__main__":
    result = check_firewall_status()
    print("--- firewall check ---")
    print(f"firewall enabled: {result['firewall_enabled']}")
    print(f"message: {result['message']}")