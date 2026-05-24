import os
import json
import requests
from datetime import datetime

ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
PERSON_URN = os.getenv("LINKEDIN_PERSON_URN")

# Load latest generated post
today = datetime.now().strftime("%Y-%m-%d")

post_file = f"output/posts/{today}.json"

asset_file = f"output/assets/{today}.json"


# Load generated content
with open(post_file, "r") as f:
    post_data = json.load(f)

content = post_data["content"]

hashtags = " ".join(post_data["hashtags"])

final_post = f"{content}\n\n{hashtags}"

url = "https://api.linkedin.com/v2/ugcPosts"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN.strip()}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0",
    "LinkedIn-Version": "202401"

}

payload = {
    "author": PERSON_URN,
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": final_post
            },
            "shareMediaCategory": "IMAGE",
                        "media": [
                            {
                                "status": "READY",
                                "description": {
                                    "text": post_data["title"]
                                },
                                "media": asset,
                                "title": {
                                    "text": post_data["title"]
                                }
                            }
                        ]
                    }
                },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

response = requests.post(
    url,
    headers=headers,
    json=payload
)

print(response.status_code)
print(response.text)

if response.status_code not in [200, 201]:
    raise Exception("LinkedIn publish failed.")
