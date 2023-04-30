import openai
import os

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Test API key by calling completion with a simple prompt
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt="Find the time expressions in the following sentence: 'It was 12o clock when I got home. The party was very boring.'",
    max_tokens=150,
    n=1,
    stop=None,
    temperature=0.6,
)
print(response.choices[0].text)