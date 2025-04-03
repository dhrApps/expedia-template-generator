import streamlit as st
import json

st.set_page_config(page_title="Expedia Template Generator", layout="wide")

st.title("Expedia Template Generator")

# Load JSON base template
template_path = "fixed_base_template_VALIDATED.json"

try:
    with open(template_path, "r") as f:
        template_data = json.load(f)
    st.success("Base template loaded successfully.")
except Exception as e:
    st.error(f"Failed to load base template: {e}")
    st.stop()

# Display the template content (for validation or review)
st.subheader("Base Template JSON Preview")
st.json(template_data)

# Optional: Save or modify logic here
if st.button("Download Base Template"):
    st.download_button(
        label="Download JSON",
        data=json.dumps(template_data, indent=2),
        file_name="generated_template.json",
        mime="application/json"
    )
