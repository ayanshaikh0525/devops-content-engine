
import os
import json
from datetime import datetime
from google import genai
from PIL import Image
from io import BytesIO
import base64

# Configure Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

today = datetime.now().strftime("%Y-%m-%d")

post_file = f"output/posts/{today}.json"

# Load generated post
with open(post_file, "r") as f:
    post_data = json.load(f)

thumbnail_prompt = post_data["thumbnail_prompt"]

# Generate image using Imagen
response = client.models.generate_images(
    model="imagen-3.0-generate-002",
    prompt=thumbnail_prompt,
    config={
        "number_of_images": 1
    }
)

# Extract image bytes
image_data = response.generated_images[0].image.image_bytes

# Save image
os.makedirs("output/thumbnails", exist_ok=True)

image_path = f"output/thumbnails/{today}.png"

with open(image_path, "wb") as f:
    f.write(image_data)

print(f"Thumbnail saved: {image_path}")
