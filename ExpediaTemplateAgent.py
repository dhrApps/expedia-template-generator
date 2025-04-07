
import streamlit as st
import json
import base64

# Set page config
st.set_page_config(layout="wide")

# Custom title bar with Expedia Group branding and travel theme
st.markdown(
    '''
    <div style="background-color: #00355F; padding: 30px; border-radius: 8px; text-align: center;">
        <h1 style="color: white; font-size: 2.5em; margin: 0;">
            ✈️ WLT Template Generator
        </h1>
    </div>
    ''',
    unsafe_allow_html=True
)

# Template type selector
template_type = st.selectbox("Select Template Type", ["WLT Landing Page Template", "WLT Curated Trips Template"])

# Main form inputs
template_name = st.text_input("Template Name")
page_title = st.text_input("Page Title")
header_text = st.text_input("Header")
brand = st.text_input("Brand")
pos = st.text_input("POS")
locale = st.text_input("Locale")

# Add a divider and Content ID header
st.markdown("---")
st.subheader("Content IDs")

# Content ID inputs based on template type
if template_type == "WLT Landing Page Template":
    hero_banner = st.text_input("Hero Banner Content ID", help="Used for the main hero image/banner shown at the top of the landing page, typically on desktop devices.")
    rtb1 = st.text_input("RTB 1 Content ID", help="First block under 'Reasons to Believe' showing key message or value.")
    rtb2 = st.text_input("RTB 2 Content ID", help="Second block under 'Reasons to Believe'.")
    rtb3 = st.text_input("RTB 3 Content ID", help="Third block under 'Reasons to Believe'.")
    tile1 = st.text_input("Tile 1 Content ID", help="Left-side card-style image or message.")
    tile2 = st.text_input("Tile 2 Content ID", help="Right-side card-style image or message.")
else:
    hero_banner = st.text_input("Hero Banner Content ID", help="Main banner at the top of the Curated Trips page.")
    body_copy_title = st.text_input("Body Copy Title Content ID", help="Headline or main title introducing the curated trip section.")
    body_copy_intro = st.text_input("Body Copy Introduction Content ID", help="Introduction paragraph under the title.")
    curated_1 = st.text_input("Curated Section Header 1 Content ID", help="Subheading for the first curated trip section.")
    curated_2 = st.text_input("Curated Section Header 2 Content ID", help="Subheading for the second curated trip section.")
    curated_3 = st.text_input("Curated Section Header 3 Content ID", help="Subheading for the third curated trip section.")
    incentive = st.text_input("Body Copy + 50 GC Content ID", help="Promotional message or incentive copy (e.g., earn $50 gift card).")
    author = st.text_input("Author Attribution Content ID", help="Displays the contributor's or writer’s name.")
    terms = st.text_input("Terms & Conditions Content ID", help="Displays the T&Cs block at the bottom of the curated trips.")

# Load base template
base_template = None
try:
    with open("fixed_base_template.json", "r") as f:
        base_template = json.load(f)
except FileNotFoundError:
    st.warning("Base template file not found. Please ensure 'fixed_base_template.json' is in your repo.")

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

            if template_type == "WLT Landing Page Template":
                # Populate Landing Page Content IDs into both metadata and structure
                populated_template[0]["heroBannerContentId"] = hero_banner
                populated_template[0]["rtb1ContentId"] = rtb1
                populated_template[0]["rtb2ContentId"] = rtb2
                populated_template[0]["rtb3ContentId"] = rtb3
                populated_template[0]["tile1ContentId"] = tile1
                populated_template[0]["tile2ContentId"] = tile2

                def assign_content_id_by_region_name(node, mapping):
                    if isinstance(node, dict):
                        if node.get("type") == "REGION":
                            name_attr = next((a["value"] for a in node.get("attributes", []) if a["name"] == "name"), None)
                            if name_attr and name_attr in mapping:
                                module = next((c for c in node.get("childNodes", []) if c["type"] == "MODULE"), None)
                                if module:
                                    for attr in module["attributes"]:
                                        if attr["name"] == "contentId":
                                            attr["value"] = mapping[name_attr]
                        for child in node.get("childNodes", []):
                            assign_content_id_by_region_name(child, mapping)
                    elif isinstance(node, list):
                        for item in node:
                            assign_content_id_by_region_name(item, mapping)

                assign_content_id_by_region_name(
                    populated_template[0]["flexNode"],
                    {
                        "Hero Full Bleed Banner": hero_banner,
                        "RTB 1": rtb1,
                        "RTB 2": rtb2,
                        "RTB 3": rtb3,
                        "Tile 1": tile1,
                        "Tile 2": tile2
                    }
                )

            json_str = json.dumps(populated_template, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="generated_template.json", mime="application/json")
    except Exception as e:
        st.error(f"⚠️ Error generating template: {repr(e)}")
