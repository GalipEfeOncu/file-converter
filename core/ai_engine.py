"""
core/ai_engine.py — AI-Powered Document Analysis Module
Owner: Galip Efe Öncü (Project Architect)

Responsibility:
    Analyse text-based files (PDF, DOCX, TXT, CSV) using either the Groq API
    or the DeepSeek API.  The active provider is resolved at call time from
    st.session_state["ai_provider"] (set by the UI selector) and falls back to
    Config.AI_PROVIDER (.env).

    Supported operations: summarise, question-answering, keyword extraction,
    text simplification.

    Output language: **always English**, regardless of the input document's
    language.  This is enforced via the system prompts.
"""

import logging
import streamlit as st

from config.settings import Config

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# ---------------------------------------------------------------------------
# Provider constants
# ---------------------------------------------------------------------------
PROVIDER_GROQ = "groq"
PROVIDER_DEEPSEEK = "deepseek"

# Best value-for-performance models (as of 2026-05):
#   Groq     → llama-3.3-70b-versatile  (fast inference, free tier generous)
#   DeepSeek → deepseek-chat            (DeepSeek-V3, best quality/cost ratio)
_GROQ_MODEL = "llama-3.3-70b-versatile"
_DEEPSEEK_MODEL = "deepseek-chat"
_DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# ---------------------------------------------------------------------------
# System Prompts — English-only output enforced in every prompt
# ---------------------------------------------------------------------------
_SYSTEM_PROMPTS: dict[str, str] = {
    "summarize": (
        "You are a professional document summarisation assistant. "
        "Summarise the user-provided text concisely, preserving the main "
        "ideas and critical details. "
        "IMPORTANT: Always respond in English regardless of the input language."
    ),
    "summarize_short": (
        "You are a professional document summarisation assistant. "
        "Summarise the provided text in AT MOST 2-3 sentences, keeping only "
        "the single most important idea. "
        "IMPORTANT: Always respond in English regardless of the input language."
    ),
    "summarize_long": (
        "You are a professional document summarisation assistant. "
        "Provide a detailed summary of the provided text, covering all "
        "important points, arguments, and supporting details. "
        "IMPORTANT: Always respond in English regardless of the input language."
    ),
    "qa": (
        "You are a precise question-answering assistant. "
        "Answer the user's question using ONLY information present in the "
        "provided context text. "
        "If the answer cannot be found in the context, clearly state that. "
        "IMPORTANT: Always respond in English regardless of the input language."
    ),
    "keywords": (
        "You are a keyword-extraction assistant. "
        "Extract the most important and representative keywords from the "
        "provided text. Write one keyword per line. "
        "Return ONLY the keywords — no explanations, no numbering. "
        "IMPORTANT: Always respond in English regardless of the input language."
    ),
    "simplify": (
        "You are a text-simplification assistant. "
        "Rewrite the provided text in clearer, simpler, and more readable "
        "language. Replace technical jargon with everyday equivalents while "
        "preserving the original meaning. "
        "IMPORTANT: Always respond in English regardless of the input language."
    ),
    "simplify_basic": (
        "You are a text-simplification assistant. "
        "Rewrite the provided text so that anyone can understand it. "
        "Use very short sentences and plain, everyday vocabulary. "
        "Completely replace all technical terms with simple words. "
        "IMPORTANT: Always respond in English regardless of the input language."
    ),
    "simplify_advanced": (
        "You are a text-improvement assistant. "
        "Improve the flow and readability of the provided text while "
        "preserving its technical accuracy and terminology. "
        "Write at an academic or professional level. "
        "IMPORTANT: Always respond in English regardless of the input language."
    ),
}

# ---------------------------------------------------------------------------
# Length / level → system prompt key maps
# ---------------------------------------------------------------------------
_SUMMARY_LENGTH_MAP: dict[str, str] = {
    "short": "summarize_short",
    "medium": "summarize",
    "long": "summarize_long",
}

_SIMPLIFY_LEVEL_MAP: dict[str, str] = {
    "basic": "simplify_basic",
    "intermediate": "simplify",
    "advanced": "simplify_advanced",
}


