#Streamlit frontend
#Original component: Alina
#Integration/compatibility updates: Valeria

import streamlit as st
import time

from main import run_website_scan, run_network_scan
from report_generator import generate_report, ISSUE_NAMES


st.title("Cybersecurity Vulnerability & Network Safety Scanner")
st.write("SLP cybersecurity team #1 :))")
# =========================================================
# WEBSITE SECURITY SCANNER
# =========================================================

st.header("Website Security Scanner")

website_url = st.text_input(
    "Enter a website URL:",
    placeholder="https://example.com"
)

st.write("You entered:", website_url)


if st.button("Scan Website"):

    if website_url.strip() == "":
        st.warning("Please enter a valid URL before scanning.")

    else:

        with st.spinner("Checking whether the website is secure..."):

            # real backend results
            results = run_website_scan(website_url)

            time.sleep(0.5)

        # if website scanner failed
        if "error" in results:

            st.error("Website scan failed.")

            st.write(
                results.get(
                    "message",
                    "Please check the URL and try again."
                )
            )

        else:

            st.success("Website scan successful.")

            security_score = results.get("score", 0)
            risk_level = results.get("risk_level", "Unknown")

            # progress bar
            progress_bar = st.progress(0)

            for number in range(security_score + 1):
                progress_bar.progress(number)

            st.subheader("Security Results")

            st.write(
                f"Security Score: **{security_score}/100**"
            )

            st.write(
                f"Risk Level: **{risk_level.capitalize()}**"
            )

            st.write(
                f"HTTPS Supported: **{results.get('uses_https')}**"
            )

            st.write(
                f"HTTP → HTTPS Redirect: "
                f"**{results.get('redirects_to_https')}**"
            )

            # findings / issues
            st.subheader("Findings")

            issues = results.get("issues", [])

            if not issues:
                st.success("No security issues were found.")

            else:

                for item in issues:

                    issue_name = ISSUE_NAMES.get(
                        item["issue"],
                        item["issue"].replace("_", " ").title()
                    )

                    with st.expander(issue_name):

                        st.write(
                            f"Severity: "
                            f"**{item['severity'].capitalize()}**"
                        )

                        st.write(
                            f"Recommendation: "
                            f"{item['recommendation']}"
                        )

            # security report
            st.subheader("Security Report")

            report = generate_report(results)

            st.code(
                report,
                language=None
            )

            st.download_button(
                label="Download Security Report",
                data=report,
                file_name="security_report.txt",
                mime="text/plain"
            )


# =========================================================
# NETWORK SECURITY SCANNER
# =========================================================

st.header("Network Security Scanner")


if st.button("Check Network"):

    with st.spinner("Checking your network..."):

        network_results = run_network_scan()

        time.sleep(0.5)

    st.success("Network check completed.")

    network = network_results["network_info"]
    firewall = network_results["firewall"]

    st.subheader("Network Results")

    st.write(
        f"Operating System: "
        f"**{network['operating_system']} "
        f"{network['os_version']}**"
    )

    st.write(
        f"Primary Interface: "
        f"**{network['primary_interface']}**"
    )

    st.write(
        f"Local IP: "
        f"**{network['local_ip']}**"
    )

    st.write(
        f"Subnet Mask: "
        f"**{network['subnet_mask']}**"
    )

    st.subheader("Firewall Check")

    if firewall["supported"]:

        if firewall["firewall_enabled"]:

            st.success(
                "Firewall is enabled."
            )

        else:

            st.warning(
                "Firewall is disabled for at least "
                "one network profile."
            )

    else:

        st.info(
            firewall["message"]
        )