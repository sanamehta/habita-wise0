# Habita-Wise: Legal Tenant Rights Assistant 🏠⚖️

## Overview

Habita-Wise is an AI-powered Flask-based application designed to help tenants navigate complex legal situations, understand their rights, and take informed actions when facing issues with their rental properties.

### Key Features

- AI-Driven Guidance: Through conversational interaction, the app collects tenant issues and provides personalized guidance based on legal knowledge.
- Document Analysis: Upload and analyze rental agreements and related documents
- Resource Finding: Access to location-specific legal resources and information
- Automated Document Generation: Create necessary legal documents and communications
- Tenant Empowerment: Simplifies complex legal jargon for better understanding

## Prerequisites

### Required API Keys
You'll need to set up the following API keys in a `.env` file:
- `OPENAI_API_KEY`: OpenAI API key for AI assistance
- `ASSISTANT_ID`: Your specific OpenAI Assistant ID
- `PERPLEXITY_API_KEY`: Perplexity API key for research capabilities
- `VAPI_AUTH_TOKEN`: Vapi API token for communication features

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/habita-wise0.git
cd habita-wise0
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key
ASSISTANT_ID=your_assistant_id
PERPLEXITY_API_KEY=your_perplexity_api_key
VAPI_AUTH_TOKEN=your_vapi_auth_token
```

## Running the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
habita-wise0/
├── app.py              # Main Flask application
├── tools.py            # Core functionality and API integrations
├── requirements.txt    # Project dependencies
├── .env               # Environment variables (not tracked in git)
├── .gitignore         # Git ignore rules
├── static/            # Static assets (CSS, JavaScript, images)
├── templates/         # HTML templates for the web interface
├── uploads/           # Directory for uploaded documents
└── venv/             # Python virtual environment
```

## Dependencies

The project requires the following main dependencies (as specified in requirements.txt):
- Flask 3.0.2
- OpenAI 1.70.0
- python-dotenv 1.0.0
- requests 2.31.0
- python-dateutil 2.8.2
- email-validator 2.1.0.post1

## Usage

1. Start the application by running `python app.py`
2. Navigate to `http://localhost:5000` in your web browser
3. Upload relevant documents (rental agreement, notices, etc.)
4. Describe your tenant issue
5. Receive AI-powered guidance and recommendations
6. Generate necessary documents or find relevant resources

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.



