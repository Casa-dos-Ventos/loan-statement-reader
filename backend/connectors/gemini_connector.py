from google import genai
from google.genai import types
import base64
import json


def generate_response(prompt, output_schema, document):
    client = genai.Client(
        vertexai=True,
        project="sap-tools-cdv",
        location="global",
    )

    text1 = types.Part.from_text(text=prompt)
    document1 = types.Part.from_bytes(
        data=document,
        mime_type="application/pdf",
    )

    model = "gemini-2.0-flash-001"
    contents = [types.Content(role="user", parts=[text1, document1])]
    generate_content_config = types.GenerateContentConfig(
        temperature=0,
        top_p=0.95,
        max_output_tokens=8192,
        response_modalities=["TEXT"],
        response_mime_type="application/json",
        response_schema=output_schema,
    )

    response = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response += chunk.text
    return json.loads(response)
