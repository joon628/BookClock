import openai
import re
import os

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define function to extract time expressions from text
def extract_time_expressions(text):
    # Send request to GPT-3 to extract time expressions
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Extract time expressions from text:\n" + text,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.6,
    )

    # Parse output to extract time expressions
    output = response.choices[0].text
    time_expressions = re.findall(r"\b((?:\d{1,2}(?:\:\d{2})?(?:\s*(?:a\.m\.|p\.m\.))?)|(?:[a-zA-Z]+\s+\d{1,2}\w*\s*,?\s*\d{4}))\b", output)
    return time_expressions

# Read in text file
with open("D:\\BookClockData\\running_water&mason_a_e_w_alfred_edward_woodley_18651948.txt", "r") as f:
    text = f.read()

# Split text into chunks of 1024 words
words = text.split()
chunks = [words[i:i+512] for i in range(0, len(words), 512)]
chunks = [' '.join(chunk) for chunk in chunks]

# Process each chunk and print sentences containing time expressions
for chunk in chunks:
    print(chunk)
    time_expressions = extract_time_expressions(chunk)
    sentences = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', chunk)
    for sentence in sentences:
        for time_expression in time_expressions:
            if time_expression in sentence:
                print(sentence.strip())
                break