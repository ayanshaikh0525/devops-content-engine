
import json
from openai import OpenAI
from pick_topic import get_next_topic

client = OpenAI()

topic = get_next_topic()

with open("templates/linkedin_prompt.txt", "r") as f:
    template = f.read()

prompt = template.format(
    title=topic["title"],
    angle=topic["angle"],
    key_points=", ".join(topic["key_points"]),
    cta=topic["cta"]
)

response = client.chat.completions.create(
    model="gpt-5.5",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

post = response.choices[0].message.content

with open("output/posts/latest_post.txt", "w") as f:
    f.write(post)

print(post)
