import streamlit as st
import pandas as pd
import json
from PIL import Image
import os
from script import alibaba_image_search
import time


def create_image_name():
    timestamp = int(time.time())
    return f"uploaded_image_{timestamp}.png"


st.set_page_config(page_title="Alibaba Suppliers Viewer", layout="wide")
st.title("Alibaba Suppliers Viewer")

st.write(
    "Upload an image (optional). The app will display the uploaded image and show extracted suppliers data from suppliers_data.json."
)

uploaded = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
if uploaded:
    try:
        img = Image.open(uploaded)
        # Save uploaded image next to this script so existing tools can pick it up
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(data_dir, exist_ok=True)
        save_path = os.path.join(data_dir, create_image_name())
        img.save(save_path)
        st.success(f"Saved uploaded image to {save_path}")

        # record uploaded path in session state so we don't re-run automatically
        st.session_state["uploaded_path"] = save_path
    except Exception as e:
        st.error(f"Could not open/save image: {e}")

# Provide an explicit control to run the scraper to avoid running on every rerun
if st.session_state.get("uploaded_path"):
    st.markdown("**Uploaded image ready.**")
    if st.button("Run scraper on uploaded image"):
        uploaded_path = st.session_state.get("uploaded_path")
        # avoid re-running for the same image unless user wants to
        if st.session_state.get("scrape_done_for") == uploaded_path:
            st.info("Scraper already run for this uploaded image.")
        else:
            with st.spinner("Running scraper... this may open a browser window"):
                try:
                    alibaba_image_search(uploaded_path)
                    st.session_state["scrape_done_for"] = uploaded_path
                    st.success("Scraper finished — suppliers_data.json updated.")
                except Exception as e:
                    st.error(f"Scraper error: {e}")

# Load suppliers data
data_path = os.path.join(os.path.dirname(__file__), "suppliers_data.json")
if not os.path.exists(data_path):
    st.error(
        "suppliers_data.json not found in repository. Run the scraper or add the file."
    )
else:
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Flatten entries for table view
    rows = []
    for item in data:
        rows.append(
            {
                "company": item.get("company", ""),
                "location": item.get("location", ""),
                "gold_years": item.get("gold_years", ""),
                "rating": item.get("rating", ""),
                "reviews": item.get("reviews", ""),
                "main_products": ", ".join(item.get("main_products", [])),
                "featured_products": ", ".join(
                    [fp.get("price", "") for fp in item.get("featured_products", [])]
                ),
                "metrics": "; ".join(
                    [f"{k}: {v}" for k, v in item.get("metrics", {}).items()]
                ),
            }
        )

    df = pd.DataFrame(rows)

    st.subheader("Suppliers Table")
    st.dataframe(df)

    # Download as CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV", data=csv, file_name="suppliers_data.csv", mime="text/csv"
    )

    if st.checkbox("Show raw JSON"):
        st.json(data)
