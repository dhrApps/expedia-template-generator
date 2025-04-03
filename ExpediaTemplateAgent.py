import streamlit as st
import json

# Load the corrected base JSON template
try:
    with open("fixed_base_template.json", "r") as f:
        base_template = json.load(f)
    st.success("✅ Base template loaded successfully.")
except Exception as e:
    st.error(f"⚠️ Error loading base template: {repr(e)}")
    base_template = None

# Title
st.title("🌍 WLT Landing Page Template Generator")

# Intro
st.write("Create a fully structured landing page template with ease. Fill in the content IDs and download a ready-to-upload JSON.")

# Input fields
template_name = st.text_input("Template Name", help="Give your template a unique and descriptive name.")
page_title = st.text_input("Page Title", help="This title appears on the browser tab and search engines.")
header_text = st.text_input("Header", help="Main heading shown on the landing page.")
brand = st.text_input("Brand", help="Brand code, e.g., GPS")
pos = st.text_input("POS", help="Point of Sale, e.g., CATHAYPACIFIC_HK")
locale = st.text_input("Locale", help="Locale code, e.g., EN_HK")

# Component Content ID Inputs (with helper tooltips)
st.subheader("📋 Component Content IDs (with helper tooltips)")
hero_banner = st.text_input("Hero Banner Content ID", help="Big banner at top of the page with CTA")
rtb1 = st.text_input("Reason To Believe 1 (RTB 1) Content ID", help="First text block under banner (e.g., trust message)")
rtb2 = st.text_input("Reason To Believe 2 (RTB 2) Content ID", help="Second text block (optional)")
rtb3 = st.text_input("Reason To Believe 3 (RTB 3) Content ID", help="Third text block (e.g., help center CTA)")
tile1 = st.text_input("Canvas Group Tile 1 Content ID", help="Left-side card (e.g., featured destination)")
tile2 = st.text_input("Canvas Group Tile 2 Content ID", help="Right-side card (e.g., flexible booking promo)")

# Generate JSON
if st.button("Generate Template JSON"):
    try:
        if base_template:
            populated_template = base_template.copy()
            populated_template[0]["name"] = template_name
            populated_template[0]["title"] = page_title
            populated_template[0]["header"] = header_text
            populated_template[0]["brand"] = brand
            populated_template[0]["pos"] = pos
            populated_template[0]["locale"] = locale

            # Assign content IDs to placeholders (example placement)
            populated_template[0]["heroBannerContentId"] = hero_banner
            populated_template[0]["rtb1ContentId"] = rtb1
            populated_template[0]["rtb2ContentId"] = rtb2
            populated_template[0]["rtb3ContentId"] = rtb3
            populated_template[0]["tile1ContentId"] = tile1
            populated_template[0]["tile2ContentId"] = tile2

            json_str = json.dumps(populated_template, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="generated_template.json", mime="application/json")
    except Exception as e:
        st.error(f"⚠️ Error generating template: {repr(e)}")
