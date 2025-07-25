import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_contract_details(extracted_text: str) -> dict:
    system_prompt = """
You are a legal assistant. Extract the following structured data from the contract text:

- Brief Summary
- Start Date
- Termination Date
- Parties Involved
- Governing Law
- Contract Type (NDA or MSA)
- Payments
- Penalties on Termination

Return only a valid JSON object with these exact keys:
- brief_summary
- start_date
- termination_date
- parties_involved
- governing_law
- contract_type
- payments
- penalties_on_termination
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": extracted_text}
        ],
        temperature=0  # Makes output more consistent
    )

    content = response.choices[0].message.content

    # Optionally convert string JSON to real Python dict
    import json
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("⚠️ Could not parse JSON:")
        print(content)
        return {"error": "Invalid JSON returned by LLM"}
