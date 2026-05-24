
import json

TOPICS_FILE = "content/topics.json"

def mark_posted(topic_id):
    with open(TOPICS_FILE, "r") as f:
        topics = json.load(f)

    for topic in topics:
        if topic["id"] == topic_id:
            topic["status"] = "posted"

    with open(TOPICS_FILE, "w") as f:
        json.dump(topics, f, indent=2)
