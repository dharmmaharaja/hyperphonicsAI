from vertexai.vision_models import Image, ImageClassifierModel

def get_leaf_condition(image_id):
    model = ImageClassifierModel.from_pretrained("your-custom-model-id")
    image_path = f"gs://your-bucket-name/{image_id}"
    image = Image.load_from_gcs(image_path)
    prediction = model.predict(image=image)
    return prediction.classifications[0].display_name