import base64
import json
from google.cloud import storage, firestore

def upload_dummy_image(bucket_name, image_id):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(image_id)
    blob.upload_from_filename("leaf_sample.jpg")  # local placeholder image

def publish_vision_trigger(pubsub_topic, data):
    from google.cloud import pubsub_v1
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("your-project-id", pubsub_topic)
    publisher.publish(topic_path, json.dumps(data).encode("utf-8"))

def process_pubsub(event, context):
    data = json.loads(base64.b64decode(event['data']).decode("utf-8"))
    
    # Upload dummy image
    upload_dummy_image("your-bucket-name", data["image_id"])

    # Store in Firestore
    db = firestore.Client()
    db.collection("plant_data").document(data["image_id"]).set(data)

    # Trigger Vision function
    publish_vision_trigger("leaf-vision", data)
