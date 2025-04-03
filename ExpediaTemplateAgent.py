
import json
import streamlit as st

# Load the base template
with open("fixed_base_template_VALIDATED.json", "r") as f:
    base_template = json.load(f)

def generate_filled_template(template_name, page_title, header, content_ids):
    template = base_template.copy()
    template[0]["name"] = template_name
    template[0]["title"] = page_title
    template[0]["header"] = header

    replacements = {
        "Hero Full Bleed Banner": content_ids.get("heroBanner", ""),
        "RTB 1": content_ids.get("rtb1", ""),
        "RTB 2": content_ids.get("rtb2", ""),
        "RTB 3": content_ids.get("rtb3", ""),
        "Tile 1": content_ids.get("tile1", ""),
        "Tile 2": content_ids.get("tile2", "")
    }

    def update_content_ids(node):
        if "attributes" in node:
            for attr in node["attributes"]:
                if attr["name"] == "contentId":
                    for region_name, content_id in replacements.items():
                        if region_name in node.get("parentName", ""):
                            attr["value"] = content_id
        if "childNodes" in node:
            for child in node["childNodes"]:
                child["parentName"] = node.get("attributes", [{}])[0].get("value", "")
                update_content_ids(child)

    update_content_ids(template[0]["flexNode"])
    return template

# Streamlit UI is managed from streamlit_app.py