class AIEngine:
    """AI-powered document analysis — supports Groq and DeepSeek providers.

    The active provider is determined lazily at each call from
    ``st.session_state["ai_provider"]`` (set by the UI selector).  If that
    key is absent, ``Config.AI_PROVIDER`` is used as the default.

    All methods return an English string (or list[str] for keywords).
    When an API key is missing or a network error occurs, a graceful English
    fallback message is returned instead of raising an exception.
    """

    # ------------------------------------------------------------------
    # Initialisation — lazy: actual clients are built on first call
    # ------------------------------------------------------------------
    def __init__(self):
        self._groq_client = None
        self._deepseek_client = None
        self._groq_ready = False
        self._deepseek_ready = False
        self._initialise_providers()

    def _initialise_providers(self):
        """Attempt to build both provider clients from available API keys."""
        self._init_groq()
        self._init_deepseek()

    # ------------------------------------------------------------------
    # Provider-specific init helpers
    # ------------------------------------------------------------------
    def _init_groq(self):
        """Initialise the Groq client using GROQ_API_KEY from .env / secrets."""
        api_key = self._read_api_key("GROQ_API_KEY", Config.GROQ_API_KEY)
        if not api_key:
            logging.warning("Groq: API key missing — Groq provider will be unavailable.")
            return

        try:
            from groq import Groq
            self._groq_client = Groq(api_key=api_key)
            self._groq_ready = True
            logging.info(f"Groq: client initialised (model: {_GROQ_MODEL}).")
        except ImportError:
            logging.error("Groq: 'groq' package not installed. Run: pip install groq")
        except Exception as exc:
            logging.error(f"Groq: initialisation failed — {exc}")

    def _init_deepseek(self):
        """Initialise the DeepSeek client (OpenAI-compatible) using DEEPSEEK_API_KEY."""
        api_key = self._read_api_key("DEEPSEEK_API_KEY", Config.DEEPSEEK_API_KEY)
        if not api_key or api_key == "your_deepseek_api_key_here":
            logging.warning("DeepSeek: API key missing — DeepSeek provider will be unavailable.")
            return

        try:
            from openai import OpenAI
            self._deepseek_client = OpenAI(
                api_key=api_key,
                base_url=_DEEPSEEK_BASE_URL,
            )
            self._deepseek_ready = True
            logging.info(f"DeepSeek: client initialised (model: {_DEEPSEEK_MODEL}).")
        except ImportError:
            logging.error("DeepSeek: 'openai' package not installed. Run: pip install openai")
        except Exception as exc:
            logging.error(f"DeepSeek: initialisation failed — {exc}")

    # ------------------------------------------------------------------
    # API key resolution helper
    # ------------------------------------------------------------------
    @staticmethod
    def _read_api_key(env_name: str, config_value: str | None) -> str | None:
        """Return the API key from session secrets, then Config, then None."""
        # 1. Try Streamlit secrets (production deployment)
        try:
            val = st.secrets.get(env_name)
            if val:
                return val
        except Exception:
            pass
        # 2. Fall back to Config (loaded from .env via dotenv)
        return config_value or None

    # ------------------------------------------------------------------
    # Active-provider resolution
    # ------------------------------------------------------------------
    def _active_provider(self) -> str:
        """Return the currently selected provider from session_state or Config."""
        return st.session_state.get("ai_provider", Config.AI_PROVIDER).lower()

    # ------------------------------------------------------------------
    # Core call dispatcher
    # ------------------------------------------------------------------
    def _call_ai(self, prompt: str, system: str | None = None) -> str:
        """Route the request to the active provider and return the response.

        Falls back gracefully with an informative English message on any error.
        """
        provider = self._active_provider()

        if provider == PROVIDER_DEEPSEEK:
            return self._call_deepseek(prompt, system)
        else:
            return self._call_groq(prompt, system)

    def _call_groq(self, prompt: str, system: str | None = None) -> str:
        """Send a request to the Groq API."""
        if not self._groq_ready:
            return (
                "Groq API connection failed. "
                "Please set GROQ_API_KEY in your .env file and ensure the "
                "'groq' package is installed."
            )

        try:
            logging.info("Groq: sending request...")
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            response = self._groq_client.chat.completions.create(
                model=_GROQ_MODEL,
                messages=messages,
            )
            logging.info("Groq: response received successfully.")
            return response.choices[0].message.content
        except Exception as exc:
            logging.error(f"Groq: API call failed — {exc}")
            return f"Groq request failed. Details: {exc}"

    def _call_deepseek(self, prompt: str, system: str | None = None) -> str:
        """Send a request to the DeepSeek API (OpenAI-compatible)."""
        if not self._deepseek_ready:
            return (
                "DeepSeek API connection failed. "
                "Please set DEEPSEEK_API_KEY in your .env file and ensure the "
                "'openai' package is installed."
            )

        try:
            logging.info("DeepSeek: sending request...")
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            response = self._deepseek_client.chat.completions.create(
                model=_DEEPSEEK_MODEL,
                messages=messages,
            )
            logging.info("DeepSeek: response received successfully.")
            return response.choices[0].message.content
        except Exception as exc:
            logging.error(f"DeepSeek: API call failed — {exc}")
            return f"DeepSeek request failed. Details: {exc}"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def summarize(self, text: str, length: str = "medium") -> str:
        """Summarise the provided text.

        Args:
            text:   Raw text to summarise.
            length: Summary length — "short" | "medium" | "long".

        Returns:
            English summary string, or a graceful fallback on error.
        """
        if not text or not text.strip():
            return "No text provided for summarisation."

        prompt_key = _SUMMARY_LENGTH_MAP.get(length, "summarize")
        return self._call_ai(text, system=_SYSTEM_PROMPTS[prompt_key])

    def answer_question(self, context: str, question: str) -> str:
        """Answer the user's question using the provided context.

        Args:
            context:  Source text (context).
            question: User's question.

        Returns:
            English answer string, or a graceful fallback on error.
        """
        if not context or not context.strip():
            return "No context text provided for question answering."
        if not question or not question.strip():
            return "Please enter a question."

        prompt = f"Context:\n{context}\n\nQuestion: {question}"
        return self._call_ai(prompt, system=_SYSTEM_PROMPTS["qa"])

    def extract_keywords(self, text: str, top_k: int = 10) -> list[str]:
        """Extract keywords from the provided text.

        Args:
            text:  Text to analyse.
            top_k: Maximum number of keywords to return.

        Returns:
            List of English keyword strings; empty list on error.
        """
        if not text or not text.strip():
            logging.error("Keyword extraction: no text provided.")
            return []

        prompt = (
            f"Extract the {top_k} most important keywords from the following text. "
            f"Write one keyword per line. Return ONLY the keywords:\n\n{text}"
        )
        raw = self._call_ai(prompt, system=_SYSTEM_PROMPTS["keywords"])

        # Detect error / fallback messages
        if raw.startswith(("Groq request failed", "DeepSeek request failed",
                            "Groq API connection", "DeepSeek API connection")):
            logging.error(f"Keyword extraction failed: {raw}")
            return []

        keywords = [
            line.strip().lstrip("•-–—*0123456789. ")
            for line in raw.strip().splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        return keywords[:top_k]

    def simplify(self, text: str, level: str = "intermediate") -> str:
        """Simplify / rewrite the provided text.

        Args:
            text:  Text to simplify.
            level: Simplification level — "basic" | "intermediate" | "advanced".

        Returns:
            English simplified text, or a graceful fallback on error.
        """
        if not text or not text.strip():
            return "No text provided for simplification."

        prompt_key = _SIMPLIFY_LEVEL_MAP.get(level, "simplify")
        return self._call_ai(text, system=_SYSTEM_PROMPTS[prompt_key])

    # ------------------------------------------------------------------
    # Provider status helpers (used by the UI to show readiness)
    # ------------------------------------------------------------------
    def is_groq_ready(self) -> bool:
        """Return True if the Groq client is initialised and ready."""
        return self._groq_ready

    def is_deepseek_ready(self) -> bool:
        """Return True if the DeepSeek client is initialised and ready."""
        return self._deepseek_ready

    def available_providers(self) -> list[str]:
        """Return a list of provider IDs that have valid API keys."""
        providers = []
        if self._groq_ready:
            providers.append(PROVIDER_GROQ)
        if self._deepseek_ready:
            providers.append(PROVIDER_DEEPSEEK)
        return providers
