import streamlit as st
import json

try:
    with open("fixed_base_template.json", "r") as f:
        base_template = json.load(f)
        st.success("✅ Base template loaded successfully.")
except Exception as e:
    st.error(f"⚠️ Failed to load base template: {repr(e)}")
    base_template = []

st.title("🌍 Expedia Landing Page Template Generator")
st.write("Create a fully structured landing page template with ease. Fill in the content IDs and download a ready-to-upload JSON.")

template_name = st.text_input("Template Name", help="Unique and descriptive name.")
page_title = st.text_input("Page Title", help="Title shown on browser tab and search engines.")
lob_options = ["Stays", "Packages", "Things to Do", "Cars", "Flights"]
selected_lob = st.selectbox("Line of Business", options=lob_options)

st.subheader("📋 Component Prompts (with helper tooltips)")
hero_banner = st.text_input("Hero Banner Content ID", help="Big banner at top of page with CTA")
rtb1 = st.text_input("RTB 1 Content ID", help="First text block under banner (e.g., trust message)")
rtb2 = st.text_input("RTB 2 Content ID", help="Second text block (optional)")
rtb3 = st.text_input("RTB 3 Content ID", help="Third text block (e.g., help center CTA)")
tile1 = st.text_input("Tile 1 Content ID", help="Left-side card (e.g., featured destination)")
tile2 = st.text_input("Tile 2 Content ID", help="Right-side card (e.g., flexible booking promo)")

if st.button("Generate Template JSON"):
    try:
        populated = base_template[0]
        populated["name"] = template_name
        populated["title"] = page_title
        populated["lineOfBusiness"] = selected_lob.lower()

        module_node = populated["flexNode"]["childNodes"][0]["childNodes"][0]
        module_node["attributes"].append({"name": "contentId", "value": hero_banner})

        populated_json_str = json.dumps([populated], indent=2)
        st.download_button("📥 Download JSON", populated_json_str, file_name=f"{template_name}.json", mime="application/json")
    except Exception as e:
        st.error(f"⚠️ Error generating template: {repr(e)}")
