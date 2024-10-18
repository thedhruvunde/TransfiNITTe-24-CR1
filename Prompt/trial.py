from openai import api_key, OpenAI
client = OpenAI(
  api_key = "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"
)

completion = client.completions.create(model='gpt-3.5-turbo', prompt="Hi gpt")
print(completion.choices[0].text)
print(dict(completion).get('usage'))
print(completion.model_dump_json(indent=2))