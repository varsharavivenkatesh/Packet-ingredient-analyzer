# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
import re
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

api_key= os.getenv("GENAI_API_KEY")
genai.configure(api_key= api_key)

app = Flask(__name__)
CORS(app)

@app.route('/scan', methods=['POST'])
def scan_image():
    file = request.files['image']
    image = Image.open(file.stream)
    extracted_text = pytesseract.image_to_string(image)

    ingredients = extract_ingredients(extracted_text)

    if not ingredients:
        return jsonify({
            "error": "No ingredients found in the image. Please upload a clearer image or ensure the ingredients section is visible."
        }), 400

    ai_result = analyze_ingredients_with_genai(ingredients)
    return jsonify(ai_result)

def extract_ingredients(text):
    text = text.lower()
    match = re.search(r'ingredients[:\-]?\s*(.+)', text)
    if match:
        raw = match.group(1)
        return [i.strip() for i in re.split(r',|\.', raw) if i.strip()]
    return []


def analyze_ingredients_with_genai(ingredients):
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')

    prompt = (
        "You are a food safety expert.\n"
        "Classify the following ingredients as vegetarian or non-vegetarian and provide reasons:\n\n"
        f"{', '.join(ingredients)}"
    )

    response = model.generate_content(prompt)

    return {
        "ingredients": ingredients,
        "analysis": response.text
    }
if __name__ == "__main__":
    app.run(debug=True)
