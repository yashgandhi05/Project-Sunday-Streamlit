import google.generativeai as genai

genai.configure(api_key="AIzaSyDaXN-I-YX1I_e5uRGGQ55nVf9o0AkEvrk")

models = genai.list_models()
for m in models:
    print(m.name)
