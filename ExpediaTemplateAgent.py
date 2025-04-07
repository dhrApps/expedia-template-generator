
import streamlit as st
import json

# =========================
# 🎨 App Styling and Header
# =========================
st.markdown("""
<div style="background-color:#f2f9ff;padding:20px;border-radius:10px;margin-bottom:10px;">
    <h1 style="color:#00355F;font-size:32px;text-align:center;">
        ✈️ WLT Template Generator
    </h1>
</div>
""", unsafe_allow_html=True)

# ===============================
# 📌 Template Type Dropdown Logic
# ===============================
template_type = st.selectbox(
    "Select Template Type",
    ["WLT Landing Page Template", "WLT Curated Trips Template"],
    help="Choose the template structure you want to generate"
)

# ========================
# 🧠 Common Template Fields
# ========================
template_name = st.text_input("Template Name", placeholder="e.g., Luxury Escapes Philippines")
page_title = st.text_input("Page Title", placeholder="e.g., Discover Your Next Escape")

# ===================================
# ✨ Content ID Input Sections by Type
# ===================================
content_ids = {}

if template_type == "WLT Landing Page Template":
    st.markdown("---")
    st.markdown("### 🧩 Content IDs – Landing Page")
    content_ids["hero_banner"] = st.text_input("Hero Banner Content ID", help="Big banner at top of the page with CTA")
    content_ids["rtb1"] = st.text_input("RTB 1 Content ID", help="Reason to believe block #1")
    content_ids["rtb2"] = st.text_input("RTB 2 Content ID", help="Reason to believe block #2")
    content_ids["rtb3"] = st.text_input("RTB 3 Content ID", help="Reason to believe block #3")
    content_ids["tile1"] = st.text_input("Tile 1 Content ID", help="First clickable module in second section")
    content_ids["tile2"] = st.text_input("Tile 2 Content ID", help="Second clickable module in second section")

elif template_type == "WLT Curated Trips Template":
    st.markdown("---")
    st.markdown("### 🧩 Content IDs – Curated Trips")
    content_ids["hero"] = st.text_input("Hero Banner Content ID", help="Top hero banner with CTA")
    content_ids["body_copy_title"] = st.text_input("Body Copy Title Content ID", help="Headline text in the body section")
    content_ids["body_copy_intro"] = st.text_input("Body Copy Introduction Content ID", help="Introductory paragraph text")
    content_ids["curated1"] = st.text_input("Curated Section Header 1 Content ID", help="Label for first curated trip group")
    content_ids["curated2"] = st.text_input("Curated Section Header 2 Content ID", help="Label for second curated trip group")
    content_ids["curated3"] = st.text_input("Curated Section Header 3 Content ID", help="Label for third curated trip group")
    content_ids["incentive"] = st.text_input("Body Copy + 50 GC Content ID", help="Promotional block with gift card or offer")
    content_ids["author"] = st.text_input("Body Copy Author Content ID", help="Author or contributor details block")
    content_ids["terms"] = st.text_input("Curated Trips Terms and Conditions Content ID", help="Legal disclaimer at bottom")

# ==========================
# 🛠 Load JSON Base Template
# ==========================
try:
    if template_type == "WLT Landing Page Template":
        with open("fixed_base_template.json", "r") as f:
            base_template = json.load(f)
    else:
        with open("exportedTemplates-47495.json", "r") as f:
            base_template = json.load(f)
except Exception as e:
    st.error(f"Error loading base template: {e}")
    base_template = None

# ================================
# 🧾 Generate and Download JSON
# ================================
if st.button("Generate Template JSON"):
    try:
        if not base_template:
            st.error("Template base could not be loaded.")
        else:
            output = base_template.copy()
            if isinstance(output, list):
                output = output[0]

            output["name"] = template_name
            output["title"] = page_title

            # LANDING PAGE MAPPING
            if template_type == "WLT Landing Page Template":
                mappings = {
                    "Hero Full Bleed Banner": content_ids.get("hero_banner", ""),
                    "RTB 1": content_ids.get("rtb1", ""),
                    "RTB 2": content_ids.get("rtb2", ""),
                    "RTB 3": content_ids.get("rtb3", ""),
                    "Tile 1": content_ids.get("tile1", ""),
                    "Tile 2": content_ids.get("tile2", ""),
                }

                def assign_landing_content_id(node):
                    if isinstance(node, dict):
                        if node.get("name") in mappings:
                            for child in node.get("childNodes", []):
                                for attr in child.get("attributes", []):
                                    if attr.get("name") == "contentId":
                                        attr["value"] = mappings[node["name"]]
                        for child in node.get("childNodes", []):
                            assign_landing_content_id(child)

                assign_landing_content_id(output["flexNode"])

            json_output = json.dumps([output], indent=4)
            st.download_button("📥 Download JSON", json_output, file_name="generated_template.json", mime="application/json")
    except Exception as e:
        st.error(f"⚠️ Error generating template: {repr(e)}")
