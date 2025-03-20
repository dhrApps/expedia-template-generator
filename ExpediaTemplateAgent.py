import streamlit as st
import json

# Load the corrected base JSON template
with open("fixed_base_template.json", "r") as f:
    base_template = json.load(f)

# Title
st.title("🌐 Expedia Landing Page Template Generator")

# Intro
st.write("Create a fully structured landing page template with ease. Fill in the content IDs and download a ready-to-upload JSON.")

# Input fields
template_name = st.text_input("Template Name", help="Give your template a unique and descriptive name.")
page_title = st.text_input("Page Title", help="This title appears on the browser tab and search engines.")

# Lines of Business selection
lob_options = ["Stays", "Packages", "Things to Do", "Cars", "Flights"]
selected_lob = st.selectbox("Line of Business", options=lob_options, help="Choose the Line of Business for which this landing page applies.")

# Component Content IDs with helper tooltips
st.subheader("📋 Component Prompts (with helper tooltips)")
hero_banner = st.text_input("Hero Banner Content ID", help="Big banner at top of the page with CTA")
rtb1 = st.text_input("RTB 1 Content ID", help="First text block under banner (e.g., trust message)")
rtb2 = st.text_input("RTB 2 Content ID", help="Second text block (optional)")
rtb3 = st.text_input("RTB 3 Content ID", help="Third text block (e.g., help center CTA)")
tile1 = st.text_input("Tile 1 Content ID", help="Left-side card (e.g., featured destination)")
tile2 = st.text_input("Tile 2 Content ID", help="Right-side card (e.g., flexible booking promo)")

# Button to generate JSON
if st.button("Generate Template JSON"):
    try:
        # Deep copy the base template to avoid altering original
        populated_template = json.loads(json.dumps(base_template))

        # Update template name and page title
        populated_template[0]["name"] = template_name
        populated_template[0]["title"] = page_title

        # Helper function to update contentId based on region name
        def update_content_id(region_name_match, new_content_id):
            for region in populated_template[0]["flexNode"]["childNodes"]:
                region_name = next((attr["value"] for attr in region["attributes"] if attr["name"] == "name"), "")
                if region_name == region_name_match:
                    # Find module inside this region
                    for module in region["childNodes"]:
                        for attr in module["attributes"]:
                            if attr["name"] == "contentId":
                                attr["value"] = new_content_id
                                return True
            return False

        # Map inputs to region names
        update_content_id("Test Full Bleed Image Card", hero_banner)
        update_content_id("Test RTB 1", rtb1)
        update_content_id("Test RTB 2", rtb2)
        update_content_id("Test RTB 3", rtb3)
        update_content_id("Tile 1", tile1)
        update_content_id("Tile 2", tile2)

        # Final JSON output
        json_output = json.dumps(populated_template, indent=4)
        st.download_button(
            label="Download JSON File",
            file_name=f"{template_name}_template.json",
            mime="application/json",
            data=json_output
        )
        st.success("Template JSON generated successfully! 🎉")

    except Exception as e:
    st.error(f"⚠️ Error generating template: {repr(e)}")
