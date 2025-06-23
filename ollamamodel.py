import ollama


model_list = ollama.list()
print("Available models:")
for model in model_list.models:
    #print model name and version
    print(f"- {model.model}")    

