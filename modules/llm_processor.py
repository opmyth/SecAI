import os
import json


def get_llm_output(prompt: str, task_type: str) -> str:
    with open('/Users/hasan/Desktop/sdaia_bootcamp/secAI/utils/system_prompts.json', 'r') as f:
        SYSTEM_PROMPTS = json.load(f)
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=os.environ.get('OPENAI_API_KEY'),
        )
        
        system_prompt = SYSTEM_PROMPTS[task_type]
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error occurred while getting LLM output: {str(e)}"

print(get_llm_output("Hello, how are you?", "task_classifier"))