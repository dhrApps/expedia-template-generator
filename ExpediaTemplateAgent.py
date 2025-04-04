
import streamlit as st
import json

# Travel-themed background and header styling
st.markdown(
    """
    <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1502920917128-1aa500764b79");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        h1 {
            color: #002244;
            font-family: 'Trebuchet MS', sans-serif;
            text-shadow: 1px 1px 2px #ccc;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("WLT Template Generator")

# Load base JSON template
with open("fixed_base_template.json", "r") as f:
    base_template = json.load(f)

# User inputs
template_name = st.text_input("Template Name", help="This is the name used internally to identify your template.")
page_title = st.text_input("Page Title", help="This is what users see on the landing page tab.")
header_text = st.text_input("Header", help="Main heading text on the landing page.")

# Separator before content fields
st.markdown("---")
st.markdown("### Content IDs")

# Content ID inputs
hero_banner = st.text_input("Hero Banner Content ID", help="Content ID for the top banner image.")
rtb1 = st.text_input("RTB 1 Content ID", help="Reason to believe section 1 content ID.")
rtb2 = st.text_input("RTB 2 Content ID", help="Reason to believe section 2 content ID.")
rtb3 = st.text_input("RTB 3 Content ID", help="Reason to believe section 3 content ID.")
tile1 = st.text_input("Tile 1 Content ID", help="First promotional tile content ID.")
tile2 = st.text_input("Tile 2 Content ID", help="Second promotional tile content ID.")

# Generate JSON
if st.button("Generate Template JSON"):
    try:
        if base_template:
            populated_template = base_template.copy()
            populated_template[0]["name"] = template_name
            populated_template[0]["title"] = page_title
            populated_template[0]["header"] = header_text

            # Insert content IDs into their appropriate regions
            def insert_content_id(region_name, content_id):
                def recurse(node):
                    if isinstance(node, dict):
                        if node.get("type") == "REGION":
                            attributes = node.get("attributes", [])
                            for attr in attributes:
                                if attr.get("name") == "name" and attr.get("value") == region_name:
                                    for child in node.get("childNodes", []):
                                        if child.get("type") == "MODULE":
                                            for attr in child.get("attributes", []):
                                                if attr.get("name") == "contentId":
                                                    attr["value"] = content_id
                        for key in node:
                            recurse(node[key])
                    elif isinstance(node, list):
                        for item in node:
                            recurse(item)

                recurse(populated_template[0]["flexNode"])

            # Apply mappings
            insert_content_id("Hero Full Bleed Banner", hero_banner)
            insert_content_id("RTB 1", rtb1)
            insert_content_id("RTB 2", rtb2)
            insert_content_id("RTB 3", rtb3)
            insert_content_id("Tile 1", tile1)
            insert_content_id("Tile 2", tile2)

            # Output JSON
            json_str = json.dumps(populated_template, indent=4)
            st.download_button("📥 Download JSON", data=json_str, file_name="generated_template.json", mime="application/json")
    except Exception as e:
        st.error(f"⚠️ Error generating template: {repr(e)}")
