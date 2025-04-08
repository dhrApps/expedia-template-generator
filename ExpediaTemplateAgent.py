# Expedia Template Generator App
import streamlit as st
import json

# ---- App Title ----
st.markdown("""
<div style="background-color:#00355F;padding:20px;border-radius:10px">
    <h1 style="color:white;text-align:center;">✈️ WLT Template Generator</h1>
</div>
""", unsafe_allow_html=True)

# ---- Template Selector ----
template_choice = st.selectbox("Select Template Type", ["WLT Landing Page Template", "WLT Curated Trips Template"])

# ---- Input Fields (shared) ----
template_name = st.text_input("Template Name", help="Unique name for the template.")
page_title = st.text_input("Page Title", help="Displayed as the browser tab title.")
header_text = st.text_input("Header", help="Displayed prominently at the top of the page.")

# ---- Dynamic Section: Content IDs ----
st.markdown("---")
st.markdown("### Content IDs")

# Sample fields for each template
if template_choice == "WLT Landing Page Template":
    hero_banner = st.text_input("Hero Banner Content ID", help="Used for the main hero image/banner.")
    rtb1 = st.text_input("RTB 1 Content ID", help="First ‘reason to believe’ module.")
    rtb2 = st.text_input("RTB 2 Content ID", help="Second ‘reason to believe’ module.")
    rtb3 = st.text_input("RTB 3 Content ID", help="Third ‘reason to believe’ module.")
    tile1 = st.text_input("Tile 1 Content ID", help="First editorial tile content.")
    tile2 = st.text_input("Tile 2 Content ID", help="Second editorial tile content.")

    # Generate Landing Page JSON
    if st.button("Generate Template JSON"):
        with open("fixed_base_template.json") as f:
            base_json = json.load(f)
        base_json[0]["name"] = template_name
        base_json[0]["title"] = page_title
        base_json[0]["header"] = header_text

        def set_content_id(region_name, content_id):
            for region in base_json[0]["flexNode"]["childNodes"]:
                if any(attr.get("name") == "name" and attr.get("value") == region_name for attr in region.get("attributes", [])):
                    for module in region.get("childNodes", []):
                        for attr in module.get("attributes", []):
                            if attr.get("name") == "contentId":
                                attr["value"] = content_id

        set_content_id("Hero Full Bleed Banner", hero_banner)
        set_content_id("RTB 1", rtb1)
        set_content_id("RTB 2", rtb2)
        set_content_id("RTB 3", rtb3)
        set_content_id("Tile 1", tile1)
        set_content_id("Tile 2", tile2)

        st.download_button("📥 Download JSON", data=json.dumps(base_json, indent=4), file_name="generated_template.json")

elif template_choice == "WLT Curated Trips Template":
    hero = st.text_input("Hero Banner Content ID", help="Top hero banner for curated trips.")
    body_title = st.text_input("Body Copy Title Content ID", help="Main heading text in body.")
    body_intro = st.text_input("Body Copy Introduction Content ID", help="Introductory paragraph text.")
    curated1 = st.text_input("Curated Section Header 1 Content ID", help="Headline for curated trip section 1.")
    curated2 = st.text_input("Curated Section Header 2 Content ID", help="Headline for curated trip section 2.")
    curated3 = st.text_input("Curated Section Header 3 Content ID", help="Headline for curated trip section 3.")
    gc50 = st.text_input("Body Copy + 50 GC Content ID", help="Gift card or incentive section.")
    author = st.text_input("Author Attribution Content ID", help="Name/attribution displayed below content.")
    tnc = st.text_input("Terms & Conditions Content ID", help="Content block for legal or terms.")

    if st.button("Generate Template JSON"):
        with open("exportedTemplates-47495.json") as f:
            base_json = json.load(f)

        def deep_insert(module_label, cid):
            for node in base_json[0]["flexNode"]["childNodes"]:
                if "childNodes" in node:
                    for sub in node["childNodes"]:
                        if "attributes" in sub:
                            for attr in sub["attributes"]:
                                if attr["name"] == "name" and attr["value"] == "editorial":
                                    for mod_attr in sub["attributes"]:
                                        if mod_attr["name"] == "contentId" and sub["attributes"]:
                                            if module_label in str(sub["attributes"]):
                                                mod_attr["value"] = cid

        deep_insert("Hero", hero)
        deep_insert("Body Copy - Title", body_title)
        deep_insert("Body Copy Intro", body_intro)
        deep_insert("Curated Headline 1", curated1)
        deep_insert("Curated Headline 2", curated2)
        deep_insert("Curated Headline 3", curated3)
        deep_insert("Body Copy + 50 GC", gc50)
        deep_insert("Body Copy - Author", author)
        deep_insert("Curated Trips - Terms and Conditions", tnc)

        st.download_button("📥 Download JSON", data=json.dumps(base_json, indent=4), file_name="curated_trips_template.json")
