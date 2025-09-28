# =========================================
# CORD-19 Research Papers Analysis - Streamlit App
# Author: Trizah
# =========================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------
# App Title
# -------------------------
st.title("📚 CORD-19 Research Papers Analysis")
st.write("Explore COVID-19 research metadata interactively.")

# -------------------------
# Load Data
# -------------------------
@st.cache
def load_data():
    df = pd.read_csv("metadata.csv")
    df = df.dropna(subset=['title', 'abstract'])  # Remove missing titles/abstracts
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')  # Convert to datetime
    return df

df = load_data()

st.sidebar.header("Filters")

# -------------------------
# Sidebar Filters
# -------------------------
# Filter by Year
years = df['publish_time'].dt.year.dropna().unique()
selected_years = st.sidebar.multiselect("Select Years", sorted(years), default=sorted(years))

# Filter by Journal
journals = df['journal'].dropna().unique()
selected_journals = st.sidebar.multiselect("Select Journals", journals, default=journals)

# Apply Filters
filtered_df = df[
    (df['publish_time'].dt.year.isin(selected_years)) &
    (df['journal'].isin(selected_journals))
]

# -------------------------
# Show Raw Data
# -------------------------
if st.checkbox("Show Raw Data"):
    st.subheader("Filtered Dataset")
    st.write(filtered_df[['title','authors','journal','publish_time']].head(50))

# -------------------------
# Visualization 1: Top Journals
# -------------------------
st.subheader("Top 10 Journals by Number of Papers")
journal_counts = filtered_df['journal'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(x=journal_counts.values, y=journal_counts.index, palette="viridis", ax=ax)
ax.set_xlabel("Number of Papers")
ax.set_ylabel("Journal")
st.pyplot(fig)

# -------------------------
# Visualization 2: Papers Per Year
# -------------------------
st.subheader("Number of Papers Published Per Year")
papers_per_year = filtered_df['publish_time'].dt.year.value_counts().sort_index()
fig2, ax2 = plt.subplots(figsize=(10,5))
sns.lineplot(x=papers_per_year.index, y=papers_per_year.values, marker="o", ax=ax2)
ax2.set_xlabel("Year")
ax2.set_ylabel("Number of Papers")
ax2.set_title("Papers Published Per Year")
st.pyplot(fig2)

# -------------------------
# Visualization 3: Paper Length Distribution (by Abstract Length)
# -------------------------
st.subheader("Distribution of Abstract Lengths")
filtered_df['abstract_length'] = filtered_df['abstract'].apply(lambda x: len(str(x).split()))
fig3, ax3 = plt.subplots(figsize=(10,5))
sns.histplot(filtered_df['abstract_length'], bins=30, color="skyblue", edgecolor="black", ax=ax3)
ax3.set_xlabel("Number of Words in Abstract")
ax3.set_ylabel("Count")
st.pyplot(fig3)

# -------------------------
# Visualization 4: Scatter Plot - Abstract Length vs Publication Year
# -------------------------
st.subheader("Abstract Length vs Publication Year")
fig4, ax4 = plt.subplots(figsize=(10,5))
sns.scatterplot(
    x=filtered_df['publish_time'].dt.year,
    y=filtered_df['abstract_length'],
    hue=filtered_df['journal'],
    palette="tab10",
    ax=ax4,
    legend=False
)
ax4.set_xlabel("Publication Year")
ax4.set_ylabel("Abstract Length (words)")
st.pyplot(fig4)

# -------------------------
# Observations / Insights
# -------------------------
st.subheader("📌 Observations / Insights")
st.markdown("""
- Some journals have published significantly more COVID-19 research papers than others.
- Paper publication trends vary by year; peaks can be seen corresponding to COVID-19 waves.
- Abstract lengths vary widely; some papers have very concise abstracts, while others are very detailed.
- Scatter plot shows relationship between abstract length and year, highlighting patterns in publishing practices.
""")
