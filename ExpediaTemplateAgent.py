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

# App title and instructions
st.title("🧩 Expedia Landing Page Template Generator")
st.write("Create a fully structured landing page template with ease. Fill in the content IDs and download a ready-to-upload JSON.")

# Input fields
template_name = st.text_input("Template Name", help="Unique template name (e.g., LuxuryEscapes_Homepage)")
page_title = st.text_input("Page Title", help="Displayed on browser tab and search engines.")

brand = st.text_input("Brand", value="GPS")
pos = st.text_input("POS", value="CATHAYPACIFIC_HK")
locale = st.text_input("Locale", value="EN_HK")

# Line of Business selection
lob_options = ["Stays", "Packages", "Things to Do", "Cars", "Flights"]
selected_lob = st.selectbox("Line of Business", options=lob_options, help="Choose the Line of Business for this landing page.")

# Component Content IDs
st.subheader("📋 Component Content IDs (with helper tooltips)")
hero_banner = st.text_input("Hero Banner Content ID", help="Big banner at top of the page with CTA")
rtb1 = st.text_input("RTB 1 Content ID", help="First text block under banner (e.g., trust message)")
rtb2 = st.text_input("RTB 2 Content ID", help="Second text block (optional)")
rtb3 = st.text_input("RTB 3 Content ID", help="Third text block (e.g., help center CTA)")
tile1 = st.text_input("Tile 1 Content ID", help="Left-side card (e.g., featured destination)")
tile2 = st.text_input("Tile 2 Content ID", help="Right-side card (e.g., flexible booking promo)")

# Button to generate JSON
if st.button("Generate Template JSON"):
    try:
        if not base_template or not isinstance(base_template, list) or len(base_template) == 0:
            st.error("⚠️ Base template is empty or malformed.")
        else:
            populated_template = base_template[0]
            populated_template["name"] = template_name
            populated_template["title"] = page_title
            populated_template["brand"] = brand
            populated_template["pos"] = pos
            populated_template["locale"] = locale

            # Traverse to update content IDs
            def update_content_id_by_purpose(node, purpose, new_id):
                if isinstance(node, dict):
                    if node.get("type") == "MODULE":
                        for attr in node.get("attributes", []):
                            if attr.get("name") == "contentPurpose" and attr.get("value") == purpose:
                                for content_attr in node["attributes"]:
                                    if content_attr.get("name") == "contentId":
                                        content_attr["value"] = new_id
                    for key in node:
                        update_content_id_by_purpose(node[key], purpose, new_id)
                elif isinstance(node, list):
                    for item in node:
                        update_content_id_by_purpose(item, purpose, new_id)

            # Update IDs
            update_content_id_by_purpose(populated_template, "Editorial", hero_banner)
            update_content_id_by_purpose(populated_template, "FreeText", rtb1)
            update_content_id_by_purpose(populated_template, "FreeText", rtb2)
            update_content_id_by_purpose(populated_template, "FreeText", rtb3)
            update_content_id_by_purpose(populated_template, "Cards", tile1)
            update_content_id_by_purpose(populated_template, "Cards", tile2)

            output_json = json.dumps([populated_template], indent=2)
            st.download_button("📥 Download JSON File", output_json, file_name="generated_template.json", mime="application/json")
    except Exception as e:
        st.error(f"⚠️ Error generating template: {repr(e)}")
