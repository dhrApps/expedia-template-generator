
import streamlit as st
import json
import copy

# Set page config
st.set_page_config(page_title="WLT Template Generator", layout="centered")

# --- Header with Travel Theme ---
st.markdown(
    "<div style='background-color:#00355F;padding:20px;border-radius:8px;'>"
    "<h1 style='color:white;text-align:center;'>✈️ WLT Template Generator</h1>"
    "</div>",
    unsafe_allow_html=True
)

# --- Template Selection ---
template_type = st.selectbox("Select Template Type", ["WLT Landing Page Template", "WLT Curated Trips Template"])

# --- Shared Fields ---
st.subheader("Template Details")
template_name = st.text_input("Template Name", help="This is the internal name of the template")
page_title = st.text_input("Page Title", help="The main page title shown in the browser tab")
header_text = st.text_input("Header", help="The main heading displayed at the top of the page")
brand = st.text_input("Brand", help="The brand code, e.g., GPS")
pos = st.text_input("POS", help="Point of sale, e.g., PHILIPPINEAIRLINES_PH")
locale = st.text_input("Locale", help="Language/Region setting, e.g., EN_PH")

# --- Load Base Template ---
base_template = None
try:
    with open("fixed_base_template.json", "r") as f:
        base_template = json.load(f)
except Exception as e:
    st.error("Base template not found or invalid.")

# --- Dynamic Content ID Fields ---
st.markdown("---")
st.subheader("Content IDs")

if template_type == "WLT Landing Page Template":
    hero_banner = st.text_input("Hero Banner Content ID", help="Used for the main hero image/banner shown at the top of the landing page, typically on desktop devices.")
    rtb1 = st.text_input("RTB 1 Content ID", help="Content ID for the first 'Reason To Believe' section.")
    rtb2 = st.text_input("RTB 2 Content ID", help="Content ID for the second 'Reason To Believe' section.")
    rtb3 = st.text_input("RTB 3 Content ID", help="Content ID for the third 'Reason To Believe' section.")
    tile1 = st.text_input("Tile 1 Content ID", help="Content ID for the first editorial tile (left).")
    tile2 = st.text_input("Tile 2 Content ID", help="Content ID for the second editorial tile (right).")
elif template_type == "WLT Curated Trips Template":
    curated1 = st.text_input("Curated Section Header 1 Content ID", help="The first subheading for curated trip recommendations.")
    curated2 = st.text_input("Curated Section Header 2 Content ID", help="The second subheading for curated trip recommendations.")
    curated3 = st.text_input("Curated Section Header 3 Content ID", help="The third subheading for curated trip recommendations.")
    hero = st.text_input("Hero Banner Content ID", help="Used for the main hero image/banner shown at the top of the landing page, typically on desktop devices.")
    intro = st.text_input("Body Copy Introduction Content ID", help="Introductory paragraph or text block that appears below the title.")
    title = st.text_input("Body Copy Title Content ID", help="Headline or main title text that introduces the body content section.")
    author = st.text_input("Author Attribution Content ID", help="Author name or contributor details, typically displayed at the bottom of body content.")
    incentive = st.text_input("Body Copy Incentive Content ID", help="A promotional block or message containing incentive details, e.g., gift card rewards.")
    terms = st.text_input("Terms & Conditions Content ID", help="Legal or disclaimers associated with the curated trips or promotions on the page.")

# --- Generate JSON ---
if st.button("Generate Template JSON"):
    if not base_template:
        st.error("Base template could not be loaded.")
    else:
        try:
            data = copy.deepcopy(base_template)
            data[0]["name"] = template_name
            data[0]["title"] = page_title
            data[0]["header"] = header_text
            data[0]["brand"] = brand
            data[0]["pos"] = pos
            data[0]["locale"] = locale

            if template_type == "WLT Landing Page Template":
                data[0]["heroBannerContentId"] = hero_banner
                data[0]["rtb1ContentId"] = rtb1
                data[0]["rtb2ContentId"] = rtb2
                data[0]["rtb3ContentId"] = rtb3
                data[0]["tile1ContentId"] = tile1
                data[0]["tile2ContentId"] = tile2

            json_str = json.dumps(data, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="generated_template.json", mime="application/json")
        except Exception as e:
            st.error(f"An error occurred while generating the JSON: {e}")
