## 🚀 Features

- **🌐 Real-time Web Search**: Get latest information from Serper API
- **📚 Internal Knowledge Base**: Semantic search with ChromaDB
- **🧠 AI-Powered Synthesis**: Google Gemini for comprehensive answers
- **💬 Conversational Interface**: Streamlit web app
- **🆓 Free Tier**: Works with free APIs and mock data

## 🛠️ Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API key ([Get free key](https://aistudio.google.com/))
- Optional: Serper API key ([100 free searches/month](https://serper.dev/))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/subh839/subh839-My-Research-Pro.git
cd subh839-My-Research-Pro
Create virtual environment

bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Configure environment

bash
cp .env.example .env
# Edit .env with your API keys
Run the application

bash
streamlit run app.py
Visit http://localhost:8501 in your browser.

⚙️ Configuration
Edit .env file:

env
# Required: Get from https://aistudio.google.com/
GEMINI_API_KEY=your_actual_gemini_key_here

# Optional: Get from https://serper.dev/ (100 free searches/month)
SERPER_API_KEY=your_serper_key_here

# Database path
CHROMA_DB_PATH=./chroma_db



🚀 Deployment Fixes Summary
🔧 Core Issues Fixed
1. Python Compatibility
Forced Python 3.9 (3.13 had package conflicts)

Added runtime.txt for version control

2. Dependency Conflicts
Pinned huggingface-hub to v0.16.4 (last version with cached_download)

Added missing six module dependency

Used compatible package versions to prevent conflicts

3. Error Handling
Graceful fallbacks when dependencies fail

User-friendly status messages instead of crashes

Basic functionality even with limited dependencies

🛠️ Technical Solutions
File Updates:
requirements.txt - Compatible dependency versions

runtime.txt - Python 3.9 specification

app.py - Enhanced error recovery

.streamlit/config.toml - Cloud configuration

Key Features:
Progressive enhancement - Basic → Full features

Clear system status indicators

Automatic fallbacks to mock data

Troubleshooting guidance for users

Reliable, user-friendly, and production-ready! 🚀

