from vertexai.preview.generative_models import GenerativeModel

def get_gemini_recommendation(data):
    prompt = f"""
    Given the following:
    - pH: {data['ph']}
    - PPM: {data['ppm']}
    - TDS: {data['tds']}
    - Temperature: {data['temperature']}°C
    - Leaf condition: {data['plant_health']}

    Suggest remedies.
    """
    model = GenerativeModel("gemini-1.5-pro-preview-0409")
    res = model.generate_content(prompt)
    return res.text
