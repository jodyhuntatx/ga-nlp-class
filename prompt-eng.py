#!/usr/bin/python3

import sys
from llama_cpp import Llama

# Load model from disk
llama_path = "../langchain/"
llama_basename = "llama-2-13b-chat.Q5_K_M.gguf"
lcpp_llm = Llama(model_path=llama_path+llama_basename,
              n_threads=2,  # CPU cores
              n_batch=512,  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
              n_gpu_layers=-1,  # Change this value based on your model and your GPU VRAM pool.
              n_ctx=6000,  # Context window)
              )

def generate_llama_response(prompt):
    # Generate a response from the LLaMA model
    response = lcpp_llm(
                    prompt=prompt,
                    max_tokens=1024,
                    temperature=0,
                    top_p=0.95,
                    repeat_penalty=1.2,
                    top_k=50,
                    stop=['INST'],
                    echo=False)
    # Extract and return the response text
    response_text = response["choices"][0]["text"]
    return response_text

######################################################
def zero_shot_example():
  print("\n\nZero shot example:\n\n")

  system_message = """
  Classify customer reviews in the input as positive or negative in sentiment.
  Review will delimited by triple backticks, that is, ```
  Do not explain your answer. Your answer should only contain the label: positive or negative.
  """
  customer_review = """I couldn't be happier with my experience at your store!
  The staff went above and beyond to assist me, providing exceptional customer service.
  They were friendly, knowledgeable, and genuinely eager to help.
  The product I purchased exceeded my expectations and was exactly what I was looking for.
  From start to finish, everything was seamless and enjoyable.
  I will definitely be returning and recommending your store to all my friends and family.
  Thank you for making my shopping experience so wonderful!
  """
  zero_shot_template = """[INST]\n <<SYS>> \n {system_message} \n <</SYS>>```{user_message}``` /n [/INST] """

  def generate_prompt(system_message, user_input):
      prompt=zero_shot_template.format(system_message=system_message,user_message=user_input)
      return prompt

  zero_shot_prompt = generate_prompt(system_message,customer_review)
  print("Zero shot prompt:\n", zero_shot_prompt)

  response = generate_llama_response(zero_shot_prompt)

  print("\nZero shot reponse:\n", response)

######################################################
def few_shot_examples():
  print("\n\nFew shot example:\n\n")

  system_message = """
  Extract entities from customer reviews in the input.
  Reviews will be delimited by triple backticks, that is, ```.
  Do not explain your answer.
  """
  user_input_example1 = """
  Ordered grey which advertises green lighting, when you're going for a cheap aesthetic, it's upsetting. Mouse works fine.
  """
  assistant_output_example1 = """
  Entities: [Mouse]
  """
  user_input_example2 = """
  I bought one of these for PC gaming. Loved it, then bought another for work.This mouse is not on par with high end mouses from like the Logitech MX Master series, but at 1/5-/8th the price, I didn't expect that level of quality.
  It does perform well, mouse wheel feels weighty, side buttons are well place with different textures so you can tell them apart.
  DPI buttons are handy for adjusting between games, work jobs, etc.
  The mouse does feel rather plasticky and cheap, but for the money, it about what I expected.I like a wired mouse to avoid the pointer/game jumping around due to latency.Long wire too, so snagging issues are minimized. Great value overall.
  """
  assistant_output_example2 = """
  Entities: [Mouse, Logitech MX Master, DPI Buttons, Mouse Wheel, Wire]
  """
  new_review = """I had a old but very nice logitech lazer gamin mouse, my dog at the cord off it so had to get a replacement.
  I was tempted to get another logitech because well I knew it was a sure thing.
  Anyways I saw the reviews on this mouse and thought it looked awesome so I thought I would give it a try.
  Well it does indeed look awesome and feels good in the hand.
  My old mouse was weighted and kind of like the feel of the heft but I'm pleased with this new one and so long as it doesn't fail on me would say its definitely worth the price.
  I would have had to play something like a First Person Shooter side by side to get a real idea how they compare on precision but this new mouse seems fine. Again my logitech was probably more than 10 years old so I can't compare to a new one.
  If I had to guess they based the button placement, size and shape of this mouse off the logitech, don't know.
  """

  first_turn_template = """[INST]\n <<SYS>> \n {system_message} \n <</SYS>>```{user_message}``` \n [/INST] \n{assistant_message}\n</s> """

  examples_template = """[INST]\n ```{user_message}``` \n [/INST] \n {assistant_message}\n</s>"""

  prediction_template = """[INST]\n ```{user_message}```[/INST]"""

  first_turn_example = first_turn_template.format(
                          system_message=system_message,
                          user_message=user_input_example1,
                          assistant_message=assistant_output_example1)

  def generate_prompt(few_shot_examples, new_input):
      prompt = few_shot_examples+prediction_template.format(user_message=new_input)
      return prompt

  first_few_shot_prompt = generate_prompt(first_turn_example, new_review)
  print("\nFirst few shot prompt:\n", first_few_shot_prompt)
  response = generate_llama_response(first_few_shot_prompt)
  print("\nFirst few shot response:\n", response)

  # Add another example to the examples
  examples = examples_template.format(user_message=user_input_example2,
                                      assistant_message=assistant_output_example2)
  few_shot_examples = first_turn_example + examples
  second_few_shot_prompt = generate_prompt(few_shot_examples, new_review)
  print("Second few shot prompt:\n", second_few_shot_prompt)
  response = generate_llama_response(second_few_shot_prompt)
  print("Second few shot response:\n", response)

######################################################
print("\n\nChain of thought example:\n\n")

system_message = """ You are an assistant that helps a customer service representatives from a mobile phone company to better understand customer complaints.
Customer complaints will be submitted as text delimited by triple backticks, that is, ```.
For each complaint, extract the following information and present it only in a JSON format:
1. phone_model: This is the name of the phone - if unknown, just say “UNKNOWN”
2. phone_price: The price in dollars - if unknown, assume it to be 1000 $
3. complaint_desc: A short description/summary of the complaint in less than 20 words
4. additional_charges: How much in dollars did the customer spend to fix the problem? - this should be an integer
5. refund_expected: TRUE or FALSE - check if the customer explicitly mentioned the word “refund” to tag as TRUE. If unknown, assume that the customer is not expecting a refund.
Take a step-by-step approach in your response, and give a detailed explanation before sharing your final answer in the following JSON format:
{phone_model:, phone_price:, complaint_desc:, additional_charges:, refund_expected:}.
"""
customer_complaint = """
I am fuming with anger and regret over my purchase of the XUI890.
First, the price tag itself was exorbitant at 1500 $, making me expect exceptional quality.
Instead, it turned out to be a colossal disappointment.
The additional charges to fix its constant glitches and defects drained my wallet even more.
I spend 275 $ to get a new battery.
The final straw was when the phone's camera malfunctioned, and the repair cost was astronomical.
I demand a full refund and an apology for this abysmal product.
Returning it would be a relief, as this phone has become nothing but a money pit. Beware, fellow buyers!
"""
cot_prompt_template = """[INST]\n <<SYS>> \n {system_message} \n <</SYS>>```{user_message}``` /n [/INST] """

def generate_prompt(system_message,user_input):
    prompt=cot_prompt_template.format(system_message=system_message,user_message=user_input)
    return prompt

chain_of_thought_prompt = generate_prompt(system_message,customer_complaint)
print("Chain of thought prompt: ", chain_of_thought_prompt)
response = generate_llama_response(chain_of_thought_prompt)
print("Chain of thought response: ", response)