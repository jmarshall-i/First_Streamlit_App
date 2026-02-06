import streamlit as st
import pandas as pd
from rapidfuzz import fuzz, process

#Establishes tab title and adds an emoji to it
st.set_page_config(
    page_title="Minecraft Item Database",
    page_icon="🪵",
    layout="wide"
)
#When user loads page they'll likely see this first. It explains the purpose of the page
st.title("🧱 Minecraft Item Database")
st.markdown("Search items, filter by category, and explore details in a clean interface.")

# Sidebar
st.sidebar.header("Filters")
category_filter = st.sidebar.selectbox(
    "Category",
    ["All", "Mob Drop", "Food", "Material"]
)

# Load data via a defined function
@st.cache_data
def load_data():
    return pd.read_csv("items.csv")

df = load_data()

# Search bar
search_query = st.text_input(
    "🔍 Search for an item",
    placeholder="Try: Oak Log, Diamond, Eye of Ender"
)

# Fuzzy search
def fuzzy_search(query, choices, limit=50):
    results = process.extract(
        query,
        choices,
        scorer=fuzz.WRatio,
        limit=limit
    )
    return [match[0] for match in results if match[1] > 60]

if search_query:
    matched_names = fuzzy_search(search_query, df["item_name"].tolist())
    results = df[df["item_name"].isin(matched_names)]
else:
    results = df

# Category filter
if category_filter != "All":
    results = results[results["category"] == category_filter]


st.markdown("---")
st.subheader("📦 Item Details")

st.dataframe(
    results,
    use_container_width=True,
    hide_index=True
)