system_message =""

def generate_promp(lecture):
    return f"""I have provided a lecture. Please extract the one and only main theme discussed in the lecture and provide relevant subthemes related to the main theme. Ensure that the number of subthemes does not exced 8 and that each subtheme is derived directly from the content in the lecture and reflects specific concepts, practices, or principles mentioned. Here is the format for your response:

Main Theme: (theme name)
(subtheme name 1)
(subtheme name 2)
(subtheme name 3)
(subtheme name 4)
(subtheme name 5)
etc.. 

Ensure that the subthemes reflect specific practices, principles, or concepts discussed in the lecture, and that they are derived directly from the content presented and i dont want any numbering or anything similar for the subthemes.
Make the subthemes elligible for data in a json file. Format the response without any blank lines between the theme abd subthemes.

Here is the lecture: {lecture}"""
    