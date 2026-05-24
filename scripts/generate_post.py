import os
import json
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

# Load prompt template
with open("templates/linkedin_prompt.txt", "r") as f:
    template = f.read()

prompt = template.format(
    title=topic["title"],
    angle=topic["angle"],
    key_points=", ".join(topic["key_points"]),
    cta=topic["cta"]
)

# Generate content
response = model.generate_content(prompt)

post = response.text

# Create output folder
os.makedirs("output/posts", exist_ok=True)

# Save generated post
with open("output/posts/latest_post.txt", "w") as f:
    f.write(post)

print(post)
