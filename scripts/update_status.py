import json

TOPICS_FILE = "content/topics.json"

with open(TOPICS_FILE, "r") as f:
    topics = json.load(f)

for topic in topics:
    if topic["status"] == "pending":
        topic["status"] = "posted"
        break

with open(TOPICS_FILE, "w") as f:
    json.dump(topics, f, indent=2)
