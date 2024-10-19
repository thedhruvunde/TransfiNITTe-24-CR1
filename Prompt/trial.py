'''
export TRANFINITTE_API_KEY="sk-proj-yo_CSrCd4B8lqMN98U7ld22028ZNeUU_QVW5sqdk4Yc9pRLaODtlbcnllbPdrRKZxsUb_7YdVQT3BlbkFJyJmt9JOzwsLHrdaulTBXu-GdEu-fgfxJ5J-ILZ_N
2f_GhzlX24G8Zu-W9dgKSzygroAbU-tIoA"
'''
from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)