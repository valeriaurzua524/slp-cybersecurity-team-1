#Streamlit frontend
#Original component: Alina
#Integration/compatibility updates: Valeria

import streamlit as st
import time
import pandas as pd

from main import run_website_scan, run_network_scan
from report_generator import generate_report, ISSUE_NAMES

st.set_page_config(
    page_title="Cybersecurity Vulnerability & Network Safety Scanner",
    page_icon="cyber_team_logo.png",
    layout="wide"
)

if "page" not in st.session_state:
    st.session_state.page = "home"

with st.sidebar:

    st.image("cyber_team_logo.png", width=80)

    if st.session_state.page != "home":
        if st.button("← Back to Home", key="back_home"):
            st.session_state.page = "home"
            st.rerun()

    with st.container(border=True):
        st.subheader("About This Scanner")
        st.write(
            "This tool checks websites and local networks "
            "for common cybersecurity risks."
        )

    with st.container(border=True):
        st.subheader("How It Works")
        st.write(
            "Choose a scanner, run the scan, and review "
            "the security results."
        )

if st.session_state.page == "home":

    st.title("Cybersecurity Vulnerability & Network Safety Scanner")
    st.subheader("SLP Cybersecurity team #1 ")
    st.subheader("Choose a scanner")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("🌐 Website Security Scanner")
            st.write("Check a website for common security vulnerabilities.")

            if st.button("Open Website Scanner", key="home_website"):
                st.session_state.page = "website"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.subheader("📡 Network Scanner")
            st.write("Check your local network and firewall settings.")

            if st.button("Open Network Scanner", key="home_network"):
                st.session_state.page = "network"
                st.rerun()

elif st.session_state.page == "website":
    st.title("Website Security Scanner")

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

elif st.session_state.page == "network":
    st.title("Network Security Scanner")


    if st.button("Check Network"):

        with st.spinner("Checking your network..."):

                network_results = run_network_scan()

                time.sleep(0.5)

        with st.container(border=True):
            st.success("✅ Network check completed ✅")

        network = network_results["network_info"]
        firewall = network_results["firewall"]

        st.subheader("Network Results")
        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                icon_col, text_col = st.columns([1, 3])

                with icon_col:
                    st.subheader("💻")

                with text_col:
                    st.caption("Operating System")
                    st.subheader(network["operating_system"])

        with col2:
            with st.container(border=True):
                icon_col, text_col = st.columns([1, 3])

                with icon_col:
                    st.subheader("📡")

                with text_col:
                    st.caption("Primary Interface")
                    st.subheader(network["primary_interface"])

        with col3:
            with st.container(border=True):
                icon_col, text_col = st.columns([1, 3])

                with icon_col:
                    st.subheader("📍")

                with text_col:
                    st.caption("Local IP")
                    st.subheader(network["local_ip"])

        network_table = pd.DataFrame(
            [
                ["Operating System", f"{network['operating_system']} {network['os_version']}"],
                ["Primary Interface", network["primary_interface"]],
                ["Local IP", network["local_ip"]],
                ["Subnet Mask", network["subnet_mask"]],
            ],
            columns=["Field", "Value"]
        )

        styled_table = (
            network_table.style
            .hide(axis="index")
            .set_properties(
                **{
                    "font-size": "18px",
                    "padding": "12px",
                    "border": "1px solid #d6dfed",
                }
            )
            .set_table_styles(
                [
                    {
                        "selector": "th",
                        "props": [("display", "none")]
                    },
                    {
                        "selector": "td:first-child",
                        "props": [
                            ("font-weight", "bold"),
                            ("background-color", ""),
                            ("width", "30%"),
                        ],
                    },
                    {
                        "selector": "table",
                        "props": [
                            ("border-collapse", "collapse"),
                            ("width", "100%"),
                        ],
                    },
                ]
            )
        )

        st.table(styled_table)

        st.subheader("Firewall Check")

        if firewall["supported"]:

            if firewall["firewall_enabled"]:
                st.success("✅ Firewall is enabled.")

            else:
                st.warning("⚠️ Firewall is disabled.")

        else:
            st.info(firewall["message"])
