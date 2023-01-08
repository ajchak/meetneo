import json, re, requests, random, os
import sys, datetime, openai
import streamlit as st
openai.api_key = "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"

st.title("Meet Neo")

st.markdown("""
### Your friendly AI who patiently explains complex concepts to kids.
""", True)

st.markdown("""
#### Try asking:
""", True)

st.markdown("""
1. What is a black hole
2. What is blockchain
3. What is a crypto currency
4. What is quantum computing
""", True)

def query(prompt, myKwargs = {}):

  kwargs = {
  "engine":"davinci",
  "temperature":.7,
  "max_tokens":150,
  "stop":"\n\n",
  }

  for kwarg in myKwargs:
    kwargs[kwarg] = myKwargs[kwarg]

  r = openai.Completion.create(prompt=prompt, **kwargs)
  return r

myAds = [
    {
      "Company":"Why is the sky blue",
      "Headline":"Sure, I can answer that!",
      "Description":"The sky looks blue because of the way the Earth's atmosphere scatters sunlight. When the sun's light hits the atmosphere, it is bounced around by the tiny particles in the air. This is called scattering. Sunlight has seven different colours and blue is one of them. Blue light are scattered more easily than other colours hence the sky looks blue most of the time. Sometimes the sky can look other colours, too. For example, the sky can look orange or red at sunrise or sunset because the sunlight has to pass through more of the atmosphere, which makes the other colours in the sunlight scatter more and the blue light scatter less.",
    },
    {
      "Company":"What is a black hole",
      "Headline":"Sure, I can answer that!",
      "Description":"A black hole is a really big ball of space that is so heavy and powerful that it can suck in anything that comes too close to it, even light! Much like how the sun has a gravitational pull so does a black hole but several thousand times higher than the sun’s. It is like a giant vacuum cleaner that sucks up everything around it. Scientists think that black holes might be made when really big stars die and collapse. They are really hard to see because they don't let anything escape, so we can't see what is happening inside of them. But we can tell they are there because they can have a big effect on the things around them.",
    },

    {
      "Company":"What is quantum computing",
      "Headline":"That’s an interesting question",
      "Description":"Quantum computing is a way of using special computers that work with very small particles called ‘qubits’ to solve problems very quickly. Regular computers use bits, which are tiny pieces of information that can be either a 1 or a 0. Quantum computers use qubits, which are like bits but can also be a 1 and a 0 at the same time. This is called ‘superposition’ and it allows quantum computers to work on multiple calculations at the same time, making them much faster than regular computers. Some people think that quantum computers could even help us answer questions about the universe and how it works.",
   },

]

def buildPrompt(someRequest, temperature=.7, verbose=False):

  # company = someRequest["company"]
  # audience = someRequest["audience"]
  # tone = someRequest["tone"]
  # promo = someRequest["promo"]
  # keywords = someRequest["keywords"]
  # background = someRequest["background"]
  if verbose:
      print("Recieved Request: {}".format(someRequest))

  #removed keywords
  possibleKeys = ["Company", "Headline", "Description"]
  targetKeys = []
  for key in possibleKeys:
    if key in someRequest:
        if someRequest[key] not in ["None","none", ""]:
            targetKeys.append(key)

  if verbose:
      print("currentKeys: {}".format(targetKeys))

  examples = []
  if len(examples) < 3:
    newExamples = random.sample(myAds, 3-len(examples))
  prompt = "Answer questions to a five year old.\n\n"
  for example in newExamples:
    for key in targetKeys:
      if key == "company":
        prompt += "Company Name: {}\nAd information:".format(example[key].strip())
      else:
        prompt += " The ad's {} is {}.".format(key, example[key])
    prompt += "\n"
    for key in ["Headline", "Description"]:
      prompt += "{}: {}\n".format(key, example[key])

    prompt += "\n"

  if verbose:
      print(prompt)

  for key in targetKeys:
      if key == "company":
        prompt += "Company Name: {}\nAd Information:".format(someRequest[key].strip())
      else:
        prompt += " The ad's {} is {}.".format(key, someRequest[key].strip())
  prompt += "\n"
  prompt += """Headline:"""

  results = query(prompt, myKwargs={"temperature":temperature, "n": 1, "frequency_penalty":.6, "stop":["\n\n", "Headline"]})
  #print("RESULTS: {}".format("\n".join([results["choices"][i]["text"] for i in range(3)])))
  outputs = []
  for i in range(len(results["choices"])):
      current = results["choices"][i]["text"]
      sections = current.split("\nDescription: ")
      if len(sections) == 2:
          output = ""
          # output += "EXAMPLE:<br>"
          heads = sections[0][:30]
          newDescription = sections[1]
          if len(sections[1]) > 500:
              newDescription = sections[1][:500] + "..."
          descriptions  = "{}".format(newDescription)
          outputs.append({"Response":heads, "Answer":descriptions})

  #return("<br><br>".join(outputs))
  return(outputs)

newAds = buildPrompt({
  "Company":st.text_input("Enter question here"),
})
if st.button("Ask"):
  print(newAds)
  st.write(newAds)
