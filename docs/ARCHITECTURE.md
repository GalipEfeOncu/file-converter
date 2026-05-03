# System Architecture — Universal File Workstation

```mermaid
graph TD
    User((User)) --> UI[Streamlit UI]
    UI --> Dash[Dashboard]
    Dash --> Conv[FileConverter]
    Dash --> View[FileViewer]
    Dash --> AI[AIEngine]
    
    Conv --> Libs[External Libraries]
    Libs --> P1[PyMuPDF]
    Libs --> P2[Pillow]
    Libs --> P3[python-docx]
    Libs --> P4[pypandoc]
    Libs --> P5[pdf2docx]
    
    AI --> Gemini[Gemini 1.5 Flash API]
    
    subgraph Core Logic
        Conv
        View
        AI
        Player[AudioConverter]
    end
    
    subgraph Storage
        Temp[(temp/)]
        Prefs[(~/.preferences.json)]
    end
    
    Dash --> Temp
    Dash --> Prefs
```

## Key Modules
1. **`main.py`**: Entry point, session state, and layout orchestration.
2. **`core/converter.py`**: Business logic for format transformations.
3. **`core/viewer.py`**: Rendering and preview logic for UI.
4. **`core/ai_engine.py`**: LLM integration and prompt management.
5. **`ui/dashboard.py`**: Streamlit layout and user interaction components.
