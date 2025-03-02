import openai
from openai import OpenAI
from dotenv import load_dotenv
import requests
import os
import json

# Load environment variables
load_dotenv()

# API Keys
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
            You are an AI agent tasked with helping users find official or community-based government agencies that handle tenancy issues in their location. Your goal is to follow the output format and redirect users to accurate and verified organizations with SPECIFIC contact details.
            
            1. Identify the Relevant Organization:
            Search for the top organization(s) responsible for addressing tenancy issues in the user location. This could include official government agencies, tenant advocacy groups, community organizations, or small claims courts.
            Verify the authenticity of the organization by checking its official website or reputable sources.
            
            2. Determine Complaint Reporting Methods:
            Find the EXACT methods available for reporting a complaint or filing a case with the identified organization including:
            - ACTUAL phone numbers with area codes (NO placeholders like "[Insert Phone Number]")
            - SPECIFIC email addresses (NO placeholders)
            - EXACT website URLs for online forms
            - COMPLETE physical addresses with zip codes
            - If you cannot find specific contact details, provide the OFFICIAL WEBSITE URL where the user can find this information
            
            3. Output the Information:
            Present the information clearly and concisely in the following format:
            Organization: [EXACT NAME]
            
            Method 1: Call [ACTUAL PHONE NUMBER WITH AREA CODE]
            Steps: [Step 1], [Step 2], [Step 3]
            
            Method 2: Email [SPECIFIC EMAIL ADDRESS]
            Steps: [Step 1], [Step 2], [Step 3]
            
            Method 3: Visit [COMPLETE PHYSICAL ADDRESS]
            Steps: [Step 1], [Step 2], [Step 3]
            
            IMPORTANT REQUIREMENTS:
            - NEVER use placeholders or phrases like "check the local directory"
            - Include ONLY methods where you can provide SPECIFIC contact information
            - If you cannot find specific contact details for a method, DO NOT include that method
            - Verify all information through official sources
            - Adapt your search based on the user location and specific tenancy-related needs
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
    
    try:
        client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")
        response = client.chat.completions.create(
            model="llama-3.1-sonar-large-128k-online",
            messages=messages,
        )
        result = response.choices[0].message.content
        print(f"Perplexity API Response: {result}")
        return result
    except Exception as e:
        print(f"Error in get_local_organization_info: {e}")
        return f"Failed to get organization info: {str(e)}"

def phone_call_organization(organization_name, organization_phone_number, steps, tenant_name, tenant_address, landlord_name, issue_description, additional_issue_info):
    """
    Call the organization and follow the steps to file a complaint.
    """
    try:
        # For demo purposes, we'll use a fixed phone number if one isn't provided
        #if not organization_phone_number or organization_phone_number == "":
        organization_phone_number = '+14152871837'
            
        # Your Vapi API Authorization token
        auth_token = "1657a012-7056-42cc-ac58-5ac03fcf8700"
        
        
        # The Phone Number ID, and the Customer details for the call
        phone_number_id = '9ed4e277-acd3-43d5-9754-4afbc0b8da72'
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
            result = response.json()
            print(f"Call created successfully: {result}")
            return 'Call created successfully'
        else:
            print(f"Failed to create call: {response.text}")
            return f'Failed to create call: {response.text}'
    except Exception as e:
        print(f"Error in phone_call_organization: {e}")
        return f"Failed to make phone call: {str(e)}"

# Map function names to their implementations for easy lookup
TOOL_MAP = {
    "get_local_organization_info": get_local_organization_info, 
    "phone_call_organization": phone_call_organization
}

def handle_tool_call(tool_call):
    """
    Process a tool call from the OpenAI assistant and execute the corresponding function.
    
    Args:
        tool_call: The tool call object from OpenAI
        
    Returns:
        The result of executing the function
    """
    try:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        print(f"Executing function: {function_name} with args: {function_args}")
        
        if function_name in TOOL_MAP:
            function_to_call = TOOL_MAP[function_name]
            
            # Use a thread-safe timeout approach using threading.Timer
            import threading
            import concurrent.futures
            
            # Execute function with a timeout
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(function_to_call, **function_args)
                try:
                    function_response = future.result(timeout=60)  # 60 seconds timeout
                    return function_response
                except concurrent.futures.TimeoutError:
                    return "Error: Function call timed out after 60 seconds"
        else:
            return f"Error: Function {function_name} not found in tool map"
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error executing function: {str(e)}\n{error_details}")
        return f"Error executing function: {str(e)}"