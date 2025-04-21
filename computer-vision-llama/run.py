import ollama
import os 

path_dir = os.path.dirname(os.path.abspath(__file__))
path_dir = path_dir + "/Meta.png"
print(path_dir)

response = ollama.chat(
    model='llama3.2-vision',
    messages=[{
        'role': 'user',
        'content': 'What is in this image?',
        'images': [path_dir]
    }]
)

print(response)