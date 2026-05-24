import os
import json
from datetime import datetime
import google.generativeai as genai

TOPICS_FILE = "content/topics.json"

# Configure Gemini
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

# Load topics
with open(TOPICS_FILE, "r") as f:
    topics = json.load(f)

# Find first pending topic
topic = next(
    (t for t in topics if t["status"] == "pending"),
    None
)

if not topic:
    raise Exception("No pending topics found.")

# Load master prompt
with open("templates/master_prompt.txt", "r") as f:
    template = f.read()

prompt = template.format(
    title=topic["title"],
    angle=topic["angle"],
    key_points=", ".join(topic["key_points"]),
    cta=topic["cta"]
)

# Generate response
response = model.generate_content(prompt)

# Parse generated JSON
generated_data = json.loads(response.text)

# Final structured output
output = {
    "date": datetime.now().strftime("%Y-%m-%d"),
    "topic_id": topic["id"],
    "category": topic["category"],
    **generated_data
}

# Save file
os.makedirs("output/posts", exist_ok=True)

filename = f"output/posts/{datetime.now().strftime('%Y-%m-%d')}.json"

with open(filename, "w") as f:
    json.dump(output, f, indent=2)

print(json.dumps(output, indent=2))
