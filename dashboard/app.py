import streamlit as st
from google.cloud import firestore, storage
import uuid
from datetime import datetime
#from streamlit_extras.card import card 

# --- CONFIGURATION ---
PROJECT_ID = "nimble-root-464019-j7"
BUCKET_NAME = "leaf_diseases_dataset_hakathon"
COLLECTION_NAME = "plant_data"

# --- FIRESTORE + STORAGE SETUP ---
db = firestore.Client(project=PROJECT_ID)
storage_client = storage.Client(project=PROJECT_ID)

st.title("🌿 Generative Hydro AI Dashboard")

def upload_to_gcs(file, destination_blob_name):
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"streamlit_upload/{destination_blob_name}")
    blob.upload_from_file(file, content_type=file.type)
    blob.make_public()  # Optional: make image public
    
    gcs_url = f"gs://{BUCKET_NAME}/streamlit_upload/{destination_blob_name}"  # GCS URL for internal use
    public_url= blob.public_url  
    
    return gcs_url,public_url

def store_data_to_firestore(data):
    db.collection(COLLECTION_NAME).document(data["image_id"]).set(data)

# def display_dashboard():
#     st.title("🌿 Hyperphonics AI Dashboard")
#     docs = db.collection(COLLECTION_NAME).stream()
#     for doc in docs:
#         data = doc.to_dict()
#         st.image(data.get("image_url"), width=300, caption=data.get("image_id"))
#         col1, col2, col3, col4 = st.columns(4)
#         col1.metric("pH", data.get("ph"))
#         col2.metric("PPM", data.get("ppm"))
#         col3.metric("TDS", data.get("tds"))
#         col4.metric("Temp (°C)", data.get("temperature"))
#         st.markdown(f"**Leaf Condition**: {data.get('plant_health', 'Analyzing...')}")
#         st.info(data.get("recommendation", "Generating recommendation..."))
#         st.divider()

def display_dashboard():
    st.set_page_config(layout="wide")
    st.header("Review Plant Diagnoses")
    docs = db.collection(COLLECTION_NAME) \
         .order_by("timestamp", direction=firestore.Query.DESCENDING) \
         .stream()

    for doc in docs:
        data = doc.to_dict()
        st.markdown("---")
        
        # Row layout
        col_left, col_right = st.columns([1, 2])

        with col_left:
            image_url = data.get("image_url")
            if image_url:
                st.image(image_url, width=250, caption=f"🖼️ {data.get('image_id')}")
            else:
                st.warning(f"⚠️ No image found for ID: {data.get('image_id')}")

        with col_right:
            # Metrics with emojis/icons
            c1, c2, c4 = st.columns(3)
            c1.metric("🧪 pH", data.get("ph"))
            c2.metric("🔬 TDS", data.get("tds"))
            c4.metric("🌡️ Temp (°C)", data.get("temperature"))

            # Health condition
            st.markdown(
                f"<div style='padding:10px; background-color:#e8f5e9; border-radius:10px;'><strong>🩺 Leaf Condition:</strong> {data.get('plant_health', 'Analyzing...')}</div>",
                unsafe_allow_html=True
            )

            # Recommendation block
            st.markdown(
                        f"""
                        <div style='margin-top:10px; padding:10px; background-color:#fff3e0;
                                    border-left:5px solid #ffa726; border-radius:5px;'>
                            <strong>💡 Recommendation:</strong><br>{data.get('recommendation', 'Generating...')}
                        </div>
                        """,
                        unsafe_allow_html=True
                        )


    st.markdown("----")


# --- STREAMLIT APP START ---
st.set_page_config(page_title="Generative Hydro AI", layout="wide")
tabs = st.tabs(["📥 Submit Leaf Data", "📊 Dashboard"])

# Tab 1: Data Submission
with tabs[0]:
    st.header("Submit New Leaf Data")

    ph = st.number_input("pH Level", min_value=0.0, max_value=14.0, step=0.1)
    tds = st.number_input("TDS", min_value=0)
    temperature = st.number_input("Temperature (°C)", min_value=-10.0, max_value=50.0, step=0.1)
    image = st.file_uploader("Upload Leaf Image", type=["jpg", "jpeg", "png"])

    if st.button("Submit"):
        if image:
            image_id = f"leaf_{uuid.uuid4()}.jpg"
            gcs_url,image_url = upload_to_gcs(image, image_id)

            data = {
                "ph": ph,
                "tds": tds,
                "temperature": temperature,
                "image_id": image_id,
                "image_gcs_url": gcs_url,
                "image_url": image_url,
                "plant_health": "Pending",
                "recommendation": "Pending",
                "timestamp": datetime.utcnow()  # store UTC time
            }

            store_data_to_firestore(data)
            st.success("✅ Uploaded successfully!")
            st.image(image_url, width=300)
        else:
            st.warning("⚠️ Please upload an image before submitting.")

# Tab 2: Dashboard
with tabs[1]:
    display_dashboard()
