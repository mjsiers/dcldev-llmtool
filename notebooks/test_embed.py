#%%
import ollama

#%%
list_models = ["nomic-embed-text", "all-minilm"]
prompt = "Why is the sky not green?"
for idx, model in enumerate(list_models):
    result = ollama.embeddings(model=model, prompt=prompt)
    print(idx, model, len(result['embedding']))


#%%
