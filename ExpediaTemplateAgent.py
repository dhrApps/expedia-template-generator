
import streamlit as st
import json

st.set_page_config(layout="centered")

st.markdown("""
<div style="background-color:#00355F;padding:30px;border-radius:10px;margin-bottom:20px;">
    <h1 style="color:white;text-align:center;">Template Generator</h1>
</div>
""", unsafe_allow_html=True)

# Dropdown to choose template type
template_type = st.selectbox("Select Template Type", ["WLT Landing Page Template", "WLT Curated Trips Template"])

# Common input fields
st.subheader("Basic Configuration")
template_name = st.text_input("Template Name")
page_title = st.text_input("Page Title")
header_text = st.text_input("Header")
brand = st.text_input("Brand")
pos = st.text_input("POS")
locale = st.text_input("Locale")

# Content ID Section
st.markdown("---")
st.subheader("Content IDs")

# Define inputs based on template type
curated_trips_fields = {
    "Hero Banner Content ID (HERO - Desktop)": "",
    "Body Copy Title Content ID (Body Copy - Title)": "",
    "Body Copy Introduction Content ID (Body Copy Intro)": "",
    "Curated Section Header 1 Content ID (Curated Headline 1)": "",
    "Curated Section Header 2 Content ID (Curated Headline 2)": "",
    "Curated Section Header 3 Content ID (Curated Headline 3)": "",
    "Body Copy Incentive Content ID (Body Copy + 50 GC)": "",
    "Author Attribution Content ID (Body Copy - Author)": "",
    "Terms & Conditions Content ID (Curated Trips - Terms and Conditions)": ""
}

landing_page_fields = {
    "Hero Banner Content ID": "",
    "RTB 1 Content ID": "",
    "RTB 2 Content ID": "",
    "RTB 3 Content ID": "",
    "Tile 1 Content ID": "",
    "Tile 2 Content ID": ""
}

content_inputs = {}

if template_type == "WLT Landing Page Template":
    for label in landing_page_fields:
        content_inputs[label] = st.text_input(label)
elif template_type == "WLT Curated Trips Template":
    for label in curated_trips_fields:
        content_inputs[label] = st.text_input(label)

# Load Base Template
base_template = None
if template_type == "WLT Landing Page Template":
    with open("fixed_base_template.json") as f:
        base_template = json.load(f)
elif template_type == "WLT Curated Trips Template":
    with open("exportedTemplates-47495.json") as f:
        base_template = json.load(f)

def inject_content_ids_curated(json_obj, ui_inputs):
    mapping = {
        "HERO - Desktop": "Hero Banner Content ID (HERO - Desktop)",
        "Body Copy - Title": "Body Copy Title Content ID (Body Copy - Title)",
        "Body Copy Intro": "Body Copy Introduction Content ID (Body Copy Intro)",
        "Curated Headline 1": "Curated Section Header 1 Content ID (Curated Headline 1)",
        "Curated Headline 2": "Curated Section Header 2 Content ID (Curated Headline 2)",
        "Curated Headline 3": "Curated Section Header 3 Content ID (Curated Headline 3)",
        "Body Copy + 50 GC": "Body Copy Incentive Content ID (Body Copy + 50 GC)",
        "Body Copy - Author": "Author Attribution Content ID (Body Copy - Author)",
        "Curated Trips - Terms and Conditions": "Terms & Conditions Content ID (Curated Trips - Terms and Conditions)"
    }

    def recursive_update(node):
        if isinstance(node, dict):
            if node.get("type") == "REGION":
                region_name = next((a["value"] for a in node.get("attributes", []) if a["name"] == "name"), None)
                if region_name and region_name in mapping:
                    content_id_label = mapping[region_name]
                    content_id_value = ui_inputs.get(content_id_label)
                    if content_id_value:
                        for mod in node.get("childNodes", []):
                            if mod.get("type") == "MODULE":
                                for attr in mod.get("attributes", []):
                                    if attr.get("name") == "contentId":
                                        attr["value"] = content_id_value
            for v in node.values():
                recursive_update(v)
        elif isinstance(node, list):
            for item in node:
                recursive_update(item)

    recursive_update(json_obj)

# Button to generate and download JSON
st.markdown("---")
if st.button("Generate Template JSON"):
    try:
        populated_template = base_template.copy()

        # Update fields
        if template_type == "WLT Landing Page Template":
            populated_template[0]["name"] = template_name
            populated_template[0]["title"] = page_title
            populated_template[0]["header"] = header_text
            populated_template[0]["brand"] = brand
            populated_template[0]["pos"] = pos
            populated_template[0]["locale"] = locale

            populated_template[0]["heroBannerContentId"] = content_inputs["Hero Banner Content ID"]
            populated_template[0]["rtb1ContentId"] = content_inputs["RTB 1 Content ID"]
            populated_template[0]["rtb2ContentId"] = content_inputs["RTB 2 Content ID"]
            populated_template[0]["rtb3ContentId"] = content_inputs["RTB 3 Content ID"]
            populated_template[0]["tile1ContentId"] = content_inputs["Tile 1 Content ID"]
            populated_template[0]["tile2ContentId"] = content_inputs["Tile 2 Content ID"]

        elif template_type == "WLT Curated Trips Template":
            inject_content_ids_curated(populated_template, content_inputs)

        json_str = json.dumps(populated_template, indent=4)
        st.download_button("📥 Download JSON", data=json_str, file_name="generated_template.json", mime="application/json")
    except Exception as e:
        st.error(f"⚠️ Error generating template: {repr(e)}")
