
import streamlit as st
import json

# Title and Styling
st.markdown(
    """
    <div style='text-align: center; padding: 20px;'>
        <h1 style='color: #00355F;'>✈️ WLT Template Generator</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Template selection dropdown
template_type = st.selectbox(
    "Select Template Type",
    ["WLT Landing Page Template", "WLT Curated Trips Template"],
    help="Choose the template structure you want to generate"
)

# Common Inputs
st.markdown("---")
st.subheader("Basic Template Info")
template_name = st.text_input("Template Name")
page_title = st.text_input("Page Title")
brand = st.text_input("Brand")
pos = st.text_input("POS")
locale = st.text_input("Locale")

# Dynamic Content ID Fields
st.markdown("---")
st.subheader("Content IDs")

if template_type == "WLT Landing Page Template":
    st.markdown("### WLT Landing Page Content IDs")
    hero_banner = st.text_input("Hero Banner Content ID", help="Big banner at top of the page with CTA")
    rtb1 = st.text_input("RTB 1 Content ID", help="Reason to Believe #1 block")
    rtb2 = st.text_input("RTB 2 Content ID", help="Reason to Believe #2 block")
    rtb3 = st.text_input("RTB 3 Content ID", help="Reason to Believe #3 block")
    tile1 = st.text_input("Tile 1 Content ID", help="First module tile block")
    tile2 = st.text_input("Tile 2 Content ID", help="Second module tile block")
else:
    st.markdown("### WLT Curated Trips Content IDs")
    curated_ids = {
        "hero": st.text_input("Hero Banner Content ID", help="Used for the main hero image/banner shown at the top of the landing page, typically on desktop devices."),
        "body_title": st.text_input("Body Copy Title Content ID", help="Headline or main title text that introduces the body content section."),
        "body_intro": st.text_input("Body Copy Introduction Content ID", help="Introductory paragraph or text block that appears below the title, giving context or engaging copy."),
        "headline_1": st.text_input("Curated Section Header 1 Content ID", help="The first subheading for curated trip recommendations."),
        "headline_2": st.text_input("Curated Section Header 2 Content ID", help="The second subheading for curated trip recommendations."),
        "headline_3": st.text_input("Curated Section Header 3 Content ID", help="The third subheading for curated trip recommendations."),
        "incentive": st.text_input("Body Copy + 50 GC Content ID", help="A promotional block or message containing incentive details, e.g., gift card rewards."),
        "author": st.text_input("Author Attribution Content ID", help="Author name or contributor details, typically displayed at the bottom of body content."),
        "terms": st.text_input("Terms & Conditions Content ID", help="Legal or disclaimers associated with the curated trips or promotions on the page.")
    }

# Generate Button Logic
st.markdown("---")
if st.button("Generate Template JSON"):
    try:
        if template_type == "WLT Landing Page Template":
            with open("fixed_base_template.json", "r") as f:
                base_template = json.load(f)

            populated_template = base_template.copy()
            populated_template[0]["name"] = template_name
            populated_template[0]["title"] = page_title
            populated_template[0]["brand"] = brand
            populated_template[0]["pos"] = pos
            populated_template[0]["locale"] = locale

            # Inject content IDs based on section titles
            for region in populated_template[0]["flexNode"]["childNodes"]:
                for subregion in region["childNodes"]:
                    module = subregion["childNodes"][0]
                    name_attr = next((a for a in subregion["attributes"] if a["name"] == "name"), {})
                    if name_attr.get("value") == "Hero Full Bleed Banner":
                        next((a for a in module["attributes"] if a["name"] == "contentId"), {})["value"] = hero_banner
                    elif name_attr.get("value") == "RTB 1":
                        next((a for a in module["attributes"] if a["name"] == "contentId"), {})["value"] = rtb1
                    elif name_attr.get("value") == "RTB 2":
                        next((a for a in module["attributes"] if a["name"] == "contentId"), {})["value"] = rtb2
                    elif name_attr.get("value") == "RTB 3":
                        next((a for a in module["attributes"] if a["name"] == "contentId"), {})["value"] = rtb3
                    elif name_attr.get("value") == "Tile 1":
                        next((a for a in module["attributes"] if a["name"] == "contentId"), {})["value"] = tile1
                    elif name_attr.get("value") == "Tile 2":
                        next((a for a in module["attributes"] if a["name"] == "contentId"), {})["value"] = tile2

            json_str = json.dumps(populated_template, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="landing_page_template.json", mime="application/json")

        elif template_type == "WLT Curated Trips Template":
            st.warning("Curated Trips template generation is coming soon.")

    except Exception as e:
        st.error(f"⚠️ Error generating template: {repr(e)}")
