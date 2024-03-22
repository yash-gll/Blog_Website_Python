from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
import os
from langchain.llms import OpenAI as LangChainOpenAI

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI with the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# LangChain setup for GPT-3.5-turbo
llm = LangChainOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route('/generate-title', methods=['POST'])
def generate_title():
    content = request.json.get('content', '').strip()
    # Constructing a detailed prompt for GPT-3.5-turbo
    prompt = [
        {'role': 'system', 'content':"You are an AI tasked with generating a compelling blog title based on the content:\n"},
        {'role': 'system', 'content':f"Content:\n ---\n{content}\n---\n Considering the content, produce a creative and relevant blog title."},
    ]

    try:
        # Use LangChain for title generation with GPT-3.5-turbo
        response = openai.ChatCompletion.create(
            messages=prompt,
            model="gpt-3.5-turbo",
            max_tokens=60,
            temperature=0.7,
            stop=["\n"],
            n=1
        )

        generated_title = response['choices'][0]['message']['content'].strip() if response.choices else "Default Title"
        print(generate_title)

    except Exception as e:
        print(f"Error during title generation: {e}")
        return jsonify({'error': 'Failed to generate title'}), 500

    return jsonify({'title': generated_title})



@app.route('/generate-cover-image', methods=['POST'])
def generate_cover_image():
    data = request.json
    title = data.get('title', '').strip()
    # content = data.get('content', '').strip()
    
    prompt = title
    if not prompt:
        return jsonify({"error": "No title or content provided"}), 400

    try:
        # Make sure to replace "davinci-codex" with the specific model for DALL-E if it's different
        response = openai.Image.create(
            quality="standard",
            prompt=prompt,
            n=1,
            size="1024x1024",
            model="dall-e-3"
        )
        # Extract the URL of the generated image
        image_url = response.data[0].url
    
    except Exception as e:
        print(f"Error generating cover image: {e}")
        return jsonify({'error': 'Failed to generate title'}), 500
    
    return jsonify({'image_url': image_url})



if __name__ == '__main__':
    port = os.getenv('PORT', '5000')  # Use the PORT environment variable if set, otherwise default to 5000
    app.run(host='0.0.0.0', port=port)
