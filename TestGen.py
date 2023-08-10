import pprint
import google.generativeai as palm
import subprocess
palm.configure(api_key='AIzaSyBVAYfleEo9e0dFlTbiYDkhclvvq3Uj4bs')
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name
# print(model)
prompt = """
Write a python program for a nvidia xavier nx as the computer 
to control a robot to search a region 
for a known person using a camera and opencv, 
and facial recognition, 
GPS for location, 
and two driven wheels. incude code for all called functions
"""
completion = palm.generate_text(
    model=model,
    prompt=prompt,
    temperature=0,
    # The maximum length of the response
    max_output_tokens=20000,
)
def save_text_to_file(text, filename):
  """Saves text to a file."""
  with open(filename, 'w') as f:
    f.write(text)

print(completion.result)
save_text_to_file(completion.result,'SearchRegionXavier.py')
