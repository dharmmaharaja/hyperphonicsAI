import json
import time
import random
from google.cloud import pubsub_v1

project_id = "your-project-id"
topic_id = "sensor-data"
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def generate_sensor_data():
    return {
        "ph": round(random.uniform(5.5, 7.5), 2),
        "tds": random.randint(100, 500),
        "temperature": round(random.uniform(20, 35), 1),
        "image_id": f"leaf_{int(time.time())}.jpg"
    }

while True:
    data = generate_sensor_data()
    publisher.publish(topic_path, json.dumps(data).encode("utf-8"))
    print(f"Published: {data}")
    time.sleep(10)
