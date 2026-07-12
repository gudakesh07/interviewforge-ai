# AI Providers

The provider interface lives in `app/services/ai/base.py`.

Supported provider names:

- `mock`
- `groq`
- `gemini`
- `openrouter`
- `ollama`

When a remote provider has no API key, the application falls back to Mock/local evaluation.

