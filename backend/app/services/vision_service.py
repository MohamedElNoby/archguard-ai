import json
import os
from google import genai
from google.genai import types

VISION_PROMPT = """You are an expert AI system specialized in software architecture and security analysis.

Analyze the provided architecture diagram carefully.

Your task is to identify the components, connections, data flow, databases, and the most important architecture risks visible in the diagram.

Follow these rules:

1. COMPONENTS
Identify all clearly visible architecture components such as:
- Application servers
- API servers
- Web servers
- Caches
- Databases
- Cloud services
- External services
- Load balancers
- Message queues

For each component, provide:
- name
- type

2. CONNECTIONS
Identify the connections between visible components.

For each connection, provide:
- source
- target
- protocol

Use protocols such as:
- HTTP/REST
- gRPC
- WebSockets
- TCP
- Other

Only report a protocol when it is explicitly shown or can be reliably inferred from the diagram.

3. DATA FLOW
Describe the main flow of data through the architecture in a concise sentence or paragraph.

4. DATABASE TYPES
Identify visible databases and classify each one as:
- Relational
- NoSQL
- In-Memory

Do not invent a database type if it cannot be determined from the diagram.

5. RISKS
Identify the top 3 architecture risks.

Rank them using only:
- CRITICAL
- HIGH
- MEDIUM

For each risk provide:
- level
- title
- description

Prioritize meaningful architecture, security, availability, scalability, performance, and reliability risks.

6. ACCURACY
Only include information supported by the diagram.

Do not invent components, connections, technologies, or risks that have no reasonable evidence in the image.

7. OUTPUT FORMAT
Return ONLY valid JSON.

Do not include:
- Markdown
- Explanations outside the JSON
- Code fences
- Additional text

The JSON must follow this exact structure:

{
    "components": [
        {
            "name": "string",
            "type": "string"
        }
    ],
    "connections": [
        {
            "source": "string",
            "target": "string",
            "protocol": "string"
        }
    ],
    "data_flow": "string",
    "database_types": [
        {
            "name": "string",
            "type": "Relational | NoSQL | In-Memory"
        }
    ],
    "risks": [
        {
            "level": "CRITICAL | HIGH | MEDIUM",
            "title": "string",
            "description": "string"
        }
    ]
}

Return exactly one JSON object."""


async def analyze_architecture_diagram(file_bytes: bytes, content_type: str) -> dict:
    """Analyze diagram image using Gemini with automatic fallback on high demand."""
    client = genai.Client()

    image_part = types.Part.from_bytes(
        data=file_bytes,
        mime_type=content_type,
    )

    models_to_try = [
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.7-flash",
        "gemini-3.6-flash",
    ]
    last_error = None

    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[image_part, VISION_PROMPT],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            return json.loads(response_text.strip())
        except Exception as e:
            last_error = e
            continue

    raise last_error