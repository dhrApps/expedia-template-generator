
import streamlit as st
import json
import copy

st.set_page_config(layout="centered")

# ======================== HEADER ========================
st.markdown(
    "<h1 style='color:#00355F; font-size: 3em;'>✈️ WLT Template Generator</h1>",
    unsafe_allow_html=True
)

# ======================== TEMPLATE TYPE ========================
template_type = st.selectbox(
    "Select Template Type",
    ["WLT Landing Page Template", "WLT Curated Trips Template"],
    help="Choose the template structure you want to generate"
)

# ======================== COMMON USER INPUT FIELDS ========================
st.markdown("---")
st.markdown("### Template Information")

template_name = st.text_input("Template Name", help="Internal name to identify this template.")
page_title = st.text_input("Page Title", help="Title that appears in the browser tab or search results.")
header_text = st.text_input("Page Header", help="Main header text shown at the top of the landing page.")
brand = st.text_input("Brand", help="Brand identifier (e.g., 'GPS', 'EAP')")
pos = st.text_input("POS", help="Point of sale identifier (e.g., 'JAPAN_JP', 'PHILIPPINES_PH')")
locale = st.text_input("Locale", help="Locale identifier (e.g., 'EN_JP', 'EN_PH')")

# ======================== CONTENT ID SECTION ========================
st.markdown("---")
st.markdown("### Content IDs")

# Initialize all fields as empty
hero_banner = rtb1 = rtb2 = rtb3 = tile1 = tile2 = ""

if template_type == "WLT Landing Page Template":
    hero_banner = st.text_input("Hero Banner Content ID", help="Used for the main hero image/banner shown at the top of the landing page, typically on desktop devices.")
    rtb1 = st.text_input("RTB 1 Content ID", help="Used for the first reason-to-book section.")
    rtb2 = st.text_input("RTB 2 Content ID", help="Used for the second reason-to-book section.")
    rtb3 = st.text_input("RTB 3 Content ID", help="Used for the third reason-to-book section.")
    tile1 = st.text_input("Tile 1 Content ID", help="Used for the first image tile in the tile section.")
    tile2 = st.text_input("Tile 2 Content ID", help="Used for the second image tile in the tile section.")

# ======================== JSON GENERATION ========================
st.markdown("---")
st.markdown("### Generate Template")

if st.button("Generate Template JSON"):
    try:
        with open("fixed_base_template.json", "r") as f:
            base_template = json.load(f)

        updated_template = copy.deepcopy(base_template)
        updated_template[0]["name"] = template_name
        updated_template[0]["title"] = page_title
        updated_template[0]["header"] = header_text
        updated_template[0]["brand"] = brand
        updated_template[0]["pos"] = pos
        updated_template[0]["locale"] = locale

        # Helper to assign content ID by region name
        def assign_content_id_by_region_name(node, region_name, content_id):
            if isinstance(node, dict):
                if node.get("type") == "REGION":
                    attributes = node.get("attributes", [])
                    for attr in attributes:
                        if attr.get("name") == "name" and attr.get("value") == region_name:
                            for child in node.get("childNodes", []):
                                if child.get("type") == "MODULE":
                                    for attr in child.get("attributes", []):
                                        if attr.get("name") == "contentId":
                                            attr["value"] = content_id
                for key in node:
                    assign_content_id_by_region_name(node[key], region_name, content_id)
            elif isinstance(node, list):
                for item in node:
                    assign_content_id_by_region_name(item, region_name, content_id)

        # Assign values
        assign_content_id_by_region_name(updated_template[0]["flexNode"], "Hero Full Bleed Banner", hero_banner)
        assign_content_id_by_region_name(updated_template[0]["flexNode"], "RTB 1", rtb1)
        assign_content_id_by_region_name(updated_template[0]["flexNode"], "RTB 2", rtb2)
        assign_content_id_by_region_name(updated_template[0]["flexNode"], "RTB 3", rtb3)
        assign_content_id_by_region_name(updated_template[0]["flexNode"], "Tile 1", tile1)
        assign_content_id_by_region_name(updated_template[0]["flexNode"], "Tile 2", tile2)

        final_output = json.dumps(updated_template, indent=4)
        st.download_button("📥 Download JSON", data=final_output, file_name="generated_template.json", mime="application/json")
    except Exception as e:
        st.error(f"⚠️ Error generating template: {repr(e)}")
