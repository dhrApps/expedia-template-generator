import streamlit as st
import json
import copy

# Load the corrected base JSON template
try:
    with open("fixed_base_template.json", "r") as f:
        base_template = json.load(f)
        st.success("✅ Base template loaded successfully.")
except Exception as e:
    base_template = None
    st.error(f"⚠️ Error loading base template: {repr(e)}")

# App Title
st.title("🌍 Expedia Landing Page Template Generator")

# Intro Text
st.write("Create a fully structured landing page template with ease. Fill in the content IDs and page info, then download a ready-to-upload JSON.")

# Input fields
template_name = st.text_input("Template Name", help="Unique and descriptive name for the template.")
page_title = st.text_input("Page Title", help="This title appears on the browser tab and search engines.")
header_text = st.text_input("Header", help="Main heading on the landing page.")
brand = st.text_input("Brand", value="GPS", help="Brand identifier (e.g., GPS, EAP, etc.)")
pos = st.text_input("POS", value="CATHAYPACIFIC_HK", help="Point of Sale (e.g., CATHAYPACIFIC_HK)")
locale = st.text_input("Locale", value="EN_HK", help="Locale code (e.g., EN_HK)")

# Component Content IDs with helper tooltips
st.subheader("📋 Component Prompts (with helper tooltips)")
hero_banner = st.text_input("Hero Banner Content ID", help="Big banner at top of the page with CTA")
rtb1 = st.text_input("Reason To Believe 1 (RTB 1) Content ID", help="First text block under banner (e.g., trust message)")
rtb2 = st.text_input("Reason To Believe 2 (RTB 2) Content ID", help="Second text block (optional)")
rtb3 = st.text_input("Reason To Believe 3 (RTB 3) Content ID", help="Third text block (e.g., help center CTA)")
tile1 = st.text_input("Canvas Group Tile 1 Content ID", help="Left-side card (e.g., featured destination)")
tile2 = st.text_input("Canvas Group Tile 2 Content ID", help="Right-side card (e.g., flexible booking promo)")

# Button to generate JSON
if st.button("🚀 Generate Template JSON"):
    try:
        if base_template and isinstance(base_template, list) and len(base_template) > 0:
            # Deep copy to avoid modifying the original
            populated_template = copy.deepcopy(base_template)

            # Fill in user inputs
            populated_template[0]["name"] = template_name
            populated_template[0]["title"] = page_title
            populated_template[0]["header"] = header_text
            populated_template[0]["brand"] = brand
            populated_template[0]["pos"] = pos
            populated_template[0]["locale"] = locale

            # Traverse the JSON and replace contentId fields
            def replace_content_id(node, component_name, new_id):
                if isinstance(node, dict):
                    if node.get("name", "").lower() == component_name.lower():
                        for attr in node.get("attributes", []):
                            if attr.get("name") == "contentId":
                                attr["value"] = new_id
                    for key, value in node.items():
                        replace_content_id(value, component_name, new_id)
                elif isinstance(node, list):
                    for item in node:
                        replace_content_id(item, component_name, new_id)

            # Update all components with provided content IDs
            component_ids = {
                "heroBanner": hero_banner,
                "rtb1": rtb1,
                "rtb2": rtb2,
                "rtb3": rtb3,
                "tile1": tile1,
                "tile2": tile2
            }

            for component, cid in component_ids.items():
                if cid.strip():
                    replace_content_id(populated_template, component, cid.strip())

            # Downloadable JSON file
            json_str = json.dumps(populated_template, indent=4)
            st.download_button(
                label="📥 Download Template JSON",
                data=json_str,
                file_name=f"{template_name}.json",
                mime="application/json"
            )
        else:
            st.warning("⚠️ Base template is empty or malformed.")
    except Exception as e:
        st.error(f"⚠️ Error generating template: {repr(e)}")
