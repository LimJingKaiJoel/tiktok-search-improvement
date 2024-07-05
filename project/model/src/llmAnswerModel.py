import openai

# to key in after making private repo
openai.api_key = ''

# qn should be input after svm identifies it as a qn
qn = "What is the tallest mountain in the world"

prompt = "In 1 to 3 sentences, answer the following concisely: " + qn
completion = openai.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
        {
            "role": "user",
            "content": prompt,
        },
    ],
)
print(completion.choices[0].message.content)
