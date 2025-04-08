
import streamlit as st
import json
import copy

st.set_page_config(layout="centered")

st.markdown(
    """
    <div style="background-color:#00355F;padding:10px;border-radius:10px;margin-bottom:20px">
        <h1 style="color:white;text-align:center;">✈️ WLT Template Generator</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

template_type = st.selectbox("Select Template Type", ["WLT Landing Page Template", "WLT Curated Trips Template"])

st.markdown("### Template Info")

template_name = st.text_input("Template Name", help="Name of the template.")
page_title = st.text_input("Page Title", help="Title that appears in the browser tab.")
header_text = st.text_input("Header", help="Main heading shown on the template.")
brand = st.text_input("Brand", help="Brand associated with this template.")
pos = st.text_input("POS", help="Point of sale (e.g., US, CA, JP).")
locale = st.text_input("Locale", help="Locale code (e.g., en_US, ja_JP).")

st.markdown("---")
st.markdown("### Content IDs")

if template_type == "WLT Landing Page Template":
    hero_banner = st.text_input("Hero Banner Content ID", help="Used for the main hero image/banner shown at the top of the landing page.")
    rtb1 = st.text_input("RTB 1 Content ID", help="First 'Reason to Believe' section.")
    rtb2 = st.text_input("RTB 2 Content ID", help="Second 'Reason to Believe' section.")
    rtb3 = st.text_input("RTB 3 Content ID", help="Third 'Reason to Believe' section.")
    tile1 = st.text_input("Tile 1 Content ID", help="First image/text tile.")
    tile2 = st.text_input("Tile 2 Content ID", help="Second image/text tile.")
else:
    curated_fields = {
        "Hero Banner Content ID": st.text_input("Hero Banner Content ID", help="Main hero image/banner typically shown on desktop."),
        "Body Copy - Title": st.text_input("Body Copy Title Content ID", help="Headline or main title text that introduces the body content."),
        "Body Copy Intro": st.text_input("Body Copy Introduction Content ID", help="Intro paragraph below title, providing context."),
        "Curated Headline 1": st.text_input("Curated Section Header 1 Content ID", help="First subheading for curated trip recommendations."),
        "Curated Headline 2": st.text_input("Curated Section Header 2 Content ID", help="Second subheading for curated trip recommendations."),
        "Curated Headline 3": st.text_input("Curated Section Header 3 Content ID", help="Third subheading for curated trip recommendations."),
        "Body Copy + 50 GC": st.text_input("Body Copy Incentive Content ID", help="Message block with incentive details, e.g., gift card reward."),
        "Body Copy - Author": st.text_input("Author Attribution Content ID", help="Author or contributor name displayed at the end of the article."),
        "Curated Trips - Terms and Conditions": st.text_input("Terms & Conditions Content ID", help="Legal disclaimers or promotional terms."),
    }
