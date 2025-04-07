
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
    st.markdown("##### 🔹 Landing Page Content ID Label Mapping")
    content_ids["hero_banner"] = st.text_input("Hero Banner Content ID", help="Big banner at top of the page with CTA")
    content_ids["rtb1"] = st.text_input("RTB 1 Content ID", help="First row of supporting features")
    content_ids["rtb2"] = st.text_input("RTB 2 Content ID", help="Second row of supporting features")
    content_ids["rtb3"] = st.text_input("RTB 3 Content ID", help="Third row of supporting features")
    content_ids["tile1"] = st.text_input("Tile 1 Content ID", help="Left tile in grid layout")
    content_ids["tile2"] = st.text_input("Tile 2 Content ID", help="Right tile in grid layout")
elif template_type == "WLT Curated Trips Template":
    st.markdown("##### 🌍 Curated Trips Content ID Label Mapping")
    content_ids["hero_desktop"] = st.text_input("Hero Banner Content ID (HERO - Desktop)", help="Main hero image shown on desktop")
    content_ids["body_title"] = st.text_input("Body Copy Title Content ID (Body Copy - Title)", help="Main title for the body section")
    content_ids["body_intro"] = st.text_input("Body Copy Introduction Content ID (Body Copy Intro)", help="Introductory paragraph below title")
    content_ids["headline1"] = st.text_input("Curated Section Header 1 Content ID (Curated Headline 1)", help="First heading for trip section")
    content_ids["headline2"] = st.text_input("Curated Section Header 2 Content ID (Curated Headline 2)", help="Second heading for trip section")
    content_ids["headline3"] = st.text_input("Curated Section Header 3 Content ID (Curated Headline 3)", help="Third heading for trip section")
    content_ids["body_incentive"] = st.text_input("Body Copy Incentive Content ID (Body Copy + 50 GC)", help="Promo block with incentive info")
    content_ids["author"] = st.text_input("Author Attribution Content ID (Body Copy - Author)", help="Name or contributor shown below body")
    content_ids["tnc"] = st.text_input("Terms & Conditions Content ID (Curated Trips - Terms and Conditions)", help="Terms/disclaimers shown")

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
