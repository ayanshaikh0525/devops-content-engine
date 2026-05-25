# pick topic 
import json

TOPICS_FILE = "content/topics.json"

def get_next_topic():
    with open(TOPICS_FILE, "r") as f:
        topics = json.load(f)

    for topic in topics:
        if topic["status"] == "pending":
            return topic

    return None

if __name__ == "__main__":
    topic = get_next_topic()

    if topic:
        print(topic)
    else:
        print("No pending topics found.")
