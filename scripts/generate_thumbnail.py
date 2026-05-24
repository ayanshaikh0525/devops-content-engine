import os
import json
import requests
from datetime import datetime
from urllib.parse import quote

today = datetime.now().strftime("%Y-%m-%d")

post_file = f"output/posts/{today}.json"

# Load generated content
with open(post_file, "r") as f:
    post_data = json.load(f)

prompt = post_data["thumbnail_prompt"]

# Encode prompt
encoded_prompt = quote(prompt)

# Pollinations image URL
image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

# Download image
response = requests.get(image_url)

# Save image
os.makedirs("output/thumbnails", exist_ok=True)

image_path = f"output/thumbnails/{today}.png"

with open(image_path, "wb") as f:
    f.write(response.content)

print(f"Thumbnail saved at: {image_path}")
