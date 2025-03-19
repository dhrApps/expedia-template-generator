
import streamlit as st
import json
import datetime

st.set_page_config(page_title="Expedia Landing Page Template Generator", page_icon="🌍", layout="centered")

st.title("🌍 Expedia Landing Page Template Generator")
st.markdown("""
Welcome to the **Expedia Template Generator!** 🏝️✈️  
Generate a fully structured **Landing Page Template JSON** — with your content seamlessly pre-assigned.

---
**How it works:**
1. Select **Lines of Business** (Stays, Packages, etc.)
2. Enter your **Content IDs** for each section
3. Download your **ready-to-import JSON template**
---
""")

st.header("Step 1: Choose Lines of Business")
selected_lobs = st.multiselect(
    "Select the sections to include on your landing page:",
    options=["Stays", "Packages", "Things To Do", "Flights", "Cars", "Cruises"]
)

st.header("Step 2: Enter Template Name")
template_name = st.text_input("Template Name", placeholder="e.g., Luxury Escapes Homepage")

st.header("Step 3: Assign Content IDs")
st.markdown("Please enter the **Content ID** for each section below.")

content_ids = {}
content_ids['hero_banner'] = st.text_input("Hero Banner (Full Bleed Image Card)", placeholder="Big banner at top of the page with CTA")
content_ids['rtb_1'] = st.text_input("RTB 1", placeholder="First text block under banner (e.g., trust message)")
content_ids['rtb_2'] = st.text_input("RTB 2 (optional)", placeholder="Second text block (optional)")
content_ids['rtb_3'] = st.text_input("RTB 3", placeholder="Third text block (e.g., help center CTA)")
content_ids['tile_1'] = st.text_input("Tile 1", placeholder="Left-side card (e.g., featured destination)")
content_ids['tile_2'] = st.text_input("Tile 2", placeholder="Right-side card (e.g., flexible booking promo)")

def is_valid_content_id(cid):
    return cid.isdigit() if cid else True

valid_inputs = all(is_valid_content_id(cid) for cid in content_ids.values())

if not valid_inputs:
    st.warning("⚠️ Please ensure all Content IDs are numeric.")

if st.button("Generate Template JSON") and template_name and valid_inputs:
    base_template = {
        "template_name": template_name,
        "created_at": datetime.datetime.now().isoformat(),
        "lines_of_business": selected_lobs,
        "components": {
            "hero_banner": content_ids['hero_banner'],
            "rtb_1": content_ids['rtb_1'],
            "rtb_2": content_ids['rtb_2'],
            "rtb_3": content_ids['rtb_3'],
            "tile_1": content_ids['tile_1'],
            "tile_2": content_ids['tile_2']
        }
    }

    if not content_ids['rtb_2']:
        del base_template['components']['rtb_2']

    json_bytes = json.dumps(base_template, indent=2).encode('utf-8')
    st.download_button("Download JSON File", data=json_bytes, file_name=f"{template_name.replace(' ', '_')}.json", mime="application/json")
    st.success("✅ Your landing page template JSON is ready!")
    st.markdown("You can now upload this JSON to create your landing page.")

st.markdown("---")
st.caption("Expedia Template Generator | Powered by Streamlit")
