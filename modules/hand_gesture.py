import base64
from openai import OpenAI
from PIL import Image
import numpy as np
import io
import os
import json

def process_gesture(image):
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    
    with open('/Users/hasan/Desktop/sdaia_bootcamp/secAI/utils/system_prompts.json', 'r') as f:
        SYSTEM_PROMPTS = json.load(f)
    system_prompt = SYSTEM_PROMPTS['hand_gesture']
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": system_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]
        )
        
        gesture = response.choices[0].message.content.strip().lower()
        
        gesture_map = {
            'one': 1,
            'two': 2,
            'three': 3
        }
        
        return gesture_map.get(gesture, 0)
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return 0
    
# print(process_gesture(Image.open('/Users/hasan/Desktop/sdaia_bootcamp/secAI/image.jpg')))