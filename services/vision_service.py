from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from typing import List

def extract_text_from_image(base64_images: List[str],
                            model: str = 'gpt-5-mini',
                            temperature: float = 0.7
                           ) -> str:

    full_text = ""
    # step -1: define vision model
    vision = ChatOpenAI(model=model,temperature=temperature)
    # step -2: creating prompt message
    instruction = "Extract all readable text from this invoice page. Do not summarize. Return plain text only."
    for index, b64img in enumerate(base64_images):
        message = HumanMessage(
            content= [
                {"type": "text", "text": instruction},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64, {b64img}"
                    }
                }
            ]
        )
        response = vision.invoke([message])
        content = response.content
        full_text += content + "\n\n"

    return full_text
        
    
    
    
