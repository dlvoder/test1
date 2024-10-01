from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
import re

app = Flask(__name__)
CORS(app)

@app.route('/api/search', methods=['GET'])
def search_images():
    '''query = request.args.get('q', '')
    print(query)
    if not query:
        return jsonify(['reberto'])'''
    query = 'get me my proof on supremum'
    openai.api_key = os.getenv('OPENAI_API_KEY')
    directory = r"C:\Users\dmitr\test1\descriptions"
    file_contents = ['filename: 2222222222222.jpg, description: The image displays handwritten mathematical work on lined paper. The topic appears to be related to the supremum (sup) and infimum (inf) of sets. Detailed descriptions of each step are given, with logical derivations shown clearly.\n\nHere's the detailed content of the writing:\n\n---\n\n**Q7**\n\n**Let \\( x \\in A \\) and \\( y \\in B \\)**.\n\n(i) For any \\( x + y \\), \\( x \\leq \\sup A \\) and \\( y \\leq \\sup B \\).\n\nConsider \\( x \\leq \\sup A \\Rightarrow x + \\sup B \\leq \\sup A + \\sup B \\).\n\\[\n\\Downarrow\n\\]\n\\( x + y \\leq x + \\sup B \\leq \\sup A + \\sup B \\)\n\\[\n\\Downarrow\n\\]\n\\( x + y \\leq \\sup A + \\sup B \\)\n\n\u2234 \\( \\sup (A + B) = \\sup A + \\sup B \\)\n\n(ii) For any \\( x + y \\), \\( x \\geq \\inf A \\) and \\( y \\geq \\inf B \\).\n\nConsider \\( x \\geq \\inf A \\Rightarrow x + \\inf B \\geq \\inf A + \\inf B \\).\n\\[\n\\Downarrow\n\\]\n\\( x + y \\geq x + \\inf B \\geq \\inf A + \\inf B \\)\n\\[\n\\Downarrow\n\\]\n\\( x + y \\geq \\inf A + \\inf B \\)\n\n\u2234 \\( \\inf (A + B) = \\inf A + \\inf B \\)\n\n---\n\nThis solution goes through the proof of how the supremum and infimum of the sum of two sets \\( A \\) and \\( B \\) relate to the supremum and infimum of the individual sets. The logic is clear, and the steps are broken down meticulously. The handwriting is neat and legible.']

    '''for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                content = file.read()
                file_contents.append(f"Filename: {filename}\nContent:\n{content}")'''

    response = openai.chat.completions.create(
        model='gpt-4o', 
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Give the file names that best matches this query: " + query},
                    {"type": "text", "text": "\n\n".join(file_contents)}
                ],
            }
        ],
        max_tokens=4000,
    )

    output = response.choices[0].message.content
    matched_images = list(set(re.findall(r'\d{13}\.txt', output)))
    jpg_files = [file.replace('.txt', '.jpg') for file in matched_images] 
    print(output)
    print(jpg_files)
    return jsonify(jpg_files)

if __name__ == '__main__':
    app.run()
