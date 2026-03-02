from langchain_core.prompts import ChatPromptTemplate


prompt = """
You are an expert invoice data extractor.

Extract the following fields from the invoice text.

Return ONLY valid JSON in this format:

{{
  "invoice_number": string,
  "buyer": string,
  "seller": string,
  "invoice_date": YYYY-MM-DD,
  "items": [
    {{
      "description": string,
      "quantity": number,
      "price": number,
      "total": number
    }}
  ],
  "currency": string,
  "subtotal": number,
  "tax": number,
  "total": number,
  
}}

If a value is missing, return null.

Invoice text:
{invoice_text}
"""

invoice_extract_prompt = ChatPromptTemplate.from_template(prompt)