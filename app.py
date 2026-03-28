import streamlit as st
import pandas as pd

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="GreenGuard", layout="wide")

# -------------------------
# CUSTOM UI STYLING
# -------------------------
st.markdown("""
<style>

/* Background */
[data-testid="stAppViewContainer"] {
    background-color: #EAF7EF;
}

/* Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Title */
.title {
    text-align: center;
    font-size: 48px;
    font-weight: 700;
    color: #1B5E20;
}

/* Tagline */
.tagline {
    text-align: center;
    font-size: 18px;
    color: #3d5c4f;
    margin-bottom: 25px;
}

/* Fix text colors globally */
h3 {
    color: #1B5E20 !important;
}

p {
    color: #333 !important;
}

/* Button styling */
button {
    background-color: #1B5E20 !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    padding: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.markdown('<div class="title">GreenGuard</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Protecting consumers from misleading sustainability claims</div>', unsafe_allow_html=True)

st.markdown("<hr style='border:1px solid #cde7d8'>", unsafe_allow_html=True)

# -------------------------
# CENTERED INPUT SECTION
# -------------------------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("<h3 style='text-align:center; color:#1B5E20;'>Enter Product Description</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Example: eco-friendly cotton shirt certified by GOTS</p>", unsafe_allow_html=True)

    text = st.text_area("", height=150)

    analyze = st.button("Analyze", use_container_width=True)

# -------------------------
# PROCESSING
# -------------------------
if analyze:

    df = pd.read_csv("certifications.csv", skiprows=1)
    df.columns = df.columns.str.strip()
    certifications = df["names"].dropna().tolist()

    buzzwords = ["eco-friendly", "natural", "green", "sustainable", "clean", "organic"]

    found_buzzwords = []
    found_certifications = []

    clean_text = text.lower()

    for word in buzzwords:
        if word in clean_text:
            found_buzzwords.append(word)

    for cert in certifications:
        if str(cert).lower() in clean_text:
            found_certifications.append(cert)

    # -------------------------
    # CENTER RESULT
    # -------------------------
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.subheader("Result")

        if found_buzzwords and not found_certifications:
            st.error("This product likely contains misleading sustainability claims.")
            st.write("The description uses vague environmental terms without verified certification.")

        elif found_buzzwords and found_certifications:
            st.warning("This product shows mixed signals.")
            st.write("Some sustainability claims are present, but certification support is partial.")

        elif not found_buzzwords and found_certifications:
            st.success("This product appears to be genuinely certified.")
            st.write("The claims are supported by recognized sustainability certifications.")

        else:
            st.info("Not enough information available.")
            st.write("The description does not provide clear sustainability details.")

        # -------------------------
        # SCORE
        # -------------------------
        score = 100 - len(found_buzzwords)*15 + len(found_certifications)*10
        score = max(min(score, 100), 0)

        st.subheader("Sustainability Score")
        st.progress(score / 100)
        st.write(f"{score}/100")

        st.markdown("---")
        st.caption("GreenGuard supports responsible and informed consumer decisions")