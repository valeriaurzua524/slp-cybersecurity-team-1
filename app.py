import streamlit as st
import pandas as pd
import re
from urllib.parse import urlparse

from main import run_website_scan, run_network_scan
from report_generator import generate_report, ISSUE_NAMES


st.set_page_config(
    page_title="Cybersecurity Vulnerability & Network Safety Scanner",
    page_icon="cyber_team_logo.png",
    layout="wide"
)


st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 75% 5%, #32105c 0%, transparent 28%),
        radial-gradient(circle at 10% 85%, #241044 0%, transparent 25%),
        #090914;
    color: #f5f3ff;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
}

/* Main heading */
.page-heading {
    text-align: center;
    margin-bottom: 35px;
}

.page-heading h1 {
    font-size: 48px;
    margin: 0;
    color: #d9a7ff !important;
    font-weight: 900 !important;
    text-shadow:
        0 0 3px rgba(192, 77, 255, 0.7),
        0 0 8px rgba(192, 77, 255, 0.45);
}

.page-heading p {
    color: #c4bdd8;
    font-size: 18px;
    margin-top: 10px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    min-width: 320px;
    max-width: 320px;
    background:
        radial-gradient(circle at 80% 85%, #32105c 0%, transparent 35%),
        linear-gradient(180deg, #110d24 0%, #090914 100%);
    border-right: 2px solid #6f2ca8;
}

.sidebar-title {
    color: #f2e6ff;
    font-size: 28px;
    font-weight: 800;
    line-height: 1.2;
    padding: 18px 0 35px 20px;
    text-shadow:
        0 0 3px rgba(192, 77, 255, 0.5),
        0 0 7px rgba(192, 77, 255, 0.3);
}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
    min-height: 82px;
    margin: 8px 0;
    border-radius: 18px;
    text-align: left;
    padding-left: 25px;
    font-size: 28px !important;
    font-weight: 800 !important;
    line-height: 1.2;
}

[data-testid="stSidebar"] button[kind="primary"] {
    background: linear-gradient(90deg, #5b1bb2, #32105c);
    border: 2px solid #c979f5;
    box-shadow:
        0 0 7px rgba(192, 77, 255, 0.65),
        0 0 15px rgba(192, 77, 255, 0.4);
}

[data-testid="stSidebar"] button[kind="secondary"] {
    background: rgba(25, 20, 45, 0.85);
    border: 1px solid #3d3157;
    color: #f5f3ff;
}

[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #c979f5;
    box-shadow: 0 0 14px rgba(192, 77, 255, 0.55);
}

/* About card */
.sidebar-spacer {
    height: 18vh;
}

.about-title {
    color: white;
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 15px;
}

.about-text {
    color: #d2cbe4;
    font-size: 19px;
    line-height: 1.7;
}

[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
    padding: 22px 18px 42px 18px;
    border-radius: 18px;
}

/* All main buttons */
.stButton > button {
    background: linear-gradient(90deg, #8b2cff, #c04dff);
    color: white;
    border: 1px solid #d58aff;
    border-radius: 10px;
    font-weight: 800 !important;
    font-size: 30px !important;
    line-height: 1.2;
    min-height: 58px;
    box-shadow: 0 0 14px rgba(174, 62, 255, 0.35);
}

.stButton > button:hover {
    border-color: white;
    box-shadow: 0 0 20px rgba(200, 92, 255, 0.6);
}

/* Text input */
[data-testid="stTextInput"] input {
    background-color: #151426;
    color: white;
    border: 1px solid #8737c7;
    border-radius: 10px;
    min-height: 48px;
    font-size: 20px;
}

[data-testid="stTextInput"] input:focus {
    border-color: #c979f5;
    box-shadow: 0 0 10px rgba(208, 92, 255, 0.45);
}

/* Progress bar */
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #8b2cff, #df63ff);
}

/* Cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(22, 18, 39, 0.85);
    border: 1px solid #5f3191;
    border-radius: 14px;
}

/* Report rows */
.report-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 20px;
    width: 100%;
    box-sizing: border-box;
    border-bottom: 1px solid #3c3154;
    padding: 12px 0;
}

.report-label {
    color: #aaa2c7;
    font-size: 17px;
}

.report-value {
    color: white;
    font-weight: 700;
    font-size: 17px;
    max-width: 55%;
    text-align: right;
    overflow-wrap: anywhere;
    word-break: break-word;
}

[data-testid="stAlert"] {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


if "page" not in st.session_state:
    st.session_state.page = "home"


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-title">
            Cybersecurity<br>
            Scanner
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.page != "home":

        if st.button(
            "←  Back to Home",
            key="back_home",
            use_container_width=True
        ):
            st.session_state.page = "home"
            st.rerun()

    website_type = (
        "primary"
        if st.session_state.page == "website"
        else "secondary"
    )

    if st.button(
        "🌐   Website Scanner      ›",
        key="sidebar_website",
        type=website_type,
        use_container_width=True
    ):
        st.session_state.page = "website"
        st.rerun()

    network_type = (
        "primary"
        if st.session_state.page == "network"
        else "secondary"
    )

    if st.button(
        "📡   Network Scanner      ›",
        key="sidebar_network",
        type=network_type,
        use_container_width=True
    ):
        st.session_state.page = "network"
        st.rerun()

    st.markdown(
        '<div class="sidebar-spacer"></div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        st.markdown(
            """
            <div class="about-title">
                ⓘ &nbsp; About
            </div>

            <div class="about-text">
                Scan websites and networks for common security risks,
                misconfigurations, and vulnerabilities.
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# HOME PAGE
# =========================================================

if st.session_state.page == "home":

    st.markdown(
        """
        <div class="page-heading">
            <h1>Cybersecurity Scanner</h1>
            <p>SLP Cybersecurity team #1</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Choose a Scanner")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):
            st.markdown("## 🌐 Website Scanner")
            st.write(
                "Analyze a website for HTTPS, redirects, "
                "and other security issues."
            )

            if st.button(
                "Open Website Scanner",
                key="home_website",
                use_container_width=True
            ):
                st.session_state.page = "website"
                st.rerun()

    with col2:

        with st.container(border=True):
            st.markdown("## 📡 Network Scanner")
            st.write(
                "Check your local network information "
                "and firewall status."
            )

            if st.button(
                "Open Network Scanner",
                key="home_network",
                use_container_width=True
            ):
                st.session_state.page = "network"
                st.rerun()


# =========================================================
# WEBSITE SCANNER
# =========================================================

elif st.session_state.page == "website":

    st.markdown(
        """
        <div class="page-heading">
            <h1>Website Security Scanner</h1>
            <p>SLP Cybersecurity team #1</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    website_url = st.text_input(
        "Website URL",
        placeholder="https://example.com"
    )

    if st.button(
        "🔍 Scan Website",
        key="scan_website",
        use_container_width=True
    ):

        website_url = website_url.strip()

        if website_url == "":
            st.warning("Please enter a valid URL.")

        else:

            if not website_url.startswith(
                ("http://", "https://")
            ):
                website_url = "https://" + website_url

            with st.spinner(
                "Checking whether the website is secure..."
            ):
                results = run_website_scan(website_url)

            if "error" in results:

                st.error("Website scan failed.")

                st.write(
                    results.get(
                        "message",
                        "Please check the URL and try again."
                    )
                )

            else:

                security_score = results.get("score", 0)
                risk_level = results.get(
                    "risk_level",
                    "Unknown"
                )
                issues = results.get("issues", [])

                https_status = (
                    "Enabled"
                    if results.get("uses_https")
                    else "Disabled"
                )

                parsed_url = urlparse(website_url)
                website_name = parsed_url.netloc

                if website_name.startswith("www."):
                    website_name = website_name[4:]

                st.success("✅ Scan completed successfully")

                st.markdown("### Scan Results")

                col1, col2, col3 = st.columns(3)

                with col1:
                    with st.container(border=True):
                        st.markdown("🛡️ **Security Score**")
                        st.markdown(
                            f"## {security_score}/100"
                        )

                with col2:
                    with st.container(border=True):
                        st.markdown("⚠️ **Risk Level**")
                        st.markdown(
                            f"## {risk_level.capitalize()}"
                        )

                with col3:
                    with st.container(border=True):
                        st.markdown("🔒 **HTTPS Supported**")
                        st.markdown(
                            f"## {https_status}"
                        )

                st.markdown("### Scan Progress")
                st.progress(security_score)

                st.markdown("## Scan Details")

                findings_col, report_col = st.columns(
                    [1.7, 1],
                    gap="medium"
                )

                with findings_col:

                    st.markdown("### 🔎 Findings")

                    if not issues:

                        st.success(
                            "✅ No security issues were found."
                        )

                    else:

                        for item in issues:

                            issue_name = ISSUE_NAMES.get(
                                item["issue"],
                                item["issue"]
                                .replace("_", " ")
                                .title()
                            )

                            severity = item.get(
                                "severity",
                                "info"
                            ).lower()

                            recommendation = item.get(
                                "recommendation",
                                "No recommendation available."
                            )

                            recommendation = re.sub(
                                r"<[^>]*>",
                                "",
                                str(recommendation)
                            )

                            recommendation = (
                                recommendation
                                .replace("```", "")
                                .strip()
                            )

                            if severity == "high":
                                icon = "🔴"

                            elif severity == "medium":
                                icon = "🟠"

                            elif severity == "low":
                                icon = "🔵"

                            else:
                                icon = "🟢"

                            with st.container(border=True):

                                st.markdown(
                                    f"### {icon} "
                                    f"{severity.capitalize()} — "
                                    f"{issue_name}"
                                )

                                st.write(recommendation)

                with report_col:

                    st.markdown("### 📄 Scan Report")

                    with st.container(border=True):

                        st.markdown(
                            f"""
                            <div class="report-row">
                                <span class="report-label">
                                    Target
                                </span>
                                <span class="report-value">
                                    {website_name}
                                </span>
                            </div>

                            <div class="report-row">
                                <span class="report-label">
                                    Security Score
                                </span>
                                <span class="report-value">
                                    {security_score}/100
                                </span>
                            </div>

                            <div class="report-row">
                                <span class="report-label">
                                    Risk Level
                                </span>
                                <span class="report-value">
                                    {risk_level.capitalize()}
                                </span>
                            </div>

                            <div class="report-row">
                                <span class="report-label">
                                    Findings
                                </span>
                                <span class="report-value">
                                    {len(issues)}
                                </span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        report = generate_report(results)

                        with st.expander(
                            "View Full Security Report"
                        ):
                            st.code(
                                report,
                                language=None
                            )

                        st.download_button(
                            label="⬇️ Download Security Report",
                            data=report,
                            file_name="security_report.txt",
                            mime="text/plain",
                            use_container_width=True
                        )


# =========================================================
# NETWORK SCANNER
# =========================================================

elif st.session_state.page == "network":

    st.markdown(
        """
        <div class="page-heading">
            <h1>Network Security Scanner</h1>
            <p>SLP Cybersecurity team #1</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🔍 Check Network",
        key="check_network",
        use_container_width=True
    ):

        with st.spinner("Checking your network..."):
            network_results = run_network_scan()

        st.success("✅ Network check completed")

        network = network_results["network_info"]
        firewall = network_results["firewall"]

        st.markdown("### Network Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.markdown("💻 **Operating System**")
                st.markdown(
                    f"## {network['operating_system']}"
                )

        with col2:
            with st.container(border=True):
                st.markdown("📡 **Primary Interface**")
                st.markdown(
                    f"## {network['primary_interface']}"
                )

        with col3:
            with st.container(border=True):
                st.markdown("📍 **Local IP**")
                st.markdown(
                    f"## {network['local_ip']}"
                )

        st.markdown("### Network Information")

        network_table = pd.DataFrame(
            [
                [
                    "Operating System",
                    f"{network['operating_system']} "
                    f"{network['os_version']}"
                ],
                [
                    "Primary Interface",
                    network["primary_interface"]
                ],
                [
                    "Local IP",
                    network["local_ip"]
                ],
                [
                    "Subnet Mask",
                    network["subnet_mask"]
                ],
            ],
            columns=["Field", "Value"]
        )

        st.table(network_table)

        st.markdown("### Firewall Check")

        if firewall["supported"]:

            if firewall["firewall_enabled"]:
                st.success("✅ Firewall is enabled.")

            else:
                st.warning("⚠️ Firewall is disabled.")

        else:
            st.info(firewall["message"])