# AI Web Terminal

A minimalist web-based AI coding chat interface designed for users who prefer keyboard-driven interactions over traditional GUI chatbots. Switch between AI models, manage conversations, and interact with AI assistants using simple terminal commands.

Targetted at developers


## Overview

AI Web Terminal provides a clean, distraction-free environment for AI interactions. Built for developers, power users, and anyone who appreciates the efficiency of command-line interfaces, this application brings the simplicity of terminal interactions to AI conversations.

**Perfect for users who want to:**
- Use AI in a minimalist, focused environment
- Switch between different AI models quickly using keyboard commands
- Avoid cluttered chat interfaces and unnecessary UI elements
- Copy code blocks and responses efficiently
- Maintain conversation flow without mouse interactions

## Features

### 🤖 Multi-Model AI Support
- **DeepSeek Chat v3.1** (default) - Fast and capable general-purpose model
- **Meta Llama 3.3 70B** - Powerful open-source language model
- **Google Gemini 2.0 Flash** - Google's latest experimental model
- Easy model switching with `!aimodel [model]` command

### ⌨️ Keyboard-First Design
- Pure keyboard navigation - no mouse required
- Terminal-style command interface
- Instant model switching without UI menus
- Quick copy commands for responses and code blocks

### 🛠️ Developer-Friendly Features
- Structured code block formatting with unique identifiers
- Individual code block copying (`!cc1`, `!cc2`, etc.)
- Full response copying with `!copy`
- Professional AI assistant with step-by-step explanations

### 📋 Built-in Commands
- `!help` - Show all available commands
- `!aimodel [model]` - Switch AI models (deepseek, llama, gemini)
- `!clear` - Clear conversation history
- `!copy` - Copy last AI response to clipboard
- `!cc[n]` - Copy specific code block to clipboard
- `!stop` - Cancel ongoing AI request
- `!exit` - Close the terminal

## Tech Stack

### Backend
- **Python 3.x** - Core application logic
- **Flask** - Lightweight web framework for API endpoints
- **OpenAI Python SDK** - AI model integration via OpenRouter

### Frontend
- **HTML5** - Semantic structure
- **Vanilla JavaScript** - Terminal interaction logic and API communication
- **CSS3** - Terminal-style theming with monospace fonts

### AI Integration
- **OpenRouter API** - Unified access to multiple AI models
- **Free tier models** - No API costs for basic usage
- **Async request handling** - Non-blocking AI interactions with cancellation support

### Architecture
- **RESTful API** - Clean separation between frontend and backend
- **AJAX communication** - Smooth real-time interactions
- **Modular design** - Easy to extend with new models and commands

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AIWebTerminalApp
   ```

2. **Install dependencies**
   ```bash
   pip install flask openai
   ```

3. **Configure API access**
   - Create a `config.py` file
   - Add your OpenRouter API key:
     ```python
     OPENROUTER_API_KEY = "your_openrouter_api_key_here"
     secret_key = "your_flask_secret_key_here"
     ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   - Navigate to `http://localhost:5000`
   - Start chatting with AI using terminal commands!

## Usage Examples

```bash
# Switch to Llama model
!aimodel llama

# Ask a coding question
How do I implement a binary search in Python?

# Copy the first code block from the response
!cc1

# Switch to Gemini model
!aimodel gemini

# Clear conversation history
!clear

# Get help
!help
```

## Why Choose AI Web Terminal?

- **Minimalist Focus** - No distracting UI elements, just you and the AI
- **Keyboard Efficiency** - Everything accessible via keyboard shortcuts
- **Multi-Model Flexibility** - Test different AI models without switching applications
- **Developer Optimized** - Built by developers, for developers
- **Zero Configuration** - Works out of the box with free AI models
- **Privacy Friendly** - No data stored locally, conversations exist only during session

