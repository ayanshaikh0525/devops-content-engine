import os
import json
import requests
from datetime import datetime

ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
PERSON_URN = os.getenv("LINKEDIN_PERSON_URN")

today = datetime.now().strftime("%Y-%m-%d")

image_path = f"output/thumbnails/{today}.png"

# STEP 1: Register upload
register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN.strip()}",
    "Content-Type": "application/json"
}

register_payload = {
    "registerUploadRequest": {
        "recipes": [
            "urn:li:digitalmediaRecipe:feedshare-image"
        ],
        "owner": PERSON_URN,
        "serviceRelationships": [
            {
                "relationshipType": "OWNER",
                "identifier": "urn:li:userGeneratedContent"
            }
        ]
    }
}

register_response = requests.post(
    register_url,
    headers=headers,
    json=register_payload
)

register_data = register_response.json()

upload_url = register_data["value"]["uploadMechanism"][
    "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
]["uploadUrl"]

asset = register_data["value"]["asset"]

print("ASSET:", asset)

# STEP 2: Upload image binary
with open(image_path, "rb") as image_file:
    upload_response = requests.put(
        upload_url,
        data=image_file,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN.strip()}"
        }
    )

print("UPLOAD STATUS:", upload_response.status_code)

# Save asset URN
os.makedirs("output/assets", exist_ok=True)

asset_file = f"output/assets/{today}.json"

with open(asset_file, "w") as f:
    json.dump({
        "asset": asset
    }, f)
