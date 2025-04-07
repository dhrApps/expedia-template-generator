
import streamlit as st
import json
import copy

# =================== UI HEADER ===================
st.markdown(
    '''
    <div style="background-color:#00355F;padding:20px;border-radius:10px;text-align:center;">
        <h1 style="color:white;">
            ✈️ WLT Template Generator
        </h1>
    </div>
    ''',
    unsafe_allow_html=True
)

# =================== TEMPLATE TYPE SELECT ===================
template_type = st.selectbox("Select Template Type", ["WLT Landing Page Template", "WLT Curated Trips Template"])

# =================== BASE INFO FIELDS ===================
st.subheader("Basic Information")
template_name = st.text_input("Template Name")
page_title = st.text_input("Page Title")
header_text = st.text_input("Header Text")
brand = st.text_input("Brand")
pos = st.text_input("POS")
locale = st.text_input("Locale")

# =================== CONTENT ID INPUTS ===================
st.markdown("---")
st.subheader("Content IDs")

if template_type == "WLT Landing Page Template":
    hero_banner = st.text_input("Hero Banner Content ID")
    rtb1 = st.text_input("RTB 1 Content ID")
    rtb2 = st.text_input("RTB 2 Content ID")
    rtb3 = st.text_input("RTB 3 Content ID")
    tile1 = st.text_input("Tile 1 Content ID")
    tile2 = st.text_input("Tile 2 Content ID")

elif template_type == "WLT Curated Trips Template":
    hero_banner = st.text_input("Hero Banner Content ID (HERO - Desktop)")
    body_copy_title = st.text_input("Body Copy Title Content ID (Body Copy - Title)")
    body_copy_intro = st.text_input("Body Copy Introduction Content ID (Body Copy Intro)")
    curated1 = st.text_input("Curated Section Header 1 Content ID (Curated Headline 1)")
    curated2 = st.text_input("Curated Section Header 2 Content ID (Curated Headline 2)")
    curated3 = st.text_input("Curated Section Header 3 Content ID (Curated Headline 3)")
    incentive = st.text_input("Body Copy Incentive Content ID (Body Copy + 50 GC)")
    author = st.text_input("Author Attribution Content ID (Body Copy - Author)")
    terms = st.text_input("Terms & Conditions Content ID (Curated Trips - Terms and Conditions)")

# =================== LOAD BASE TEMPLATE ===================
try:
    with open("fixed_base_template.json", "r") as f:
        base_template = json.load(f)
except Exception:
    base_template = None
    st.error("Base template could not be loaded.")

# =================== GENERATE JSON ===================
if st.button("Generate Template JSON"):
    try:
        if base_template:
            final_json = copy.deepcopy(base_template)
            final_json[0]["name"] = template_name
            final_json[0]["title"] = page_title
            final_json[0]["header"] = header_text
            final_json[0]["brand"] = brand
            final_json[0]["pos"] = pos
            final_json[0]["locale"] = locale

            def set_content_id(region_name, content_id):
                def recurse(nodes):
                    for node in nodes:
                        if node.get("attributes"):
                            for attr in node["attributes"]:
                                if attr.get("name") == "name" and attr.get("value") == region_name:
                                    for module in node.get("childNodes", []):
                                        if module.get("type") == "MODULE":
                                            for a in module.get("attributes", []):
                                                if a["name"] == "contentId":
                                                    a["value"] = content_id
                    return nodes

                final_json[0]["flexNode"]["childNodes"] = recurse(final_json[0]["flexNode"]["childNodes"])

            if template_type == "WLT Landing Page Template":
                set_content_id("Hero Full Bleed Banner", hero_banner)
                set_content_id("RTB 1", rtb1)
                set_content_id("RTB 2", rtb2)
                set_content_id("RTB 3", rtb3)
                set_content_id("Tile 1", tile1)
                set_content_id("Tile 2", tile2)

            json_str = json.dumps(final_json, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="generated_template.json", mime="application/json")
        else:
            st.error("❌ Could not generate JSON: Base template is missing.")
    except Exception as e:
        st.error(f"⚠️ Error: {repr(e)}")
