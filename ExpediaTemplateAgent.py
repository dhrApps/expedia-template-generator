
import streamlit as st
import json
import base64

# --- Constants ---
EXPEDIA_BLUE = "#00355F"
PLANE_ICON = "✈️"

# --- Page Config ---
st.set_page_config(layout="centered")

# --- Title with Travel Theme ---
st.markdown(f"""
<div style="background-color:{EXPEDIA_BLUE}; padding: 30px; border-radius: 8px; text-align: center;">
    <h1 style="color:white; font-size: 40px;">{PLANE_ICON} WLT Template Generator</h1>
</div>
""", unsafe_allow_html=True)

# --- Template Type Selection ---
template_type = st.selectbox("Choose Template Type", ["WLT Landing Page Template", "WLT Curated Trips Template"])

# --- Common Inputs ---
st.markdown("### Template Metadata")
template_name = st.text_input("Template Name", help="Name of the template to uniquely identify it.")
page_title = st.text_input("Page Title", help="Title that appears on the browser tab and SEO.")
header_text = st.text_input("Header", help="Main header text shown on the landing page.")
brand = st.text_input("Brand", help="e.g., GPS, WEX")
pos = st.text_input("POS", help="e.g., PHILIPPINEAIRLINES_PH")
locale = st.text_input("Locale", help="e.g., EN_PH")

# --- Dynamic Content ID Section ---
st.markdown("---")
if template_type == "WLT Landing Page Template":
    st.markdown("### Landing Page Content IDs")
    hero_banner = st.text_input("Hero Banner Content ID", help="Used for the main hero image/banner shown at the top of the landing page, typically on desktop devices."), help="Used for the main hero image/banner shown at the top of the landing page.")
    rtb1 = st.text_input("RTB 1 Content ID", help="Content ID for the first Reason-To-Believe section."), help="First 'Reason to Believe' section.")
    rtb2 = st.text_input("RTB 2 Content ID", help="Content ID for the second Reason-To-Believe section."), help="Second 'Reason to Believe' section.")
    rtb3 = st.text_input("RTB 3 Content ID", help="Content ID for the third Reason-To-Believe section."), help="Third 'Reason to Believe' section.")
    tile1 = st.text_input("Tile 1 Content ID", help="Content ID for the first image card or promotional tile."), help="First image/text tile.")
    tile2 = st.text_input("Tile 2 Content ID", help="Content ID for the second image card or promotional tile."), help="Second image/text tile.")
else:
    st.markdown("### Curated Trips Content IDs")
    curated_ids = {
        "Hero Banner Content ID": st.text_input("Hero Banner Content ID", help="Main hero image/banner typically shown on desktop."),
        "Body Copy - Title": st.text_input("Body Copy Title Content ID", help="Headline or main title text that introduces the body content."),
        "Body Copy Intro": st.text_input("Body Copy Introduction Content ID", help="Intro paragraph below title, providing context."),
        "Curated Headline 1": st.text_input("Curated Section Header 1 Content ID", help="First subheading for curated trip recommendations."),
        "Curated Headline 2": st.text_input("Curated Section Header 2 Content ID", help="Second subheading for curated trip recommendations."),
        "Curated Headline 3": st.text_input("Curated Section Header 3 Content ID", help="Third subheading for curated trip recommendations."),
        "Body Copy + 50 GC": st.text_input("Body Copy Incentive Content ID", help="Message block with incentive details, e.g., gift card reward."),
        "Body Copy - Author": st.text_input("Author Attribution Content ID", help="Author or contributor name displayed at the end of the article."),
        "Curated Trips - Terms and Conditions": st.text_input("Terms & Conditions Content ID", help="Legal disclaimers or promotional terms.")
    }

# --- JSON Generation Logic ---
st.markdown("---")
if template_type == "WLT Landing Page Template":
    if st.button("Generate Template JSON"):
        try:
            with open("fixed_base_template.json", "r") as f:
                base_template = json.load(f)

            populated_template = base_template.copy()
            populated_template[0]["name"] = template_name
            populated_template[0]["title"] = page_title
            populated_template[0]["header"] = header_text
            populated_template[0]["brand"] = brand
            populated_template[0]["pos"] = pos
            populated_template[0]["locale"] = locale

            def insert_content_id(node, region_name, cid_value):
                if node.get("type") == "REGION":
                    for attr in node.get("attributes", []):
                        if attr["name"] == "name" and attr["value"] == region_name:
                            for module in node.get("childNodes", []):
                                if module.get("type") == "MODULE":
                                    for mod_attr in module["attributes"]:
                                        if mod_attr["name"] == "contentId":
                                            mod_attr["value"] = cid_value
                for child in node.get("childNodes", []):
                    insert_content_id(child, region_name, cid_value)

            root_node = populated_template[0]["flexNode"]
            insert_content_id(root_node, "Hero Full Bleed Banner", hero_banner)
            insert_content_id(root_node, "RTB 1", rtb1)
            insert_content_id(root_node, "RTB 2", rtb2)
            insert_content_id(root_node, "RTB 3", rtb3)
            insert_content_id(root_node, "Tile 1", tile1)
            insert_content_id(root_node, "Tile 2", tile2)

            json_str = json.dumps(populated_template, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="generated_template.json", mime="application/json")
        except Exception as e:
            st.error(f"Error generating template: {e}")
else:
    if st.button("Generate Template JSON"):
        try:
            with open("exportedTemplates-47495.json", "r") as f:
                curated_template = json.load(f)

            def assign_curated_id(template, label, value):
                def search_and_assign(node):
                    if isinstance(node, dict):
                        if node.get("name") == "contentId":
                            if label.lower() in json.dumps(node).lower():
                                node["value"] = value
                        for v in node.values():
                            search_and_assign(v)
                    elif isinstance(node, list):
                        for item in node:
                            search_and_assign(item)
                search_and_assign(template)

            for label, value in curated_ids.items():
                assign_curated_id(curated_template, label, value)

            json_str = json.dumps(curated_template, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="generated_curated_template.json", mime="application/json")
        except Exception as e:
            st.error(f"Error generating curated template: {e}")
