# CodeSonor 🔍

**AI-powered GitHub repository analyzer with multi-LLM support** - Choose from 8 different AI providers!

[![PyPI version](https://img.shields.io/pypi/v/codesonor.svg)](https://pypi.org/project/codesonor/)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/pypi/dm/codesonor.svg)](https://pypi.org/project/codesonor/)

Analyze any GitHub repository with AI-powered insights. Get language statistics, code summaries, and repository metrics in seconds.

## 🚀 Quick Start

```bash
pip install codesonor
codesonor setup  # Interactive configuration wizard
codesonor analyze https://github.com/pallets/flask
```

## ✨ Features

- 🤖 **Multi-LLM Support** - Choose from Gemini, OpenAI, Claude, Mistral, or Groq
- 🔧 **Interactive Setup** - One-time configuration wizard saves your preferences
- 📊 **Language Analysis** - Distribution breakdown across 20+ programming languages
- 🧠 **AI Code Summaries** - AI-generated insights for key files
- 📈 **Repository Stats** - Stars, forks, contributors, file counts
- ⚡ **Fast Analysis** - Smart filtering and caching
- 🎨 **Beautiful Output** - Rich terminal formatting with tables and colors
- 💾 **Export Options** - JSON output for integration

## 🤖 Supported AI Providers

| Provider | Free Tier | Speed | Quality | Best For |
|----------|-----------|-------|---------|----------|
| **Gemini** ⭐ | ✅ Yes | Fast | Good | Beginners |
| **OpenAI** | ❌ Paid | Medium | Excellent | Production |
| **Claude** | ❌ Paid | Fast | Excellent | Long code |
| **Mistral** | ❌ Paid | Fast | Good | Europe |
| **Groq** ⚡ | ✅ Yes | Ultra-fast | Good | Speed |
| **OpenRouter** 🌐 | 💳 Pay-per-use | Fast | Excellent | 100+ models |
| **xAI Grok** | ❌ Paid | Fast | Excellent | Latest tech |
| **Ollama** 🆓 | ✅ FREE | Medium | Good | Privacy/Local |

⭐ Default provider | ⚡ Fastest inference | 🌐 Access to 100+ models | 🆓 Runs locally, no API key needed

## 📦 Installation

### Basic Installation (includes Gemini)
```bash
pip install codesonor
```

### With Specific Provider
```bash
pip install codesonor[openai]      # For OpenAI GPT
pip install codesonor[anthropic]   # For Claude
pip install codesonor[mistral]     # For Mistral
pip install codesonor[groq]        # For Groq
# Note: OpenRouter, xAI, and Ollama use OpenAI-compatible APIs (included by default)
pip install codesonor[all-llm]     # All providers
```

## 🔧 Configuration

### Interactive Setup (Recommended)
```bash
codesonor setup
```

This wizard will:
1. Let you choose your preferred AI provider
2. Guide you to get the API key
3. Optionally select a specific model
4. Save everything to `~/.codesonor/config.json`

### Manual Configuration

Edit `~/.codesonor/config.json`:
```json
{
  "github_token": "ghp_your_token_here",
  "llm_provider": "openai",
  "llm_api_key": "sk-your-key",
  "llm_model": "gpt-4"
}
```

### Environment Variables
```bash
# GitHub token (optional but recommended)
export GITHUB_TOKEN="ghp_your_token"

# LLM provider API keys (choose one or more)
export GEMINI_API_KEY="your_key"
export OPENAI_API_KEY="sk-your_key"
export ANTHROPIC_API_KEY="sk-ant-your_key"
export MISTRAL_API_KEY="your_key"
export GROQ_API_KEY="gsk_your_key"
export OPENROUTER_API_KEY="sk-or-your_key"
export XAI_API_KEY="xai-your_key"
# Ollama runs locally, no API key needed!
```

## 📖 Usage

### Basic Analysis
```bash
codesonor analyze https://github.com/torvalds/linux
```

### Use Specific Provider
```bash
# OpenAI GPT-4
codesonor analyze URL --llm-provider openai --llm-model gpt-4

# Anthropic Claude
codesonor analyze URL --llm-provider anthropic

# Groq (fastest)
codesonor analyze URL --llm-provider groq
```

### Advanced Options
```bash
# Skip AI analysis (stats only, faster)
codesonor analyze URL --no-ai

# Limit files analyzed
codesonor analyze URL --max-files 100

# Export as JSON
codesonor analyze URL --json-output results.json

# Quick summary without AI
codesonor summary https://github.com/django/django
```

### Check Configuration
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

## 🎯 Example Output

```
╭─────────────────────────────────────────────────╮
│  Repository: flask by pallets                   │
╰─────────────────────────────────────────────────╯

Stars: ⭐ 70,501  Forks: 🔱 16,551
Primary Language: Python
Total Files: 218

Language Distribution:
┏━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Language  ┃ Percentage ┃ Bar                     ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Python    │    95.80%  │ ███████████████████████ │
│ HTML      │     1.74%  │ █                       │
│ YAML      │     1.15%  │ █                       │
└───────────┴────────────┴─────────────────────────┘

🤖 AI-Powered Code Analysis
File 1: src/flask/app.py
Flask application core implementation. Defines the Flask class which
serves as the central object for WSGI applications...
```

## 🔑 Getting API Keys

- **Google Gemini** (Free): https://aistudio.google.com/app/apikey
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic Claude**: https://console.anthropic.com/settings/keys
- **Mistral AI**: https://console.mistral.ai/api-keys/
- **Groq** (Free): https://console.groq.com/keys
- **OpenRouter**: https://openrouter.ai/keys
- **xAI Grok**: https://console.x.ai
- **Ollama**: https://ollama.ai/download (FREE, runs locally!)
- **GitHub Token**: https://github.com/settings/tokens (optional, prevents rate limits)

## 🛠️ Tech Stack

- **Python 3.9+**
- **Click** - CLI framework
- **Rich** - Terminal formatting
- **Requests** - HTTP library
- **Multiple LLM SDKs** - OpenAI, Anthropic, Groq, Mistral, Google Generative AI

## 📚 Documentation

- [Multi-LLM Guide](MULTI_LLM.md) - Detailed guide on using different AI providers
- [CLI Documentation](CLI_README.md) - Complete CLI reference
- [Contributing](CONTRIBUTING.md) - How to contribute
- [Quick Start](QUICKSTART.md) - Get started in 5 minutes

## 🤝 Contributing

Contributions are welcome! Please check out our [Contributing Guide](CONTRIBUTING.md).

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🌟 Star History

If you find CodeSonor useful, please consider giving it a star! ⭐

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/farhanmir/CodeSonor/issues)
- **PyPI**: [PyPI Project](https://pypi.org/project/codesonor/)

## 🚀 What's New in v0.4.1

- � **OpenRouter Support** - Access to 100+ AI models with a single API key
- 🤖 **xAI Grok** - Latest AI from xAI
- 🆓 **Ollama Integration** - Run AI models locally for FREE (no API key needed!)
- 🧹 **Code Quality** - Enhanced metadata and package information
- � **8 LLM Providers** - More choice than ever before!

See [V0.4.1_UPDATE.md](V0.4.1_UPDATE.md) for complete details.

Made by [Farhan Mir](https://github.com/farhanmir)
