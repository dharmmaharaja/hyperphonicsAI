 # 🌿 Hyperphonics AI

Hyperphonics AI is a GCP-based smart plant monitoring and recommendation system using:

- Pub/Sub + IoT simulator
- Firestore & Cloud Storage
- Vertex AI Vision for leaf health detection
- Vertex AI Gemini for natural language recommendations
- Streamlit dashboard (Cloud Run-ready)

## 💻 How to Use

1. Simulate IoT data with `iot_simulator/simulator.py`
2. Deploy Cloud Functions (`ingest_data`, `vision_trigger`)
3. Deploy custom Vertex AI Vision model
4. Enable Gemini API in Vertex AI
5. Run Streamlit dashboard via Cloud Run
 
 
 
 
     +-----------------+
     |  IoT Simulator  |  <-- Python: sensor + image
     +--------+--------+
              |
              v
     +-----------------+
     |   Pub/Sub       |
     | "sensor-data"   |
     +--------+--------+
              |
              v
+--------------------------+
|  Cloud Function (Trigger)|
|                          |
| - Parse data             |
| - Store to Firestore     |
| - Upload image to GCS    |
| - Call Vertex AI Vision  |
+--------------------------+
              |
              v
   +------------------------+
   | Vertex AI Vision       |
   | Leaf Condition Detection|
   +------------------------+
              |
              v
+--------------------------+
| Store Leaf Health Output |
|      in Firestore        |
+--------------------------+
              |
              v
+--------------------------+
| Vertex Gemini (LLM)      |
| Prompt: sensor + health  |
| → Recommendation         |
+--------------------------+
              |
              v
+--------------------------+
|  Firestore (Final Result)|
|  - Sensor Data           |
|  - Leaf Health           |
|  - Recommendation        |
+--------------------------+
              |
              v
+--------------------------+
| Streamlit on Cloud Run   |
| - Dashboard UI           |
| - Show data + images     |
| - Health + tips          |
+--------------------------+
