
import streamlit as st
import json
import copy

# App title
st.title("WLT Landing Page Template Generator")

# User Inputs with help text and NO default values
template_name = st.text_input("Template Name", help="Enter a unique name for this template.")
page_title = st.text_input("Page Title", help="Displayed as the main title on the landing page.")
header_text = st.text_input("Header Text", help="Header displayed at the top of the landing page.")

brand = st.text_input("Brand", help="Brand identifier, e.g., GPS or WLT.")
pos = st.text_input("POS", help="Point of Sale identifier, e.g., CATHAYPACIFIC_HK.")
locale = st.text_input("Locale", help="Locale code, e.g., EN_HK.")

st.markdown("---")
st.subheader("Content IDs")

hero_banner = st.text_input("Hero Banner Content ID", help="Content ID for the hero banner at the top of the page.")
rtb1 = st.text_input("Reason To Believe 1 (RTB 1) Content ID", help="Content ID for the first RTB section.")
rtb2 = st.text_input("Reason To Believe 2 (RTB 2) Content ID", help="Content ID for the second RTB section.")
rtb3 = st.text_input("Reason To Believe 3 (RTB 3) Content ID", help="Content ID for the third RTB section.")
tile1 = st.text_input("Canvas Group Tile 1 Content ID", help="Content ID for the first tile in the canvas group.")
tile2 = st.text_input("Canvas Group Tile 2 Content ID", help="Content ID for the second tile in the canvas group.")

# Load base template
base_template = None
try:
    with open("fixed_base_template.json") as f:
        base_template = json.load(f)
except Exception as e:
    st.error(f"Error loading base template: {e}")

# Generate JSON
if st.button("Generate Template JSON"):
    try:
        if base_template:
            populated_template = copy.deepcopy(base_template)
            populated_template[0]["name"] = template_name
            populated_template[0]["title"] = page_title
            populated_template[0]["header"] = header_text
            populated_template[0]["brand"] = brand
            populated_template[0]["pos"] = pos
            populated_template[0]["locale"] = locale

            # Assign content IDs dynamically into the relevant sections
            def assign_content_ids(node, content_id_map):
                if isinstance(node, dict):
                    for key, value in node.items():
                        if key == "attributes" and isinstance(value, list):
                            for attr in value:
                                if attr.get("name") == "contentId":
                                    parent_name = next((a.get("value", "").lower() for a in value if a.get("name") == "name"), "")
                                    for label, cid in content_id_map.items():
                                        if label in parent_name:
                                            attr["value"] = cid
                        else:
                            assign_content_ids(value, content_id_map)
                elif isinstance(node, list):
                    for item in node:
                        assign_content_ids(item, content_id_map)

            content_id_map = {
                "hero": hero_banner,
                "rtb 1": rtb1,
                "rtb 2": rtb2,
                "rtb 3": rtb3,
                "tile 1": tile1,
                "tile 2": tile2
            }

            assign_content_ids(populated_template[0]["flexNode"], content_id_map)

            json_str = json.dumps(populated_template, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="generated_template.json", mime="application/json")
    except Exception as e:
        st.error(f"⚠️ Error generating template: {repr(e)}")
