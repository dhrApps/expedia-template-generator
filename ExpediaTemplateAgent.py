import streamlit as st
import json

# Load the corrected base JSON template
try:
    with open("fixed_base_template.json", "r") as f:
        base_template = json.load(f)
        st.write("✅ Base template loaded successfully.")  # Debug message
except Exception as e:
    st.error(f"❌ Failed to load base template: {repr(e)}")
    st.stop()

# Ensure template is not empty
if not base_template or not isinstance(base_template, list):
    st.error("⚠️ Base template is empty or malformed.")
    st.stop()

# Title
st.title("🗺️ Expedia Landing Page Template Generator")

# Intro
st.write("Create a fully structured landing page template with ease. Fill in the content IDs and download a ready-to-upload JSON.")

# Input fields
template_name = st.text_input("Template Name", help="Give your template a unique and descriptive name.")
page_title = st.text_input("Page Title", help="This title appears on the browser tab and search engines.")

# Lines of Business selection
lob_options = ['Stays', 'Packages', 'Things to Do', 'Cars', 'Flights']
selected_lob = st.selectbox("Line of Business", options=lob_options, help="Choose the Line of Business for which this landing page applies.")

# Component Content IDs (with tooltips)
st.subheader("📋 Component Prompts (with helper tooltips)")
hero_banner = st.text_input("Hero Banner Content ID", help="Big banner at top of the page with CTA")
rtb1 = st.text_input("RTB 1 Content ID", help="First text block under banner (e.g., trust message)")
rtb2 = st.text_input("RTB 2 Content ID", help="Second text block (optional)")
rtb3 = st.text_input("RTB 3 Content ID", help="Third text block (e.g., help center CTA)")
tile1 = st.text_input("Tile 1 Content ID", help="Left-side card (e.g., featured destination)")
tile2 = st.text_input("Tile 2 Content ID", help="Right-side card (e.g., flexible booking promo)")

# Button to generate JSON
if st.button("Generate Template JSON"):
    try:
        # Copy base template
        populated_template = base_template.copy()

        # Insert user inputs into the first item of the template
        populated_template[0]["name"] = template_name
        populated_template[0]["title"] = page_title

        # Insert content IDs into correct positions
        populated_template[0]["flexNode"]["childNodes"][1]["childNodes"][0]["attributes"][0]["value"] = hero_banner
        populated_template[0]["flexNode"]["childNodes"][2]["childNodes"][0]["childNodes"][0]["attributes"][0]["value"] = rtb1
        populated_template[0]["flexNode"]["childNodes"][2]["childNodes"][1]["childNodes"][0]["attributes"][0]["value"] = rtb2
        populated_template[0]["flexNode"]["childNodes"][2]["childNodes"][2]["childNodes"][0]["attributes"][0]["value"] = rtb3
        populated_template[0]["flexNode"]["childNodes"][3]["childNodes"][0]["childNodes"][0]["childNodes"][0]["attributes"][1]["value"] = tile1
        populated_template[0]["flexNode"]["childNodes"][3]["childNodes"][1]["childNodes"][0]["attributes"][1]["value"] = tile2

        # Download JSON
        st.success("✅ Template JSON generated successfully!")
        st.download_button("Download JSON", data=json.dumps(populated_template, indent=4), file_name="generated_template.json", mime="application/json")

    except Exception as e:
        st.error(f"⚠️ Error generating template: {repr(e)}")
