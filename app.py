import streamlit as st
import time 

st.title("Website Security Scanner")
st.write("SLP cybersecurity team #1 :))")

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
            security_score = 85
            progress_bar = st.progress(0)

            for number in range(security_score + 1):
                time.sleep(0.02)
                progress_bar.progress(number)

        if website_url.startswith("https://"):
            st.success("Website scan successful.")
            risk_level = "Low"
        else:
            st.error("Website scan failed.")
            risk_level = "High"

        st.subheader("Security Results")
        st.write(f"Security Score: **{security_score}/100**")
        st.write(f"Risk Level: **{risk_level}**")
        
    #work on for what kind of vulnaribilities to chekc the website for 
    #add the findings/issues area
    #recommendations area

st.title("Network Security Scanner")
    #what do you mean bythe network/ public wifi area?

if st.button("Check Network"):
    with st.spinner("Checking your network..."):
        time.sleep(2)

    # Placeholder data for now
    network_score = 80
    risk_level = "Moderate"

    st.success("Network check completed.")

    st.subheader("Network Results")

    st.write(f"Security Score: **{network_score}/100**")
    st.write(f"Risk Level: **{risk_level}**")

   #add issues and recommendations area