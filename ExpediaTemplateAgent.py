
import streamlit as st
import json

# Custom-styled Title with Expedia Group theme

    # Template Type Selector
    template_type = st.selectbox("Select Template Type", ["WLT Landing Page Template", "WLT Curated Trips Template"])

    st.markdown("---")
    st.subheader("Content IDs")

    if template_type == "WLT Landing Page Template":
        st.text_input("Hero Banner Content ID", key="hero_banner", help="Used for the main hero image/banner shown at the top of the landing page, typically on desktop devices.")
        st.text_input("RTB 1 Content ID", key="rtb1", help="First Reasons-To-Believe block.")
        st.text_input("RTB 2 Content ID", key="rtb2", help="Second Reasons-To-Believe block.")
        st.text_input("RTB 3 Content ID", key="rtb3", help="Third Reasons-To-Believe block.")
        st.text_input("Tile 1 Content ID", key="tile1", help="First tile image or block in the layout.")
        st.text_input("Tile 2 Content ID", key="tile2", help="Second tile image or block in the layout.")

    elif template_type == "WLT Curated Trips Template":
        st.text_input("Hero Banner Content ID (HERO - Desktop)", key="hero_banner_ct", help="Used for the main hero image/banner shown at the top of the curated trips page.")
        st.text_input("Body Copy Title Content ID (Body Copy - Title)", key="body_title_ct", help="Headline or main title text that introduces the body content section.")
        st.text_input("Body Copy Introduction Content ID (Body Copy Intro)", key="body_intro_ct", help="Introductory paragraph or text block that appears below the title.")
        st.text_input("Curated Section Header 1 Content ID (Curated Headline 1)", key="headline1_ct", help="The first subheading for curated trip recommendations.")
        st.text_input("Curated Section Header 2 Content ID (Curated Headline 2)", key="headline2_ct", help="The second subheading for curated trip recommendations.")
        st.text_input("Curated Section Header 3 Content ID (Curated Headline 3)", key="headline3_ct", help="The third subheading for curated trip recommendations.")
        st.text_input("Body Copy Incentive Content ID (Body Copy + 50 GC)", key="incentive_ct", help="A promotional block or message containing incentive details, e.g., gift card rewards.")
        st.text_input("Author Attribution Content ID (Body Copy - Author)", key="author_ct", help="Author name or contributor details.")
        st.text_input("Terms & Conditions Content ID (Curated Trips - Terms and Conditions)", key="terms_ct", help="Legal or disclaimers associated with the curated trips.")


st.markdown("""
<h1 style='color: #00355F; text-align: center; font-size: 2.5em; font-weight: bold;'>
✈️ WLT Template Generator
</h1>
""", unsafe_allow_html=True)


# Template type selection
st.markdown("### --- Template Type Selection ---")
template_type = st.selectbox(
    "Select Template Type",
    ["WLT Landing Page Template", "WLT Curated Trips Template"],
    help="Choose the template structure you want to generate"
)
# User Inputs with help text and NO default values
template_name = st.text_input("Template Name", help="Enter a unique name for this template.")
page_title = st.text_input("Page Title", help="Displayed as the main title on the landing page.")
header_text = st.text_input("Header Text", help="Header displayed at the top of the landing page.")

brand = st.text_input("Brand", help="Brand identifier, e.g., GPS or WLT.")
pos = st.text_input("POS", help="Point of Sale identifier, e.g., CATHAYPACIFIC_HK.")
locale = st.text_input("Locale", help="Locale code, e.g., en_HK.")

st.markdown("---")
st.subheader("Content IDs")

hero_banner = st.text_input("Hero Banner Content ID", help="Content ID for the hero banner at the top of the page.")
rtb1 = st.text_input("Reason To Believe 1 (RTB 1) Content ID", help="Content ID for the first RTB section.")
rtb2 = st.text_input("Reason To Believe 2 (RTB 2) Content ID", help="Content ID for the second RTB section.")
rtb3 = st.text_input("Reason To Believe 3 (RTB 3) Content ID", help="Content ID for the third RTB section.")
tile1 = st.text_input("Canvas Group Tile 1 Content ID", help="Content ID for the first tile in the canvas group.")
tile2 = st.text_input("Canvas Group Tile 2 Content ID", help="Content ID for the second tile in the canvas group.")

# Load base template
base_template = None
try:
    with open("fixed_base_template.json") as f:
        base_template = json.load(f)
except Exception as e:
    st.error(f"⚠️ Error loading base template: {repr(e)}")

# Content ID Mapping Function
def assign_content_ids(flex_node, region_map):
    if flex_node.get("type") == "REGION":
        region_name = next((a["value"] for a in flex_node.get("attributes", []) if a["name"] == "name"), "")
        if region_name in region_map:
            for module in flex_node.get("childNodes", []):
                if module.get("type") == "MODULE":
                    for attr in module.get("attributes", []):
                        if attr["name"] == "contentId":
                            attr["value"] = region_map[region_name]
    for child in flex_node.get("childNodes", []):
        assign_content_ids(child, region_map)

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

            region_content_map = {
                "Hero Full Bleed Banner": hero_banner,
                "RTB 1": rtb1,
                "RTB 2": rtb2,
                "RTB 3": rtb3,
                "Tile 1": tile1,
                "Tile 2": tile2
            }

            assign_content_ids(populated_template[0]["flexNode"], region_content_map)

            # Show preview
            st.subheader("🔍 Preview of Generated JSON")
            st.json(populated_template)

            # Allow download
            json_str = json.dumps(populated_template, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="generated_template.json", mime="application/json")
    except Exception as e:
        st.error(f"⚠️ Error generating template: {repr(e)}")
