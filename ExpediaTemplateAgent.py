
import streamlit as st
import json

# Set page layout and title
st.set_page_config(layout="centered")
st.markdown("""
<div style='padding: 20px; background-color: #00355F; border-radius: 10px;'>
<h1 style='color: white; display: flex; align-items: center; gap: 10px;'>
    ✈️ WLT Template Generator
</h1>
</div>
""", unsafe_allow_html=True)

# Dropdown for selecting template type
template_type = st.selectbox("Select Template Type", ["WLT Landing Page Template", "WLT Curated Trips Template"])

# Basic Inputs
st.markdown("### Template Metadata")
template_name = st.text_input("Template Name", help="Internal name for the template")
page_title = st.text_input("Page Title", help="Page title shown in the browser tab")
header_text = st.text_input("Header Text", help="Main header displayed on the page")
brand = st.text_input("Brand", help="Brand code used internally (e.g. 'EPS')")
pos = st.text_input("POS", help="Point of Sale (e.g. 'US')")
locale = st.text_input("Locale", help="Locale code (e.g. 'en_US')")

# Curated Trips Content ID UI Labels & Tooltips
curated_content_fields = [
    ("Hero Banner Content ID", "Used for the main hero image/banner shown at the top of the landing page, typically on desktop devices."),
    ("Body Copy Title Content ID", "Headline or main title text that introduces the body content section."),
    ("Body Copy Introduction Content ID", "Introductory paragraph or text block that appears below the title, giving context or engaging copy."),
    ("Curated Section Header 1 Content ID", "The first subheading for curated trip recommendations."),
    ("Curated Section Header 2 Content ID", "The second subheading for curated trip recommendations."),
    ("Curated Section Header 3 Content ID", "The third subheading for curated trip recommendations."),
    ("Body Copy Incentive Content ID", "A promotional block or message containing incentive details, e.g., gift card rewards."),
    ("Author Attribution Content ID", "Author name or contributor details, typically displayed at the bottom of body content."),
    ("Terms & Conditions Content ID", "Legal or disclaimers associated with the curated trips or promotions on the page.")
]

# Landing Page Content ID UI Labels & Tooltips
landing_page_content_fields = [
    ("Hero Banner Content ID", "Content ID for the top banner region."),
    ("RTB 1 Content ID", "Content ID for the first 'Reason to Believe' tile."),
    ("RTB 2 Content ID", "Content ID for the second 'Reason to Believe' tile."),
    ("RTB 3 Content ID", "Content ID for the third 'Reason to Believe' tile."),
    ("Tile 1 Content ID", "Content ID for the first editorial tile."),
    ("Tile 2 Content ID", "Content ID for the second editorial tile.")
]

# Show Content ID Fields Dynamically
st.markdown("### Content IDs")
content_ids = {}
selected_fields = landing_page_content_fields if template_type == "WLT Landing Page Template" else curated_content_fields
for label, tooltip in selected_fields:
    content_ids[label] = st.text_input(label, help=tooltip)

# Generate JSON Button
if st.button("Generate Template JSON"):
    try:
        if template_type == "WLT Landing Page Template":
            # Load base template
            with open("fixed_base_template.json") as f:
                base_template = json.load(f)

            # Populate metadata
            base_template[0]["name"] = template_name
            base_template[0]["title"] = page_title
            base_template[0]["header"] = header_text
            base_template[0]["brand"] = brand
            base_template[0]["pos"] = pos
            base_template[0]["locale"] = locale

            # Region mapping logic
            name_to_content_id = {
                "Hero Full Bleed Banner": content_ids.get("Hero Banner Content ID"),
                "RTB 1": content_ids.get("RTB 1 Content ID"),
                "RTB 2": content_ids.get("RTB 2 Content ID"),
                "RTB 3": content_ids.get("RTB 3 Content ID"),
                "Tile 1": content_ids.get("Tile 1 Content ID"),
                "Tile 2": content_ids.get("Tile 2 Content ID")
            }

            def apply_content_ids(node):
                if isinstance(node, dict):
                    if node.get("type") == "REGION":
                        name_attr = next((attr for attr in node.get("attributes", []) if attr["name"] == "name"), None)
                        if name_attr and name_attr["value"] in name_to_content_id:
                            for child in node.get("childNodes", []):
                                if child["type"] == "MODULE":
                                    for attr in child["attributes"]:
                                        if attr["name"] == "contentId":
                                            attr["value"] = name_to_content_id[name_attr["value"]]
                    for k, v in node.items():
                        apply_content_ids(v)
                elif isinstance(node, list):
                    for item in node:
                        apply_content_ids(item)

            apply_content_ids(base_template[0]["flexNode"])

            json_str = json.dumps(base_template, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="generated_template.json", mime="application/json")

        elif template_type == "WLT Curated Trips Template":
            with open("exportedTemplates-47495.json") as f:
                curated_template = json.load(f)

            label_to_content_id = {
                "HERO - Desktop": content_ids.get("Hero Banner Content ID"),
                "Body Copy - Title": content_ids.get("Body Copy Title Content ID"),
                "Body Copy Intro": content_ids.get("Body Copy Introduction Content ID"),
                "Curated Headline 1": content_ids.get("Curated Section Header 1 Content ID"),
                "Curated Headline 2": content_ids.get("Curated Section Header 2 Content ID"),
                "Curated Headline 3": content_ids.get("Curated Section Header 3 Content ID"),
                "Body Copy + 50 GC": content_ids.get("Body Copy Incentive Content ID"),
                "Body Copy - Author": content_ids.get("Author Attribution Content ID"),
                "Curated Trips - Terms and Conditions": content_ids.get("Terms & Conditions Content ID")
            }

            def replace_content_ids_curated(node):
                if isinstance(node, dict):
                    attributes = node.get("attributes", [])
                    for attr in attributes:
                        if attr.get("name") == "contentId":
                            label_attr = next((a for a in attributes if a["name"] == "label"), None)
                            if label_attr:
                                label_value = label_attr["value"]
                                if label_value in label_to_content_id:
                                    attr["value"] = label_to_content_id[label_value]
                    for v in node.values():
                        replace_content_ids_curated(v)
                elif isinstance(node, list):
                    for item in node:
                        replace_content_ids_curated(item)

            replace_content_ids_curated(curated_template)
            json_str = json.dumps(curated_template, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="curated_trips_template.json", mime="application/json")

    except Exception as e:
        st.error(f"Error: {e}")
