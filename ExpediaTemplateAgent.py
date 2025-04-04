
import streamlit as st
import json

# Title
st.title("Expedia Template JSON Generator")

# Input fields with tooltips
template_name = st.text_input("Template Name", help="The internal name of the template.")
page_title = st.text_input("Page Title", help="Displayed in browser tab and SEO metadata.")
header_text = st.text_input("Header", help="Main heading text on the page.")

brand = st.text_input("Brand", help="Brand identifier, e.g., 'GPS'.")
pos = st.text_input("POS", help="Point of Sale identifier, e.g., 'PHILIPPINEAIRLINES_PH'.")
locale = st.text_input("Locale", help="Locale code, e.g., 'EN_PH'.")

hero_banner = st.text_input("Hero Banner Content ID", help="Content ID for the Hero Full Bleed Banner region.")
rtb1 = st.text_input("RTB 1 Content ID", help="Content ID for the RTB 1 region.")
rtb2 = st.text_input("RTB 2 Content ID", help="Content ID for the RTB 2 region.")
rtb3 = st.text_input("RTB 3 Content ID", help="Content ID for the RTB 3 region.")
tile1 = st.text_input("Tile 1 Content ID", help="Content ID for the Tile 1 region.")
tile2 = st.text_input("Tile 2 Content ID", help="Content ID for the Tile 2 region.")

# Upload base template
base_template_file = st.file_uploader("Upload Base Template JSON", type="json")

def update_content_id_in_region(region, target_name, content_id_value):
    if region.get("attributes"):
        for attr in region["attributes"]:
            if attr["name"] == "name" and attr["value"] == target_name:
                # Found the region. Look for the contentId inside its modules
                for node in region.get("childNodes", []):
                    if node["type"] == "MODULE":
                        for attr in node.get("attributes", []):
                            if attr["name"] == "contentId":
                                attr["value"] = content_id_value
                    elif node["type"] == "REGION":
                        # For nested regions (e.g., Tile 1)
                        update_content_id_in_region(node, target_name, content_id_value)

def inject_content_ids(template, mappings):
    layout_node = template[0]["flexNode"]
    regions = layout_node.get("childNodes", [])
    for region in regions:
        for target_name, content_id in mappings.items():
            update_content_id_in_region(region, target_name, content_id)

# Generate JSON
if st.button("Generate Template JSON"):
    try:
        if base_template_file:
            base_template = json.load(base_template_file)
            populated_template = base_template.copy()
            populated_template[0]["name"] = template_name
            populated_template[0]["title"] = page_title
            populated_template[0]["header"] = header_text
            populated_template[0]["brand"] = brand
            populated_template[0]["pos"] = pos
            populated_template[0]["locale"] = locale

            # Assign content IDs in both fields and JSON structure
            populated_template[0]["heroBannerContentId"] = hero_banner
            populated_template[0]["rtb1ContentId"] = rtb1
            populated_template[0]["rtb2ContentId"] = rtb2
            populated_template[0]["rtb3ContentId"] = rtb3
            populated_template[0]["tile1ContentId"] = tile1
            populated_template[0]["tile2ContentId"] = tile2

            inject_content_ids(populated_template, {
                "Hero Full Bleed Banner": hero_banner,
                "RTB 1": rtb1,
                "RTB 2": rtb2,
                "RTB 3": rtb3,
                "Tile 1": tile1,
                "Tile 2": tile2,
            })

            json_str = json.dumps(populated_template, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="generated_template.json", mime="application/json")
    except Exception as e:
        st.error(f"⚠️ Error generating template: {repr(e)}")
