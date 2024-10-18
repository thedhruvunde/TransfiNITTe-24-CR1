import openai
openai.api_key='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'

messages = [ {"role": "system", "content": 
              "You are a intelligent assistant."} ]
while True:
    message = input("User : ")
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})
