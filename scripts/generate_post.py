import os
import json
from openai import OpenAI
# topics
TOPICS_FILE = "content/topics.json"

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Load topics
with open(TOPICS_FILE, "r") as f:
    topics = json.load(f)

# Find pending topic
topic = next(
    (t for t in topics if t["status"] == "pending"),
    None
)

if not topic:
    raise Exception("No pending topics found.")

# Load prompt template
with open("templates/linkedin_prompt.txt", "r") as f:
    template = f.read()

prompt = template.format(
    title=topic["title"],
    angle=topic["angle"],
    key_points=", ".join(topic["key_points"]),
    cta=topic["cta"]
)

# Generate post
response = client.chat.completions.create(
    model="gpt-5.5",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

post = response.choices[0].message.content

# Create output directory
os.makedirs("output/posts", exist_ok=True)

# Save post
with open("output/posts/latest_post.txt", "w") as f:
    f.write(post)

print(post)
