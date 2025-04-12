from crewai.tools.structured_tool import CrewStructuredTool
from crewai.tools import tool
from pydantic import BaseModel
import requests

@tool
def duke_event_api_tool(future_days: int):
    '''
    Calls the Duke Events API

    Parameters:
        future_days (int): future days to look ahead for events

    Returns:
        A Python dictionary of the following format:

        {
        "events": [
            {
            "id": "CAL-8a000483-92c3adf6-0194-dd19428a-000027cfdemobedework@mysite.edu",
            "start_timestamp": "2025-04-25T04:00:00Z",
            "end_timestamp": "2025-04-27T04:00:00Z",
            "summary": "Duke Datathon",
            "description": "Join us at the Duke Health IPEC Building for an exciting weekend focused on \"Data Science in Critical/Acute Care.\" The event kicks off with a symposium on Friday, April 25, followed by a two-day datathon where clinicians and data scientists collaborate to develop data-driven models using de-identified critical care datasets. No prior experience is required, and teams will be formed to blend clinical and data science expertise. Early registration (through Feb. 28) starts at $50 for trainees and $200 for faculty or industry participants. Registration fees increase on March 1. Sponsorship opportunities are also available.",
            "status": "CONFIRMED",
            "sponsor": "AI Health",
            "co_sponsors": [
                "+DataScience (+DS)",
                "Biomedical Engineering (BME)",
                "Biostatistics and Bioinformatics",
                "Center for Computational Thinking",
                "Computer Science",
                "Department of Medicine",
                "DHTS Web Services",
                "Electrical and Computer Engineering (ECE)",
                "Pratt School of Engineering"
            ],
            "location": {
                "address": "311 Trent Drive, Durham, NC 27710"
            },
            "contact": {
                "name": "A. Ian WONG, MD, PhD",
                "email": "a.ian.wong@duke.edu"
            },
            "categories": null,
            "link": "https://calendar.duke.edu/show?fq=id:CAL-8a000483-92c3adf6-0194-dd19428a-000027cfdemobedework@mysite.edu",
            "event_url": "https://sites.duke.edu/datathon2025/",
            "submitted_by": [
                "tmt26"
            ]
            }
        ]
        }
    '''

     # Construct the URL with the future_days parameter
    url = f'https://calendar.duke.edu/events/index.json?&gfu[]=AI%20Health&future_days={future_days}&feed_type=simple'
    
    print(f'Calling the API with {future_days} future days')
    
    # Make the GET request to the API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Return the JSON body from the response
    else:
        raise Exception(f"Error fetching data from API: {response.status_code} - {response.text}")

# # Define the schema for the tool's input using Pydantic
# class APICallInput(BaseModel):
#     endpoint: str
#     parameters: dict

# # Wrapper function to execute the API call
# def tool_wrapper(*args, **kwargs):
    
#     # For demonstration, we'll return a placeholder string
#     return f"Call the API at {kwargs['endpoint']} with parameters {kwargs['parameters']}"

# # Create and return the structured tool
# def create_structured_tool():
#     return CrewStructuredTool.from_function(
#         name='Wrapper API',
#         description="A tool to wrap API calls with structured input.",
#         args_schema=APICallInput,
#         func=tool_wrapper,
#     )

# # Example usage
# structured_tool = create_structured_tool()

# # Execute the tool with structured input
# result = structured_tool._run(**{
#     "endpoint": "https://calendar.duke.edu/events/index.json?&gfu[]=Academic%20Resource%20Center%20%28ARC%29&future_days=45&feed_type=simple",
#     "parameters": {"events": []}
# })
# print(result)  # Output: Call the API at https://example.com/api with parameters {'key1': 'value1', 'key2': 'value2'}