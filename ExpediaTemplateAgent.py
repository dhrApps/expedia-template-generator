
import streamlit as st
import json
import datetime
from io import BytesIO

st.set_page_config(page_title="Expedia Landing Page Template Generator", page_icon="🌍")

st.title("🌍 Expedia Landing Page Template Generator")
st.markdown("""
Welcome to the **Landing Page Template Generator!** ✈️🏝️

This tool helps you generate a fully structured **Landing Page Template JSON** with your content pre-populated.

📂 **Workflow:**
1. Enter Template Name and Page Title.
2. Select Lines of Business.
3. Enter Content IDs for each section.
4. Download the final template ready for upload.
--- 
""")

# Load fixed base JSON
with open("fixed_base_template.json", "r") as f:
    base_template = json.load(f)

# Step 1: Template Name and Page Title
st.header("Step 1: Template Info")
template_name = st.text_input("Template Name", placeholder="e.g., Luxury Escapes Homepage")
page_title = st.text_input("Page Title", placeholder="e.g., Book Your Luxury Escape Today")

# Step 2: Lines of Business
st.header("Step 2: Choose Lines of Business")
selected_lobs = st.multiselect(
    "Select the Lines of Business to display:",
    options=["Stays", "Packages", "Things To Do", "Flights", "Cars", "Cruises"]
)

# Step 3: Content IDs with helper tooltips
st.header("Step 3: Enter Content IDs")
st.markdown("Please enter the **Content ID** for each section below.")

content_ids = {}
content_ids['hero_banner'] = st.text_input("Hero Banner Content ID", placeholder="Big banner at top of the page with CTA")
content_ids['rtb_1'] = st.text_input("RTB 1 Content ID", placeholder="First text block under banner (e.g., trust message)")
content_ids['rtb_2'] = st.text_input("RTB 2 Content ID (optional)", placeholder="Second text block (optional)")
content_ids['rtb_3'] = st.text_input("RTB 3 Content ID", placeholder="Third text block (e.g., help center CTA)")
content_ids['tile_1'] = st.text_input("Tile 1 Content ID", placeholder="Left-side card (e.g., featured destination)")
content_ids['tile_2'] = st.text_input("Tile 2 Content ID", placeholder="Right-side card (e.g., flexible booking promo)")

# Content ID validation
def is_valid_id(cid):
    return cid.strip().isdigit() if cid else True

valid_ids = all(is_valid_id(cid) for cid in content_ids.values())

if not valid_ids:
    st.warning("⚠️ All Content IDs must be numeric.")

# Generate JSON
if st.button("Generate Template JSON") and template_name and page_title and valid_ids:
    populated_template = base_template.copy()
    populated_template["templateName"] = template_name
    populated_template["pageTitle"] = page_title

    # Populate content IDs into modules
    for module in populated_template["flexNode"]["children"]:
        if module.get("meta", {}).get("moduleType") == "FullBleedImageCard":
            module["meta"]["contentId"] = int(content_ids["hero_banner"])
        elif module.get("meta", {}).get("moduleType") == "FreeText":
            idx = populated_template["flexNode"]["children"].index(module)
            if idx == 1 and content_ids["rtb_1"]:
                module["meta"]["contentId"] = int(content_ids["rtb_1"])
            elif idx == 2 and content_ids["rtb_2"]:
                module["meta"]["contentId"] = int(content_ids["rtb_2"])
            elif idx == 3 and content_ids["rtb_3"]:
                module["meta"]["contentId"] = int(content_ids["rtb_3"])
        elif module.get("meta", {}).get("moduleType") == "CanvasGroup":
            tiles = module.get("meta", {}).get("children", [])
            if len(tiles) > 0 and content_ids["tile_1"]:
                tiles[0]["meta"]["contentId"] = int(content_ids["tile_1"])
            if len(tiles) > 1 and content_ids["tile_2"]:
                tiles[1]["meta"]["contentId"] = int(content_ids["tile_2"])
    
    # Adjust Main Wizard based on Lines of Business
    for module in populated_template["flexNode"]["children"]:
        if module.get("meta", {}).get("moduleType") == "MainWizard":
            lob_tiles = []
            lob_content_map = {
                "Stays": "Stays Card",
                "Packages": "Packages Card",
                "Things To Do": "Things To Do Card",
                "Flights": "Flights Card",
                "Cars": "Cars Card",
                "Cruises": "Cruises Card"
            }
            for lob in selected_lobs:
                lob_tiles.append({"meta": {"title": lob_content_map[lob]}})
            module["meta"]["children"] = lob_tiles

    # Prepare JSON for download
    output = BytesIO()
    json_bytes = json.dumps(populated_template, indent=2).encode('utf-8')
    output.write(json_bytes)
    output.seek(0)
    st.download_button("📥 Download Template JSON", data=output, file_name=f"{template_name.replace(' ', '_')}.json", mime="application/json")
    st.success("✅ Your landing page template JSON is ready for upload!")

st.markdown("---")
st.caption("Expedia Template Generator | Powered by Streamlit")
