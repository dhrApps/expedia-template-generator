
import streamlit as st
import json

# Page Title
st.set_page_config(page_title="WLT Landing Page Template Generator")
st.title("🛠️ WLT Landing Page Template Generator")

# Inputs
template_name = st.text_input("Template Name")
page_title = st.text_input("Page Title")
header_text = st.text_input("Header")
brand = st.text_input("Brand")
pos = st.text_input("POS")
locale = st.text_input("Locale")

st.markdown("---")

st.subheader("Enter Content IDs for Each Component")
hero_banner = st.text_input("Hero Banner Content ID", help="Main hero banner (aka Full Bleed Image Banner)")
rtb1 = st.text_input("Reason To Believe 1 (RTB 1) Content ID", help="First RTB section")
rtb2 = st.text_input("Reason To Believe 2 (RTB 2) Content ID", help="Second RTB section")
rtb3 = st.text_input("Reason To Believe 3 (RTB 3) Content ID", help="Third RTB section")
tile1 = st.text_input("Canvas Group Tile 1 Content ID", help="Left tile in canvas group")
tile2 = st.text_input("Canvas Group Tile 2 Content ID", help="Right tile in canvas group")

# Load base template
try:
    with open("fixed_base_template.json", "r") as f:
        base_template = json.load(f)
except Exception as e:
    st.error(f"Error loading base template: {e}")
    base_template = None

def assign_content_id(template, region_name, content_id):
    def traverse(node):
        if isinstance(node, dict):
            if node.get("type") == "REGION":
                for attr in node.get("attributes", []):
                    if attr.get("name") == "name" and attr.get("value") == region_name:
                        for child in node.get("childNodes", []):
                            if child.get("type") == "MODULE":
                                for attr in child.get("attributes", []):
                                    if attr.get("name") == "contentId":
                                        attr["value"] = content_id
            for val in node.values():
                traverse(val)
        elif isinstance(node, list):
            for item in node:
                traverse(item)

    traverse(template)

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

            region_mappings = {
                "Hero Full Bleed Banner": hero_banner,
                "RTB 1": rtb1,
                "RTB 2": rtb2,
                "RTB 3": rtb3,
                "Tile 1": tile1,
                "Tile 2": tile2
            }

            for region, cid in region_mappings.items():
                assign_content_id(populated_template, region, cid)

            json_str = json.dumps(populated_template, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="generated_template.json", mime="application/json")
    except Exception as e:
        st.error(f"⚠️ Error generating template: {repr(e)}")
