import streamlit as st
import json
import copy

# App title
st.title("WLT Landing Page Template Generator")

# User Inputs
template_name = st.text_input("Template Name")
page_title = st.text_input("Page Title")
header_text = st.text_input("Header Text")
brand = st.text_input("Brand", "GPS")
pos = st.text_input("POS", "PHILIPPINEAIRLINES_PH")
locale = st.text_input("Locale", "EN_PH")

st.markdown("---")
st.subheader("Content IDs")
hero_banner = st.text_input("Hero Banner Content ID")
rtb1 = st.text_input("Reason To Believe 1 (RTB 1) Content ID")
rtb2 = st.text_input("Reason To Believe 2 (RTB 2) Content ID")
rtb3 = st.text_input("Reason To Believe 3 (RTB 3) Content ID")
tile1 = st.text_input("Canvas Group Tile 1 Content ID")
tile2 = st.text_input("Canvas Group Tile 2 Content ID")

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

            # Dynamically assign content IDs
            def assign_content_id(node, label, content_id):
                if isinstance(node, dict):
                    for key, value in node.items():
                        if key == "attributes" and isinstance(value, list):
                            for attr in value:
                                if attr.get("name") == "contentId":
                                    # Match based on label in the UI
                                    if label.lower() in node.get("attributes", [{}])[0].get("value", "").lower() or label.lower() in json.dumps(node).lower():
                                        attr["value"] = content_id
                        else:
                            assign_content_id(value, label, content_id)
                elif isinstance(node, list):
                    for item in node:
                        assign_content_id(item, label, content_id)

            assign_content_id(populated_template[0]["flexNode"], "hero", hero_banner)
            assign_content_id(populated_template[0]["flexNode"], "rtb1", rtb1)
            assign_content_id(populated_template[0]["flexNode"], "rtb2", rtb2)
            assign_content_id(populated_template[0]["flexNode"], "rtb3", rtb3)
            assign_content_id(populated_template[0]["flexNode"], "tile1", tile1)
            assign_content_id(populated_template[0]["flexNode"], "tile2", tile2)

            # Optional: display preview in UI
            st.subheader("🔍 Preview of Generated JSON")
            st.json(populated_template)

            # Download button
            json_str = json.dumps(populated_template, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="generated_template.json", mime="application/json")
    except Exception as e:
        st.error(f"⚠️ Error generating template: {repr(e)}")
