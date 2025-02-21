from flask import Flask, render_template, request, jsonify, url_for
import os
import fal_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)
application = app

# Function to call FAL AI API
def generate_image(prompt):
    result = fal_client.subscribe(
        "fal-ai/flux-realism",
        arguments={
            "prompt": prompt,
            "output_format": "jpeg"
        },
        with_logs=True
    )
    return result

@app.route("/", methods=["GET", "POST"])
def index():
    image_data = None
    error_message = None

    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()

        # Validate input length
        if len(prompt) == 0 or len(prompt) > 50:
            error_message = "Prompt must be between 1 and 50 characters."
        else:
            # Call the image generation API
            response = generate_image(prompt)

            if "images" in response and response["images"]:
                image_data = {
                    "url": response["images"][0]["url"],
                    "width": response["images"][0]["width"],
                    "height": response["images"][0]["height"],
                    "content_type": response["images"][0]["content_type"],
                    "timing": response["timings"]["inference"],
                    "prompt": response["prompt"]
                }
            else:
                error_message = "Image generation failed. Please try again."

    return render_template("index.html", image_data=image_data, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
