import streamlit as st
import json
import copy

st.set_page_config(layout="centered")

# ---- Page Header ----
st.markdown(
    "<h1 style='text-align: center; color: #00355F;'>✈️ WLT Template Generator</h1>",
    unsafe_allow_html=True
)

# ---- Template Type Selection ----
template_type = st.selectbox(
    "Select Template Type",
    ["WLT Landing Page Template", "WLT Curated Trips Template"],
    help="Choose the template structure you want to generate"
)

# ---- Template Details Section ----
st.markdown("### Template Details")
template_name = st.text_input("Template Name", help="A unique name for this template")
page_title = st.text_input("Page Title", help="Page title as seen in the browser tab")
header_text = st.text_input("Header", help="Main header displayed on the page")
brand = st.text_input("Brand", help="Brand associated with this template, e.g., GPS")
pos = st.text_input("POS", help="Point of sale, e.g., PHILIPPINEAIRLINES_PH")
locale = st.text_input("Locale", help="Locale setting, e.g., EN_PH")

# ---- Content IDs Section (Dynamic) ----
if template_type == "WLT Landing Page Template":
    st.markdown("### Content IDs (Landing Page)")
    hero_banner = st.text_input("Hero Banner Content ID", help="Used for the main hero image/banner shown at the top of the landing page, typically on desktop devices.")
    rtb1 = st.text_input("RTB 1 Content ID", help="Used for the first trust-building message or block")
    rtb2 = st.text_input("RTB 2 Content ID", help="Used for the second trust-building message or block")
    rtb3 = st.text_input("RTB 3 Content ID", help="Used for the third trust-building message or block")
    tile1 = st.text_input("Tile 1 Content ID", help="Used for the first tile, such as a featured trip")
    tile2 = st.text_input("Tile 2 Content ID", help="Used for the second tile, such as a supporting trip")

    # Load Landing Page base JSON
    with open("fixed_base_template.json", "r") as f:
        base_template = json.load(f)

    def assign_content_id_by_name(node, name_map):
        if isinstance(node, dict):
            if node.get("type") == "REGION":
                region_name = next((attr["value"] for attr in node.get("attributes", []) if attr["name"] == "name"), None)
                if region_name and region_name in name_map:
                    for child in node.get("childNodes", []):
                        for attr in child.get("attributes", []):
                            if attr["name"] == "contentId":
                                attr["value"] = name_map[region_name]
            for k, v in node.items():
                assign_content_id_by_name(v, name_map)
        elif isinstance(node, list):
            for item in node:
                assign_content_id_by_name(item, name_map)

    if st.button("Generate Template JSON"):
        try:
            populated = copy.deepcopy(base_template)
            populated[0]["name"] = template_name
            populated[0]["title"] = page_title
            populated[0]["header"] = header_text
            populated[0]["brand"] = brand
            populated[0]["pos"] = pos
            populated[0]["locale"] = locale

            content_map = {
                "Hero Full Bleed Banner": hero_banner,
                "RTB 1": rtb1,
                "RTB 2": rtb2,
                "RTB 3": rtb3,
                "Tile 1": tile1,
                "Tile 2": tile2
            }

            assign_content_id_by_name(populated[0]["flexNode"], content_map)

            json_str = json.dumps(populated, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="generated_template.json", mime="application/json")
        except Exception as e:
            st.error(f"Error generating JSON: {e}")

elif template_type == "WLT Curated Trips Template":
    st.markdown("### Content IDs (Curated Trips)")
    hero = st.text_input("Hero Banner Content ID", help="Used for the main hero image/banner shown at the top of the landing page, typically on desktop devices.")
    title = st.text_input("Body Copy Title Content ID", help="Headline or main title text that introduces the body content section.")
    intro = st.text_input("Body Copy Introduction Content ID", help="Introductory paragraph or text block that appears below the title, giving context or engaging copy.")
    headline1 = st.text_input("Curated Section Header 1 Content ID", help="The first subheading for curated trip recommendations.")
    headline2 = st.text_input("Curated Section Header 2 Content ID", help="The second subheading for curated trip recommendations.")
    headline3 = st.text_input("Curated Section Header 3 Content ID", help="The third subheading for curated trip recommendations.")
    incentive = st.text_input("Body Copy Incentive Content ID", help="A promotional block or message containing incentive details, e.g., gift card rewards.")
    author = st.text_input("Author Attribution Content ID", help="Author name or contributor details, typically displayed at the bottom of body content.")
    terms = st.text_input("Terms & Conditions Content ID", help="Legal or disclaimers associated with the curated trips or promotions on the page.")

    def map_curated_ids(template_json):
        name_to_value = {
            "HERO - Desktop": hero,
            "Body Copy - Title": title,
            "Body Copy Intro": intro,
            "Curated Headline 1": headline1,
            "Curated Headline 2": headline2,
            "Curated Headline 3": headline3,
            "Body Copy + 50 GC": incentive,
            "Body Copy - Author": author,
            "Curated Trips - Terms and Conditions": terms,
        }

        def walk(node):
            if isinstance(node, dict):
                attrs = node.get("attributes", [])
                for attr in attrs:
                    if attr["name"] == "name":
                        for label, val in name_to_value.items():
                            if attr["value"] == label:
                                for a in attrs:
                                    if a["name"] == "contentId":
                                        a["value"] = val
                for v in node.values():
                    walk(v)
            elif isinstance(node, list):
                for item in node:
                    walk(item)

        return walk

    if st.button("Generate Template JSON"):
        try:
            with open("exportedTemplates-47495.json", "r") as f:
                curated_template = json.load(f)
            curated = copy.deepcopy(curated_template)
            walk = map_curated_ids(curated[0]["flexNode"])
            walk(curated[0]["flexNode"])

            curated[0]["name"] = template_name
            curated[0]["title"] = page_title
            curated[0]["header"] = header_text
            curated[0]["brand"] = brand
            curated[0]["pos"] = pos
            curated[0]["locale"] = locale

            json_str = json.dumps(curated, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="generated_curated_template.json", mime="application/json")
        except Exception as e:
            st.error(f"Error generating curated template: {e}")
