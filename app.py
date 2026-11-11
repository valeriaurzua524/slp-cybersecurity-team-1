# Streamlit frontend
# Original component: Alina
# Integration/compatibility updates: Valeria

import streamlit as st
import time
import pandas as pd

from main import run_website_scan, run_network_scan
from report_generator import generate_report, ISSUE_NAMES


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Cybersecurity Vulnerability & Network Safety Scanner",
    page_icon="cyber_team_logo.png",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"


# =========================================================
# SIDEBAR
# =========================================================

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


# =========================================================
# HOME PAGE
# =========================================================

if st.session_state.page == "home":

    st.title("Cybersecurity Vulnerability & Network Safety Scanner")
    st.subheader("SLP Cybersecurity Team #1")
    st.write(
        "Choose a scanner below to check website or network security."
    )

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("🌐 Website Security Scanner")

            st.write(
                "Check a website for common security vulnerabilities "
                "and missing security protections."
            )

            if st.button(
                "Open Website Scanner",
                key="home_website"
            ):
                st.session_state.page = "website"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.subheader("📡 Network Security Scanner")

            st.write(
                "Check your local network information "
                "and firewall status."
            )

            if st.button(
                "Open Network Scanner",
                key="home_network"
            ):
                st.session_state.page = "network"
                st.rerun()


# =========================================================
# WEBSITE SECURITY SCANNER
# =========================================================

elif st.session_state.page == "website":

    st.title("Website Security Scanner")

    st.write(
        "Enter a website URL to check HTTPS, redirects, "
        "security headers, risk level, and recommendations."
    )

    website_url = st.text_input(
        "Enter a website URL:",
        placeholder="https://example.com"
    )

    if website_url:
        st.caption(f"You entered: {website_url}")

    if st.button("Scan Website"):

        if website_url.strip() == "":

            st.warning(
                "Please enter a valid URL before scanning."
            )

        else:

            with st.spinner(
                "Checking whether the website is secure..."
            ):

                results = run_website_scan(
                    website_url
                )

                time.sleep(0.5)

            # -------------------------------------------------
            # Scan failed
            # -------------------------------------------------

            if "error" in results:

                st.error(
                    "Website scan failed."
                )

                st.write(
                    results.get(
                        "message",
                        "Please check the URL and try again."
                    )
                )

            # -------------------------------------------------
            # Scan successful
            # -------------------------------------------------

            else:

                st.success(
                    "Website scan successful."
                )

                security_score = results.get(
                    "score",
                    0
                )

                risk_level = results.get(
                    "risk_level",
                    "Unknown"
                )

                # progress bar
                progress_bar = st.progress(0)

                for number in range(
                    security_score + 1
                ):
                    progress_bar.progress(
                        number
                    )

                # -------------------------------------------------
                # Security summary
                # -------------------------------------------------

                st.subheader(
                    "Security Results"
                )

                result_col1, result_col2 = st.columns(2)

                with result_col1:

                    with st.container(border=True):

                        st.metric(
                            "Security Score",
                            f"{security_score}/100"
                        )

                with result_col2:

                    with st.container(border=True):

                        st.metric(
                            "Risk Level",
                            risk_level.capitalize()
                        )

                st.write(
                    f"HTTPS Supported: "
                    f"**{results.get('uses_https')}**"
                )

                st.write(
                    f"HTTP → HTTPS Redirect: "
                    f"**{results.get('redirects_to_https')}**"
                )

                # -------------------------------------------------
                # Findings
                # -------------------------------------------------

                st.subheader(
                    "Findings"
                )

                issues = results.get(
                    "issues",
                    []
                )

                if not issues:

                    st.success(
                        "No security issues were found."
                    )

                else:

                    for item in issues:

                        issue_name = ISSUE_NAMES.get(
                            item["issue"],
                            item["issue"]
                            .replace("_", " ")
                            .title()
                        )

                        with st.expander(
                            issue_name
                        ):

                            st.write(
                                f"Severity: "
                                f"**{item['severity'].capitalize()}**"
                            )

                            st.write(
                                f"Recommendation: "
                                f"{item['recommendation']}"
                            )

                # -------------------------------------------------
                # Security report
                # -------------------------------------------------

                st.subheader(
                    "Security Report"
                )

                report = generate_report(
                    results
                )

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

elif st.session_state.page == "network":

    st.title(
        "Network Security Scanner"
    )

    st.write(
        "Check your device and local network information, "
        "including connection type and firewall status."
    )

    if st.button(
        "Check Network"
    ):

        with st.spinner(
            "Checking your network..."
        ):

            network_results = run_network_scan()

            time.sleep(0.5)

        st.success(
            "✅ Network check completed."
        )

        network = network_results[
            "network_info"
        ]

        firewall = network_results[
            "firewall"
        ]

        # -------------------------------------------------
        # Network summary cards
        # -------------------------------------------------

        st.subheader(
            "Network Results"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            with st.container(
                border=True
            ):

                st.subheader(
                    "💻"
                )

                st.caption(
                    "Operating System"
                )

                st.subheader(
                    network.get(
                        "operating_system",
                        "Unknown"
                    )
                )

        with col2:

            with st.container(
                border=True
            ):

                st.subheader(
                    "📡"
                )

                st.caption(
                    "Connection Type"
                )

                st.subheader(
                    network.get(
                        "connection_type",
                        "Unknown"
                    )
                )

        with col3:

            with st.container(
                border=True
            ):

                st.subheader(
                    "📍"
                )

                st.caption(
                    "Local IP"
                )

                st.subheader(
                    network.get(
                        "local_ip",
                        "Unknown"
                    )
                )

        # -------------------------------------------------
        # Network details table
        # -------------------------------------------------

        network_table = pd.DataFrame(
            [
                [
                    "Operating System",
                    (
                        f"{network.get('operating_system', 'Unknown')} "
                        f"{network.get('os_version', '')}"
                    ).strip()
                ],
                [
                    "Primary Interface",
                    network.get(
                        "primary_interface",
                        "Unknown"
                    )
                ],
                [
                    "Connection Type",
                    network.get(
                        "connection_type",
                        "Unknown"
                    )
                ],
                [
                    "Local IP",
                    network.get(
                        "local_ip",
                        "Unknown"
                    )
                ],
                [
                    "Subnet Mask",
                    network.get(
                        "subnet_mask",
                        "Unknown"
                    )
                ],
            ],
            columns=[
                "Field",
                "Value"
            ]
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
                        "props": [
                            (
                                "display",
                                "none"
                            )
                        ]
                    },
                    {
                        "selector": "td:first-child",
                        "props": [
                            (
                                "font-weight",
                                "bold"
                            ),
                            (
                                "width",
                                "30%"
                            ),
                        ],
                    },
                    {
                        "selector": "table",
                        "props": [
                            (
                                "border-collapse",
                                "collapse"
                            ),
                            (
                                "width",
                                "100%"
                            ),
                        ],
                    },
                ]
            )
        )

        st.table(
            styled_table
        )

        # -------------------------------------------------
        # Firewall check
        # -------------------------------------------------

        st.subheader(
            "Firewall Check"
        )

        if firewall.get(
            "supported",
            False
        ):

            if firewall.get(
                "firewall_enabled",
                False
            ):

                st.success(
                    "✅ Firewall is enabled."
                )

            else:

                st.warning(
                    "⚠️ Firewall is disabled "
                    "for at least one network profile."
                )

        else:

            st.info(
                firewall.get(
                    "message",
                    "Firewall status could not be determined."
                )
            )