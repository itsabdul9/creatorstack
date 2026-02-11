import os
from flask import Flask, render_template, request, redirect, url_for, session
from openai import OpenAI

app = Flask(__name__)
app.secret_key = "supersecretkey"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form["topic"]
        content_type = request.form["content_type"]
        platform = request.form["platform"]

        prompt = f"""
You are an expert YouTube growth strategist.

Create HIGH-RETENTION content.

Details:
Topic: {topic}
Content Type: {content_type}
Platform: {platform}

Generate:
1. 5 Highly Clickable Titles
2. Scroll-Stopping Hook
3. Full Script (Hook → Build-up → Emotional Peak → CTA)
4. SEO Optimized Description
5. 15 Hashtags
6. Thumbnail Text Idea
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        session["output"] = response.choices[0].message.content

        return redirect(url_for("index"))

    output = session.pop("output", None)
    return render_template("index.html", output=output)


if __name__ == "__main__":
    app.run(debug=True)
