import google.generativeai as genai
from google.adk.agents import Agent
import os
from dotenv import load_dotenv
import uuid

def get_service_types() -> list:
    """
    Retrieves a list of available service request types.
    """
    return [
        "Noise Complaint",
        "Illegal Parking",
        "Street Light Outage",
        "Graffiti",
        "Damaged Tree"
    ]

def submit_service_request(service_name: str, description: str, address: str) -> dict:
    """
    Submits a new service request.

    Args:
        service_name: The type of service request (e.g., "Noise Complaint").
        description: A detailed description of the issue.
        address: The address where the issue is located.
    """
    if service_name not in get_service_types():
        return {"error": "Invalid service name."}
    
    request_id = str(uuid.uuid4())
    return {
        "request_id": request_id,
        "status": "open",
        "service_name": service_name,
        "description": description,
        "address": address
    }

def check_request_status(request_id: str) -> dict:
    """
    Checks the status of a previously submitted service request.

    Args:
        request_id: The unique ID of the service request.
    """
    # For this mock, we'll just return a static status.
    # A real implementation would check a database.
    return {
        "request_id": request_id,
        "status": "In Progress",
        "service_name": "Mock Service",
        "description": "This is a mock status for your request.",
        "address": "123 Mock St"
    }

# Load environment variables from .env file
load_dotenv()

# Configure the generative AI model with the API key from the environment
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file or environment variables.")
genai.configure(api_key=api_key)

# Define the ADK Agent
root_agent = Agent(
    name="nyc_311_agent",
    model="gemini-2.5-flash",
    description="Agent to interact with the NYC 311 mock API to submit and check service requests.",
    instruction="You are a helpful agent that can assist users with NYC 311 service requests. You can list available service types, submit new requests, and check the status of existing requests.",
    tools=[get_service_types, submit_service_request, check_request_status],
)