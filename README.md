# Habita-Wise: Legal Tenant Rights Assistant 🏠⚖️

## Overview

Tenant Rights Assistant is an AI-powered Streamlit application designed to help tenants navigate complex legal situations, understand their rights, and take informed actions when facing issues with their rental properties.

### Key Features

- AI-Driven Guidance: Through conversational interaction, the app collects tenant issues, retrieves insights from a database of historical landlord-tenant cases, and predicts the likelihood of success in legal disputes.

- Legal Resource Retrieval: An integrated Researcher agent fetches location-specific, up-to-date filing procedures, forms, and contact details.

- Automated Action Tools: Features like email drafting, report generation, and voice-enabled calls save time and reduce stress for tenants.

- Tenant Empowerment: The platform simplifies complex legal jargon, ensuring users understand their rights and are equipped to take informed action.

- Scalability: While the app initially focuses on California, it is designed to scale nationally to address the broader rental market.
- Legal Consultation: Generate lists of potential legal professionals
- Document Upload: Support for uploading and analyzing rental agreements and evidence

## Prerequisites

### Required API Keys
You'll need to set up the following API keys in a `.env` file:
- `OPENAI_API_KEY`: OpenAI API key for AI assistance
- `ASSISTANT_ID`: Your specific OpenAI Assistant ID
- `PERPLEXITY_API_KEY`: Perplexity API key for local organization research
- `VAPI_AUTH_TOKEN`: Vapi API token for potential phone call features

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tenant-rights-assistant.git
cd tenant-rights-assistant
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
streamlit run app.py
```

## Project Structure

- `app.py`: Main Streamlit application
- `tools.py`: Backend functions for API calls and tool handling
- `next_action_steps.py`: Generate interactive next action steps
- `style.css`: Custom styling for the application
- `.env`: Environment variables (not tracked in version control)

## Usage

1. Open the application in your browser
2. Upload relevant documents (rental agreement, notices, etc.)
3. Describe your tenant issue
4. Receive AI-powered guidance
5. Choose from next action steps:
   - File a Complaint with Local Authority
   - Communicate with Landlord
   - Consult Legal Professionals

Project Demo: [https://www.loom.com/share/4fc28087b0f143669264fa0576234c22?sid=67f74217-41e7-4d83-8e2f-3fac3fdfdf8a]

## Legal Disclaimer

This application provides general information and guidance. It is not a substitute for professional legal advice. Always consult with a qualified legal professional for specific legal concerns.



