
import streamlit as st
import json
import copy

# Load base template
with open("fixed_base_template.json", "r") as f:
    base_template = json.load(f)

# Header with logo and styled title
st.markdown(
    """
    <div style='display: flex; align-items: center; gap: 10px;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/5/5e/Expedia_Group_logo_2021.svg' width='40'/>
        <h1 style='color:#0073e6;font-size:28px;'>✈️ WLT Template Generator</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

# Input fields
template_name = st.text_input("Template Name")
page_title = st.text_input("Page Title")
header_text = st.text_input("Header")
brand = st.text_input("Brand")
pos = st.text_input("POS")
locale = st.text_input("Locale")

hero_banner = st.text_input("Hero Banner Content ID", help="Content ID for Hero Full Bleed Banner")
rtb1 = st.text_input("Reason To Believe 1 (RTB 1) Content ID", help="Content ID for RTB 1 section")
rtb2 = st.text_input("Reason To Believe 2 (RTB 2) Content ID", help="Content ID for RTB 2 section")
rtb3 = st.text_input("Reason To Believe 3 (RTB 3) Content ID", help="Content ID for RTB 3 section")
tile1 = st.text_input("Canvas Group Tile 1 Content ID", help="Content ID for Tile 1 in Canvas Group")
tile2 = st.text_input("Canvas Group Tile 2 Content ID", help="Content ID for Tile 2 in Canvas Group")

# Helper to assign contentId into the correct region
def assign_content_id(template, region_name, content_id_value):
    def recursive_assign(node):
        if node.get("type") == "REGION":
            attributes = node.get("attributes", [])
            for attr in attributes:
                if attr.get("name") == "name" and attr.get("value") == region_name:
                    for module in node.get("childNodes", []):
                        if module.get("type") == "MODULE":
                            for attr in module.get("attributes", []):
                                if attr.get("name") == "contentId":
                                    attr["value"] = content_id_value
        for child in node.get("childNodes", []):
            recursive_assign(child)
    recursive_assign(template["flexNode"])

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

            # Assign content IDs to corresponding regions
            assign_content_id(populated_template[0], "Hero Full Bleed Banner", hero_banner)
            assign_content_id(populated_template[0], "RTB 1", rtb1)
            assign_content_id(populated_template[0], "RTB 2", rtb2)
            assign_content_id(populated_template[0], "RTB 3", rtb3)
            assign_content_id(populated_template[0], "Tile 1", tile1)
            assign_content_id(populated_template[0], "Tile 2", tile2)

            json_str = json.dumps(populated_template, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="generated_template.json", mime="application/json")
    except Exception as e:
        st.error(f"⚠️ Error generating template: {repr(e)}")
