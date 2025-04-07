
import streamlit as st
import json
import copy

st.set_page_config(layout="centered")

# --- Styling ---
st.markdown(
    """
    <div style="background-color: #00355F; padding: 20px 10px; border-radius: 8px; text-align: center;">
        <h1 style="color: white; font-size: 36px;">✈️ WLT Template Generator</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# --- Template Selection ---
template_type = st.selectbox("Select Template Type", ["WLT Landing Page Template", "WLT Curated Trips Template"])

st.write("")

# --- Static Fields ---
st.subheader("Basic Information")
template_name = st.text_input("Template Name", help="This will be the internal name for your template.")
page_title = st.text_input("Page Title", help="Displayed in the browser tab or page header.")
header_text = st.text_input("Header", help="Main heading of the page.")
brand = st.text_input("Brand", help="The Expedia Group brand this template is for.")
pos = st.text_input("POS (Point of Sale)", help="E.g., EXPEDIA_US or HOTELS_COM_AU.")
locale = st.text_input("Locale", help="E.g., EN_US, FR_FR.")

st.markdown("---")

# --- Content ID Fields ---
st.subheader("Content IDs")

# LANDING PAGE MAPPING
landing_page_content_ids = {
    "Hero Banner Content ID": "Hero Full Bleed Banner",
    "RTB 1 Content ID": "RTB 1",
    "RTB 2 Content ID": "RTB 2",
    "RTB 3 Content ID": "RTB 3",
    "Tile 1 Content ID": "Tile 1",
    "Tile 2 Content ID": "Tile 2"
}

landing_inputs = {}

if template_type == "WLT Landing Page Template":
    for label in landing_page_content_ids:
        landing_inputs[label] = st.text_input(label, help=f"Content ID for {label}")

# --- Upload Base Template ---
st.markdown("---")
st.subheader("Upload Base Template")
uploaded_file = st.file_uploader("Upload your base JSON file", type=["json"])
base_template = None

if uploaded_file:
    try:
        base_template = json.load(uploaded_file)
        st.success("Base template loaded successfully.")
    except Exception as e:
        st.error(f"Error loading JSON: {e}")

# --- Generate JSON ---
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

            def insert_content_id(node, region_name, content_id):
                if isinstance(node, dict):
                    if node.get("attributes"):
                        for attr in node["attributes"]:
                            if attr["name"] == "name" and attr["value"] == region_name:
                                # insert into module with contentId inside this region
                                for child in node.get("childNodes", []):
                                    for mod_attr in child.get("attributes", []):
                                        if mod_attr["name"] == "contentId":
                                            mod_attr["value"] = content_id
                    for child in node.get("childNodes", []):
                        insert_content_id(child, region_name, content_id)
                elif isinstance(node, list):
                    for item in node:
                        insert_content_id(item, region_name, content_id)

            # Insert Landing Page Content IDs
            if template_type == "WLT Landing Page Template":
                for label, region in landing_page_content_ids.items():
                    insert_content_id(populated_template[0]["flexNode"], region, landing_inputs[label])

            json_str = json.dumps(populated_template, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="generated_template.json", mime="application/json")
    except Exception as e:
        st.error(f"⚠️ Error generating template: {repr(e)}")
