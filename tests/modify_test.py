import os

test_file = "/Users/saidhamza/file-converter/tests/test_ai_engine.py"
with open(test_file, "r") as f:
    content = f.read()

content = content.replace("_call_gemini", "_call_groq")
content = content.replace("Gemini", "Groq")
content = content.replace("GEMINI_API_KEY", "GROQ_API_KEY")

with open(test_file, "w") as f:
    f.write(content)

print("test_ai_engine.py updated successfully.")
