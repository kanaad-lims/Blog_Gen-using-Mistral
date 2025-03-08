from flask import Flask, render_template, request, jsonify
import markdown
from huggingface_hub import InferenceClient

app = Flask(__name__)


### Initializing the Hugging Face Inference Client
client = InferenceClient(
	provider="fireworks-ai",
	api_key="YOUR_API_KEY_HERE"    ### Write your HuggingFace api key under InferenceClient function.
)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form.get("blog_topic")
        word_limit = int(request.form.get("word_limit"))
        
        messages = [{"role": "user", "content": f"Write a well-structured blog post on {user_input}. Ensure the blog has proper conclusion."}]

        
        ### Calling the mistral API.
        completion = client.chat.completions.create(
            model="mistralai/Mistral-Small-24B-Instruct-2501", 
            messages=messages, 
            max_tokens=word_limit
        )
        
        ###Extract responce from the API
        
        blog_text = completion.choices[0].message.content.strip()
        formatted_blog = markdown.markdown(blog_text)
        return render_template("creation.html", blog = formatted_blog)
    
    return render_template("creation.html", blog = " ")

if __name__ == "__main__":
    app.run(debug=True)
    


