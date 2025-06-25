import streamlit as st
from google.cloud import firestore

st.set_page_config(page_title="Hyperphonics AI Dashboard", layout="wide")
db = firestore.Client()
docs = db.collection("plant_data").stream()

st.title("Hyperphonics AI Dashboard")

for doc in docs:
    data = doc.to_dict()
    st.image(f"https://storage.googleapis.com/your-bucket-name/{data['image_id']}", width=300)
    st.metric("pH", data["ph"])
    st.metric("PPM", data["ppm"])
    st.metric("TDS", data["tds"])
    st.metric("Temperature", f"{data['temperature']} °C")
    st.markdown(f"**Leaf Condition**: {data.get('plant_health', 'Analyzing...')}")
    st.info(data.get("recommendation", "Generating recommendation..."))
    st.markdown("---")