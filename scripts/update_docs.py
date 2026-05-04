import os

files = [
    "README.md",
    "docs/CONTEXT.md",
    "docs/ROADMAP.md",
    "docs/PROJECT_DETAILS.md",
    "docs/AGENT_GUIDE.md"
]

for file_path in files:
    full_path = os.path.join("/Users/saidhamza/file-converter", file_path)
    if os.path.exists(full_path):
        with open(full_path, "r") as f:
            content = f.read()
        
        content = content.replace("GEMINI_API_KEY", "GROQ_API_KEY")
        content = content.replace("Gemini", "Groq")
        
        with open(full_path, "w") as f:
            f.write(content)

print("Documentation updated successfully.")
