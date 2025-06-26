from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
from google.cloud.aiplatform.gapic.schema import instance as instance_schema

import base64
from google.cloud import storage

def encode_image_to_base64(gcs_uri: str) -> str:
    """Downloads image from GCS and returns base64-encoded string."""
    if not gcs_uri.startswith("gs://"):
        raise ValueError("Only GCS URIs (gs://...) are supported.")

    bucket_name, blob_path = gcs_uri[5:].split("/", 1)
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)
    image_bytes = blob.download_as_bytes()
    return base64.b64encode(image_bytes).decode("utf-8")



def get_leaf_condition(image_uri: str):
    project = "nimble-root-464019-j7"
    location = "us-central1"
    endpoint_id = "4360589448480555008"

    aiplatform.init(project=project, location=location)

    endpoint = aiplatform.Endpoint(endpoint_name=f"projects/{project}/locations/{location}/endpoints/{endpoint_id}")

    # Encode image from GCS to base64
    image_base64 = encode_image_to_base64(image_uri)

    instance = {
        "content": image_base64,
        "mimeType": "image/jpeg"  # or "image/png", depending on your data
    }

    prediction = endpoint.predict(instances=[instance])

    result = prediction.predictions[0]
    confidences = result['confidences']
    display_names = result['displayNames']

    max_index = confidences.index(max(confidences))
    return display_names[max_index] 


def main():
    test_image_uri = "gs://leaf_diseases_dataset_hakathon/test_img/UF.GRC_BS_Lab Leaf 0666_bectarial_spot.JPG"  # Replace with your actual GCS image path
    test_image_uri2 = "gs://leaf_diseases_dataset_hakathon/test_img/288e94bf96b0___Crnl_L.Mold 9182.JPG"
    test_image_uri3= "gs://leaf_diseases_dataset_hakathon/test_img/a39d-86c22f64da83___GH_HL Leaf 356.JPG"
    condition = get_leaf_condition(test_image_uri3)
    print("Predicted Leaf Condition:", condition)


if __name__ == "__main__":
    main()