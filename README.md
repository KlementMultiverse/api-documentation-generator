# API Documentation Generator

> Auto-generate API docs from code

[![Category](https://img.shields.io/badge/Category-LLM%20Applications-blue)]()
[![Domain](https://img.shields.io/badge/Domain-E-commerce-green)]()
[![Status](https://img.shields.io/badge/Status-Active-success)]()

## 🎯 Overview

Auto-generate API docs from code built with modern AI technologies including Ollama, DSPy.

This project demonstrates practical applications in the **E-commerce** domain.

## ✨ Features

- Code parsing
- Example generation
- Markdown output

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip or conda

### Installation

```bash
# Clone the repository
git clone https://github.com/KlementMultiverse/api-documentation-generator.git
cd api-documentation-generator

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Usage

```bash
# Run the main application
python src/main.py

# Run with examples
python examples/demo.py
```

## 📁 Project Structure

```
api-documentation-generator/
├── src/              # Source code
├── tests/            # Unit tests
├── examples/         # Usage examples
├── docs/             # Documentation
├── requirements.txt  # Dependencies
└── README.md         # This file
```

## 🛠️ Technology Stack

- **Ollama**
- **DSPy**

## 🔧 Configuration

Create a `.env` file in the root directory:

```env
# Add your API keys here (NEVER commit this file)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

## 📊 Examples

Check the `examples/` directory for:
- Basic usage examples
- Advanced use cases
- Integration patterns

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## 📝 Documentation

See the `docs/` folder for detailed documentation:
- Architecture overview
- API reference
- Deployment guide

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 👨‍💻 Author

**Klement Gunndu** - GenAI Engineer

- Portfolio: [klementmultiverse.github.io](https://klementmultiverse.github.io)
- LinkedIn: [klement-gunndu](https://www.linkedin.com/in/klement-gunndu-601872351)
- GitHub: [@KlementMultiverse](https://github.com/KlementMultiverse)

## 🙏 Acknowledgments

Built with Claude Code automation - part of my daily AI project challenge!

---

*Generated on 2025-10-06 as part of the Daily AI Project initiative*
