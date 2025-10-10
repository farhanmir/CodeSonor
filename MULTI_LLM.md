# Multi-LLM Provider Support 🤖

CodeSonor v0.3.0+ supports multiple LLM (Large Language Model) providers for AI-powered code analysis!

## Supported Providers

| Provider | Models | API Cost | Speed | Get API Key |
|----------|---------|----------|-------|-------------|
| **Google Gemini** ⭐ | gemini-1.5-flash, gemini-1.5-pro | Free tier available | Fast | [Get Key](https://aistudio.google.com/app/apikey) |
| **OpenAI** | gpt-3.5-turbo, gpt-4, gpt-4-turbo | Pay per use | Medium | [Get Key](https://platform.openai.com/api-keys) |
| **Anthropic Claude** | claude-3-haiku, claude-3-sonnet, claude-3-opus | Pay per use | Fast | [Get Key](https://console.anthropic.com/settings/keys) |
| **Mistral AI** | mistral-small, mistral-large | Pay per use | Fast | [Get Key](https://console.mistral.ai/api-keys/) |
| **Groq** ⚡ | mixtral-8x7b, llama3-70b, gemma-7b | Free tier available | Very Fast | [Get Key](https://console.groq.com/keys) |

⭐ = Recommended for beginners (has free tier)  
⚡ = Fastest inference

## Quick Setup

### Option 1: Interactive Setup (Recommended)

```bash
codesonor setup
```

This wizard will:
1. Let you choose your preferred LLM provider
2. Guide you to get the API key
3. Optionally select a specific model
4. Save everything to `~/.codesonor/config.json`

### Option 2: Manual Configuration

Edit `~/.codesonor/config.json`:

```json
{
  "github_token": "ghp_your_token_here",
  "llm_provider": "openai",
  "llm_api_key": "sk-your-openai-key",
  "llm_model": "gpt-4-turbo"
}
```

### Option 3: Environment Variables

```bash
# Set your provider
export OPENAI_API_KEY="sk-your-key"
# or
export ANTHROPIC_API_KEY="sk-ant-your-key"
# or
export MISTRAL_API_KEY="your-key"
# or
export GROQ_API_KEY="gsk_your-key"
```

### Option 4: CLI Flags (Per-Command)

```bash
codesonor analyze URL \
  --llm-provider openai \
  --llm-api-key sk-your-key \
  --llm-model gpt-4
```

## Installation

### Base Installation (Gemini only - default)

```bash
pip install codesonor
```

### Install with Specific Provider

```bash
# OpenAI
pip install codesonor[openai]

# Anthropic Claude
pip install codesonor[anthropic]

# Mistral AI
pip install codesonor[mistral]

# Groq
pip install codesonor[groq]

# Install ALL providers
pip install codesonor[all-llm]
```

## Usage Examples

### Using Default Provider (from config)

```bash
codesonor analyze https://github.com/pallets/flask
```

### Using Specific Provider

```bash
# OpenAI GPT-4
codesonor analyze https://github.com/torvalds/linux \
  --llm-provider openai \
  --llm-model gpt-4

# Anthropic Claude
codesonor analyze https://github.com/django/django \
  --llm-provider anthropic \
  --llm-model claude-3-opus-20240229

# Groq (super fast!)
codesonor analyze https://github.com/python/cpython \
  --llm-provider groq \
  --llm-model mixtral-8x7b-32768
```

### Check Your Configuration

```bash
codesonor config
```

Output:
```
📋 CodeSonor Configuration

┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Setting       ┃ Status        ┃ Source     ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ GitHub Token  │ ✅ Configured │ config     │
│ LLM Provider  │ Openai        │ config     │
│ LLM Model     │               │ gpt-4      │
│ LLM API Key   │ ✅ Configured │ config     │
└───────────────┴───────────────┴────────────┘
```

## Provider-Specific Notes

### Google Gemini (Default)
- **Best for**: Beginners, free usage
- **Free tier**: Yes (60 requests/minute)
- **Pros**: Fast, free, no credit card needed
- **Cons**: May have content filters

### OpenAI
- **Best for**: Highest quality analysis
- **Free tier**: No (pay per use)
- **Pros**: Best quality, most reliable
- **Cons**: Most expensive, requires payment method
- **Models**: 
  - `gpt-3.5-turbo` - Cheap and fast
  - `gpt-4` - Best quality
  - `gpt-4-turbo` - Good balance

### Anthropic Claude
- **Best for**: Long code analysis, context understanding
- **Free tier**: No (pay per use)
- **Pros**: Large context window, great at code
- **Cons**: Requires payment
- **Models**:
  - `claude-3-haiku-20240307` - Fastest, cheapest
  - `claude-3-sonnet-20240229` - Balanced
  - `claude-3-opus-20240229` - Most capable

### Mistral AI
- **Best for**: European users, open-source friendly
- **Free tier**: No (pay per use)
- **Pros**: Fast, European servers
- **Cons**: Smaller model selection

### Groq
- **Best for**: Speed, experimentation
- **Free tier**: Yes
- **Pros**: Incredibly fast inference
- **Cons**: Limited rate limits on free tier

## Troubleshooting

### "Provider not available" error

Install the provider's package:
```bash
pip install openai  # for OpenAI
pip install anthropic  # for Claude
pip install mistralai  # for Mistral
pip install groq  # for Groq
```

### Check what's installed

```python
python -c "import openai; print('OpenAI installed')"
```

### Reset configuration

```bash
codesonor reset
```

### Test different providers

```bash
# Try Gemini (free)
codesonor analyze URL --llm-provider gemini

# Try Groq (free, fast)
codesonor analyze URL --llm-provider groq

# Try OpenAI (paid, best quality)
codesonor analyze URL --llm-provider openai --llm-model gpt-3.5-turbo
```

## API Key Priority

CodeSonor checks for API keys in this order:

1. **CLI flags** (`--llm-api-key`)
2. **Config file** (`~/.codesonor/config.json`)
3. **Environment variables** (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.)

## Migration from v0.2.0

Old configuration (Gemini only):
```json
{
  "github_token": "...",
  "gemini_key": "..."
}
```

Will automatically work! CodeSonor converts it to:
```json
{
  "github_token": "...",
  "llm_provider": "gemini",
  "llm_api_key": "..."
}
```

Legacy `--gemini-key` flag still works but shows a deprecation warning.

## Cost Comparison (Approximate)

Based on analyzing a repository with 1,000 lines of code analyzed (3 files):

| Provider | Cost per Analysis | Free Tier |
|----------|-------------------|-----------|
| Gemini | Free | 60 req/min |
| Groq | Free | 30 req/min (free tier) |
| OpenAI (GPT-3.5) | $0.001 | No |
| OpenAI (GPT-4) | $0.03 | No |
| Claude (Haiku) | $0.001 | No |
| Claude (Opus) | $0.015 | No |
| Mistral (Small) | $0.002 | No |

## Examples

### Budget Setup (Free)
```bash
# Use Gemini (best free option)
codesonor setup
# Select: 1 (Gemini)
```

### Quality Setup (Paid)
```bash
# Use OpenAI GPT-4
codesonor setup
# Select: 2 (OpenAI)
# Select model: 1 (gpt-4)
```

### Speed Setup (Free/Paid)
```bash
# Use Groq (fastest)
codesonor setup
# Select: 5 (Groq)
```

## Contributing

Want to add support for more LLM providers? Check out `src/codesonor/llm_providers.py` and submit a PR!
