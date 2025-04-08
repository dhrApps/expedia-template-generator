
import streamlit as st
import json

st.set_page_config(layout="wide")

# Title with emoji
st.markdown(
    "<h1 style='text-align: center; color: #00355F;'>✈️ WLT Template Generator</h1>",
    unsafe_allow_html=True
)

# Dropdown for template selection
template_type = st.selectbox(
    "Select Template Type",
    ["WLT Landing Page Template", "WLT Curated Trips Template"],
    help="Choose the template structure you want to generate"
)

# Common fields
st.markdown("### Template Details")
template_name = st.text_input("Template Name", help="A unique name for this template")
page_title = st.text_input("Page Title", help="Page title as seen in the browser tab")
header_text = st.text_input("Header", help="Main header displayed on the page")
brand = st.text_input("Brand", help="Brand associated with this template, e.g., GPS")
pos = st.text_input("POS", help="Point of sale, e.g., PHILIPPINEAIRLINES_PH")
locale = st.text_input("Locale", help="Locale setting, e.g., EN_PH")

# Conditional Content ID Fields
if template_type == "WLT Landing Page Template":
    st.markdown("### Content IDs (Landing Page)")
    hero_banner = st.text_input("Hero Banner Content ID", help="Used for the main hero image/banner shown at the top of the landing page, typically on desktop devices.")
    rtb1 = st.text_input("RTB 1 Content ID", help="Used for the first trust-building message or block")
    rtb2 = st.text_input("RTB 2 Content ID", help="Used for the second trust-building message or block")
    rtb3 = st.text_input("RTB 3 Content ID", help="Used for the third trust-building message or block")
    tile1 = st.text_input("Tile 1 Content ID", help="Used for the first tile, such as a featured trip")
    tile2 = st.text_input("Tile 2 Content ID", help="Used for the second tile, such as a supporting trip")

elif template_type == "WLT Curated Trips Template":
    st.markdown("### Content IDs (Curated Trips)")
    hero_banner = st.text_input("Hero Banner Content ID (HERO - Desktop)", help="Main hero image/banner shown at the top of the page")
    body_title = st.text_input("Body Copy Title Content ID (Body Copy - Title)", help="Headline or title of the body copy section")
    body_intro = st.text_input("Body Copy Introduction Content ID (Body Copy Intro)", help="Intro paragraph that follows the body copy title")
    curated_headline_1 = st.text_input("Curated Section Header 1 Content ID (Curated Headline 1)", help="First header in curated trips section")
    curated_headline_2 = st.text_input("Curated Section Header 2 Content ID (Curated Headline 2)", help="Second header in curated trips section")
    curated_headline_3 = st.text_input("Curated Section Header 3 Content ID (Curated Headline 3)", help="Third header in curated trips section")
    promo_block = st.text_input("Body Copy Incentive Content ID (Body Copy + 50 GC)", help="Incentive or promotional message")
    author = st.text_input("Author Attribution Content ID (Body Copy - Author)", help="Author name or credit line")
    terms = st.text_input("Terms & Conditions Content ID (Curated Trips - Terms and Conditions)", help="Legal terms and conditions")

# Load the correct base template
if template_type == "WLT Landing Page Template":
    json_path = "fixed_base_template.json"
    try:
        with open(json_path, "r") as f:
            base_template = json.load(f)
    except Exception as e:
        st.error(f"Failed to load base template: {e}")
        base_template = None
else:
    base_template = None  # Curated Trips not implemented yet

# Generate JSON Button
if template_type == "WLT Landing Page Template" and st.button("Generate Template JSON"):
    try:
        if base_template:
            updated = base_template.copy()
            updated[0]["name"] = template_name
            updated[0]["title"] = page_title
            updated[0]["header"] = header_text
            updated[0]["brand"] = brand
            updated[0]["pos"] = pos
            updated[0]["locale"] = locale

            # Walk the structure and insert contentId where needed based on region name
            def inject_content_id(node):
                if isinstance(node, dict):
                    if node.get("type") == "REGION":
                        region_name = ""
                        for attr in node.get("attributes", []):
                            if attr.get("name") == "name":
                                region_name = attr.get("value", "")
                                break
                        for child in node.get("childNodes", []):
                            if child.get("type") == "MODULE":
                                for attr in child.get("attributes", []):
                                    if attr.get("name") == "contentId":
                                        if region_name == "Hero Full Bleed Banner":
                                            attr["value"] = hero_banner
                                        elif region_name == "RTB 1":
                                            attr["value"] = rtb1
                                        elif region_name == "RTB 2":
                                            attr["value"] = rtb2
                                        elif region_name == "RTB 3":
                                            attr["value"] = rtb3
                                        elif region_name == "Tile 1":
                                            attr["value"] = tile1
                                        elif region_name == "Tile 2":
                                            attr["value"] = tile2
                    for child in node.get("childNodes", []):
                        inject_content_id(child)
                elif isinstance(node, list):
                    for item in node:
                        inject_content_id(item)

            inject_content_id(updated[0]["flexNode"]["childNodes"])
            json_str = json.dumps(updated, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="generated_template.json", mime="application/json")
    except Exception as e:
        st.error(f"⚠️ Error generating template: {repr(e)}")
