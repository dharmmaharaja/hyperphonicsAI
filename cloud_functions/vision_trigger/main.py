from google.cloud import firestore
import sys
import os

# Add project root (hyperphonicsAI) to sys.path so Python can find vertex_ai
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from vertex_ai.gemini.get_recommendation import get_gemini_recommendation
from vertex_ai.vision.predict_leaf_condition import get_leaf_condition

def process_document(doc_id, data):
    # Get leaf condition
    condition = get_leaf_condition(data["image_gcs_url"])
    data["plant_health"] = condition

    # Get Gemini recommendation
    recommendation = get_gemini_recommendation(data)

    # Update Firestore document
    db = firestore.Client()
    db.collection("plant_data").document(doc_id).update({
            "plant_health": condition,
            "recommendation": recommendation
        })

    print(f"Processed {doc_id} \n → Condition: {condition}, \n Recommendation: {recommendation}")


def main():
    db = firestore.Client()
    docs = db.collection("plant_data").stream()

    for doc in docs:
        doc_data = doc.to_dict()
        doc_id = doc.id
        print(f"Processing document ID: {doc_id}")

        if doc_data.get("plant_health") == "Pending":
            print(f"Document {doc_id} has {doc_data} plant_health='Pending'. Calling process_document.")
            process_document(doc_id, doc_data)

if __name__ == "__main__":
    main()