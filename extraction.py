import os
import openai
from openai import OpenAI
import PyPDF2
from dotenv import load_dotenv, find_dotenv
import json
import prompts

def extract_and_save_concepts():
    # Load environment variables
    _ = load_dotenv(find_dotenv())
    client = OpenAI(api_key=os.environ.get('openai_api_key'))
    
    # Define model parameters
    model = "gpt-4o"
    temperature = 0.5
    max_tokens = 500

    # Example function call
    file_path = r"static\files\uploadedPDF.pdf"
    json_file_path = r"concepts.json"

    # Read the PDF content
    lecture = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            lecture += page.extract_text() + " "
    
    # Generate prompt
    system_message = prompts.system_message
    prompt = prompts.generate_promp(lecture)
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    
    # Get completion
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    response = completion.choices[0].message.content
    
    # Parse the response
    lines = response.splitlines()
    main_theme = lines[0].replace("Main Theme: ", "")
    subthemes = [line.strip() for line in lines[1:]]
    
    # Prepare and save data
    data = {
        "main_theme": main_theme,
        "subthemes": subthemes
    }
    
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    
    print(f"Main theme and subthemes saved to {json_file_path}")
    return data


extract_and_save_concepts()

