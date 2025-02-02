import os
import io
import requests
import textwrap
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# Load API key from .env file
_ = load_dotenv(find_dotenv())
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Sample comic page structure: (Scene Description, Dialogue)
COMIC_SCENES = [
    ("A dark alley at night, shadows creeping along the walls.", "We shouldn't be here..."),
    ("A figure in a trench coat steps forward, face hidden.", "Who are you?"),
    ("The stranger pulls out an old, weathered map.", "This will lead us to the truth."),
    ("The ground shakes as something emerges from below.", "What is that?!"),
    ("A monstrous creature, eyes glowing red, towers over them.", "RUN!"),
    ("A final shot of them fleeing into the night.", "To be continued...")
]

def generate_image(description: str) -> Image:

    comic_prompt = (
    f"A professional hand-drawn American comic book panel, inked and colored in a vintage 1980s Marvel/DC style. "
    f"High contrast, strong shadows, and cel-shading. "
    f"Bold line art, cross-hatching for depth, dynamic perspective. "
    f"A single scene shown (NO multi-panel image) "
    f"If a character is described, seen engaging in action or dramatic moment or at least expressing emotion. "
    f"Detailed background for storytelling continuity. "
    f"No text, no speech bubbles, no captions, no words. "
    f"{description} --ar 1:1 --v 5 --no text, words, captions"
    )
    
    response = client.images.generate(
        model="dall-e-3",  
        prompt=comic_prompt,
        n=1,
        size="1024x1024"
    )

    image_url = response.data[0].url
    img_response = requests.get(image_url)
    return Image.open(io.BytesIO(img_response.content))

def add_dialogue(image: Image, text: str) -> Image:
    """
    Adds a Marvel-style dialogue box with text to an image.

    Args:
        image (Image): The original comic panel image.
        text (str): The dialogue to be displayed.

    Returns:
        Image: The image with the dialogue added inside a classic Marvel comic-style box.
    """
    draw = ImageDraw.Draw(image)
    width, height = image.size
    box_height = int(height * 0.25)  # Dialogue box height (25% of image)

    # Define Marvel-style light yellow text box
    box_x1, box_y1 = width * 0.05, height - box_height - 30
    box_x2, box_y2 = width * 0.95, height - 30

    draw.rectangle(
        [(box_x1, box_y1), (box_x2, box_y2)],
        fill="#FFEB85",  # Light yellow like Marvel captions
        outline="black",
        width=5
    )

    # Load a classic comic book font
    try:
        font = ImageFont.truetype("Comic Sans.ttf", 45)  # Marvel-style font
    except IOError:
        try:
            font = ImageFont.truetype("arialbd.ttf", 45)  # Bold Arial as a backup
        except IOError:
            font = ImageFont.load_default()

    # Wrap text inside the dialogue box
    wrapped_text = textwrap.fill(text, width=35)

    # Draw the text with a slight black outline (Marvel print style)
    text_x, text_y = box_x1 + 20, box_y1 + 15
    outline_offset = 2  # Small shadow effect for boldness

    # Create a black outline for the text (simulates classic print effect)
    for dx, dy in [(-outline_offset, 0), (outline_offset, 0), (0, -outline_offset), (0, outline_offset)]:
        draw.text((text_x + dx, text_y + dy), wrapped_text, fill="black", font=font)

    # Draw the actual text in black
    draw.text((text_x, text_y), wrapped_text, fill="black", font=font)

    return image

def create_comic_page(scenes: list) -> Image:

    panels = []

    for description, dialogue in scenes:
        img = generate_image(description)
        img_with_text = add_dialogue(img, dialogue)
        img_with_text.thumbnail((512, 512))  # Resize for consistency
        panels.append(img_with_text)

    # Create a blank comic page (2x3 grid)
    final_page = Image.new("RGB", (1024, 1536), "white")

    # Arrange panels in grid format
    for i, panel in enumerate(panels):
        x = (i % 2) * 512  # Two columns
        y = (i // 2) * 512  # Three rows
        final_page.paste(panel, (x, y))

    final_page.show()  # Display the final comic page
    final_page.save("comic_page.jpg")
    return final_page


