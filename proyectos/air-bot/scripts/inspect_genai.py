import google.generativeai as genai
import inspect

print("--- GENAI MODULE ATTRIBUTES ---")
for attr in dir(genai):
    if not attr.startswith("_"):
        print(attr)

print("\n--- GENERATIVE MODEL ATTRIBUTES ---")
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    for attr in dir(model):
        if not attr.startswith("_"):
            print(attr)
except:
    pass
