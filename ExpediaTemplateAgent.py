
import streamlit as st
import json

# Load the corrected base JSON template
with open("fixed_base_template.json", "r") as f:
    base_template = json.load(f)

# Title
st.title("🧩 Expedia Landing Page Template Generator")

# Intro
st.write("Create a fully structured landing page template with ease. Fill in the content IDs and download a ready-to-upload JSON.")

# Input fields
template_name = st.text_input("Template Name", help="Give your template a unique and descriptive name.")
page_title = st.text_input("Page Title", help="This title appears on the browser tab and search engines.")

# Lines of Business selection
lob_options = ["Stays", "Packages", "Things to Do", "Cars", "Flights"]
selected_lob = st.selectbox("Select Line of Business", options=lob_options, help="Choose the Line of Business for which this landing page applies.")

# Component Content ID Inputs with helper tooltips
st.subheader("📋 Component Prompts (with helper tooltips)")
hero_banner = st.text_input("Hero Banner Content ID", help="Big banner at top of the page with CTA")
rtb1 = st.text_input("RTB 1 Content ID", help="First text block under banner (e.g., trust message)")
rtb2 = st.text_input("RTB 2 Content ID", help="Second text block (optional)")
rtb3 = st.text_input("RTB 3 Content ID", help="Third text block (e.g., help center CTA)")
tile1 = st.text_input("Tile 1 Content ID", help="Left-side card (e.g., featured destination)")
tile2 = st.text_input("Tile 2 Content ID", help="Right-side card (e.g., flexible booking promo)")

# Button to generate JSON
if st.button("Generate Template JSON"):
    populated_template = base_template.copy()
    populated_template["templateName"] = template_name
    populated_template["pageTitle"] = page_title
    populated_template["lineOfBusiness"] = selected_lob.lower()
    components = populated_template["templateComponents"]

    # Fill in the content IDs
    components["heroBanner"]["contentId"] = hero_banner
    components["rtb1"]["contentId"] = rtb1
    components["rtb2"]["contentId"] = rtb2
    components["rtb3"]["contentId"] = rtb3
    components["tile1"]["contentId"] = tile1
    components["tile2"]["contentId"] = tile2

    json_str = json.dumps(populated_template, indent=4)
    st.download_button("📥 Download Template JSON", data=json_str, file_name=f"{template_name}_template.json", mime="application/json")
