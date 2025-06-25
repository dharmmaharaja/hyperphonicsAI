from vertex_ai.vision.predict_leaf_condition import get_leaf_condition
from vertex_ai.gemini.get_recommendation import get_gemini_recommendation
from google.cloud import firestore

def process_pubsub(event, context):
    import json, base64
    data = json.loads(base64.b64decode(event['data']).decode("utf-8"))
    image_id = data["image_id"]

    condition = get_leaf_condition(image_id)
    data["plant_health"] = condition

    # Generate recommendation
    recommendation = get_gemini_recommendation(data)

    # Save all to Firestore
    db = firestore.Client()
    db.collection("plant_data").document(image_id).update({
        "plant_health": condition,
        "recommendation": recommendation
    })
