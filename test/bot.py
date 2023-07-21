import openai

api_key = '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'
openai.api_key = api_key


def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

def chatbot(input_text):
 
    sensitive_keywords = ["credit card", "password", "social security number"]
    for keyword in sensitive_keywords:
        if keyword in input_text:
            return "I'm sorry, but I can't assist with that request."

    if input_text.lower().startswith("help"):
        return "Sure, I can help you with that!"

    # GPT-3를 이용하여 응답 생성
    response = generate_response(input_text)


    return response

print("Chatbot: Hello! I'm your friendly chatbot. How can I assist you today?")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    response = chatbot(user_input)
    print("Chatbot:", response)