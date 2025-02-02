system_message="""
You are an expert story writer.

Your primary role today is to create a complete story from a main concept and its subthemes. 
I will provide you with a principal theme and a set of subthemes. Your task is to craft a captivating, fully developed story that vividly conveys the concept. The story should naturally weave together the theme and subthemes, ensuring the idea is clear, engaging, and thought-provoking.

Make the story interactive and immersive—grabbing the reader’s attention from the start. Use rich descriptions, compelling characters, and an engaging narrative structure to bring the concept to life. The tone should be both entertaining and informative, ensuring the story is not only enjoyable but also insightful.

The final result should feel like an experience, not just an explanation—keeping the reader intrigued while subtly teaching them about the concept in a creative way.

"""

system_message_split="""You are an expert in text analysis and story structuring. Your task is to take a given story and split it into exactly 10 equal parts while maintaining logical continuity, coherence, and flow.

Instructions:
Split the story into 10 equal parts in terms of word count, ensuring that each part is as balanced as possible.
Preserve natural breaks in the story (e.g., sentences and paragraphs should not be split awkwardly).
Ensure logical flow so that no key event or narrative structure is disrupted.
If necessary, adjust breakpoints slightly to avoid cutting off sentences or splitting key moments in a way that affects readability.

Here is a description of the output format:
    - parts: an array of 10 strings, where each entry represents a logically structured part of the story.
    
    Instructions:
    - Ensure each part is **roughly equal in length** while preserving natural breaks in the text.
    - Do **not split mid-sentence or mid-paragraph**; ensure smooth transitions.
    - The output must be **strictly formatted as a JSON array** of 10 strings.
    - Return **only the JSON array**—do not include any explanations or extra text.
    
    Here is an example output format:
    ```json
    {
      "parts": [
        "First part of the story...",
        "Second part of the story...",
        "Third part of the story...",
        "...",
        "Tenth part of the story..."
      ]
    }
    ```
"""

system_message_splitv2="""
You are a professional book writer and editor, experienced in structuring stories
into well-paced sections. Your role is to take a given story and divide it into 15 pages.
Each page should end at a natural stopping point, such as the conclusion of a scene, a key event, 
or a well-placed paragraph break, ensuring smooth transitions. If necessary, make minor adjustments
to enhance readability while preserving the original meaning. Format the output clearly as 'Page 1:',
'Page 2:', etc., to maintain a structured presentation.

"""

system_message_panels= """
You are an expert in comic book storytelling and scriptwriting.
Your task is to convert a description of a single page from a story into a structured six-panel comic book script that remains visually dynamic, engaging, and easy to follow.

### **Instructions:**
1. **Adapt the Story Page into a Six-Panel Comic Script**  
   - The story page must be translated into **exactly six comic panels**.  
   - Each panel should contain:  
     - **A detailed visual description** that focuses on action, setting, characters, and expressions to create an immersive experience.  
     - **Corresponding dialogue or narration** that fits the scene naturally while maintaining clarity and flow.  

2. **Preserve Narrative Integrity**  
   - Do **not** add, remove, or alter any content—the scene must fit seamlessly within a larger story.  
   - Ensure each moment **flows naturally**, maintaining **consistent structure and coherence** with the surrounding narrative.  
   - Use **cinematic storytelling techniques** to emphasize key moments, emotions, and dramatic beats effectively.  

3. **Maintain a Clear and Structured Output Format**  
   - **Return the output in the following JSON format** to match the `Page` data model:  

### **Output Format (Strict JSON structure)**  
```json
{
  "page": [
    {"panel": ["[Image description for Panel 1]", "[Dialogue/Narration for Panel 1]"]},
    {"panel": ["[Image description for Panel 2]", "[Dialogue/Narration for Panel 2]"]},
    {"panel": ["[Image description for Panel 3]", "[Dialogue/Narration for Panel 3]"]},
    {"panel": ["[Image description for Panel 4]", "[Dialogue/Narration for Panel 4]"]},
    {"panel": ["[Image description for Panel 5]", "[Dialogue/Narration for Panel 5]"]},
    {"panel": ["[Image description for Panel 6]", "[Dialogue/Narration for Panel 6]"]}
  ]
}  

Additional Guidelines:  
Do NOT summarize the story—transform it into sequential, visually engaging storytelling.  
Use varied panel compositions (e.g., close-ups, wide shots, dynamic action angles) to enhance the visual impact.  
Ensure smooth transitions between panels for a natural reading experience.  
Maintain the correct tone (e.g., dramatic, action-packed, suspenseful, emotional) as dictated by the original content.  

Your Task:  
Generate the comic book script with six panels per page, ensuring a compelling, immersive, and sequential adaptation while maintaining perfect consistency with the original story."""


def generate_prompt(theme, subthemes):
    subthemes_str = ', '.join(subthemes)
    prompt = (
        f"""As an expert story writer, create a complete story about {theme}, 
        that touches on each of these related subthemes: {subthemes_str}.
        
Instructions for the task:
- Make sure the story seamlessly integrates all the subthemes mentioned.
- Make sure the story is easy to follow, and has a lot of visual description and dialogues.
- Make sure the characters are well-described.
- Make sure the dialogue is easy to understand.
- Make sure the final story is separated in chapters"""
    )
    return prompt




def generate_prompt_panels(page):
    return f"""
You are an expert in comic book storytelling and scriptwriting. I will provide you with a page of a story.
Your task is to transform it into a comic book format using the following steps:

- Generate a comic book script with **six panels** that illustrate the part of the story described in the page.
- Each panel should contain:
  - A **visual description** of what the panel should depict. 
  - **Dialogue or narration** that fits the scene naturally.
- The script should be **immersive, easy to follow, and visually engaging**, balancing **action, expressions, and environment details**.
- The narration should NOT be specified with a "Narration:" beforehand. Write it directly with no introduction.

### **Output Format (Strict JSON)**
The output must be a **JSON object** formatted **exactly** as shown below:

```json
{{
  "page": [
    {{"panel": ["[Image description for Panel 1]", "[Dialogue/Narration for Panel 1]"]}},
    {{"panel": ["[Image description for Panel 2]", "[Dialogue/Narration for Panel 2]"]}},
    {{"panel": ["[Image description for Panel 3]", "[Dialogue/Narration for Panel 3]"]}},
    {{"panel": ["[Image description for Panel 4]", "[Dialogue/Narration for Panel 4]"]}},
    {{"panel": ["[Image description for Panel 5]", "[Dialogue/Narration for Panel 5]"]}},
    {{"panel": ["[Image description for Panel 6]", "[Dialogue/Narration for Panel 6]"]}}
  ]
}}

Now, here is the page to adapt into comic book panels: {page}
  """
  
  

def generate_prompt_split(story):
  prompt=(
    f"""Take the following story and divide it into ten pages. 
Each page should end at a natural break in the story, such as
the end of a scene, paragraph, or key moment, ensuring a smooth flow. 
If needed, adjust the story slightly to make each page feel complete 
while maintaining the original meaning. Here is a description of the output format:
- parts: an array of 10 strings, where each entry represents a logically structured part of the story.
    
    Instructions:
    - Ensure each part is **roughly equal in length** while preserving natural breaks in the text.
    - Do **not split mid-sentence or mid-paragraph**; ensure smooth transitions.
    - The output must be **strictly formatted as a JSON array** of 10 strings.
    - Return **only the JSON array**—do not include any explanations or extra text.
    

    Now, split the following story accordingly:{story}."""
)
  
  return prompt