import streamlit as st
import json

# Load the corrected base JSON structure
with open("fixed_base_template.json", "r") as f:
    base_template = json.load(f)

# Title
st.title("🗺️ Expedia Landing Page Template Generator")

# Intro
st.write("Create a fully structured landing page template with ease. Fill in the content IDs and download a ready-to-upload JSON.")

# Input fields
template_name = st.text_input("Template Name", help="Give your template a unique and descriptive name.")
page_title = st.text_input("Page Title", help="This title appears on the browser tab and search engines.")

# Lines of Business selection
lob_options = ["Stays", "Packages", "Things to Do", "Cars", "Flights"]
selected_lob = st.selectbox("Line of Business", options=lob_options, help="Choose the Line of Business for which this landing page applies.")

# Component Content ID Inputs (with helper tooltips)
st.subheader("📋 Component Prompts (with helper tooltips)")
hero_banner = st.text_input("Hero Banner Content ID", help="Big banner at top of the page with CTA")
rtb1 = st.text_input("RTB 1 Content ID", help="First text block under banner (e.g., trust message)")
rtb2 = st.text_input("RTB 2 Content ID", help="Second text block (optional)")
rtb3 = st.text_input("RTB 3 Content ID", help="Third text block (e.g., help center CTA)")
tile1 = st.text_input("Tile 1 Content ID", help="Left-side card (e.g., featured destination)")
tile2 = st.text_input("Tile 2 Content ID", help="Right-side card (e.g., flexible booking promo)")

# Button to generate JSON
if st.button("Generate Template JSON"):
    # Deep copy the base template
    populated_template = json.loads(json.dumps(base_template))

    # Inject user inputs
    populated_template[0]["name"] = template_name
    populated_template[0]["title"] = page_title

    # Replace content IDs in correct places
    # Mapping from user input to known module IDs in the base JSON
    content_id_mapping = {
        "4665431": hero_banner,
        "4665432": rtb1,
        "4665433": rtb2,
        "4665434": rtb3,
        "4665435": tile1,
        "4665436": tile2,
    }

    def update_content_ids(node):
        if node.get("type") == "MODULE":
            for attr in node.get("attributes", []):
                if attr["name"] == "contentId":
                    old_id = attr["value"]
                    if old_id in content_id_mapping:
                        attr["value"] = content_id_mapping[old_id]
        for child in node.get("childNodes", []):
            update_content_ids(child)

    # Traverse the flexNode and update content IDs
    update_content_ids(populated_template[0]["flexNode"])

    # Download JSON
    json_data = json.dumps(populated_template, indent=4)
    st.download_button(
        label="📥 Download JSON File",
        data=json_data,
        file_name=f"{template_name}_template.json",
        mime="application/json"
    )
