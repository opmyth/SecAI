# secAI: Your AI Secretary

**Team Members:**
- Bassam Alshammari
- Hassan Alshanqiti

## Description
secAI is an AI-powered secretary that helps manage your tasks using voice commands or hand gestures. It can handle three main tasks:
1. Email Summary: View summaries of your unread emails
2. Calendar Meetings: Check today's meetings
3. Paper Updates: Get summaries of the latest computer vision papers

## Project Structure
```
├── credentials/
│   ├── credentials.json        # Google API credentials
│   ├── token.json             # Google API token
├── main.py                    # Main application file
├── modules/                   # Core functionality modules
│   ├── hand_gesture.py        # Hand gesture processing
│   ├── input_handlers.py      # Input processing
│   ├── llm_processor.py       # LLM integration
│   ├── speech_to_text.py      # Speech processing
├── utils/                     # Utility functions
│   ├── sdaiaAcademyLogo.png   # Logo file
│   ├── system_prompts.json    # System prompts
│   ├── ui.py                  # UI components
│   └── utils.py              # Utility functions
└── requirements.txt          # Project dependencies
```

## Prerequisites
- Python 3.12 or higher
- MacOS (for Calendar integration)
- Gmail account
- OpenAI API key

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/opmyth/SecAI
cd secAI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. API Setup

#### OpenAI API or deepseek API
1. Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/)
2. Set it as an environment variable:
```bash
export OPENAI_API_KEY='your-api-key'
export DEEPSEEK_API_KEY='your-api-key'
```

#### Google Gmail API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Gmail API
4. Create OAuth 2.0 credentials
5. Download the credentials and save as `credentials/credentials.json`

### 4. System Prompts
Modify `utils/system_prompts.json` with your custom prompts for:
- Hand gesture recognition
- Task classification
- Email summarization
- Content summarization

## Running the Application
```bash
python main.py
```

## Usage
### Voice Commands
- "Show my emails" - View email summary
- "Show my calendar" - View today's meetings
- "Get latest papers" - Get computer vision paper updates

### Hand Gestures
- ☝️ One finger - Email summary
- ✌️ Two fingers - Calendar meetings
- 👌 Three fingers - Paper updates

## Troubleshooting
- If calendar access fails, ensure you're on MacOS and have Calendar app permissions enabled
- For Gmail API issues, verify your credentials and token files
- For gesture recognition issues, ensure good lighting and clear hand gestures

