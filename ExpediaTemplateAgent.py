
import streamlit as st
import json

# Styling for title
st.markdown(
    """
    <div style="background-image: url('https://images.unsplash.com/photo-1502920917128-1aa500764b8a?auto=format&fit=crop&w=1350&q=80'); background-size: cover; padding: 40px 20px; border-radius: 10px;">
        <h1 style="color: #00355F; text-align: center;">
            ✈️ WLT Template Generator
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Dropdown for Template Type
template_type = st.selectbox(
    "Select Template Type",
    ["WLT Landing Page Template", "WLT Curated Trips Template"],
    help="Choose the template structure you want to generate"
)

# Separator
st.markdown("---")

# Universal Inputs
template_name = st.text_input("Template Name", help="Enter the name of the template")
page_title = st.text_input("Page Title", help="Enter the title for the browser tab or search engine")
brand = st.text_input("Brand", help="Brand code (e.g., 'WLT')")
pos = st.text_input("POS", help="Point of sale (e.g., 'WLT_US')")
locale = st.text_input("Locale", help="Locale code (e.g., 'EN_US')")

# Separator for Content IDs
st.markdown("---")
st.markdown("### 🧩 Content IDs")

content_ids = {}

if template_type == "WLT Landing Page Template":
    st.markdown("##### 🔹 Landing Page Content ID Label Mapping")
    content_ids["hero_banner"] = st.text_input("Hero Banner Content ID", help="Big banner at top of the page with CTA")
    content_ids["rtb1"] = st.text_input("RTB 1 Content ID", help="First row of supporting features")
    content_ids["rtb2"] = st.text_input("RTB 2 Content ID", help="Second row of supporting features")
    content_ids["rtb3"] = st.text_input("RTB 3 Content ID", help="Third row of supporting features")
    content_ids["tile1"] = st.text_input("Tile 1 Content ID", help="Left tile in grid layout")
    content_ids["tile2"] = st.text_input("Tile 2 Content ID", help="Right tile in grid layout")

elif template_type == "WLT Curated Trips Template":
    st.markdown("##### 🌍 Curated Trips Content ID Label Mapping")
    content_ids["hero_desktop"] = st.text_input("Hero Banner Content ID (HERO - Desktop)", help="Main hero image shown on desktop")
    content_ids["body_title"] = st.text_input("Body Copy Title Content ID (Body Copy - Title)", help="Main title for the body section")
    content_ids["body_intro"] = st.text_input("Body Copy Introduction Content ID (Body Copy Intro)", help="Introductory paragraph below title")
    content_ids["headline1"] = st.text_input("Curated Section Header 1 Content ID (Curated Headline 1)", help="First heading for trip section")
    content_ids["headline2"] = st.text_input("Curated Section Header 2 Content ID (Curated Headline 2)", help="Second heading for trip section")
    content_ids["headline3"] = st.text_input("Curated Section Header 3 Content ID (Curated Headline 3)", help="Third heading for trip section")
    content_ids["body_incentive"] = st.text_input("Body Copy Incentive Content ID (Body Copy + 50 GC)", help="Promo block with incentive info")
    content_ids["author"] = st.text_input("Author Attribution Content ID (Body Copy - Author)", help="Name or contributor shown below body")
    content_ids["tnc"] = st.text_input("Terms & Conditions Content ID (Curated Trips - Terms and Conditions)", help="Terms/disclaimers shown")

# Placeholder for next actions (e.g., JSON generation)
st.markdown("---")
