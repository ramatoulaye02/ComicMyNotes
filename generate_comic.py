import os
import json
from typing import List, Tuple
import PyPDF2
import re
import comic
import prompts2
import extract
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv


def get_book(jsonfile):
    #ini model
    _ = load_dotenv(find_dotenv())
    client=OpenAI(
        api_key=os.environ.get('OPENAI_API_KEY'),
    )



    class StoryParts(BaseModel):
        parts: List[str]
        

    class ComicPage(BaseModel):   
        page: List[List[str]]
        

    model="gpt-4o"
    temperature=0.6
    max_tokens=2200


    file= jsonfile
    theme, subthemes=extract.extract_data(file)

    #generate prompts
    system_msg=prompts2.system_message
    prompt=prompts2.generate_prompt(theme, subthemes)

    messages=[
            {"role":"system", "content":system_msg},
            {"role":"user", "content":prompt}
    ]

    def get_story():
        completion=client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        return completion.choices[0].message.content

    story=get_story()


    system_msg_split = prompts2.system_message_split
    prompt_split = prompts2.generate_prompt_split(story)

    messages_split = [
        {"role": "system", "content": system_msg_split},
        {"role": "user", "content": prompt_split},
    ]

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=messages_split,
        temperature=temperature,
        max_tokens=max_tokens,
        response_format=StoryParts,
    )

    parts=completion.choices[0].message.parsed.parts

    book=[]

    for part in parts:
        messages_panels = [
            {"role": "system", "content": prompts2.system_message_panels},
            {"role": "user", "content": prompts2.generate_prompt_panels(part)},
        ]

        completion = client.beta.chat.completions.parse(
            model=model,
            messages=messages_panels,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=ComicPage,
        )
        
        book.append(completion.choices[0].message.parsed.page)
    



    output_images = []
    for i in range(0,3):
        image = comic.create_comic_page(book[i])  # Generate comic page
        output_images.append(image)

    

    # Convert comic pages into a PDF
    def save_to_pdf(images, filename="comic_book.pdf"):
        """Saves a list of PIL images as a PDF."""
        if images:
            images[0].save(filename, save_all=True, append_images=images[1:])
            print(f"Comic book saved as {filename}")
            return filename

    # Save the generated comic book as a PDF
    save_to_pdf(output_images)
    
        
        





