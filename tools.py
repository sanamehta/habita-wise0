import openai
from openai import OpenAI
from dotenv import load_dotenv
import requests
import os

load_dotenv()

PERPLEXITY_API_KEY = os.environ.get("PERPLEXITY_API_KEY")
VAPI_AUTH_TOKEN = os.environ.get("VAPI_AUTH_TOKEN")


def get_local_organization_info(city, state, issue):
    """
    Get information about the local organization in the given city and state that deals with tenant complaints against landlords.
    """
    messages = [
    {
        "role": "system",
        "content": (
            """
            You are an AI agent tasked with helping users find official or community-based government agencies that handle tenancy issues in their location. Your goal is to follow the output format and redirect user to accurate and verified organization that user can go to:
            
            1. Identify the Relevant Organization:
            Search for the top organization(s) responsible for addressing tenancy issues in the user location. This could include official government agencies, tenant advocacy groups, community organizations, or small claims courts.
            Verify the authenticity of the organization by checking its official website or reputable sources.
            
            2. Determine Complaint Reporting Methods:
            Find the methods available for reporting a complaint or filing a case with the identified organization. These methods and steps might include: Calling a phone number. Sending an email. Submitting a complaint through an online portal or form. Visiting an office in person (if applicable). Also, determine what information user needs in order to file the complaint case.

            3. Output the Information:
            Present the information clearly and concisely in the following format:
            Organization: [NAME]
            Method: [LIST A METHOD TO REPORT including applicable Contact info to report such as phone number, email address, online form link, physical address]
            Steps: []

            Hypothetical Example Response:
            Organization: City of Santa Rosa Court
            
            Method 1: Call 415 555 1234
            Steps: Call and Give your name, address, landlord name, issue description, issue origin date.
            
            Method 2: Email contact@domain.com 
            Steps: Email with your address, evidence photos, and phone number.

            NOTE
            - Include only actionable and up-to-date contact details.
            - If multiple options are available, prioritize official method only.
            - Adapt your search based on the user location and specific tenancy-related needs.
            - If precise location information is unavailable, provide general guidance and suggest additional steps for the user to confirm local jurisdiction details.
            - Your output should strictly follow the format given in step 3, do NOT say anything else. You can NOT advise on anything. You are not supposed to remedy the user's issue.
            """
        ),
    },
    {   
        "role": "user",
        "content": (
            f"I am based in {city} {state}. My issue is {issue}. How and where can I file a complaint against landlord officially? Give me the organization name, method, and steps to file a complaint."
        ),
    },
    ]
    client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")
    response = client.chat.completions.create(
    model="llama-3.1-sonar-large-128k-online",
    messages=messages,
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

def phone_call_organization(organization_name, organization_phone_number, steps, tenant_name, tenant_address, landlord_name, issue_description, additional_issue_info):
    """
    Call the organization and follow the steps to file a complaint.
    """
    organization_phone_number = '+14152871837'
    # Your Vapi API Authorization token
    auth_token = VAPI_AUTH_TOKEN
    # The Phone Number ID, and the Customer details for the call
    phone_number_id = 'd9449e50-7038-4d75-a6ce-727542feaa33'
    customer_number = organization_phone_number
    # Create the header with Authorization token
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }
    # Create the data payload for the API request
    data = {
    'assistant': {
        "firstMessage": f"Hello, I am calling on behalf of a tenant name {tenant_name}. I have a complaint against the landlord named {landlord_name}. I want to file an official complaint. Can you help me?",
        "model": {
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are an legal representative assistant. You are calling the organization: {organization_name} to file a complaint against landlord. You are following the steps to file a complaint: {steps}. The tenant name is {tenant_name}. The tenant address is {tenant_address}. The landlord name is {landlord_name}. The issue description is {issue_description}. The additional issue info is {additional_issue_info}"
                }
            ]
        },
        "voice": "jennifer-playht"
    },
    'phoneNumberId': phone_number_id,
        'customer': {
            'number': customer_number,
        },
    }   
    # Make the POST request to Vapi to create the phone call
    response = requests.post(
        'https://api.vapi.ai/call/phone', headers=headers, json=data)
    # Check if the request was successful and print the response
    if response.status_code == 201:
        print(response.json())
        return 'Call created successfully'
    else:
        print(response.text)
        return 'Failed to create call'

TOOL_MAP = {"get_local_organization_info": get_local_organization_info, "phone_call_organization": phone_call_organization}
