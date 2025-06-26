import vertexai
from google.oauth2 import service_account
from vertexai.preview.generative_models import GenerativeModel

def get_gemini_recommendation(data: dict) -> str:

    creds = service_account.Credentials.from_service_account_file(
    r"C:/Users/dharm/Downloads/nimble-root-464019-j7-cba4bb80f715.json"
    )
    vertexai.init(
        project="nimble-root-464019-j7",
        location="us-central1",  # or your preferred region
        credentials=creds
    )
    prompt = f"""
     Given the following in my hydroponics plant system for tomato:
    - pH: {data.get('ph')}
    - TDS: {data.get('tds')}
    - Temperature: {data.get('temperature')}°C
    - Leaf condition: {data.get('plant_health')}

    Suggest next step for improving plant health and nutrient balance in 150 words.
    """
    
    model = GenerativeModel("gemini-2.5-pro")
    
    response = model.generate_content(prompt)
    
    return response.text if hasattr(response, 'text') else str(response)


def main():
    # Example input data


    sample_data = {
        "ph": 6.5,
        "tds": 900,
        "temperature": 28,
        "plant_health": "Yellowing and curling leaves with brown spots"
    }

    # Call Gemini recommendation function
    recommendation = get_gemini_recommendation(sample_data)
    
    print("\n--- Gemini Recommendation ---")
    print(recommendation)

if __name__ == "__main__":
    main()
