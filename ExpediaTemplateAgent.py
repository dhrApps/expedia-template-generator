
import streamlit as st
import json
import base64

# Set page config
st.set_page_config(page_title="WLT Template Generator", layout="wide")

# Embed Expedia Group logo using base64
logo_base64 = "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"
logo_html = f'<img src="data:image/png;base64,' + logo_base64 + '" width="50"/>'

# Title with logo
st.markdown(
    "<div style='display: flex; align-items: center;'>"
    "<h1 style='color: #00355F; margin-right: 15px;'>WLT Template Generator</h1>" + logo_html +
    "</div>",
    unsafe_allow_html=True
)

# Load base JSON template
with open("fixed_base_template.json", "r") as f:
    base_template = json.load(f)

# Inputs
template_name = st.text_input("Template Name", placeholder="e.g., Luxury Escapes Asia")
page_title = st.text_input("Page Title", placeholder="e.g., Luxury Escapes Summer Deals")
header_text = st.text_input("Header", placeholder="e.g., Book Early & Save")
brand = st.text_input("Brand", placeholder="e.g., WLT")
pos = st.text_input("POS", placeholder="e.g., WLT_US")
locale = st.text_input("Locale", placeholder="e.g., EN_US")

st.markdown("---")
st.markdown("### Content IDs")

# Tooltipped inputs for content IDs
hero_banner = st.text_input("Hero Banner Content ID", help="Big banner at top of page with CTA")
rtb1 = st.text_input("RTB 1 Content ID", help="First of the 3 RTB content blocks")
rtb2 = st.text_input("RTB 2 Content ID", help="Second of the 3 RTB content blocks")
rtb3 = st.text_input("RTB 3 Content ID", help="Third of the 3 RTB content blocks")
tile1 = st.text_input("Tile 1 Content ID", help="First of two side-by-side tiles")
tile2 = st.text_input("Tile 2 Content ID", help="Second of two side-by-side tiles")

# Helper function to assign content IDs
def assign_content_id(region, region_name, content_id):
    if region.get("attributes"):
        for attr in region["attributes"]:
            if attr.get("name") == "name" and attr.get("value") == region_name:
                for child in region.get("childNodes", []):
                    if child.get("type") == "MODULE":
                        for attr in child.get("attributes", []):
                            if attr["name"] == "contentId":
                                attr["value"] = content_id
                                return True
    return False

def deep_assign(template, mappings):
    def recurse(nodes):
        for node in nodes:
            if node["type"] == "REGION":
                name_attr = next((a for a in node.get("attributes", []) if a["name"] == "name"), None)
                if name_attr and name_attr["value"] in mappings:
                    assign_content_id(node, name_attr["value"], mappings[name_attr["value"]])
                recurse(node.get("childNodes", []))
    recurse(template[0]["flexNode"]["childNodes"])

# Generate JSON button
if st.button("Generate Template JSON"):
    try:
        populated_template = json.loads(json.dumps(base_template))  # Deep copy
        populated_template[0]["name"] = template_name
        populated_template[0]["title"] = page_title
        populated_template[0]["header"] = header_text
        populated_template[0]["brand"] = brand
        populated_template[0]["pos"] = pos
        populated_template[0]["locale"] = locale

        # Populate contentId fields
        mappings = {
            "Hero Full Bleed Banner": hero_banner,
            "RTB 1": rtb1,
            "RTB 2": rtb2,
            "RTB 3": rtb3,
            "Tile 1": tile1,
            "Tile 2": tile2
        }
        deep_assign(populated_template, mappings)

        # Output JSON
        generated_json = json.dumps(populated_template, indent=4)
        st.download_button("📥 Download Template JSON", generated_json, "generated_template.json", "application/json")
    except Exception as e:
        st.error(f"Error generating JSON: {e}")
