import streamlit as st
import json

# Load base JSON template
with open("template_base.json", "r") as f:
    base_template = json.load(f)

st.title("📄 Expedia Landing Page Template Generator")
st.write("Easily generate your JSON template with content IDs for your landing page.")

# User inputs for template details
template_name = st.text_input("Template Name", placeholder="e.g., Luxury Escapes Homepage")
page_title = st.text_input("Page Title", placeholder="e.g., Luxury Escapes")

# Line of Business selection
lob_options = ["Stays", "Packages", "Things to Do", "Flights"]
selected_lobs = st.multiselect("Select Lines of Business", lob_options)

st.markdown("---")
st.markdown("### 📋 Component Prompts (with helper tooltips)")

# Content ID input fields with helper tooltips
content_ids = {}
components = [
    ("Hero Banner", "Big banner at top of the page with CTA"),
    ("RTB 1", "First text block under banner (e.g., trust message)"),
    ("RTB 2", "Second text block (optional)"),
    ("RTB 3", "Third text block (e.g., help center CTA)"),
    ("Tile 1", "Left-side card (e.g., featured destination)"),
    ("Tile 2", "Right-side card (e.g., flexible booking promo)"),
]

for comp, tip in components:
    content_ids[comp] = st.text_input(f"{comp} Content ID", help=tip)

# Generate and download JSON file
if st.button("Generate Template JSON"):
    populated_template = base_template.copy()
    populated_template["templateName"] = template_name
    populated_template["pageTitle"] = page_title
    populated_template["linesOfBusiness"] = selected_lobs

    # Assign content IDs to the correct places in the JSON
    try:
        populated_template["page"]["sections"][0]["modules"][0]["contentId"] = content_ids["Hero Banner"]
        populated_template["page"]["sections"][1]["modules"][0]["contentId"] = content_ids["RTB 1"]
        populated_template["page"]["sections"][1]["modules"][1]["contentId"] = content_ids["RTB 2"]
        populated_template["page"]["sections"][1]["modules"][2]["contentId"] = content_ids["RTB 3"]
        populated_template["page"]["sections"][2]["modules"][0]["contentId"] = content_ids["Tile 1"]
        populated_template["page"]["sections"][2]["modules"][1]["contentId"] = content_ids["Tile 2"]

        json_data = json.dumps(populated_template, indent=2)
        st.download_button(label="Download JSON Template", file_name="generated_template.json", mime="application/json", data=json_data)
    except Exception as e:
        st.error(f"An error occurred while generating the template: {e}")
