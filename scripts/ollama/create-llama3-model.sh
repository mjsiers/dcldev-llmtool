#!/bin/bash

model_name="llama3:8b"
custom_model_name="crewai-llama3"
custom_model_file="./llama3-modelfile"

# get the base model
ollama pull $model_name

# create the model using the model file
ollama create $custom_model_name -f $custom_model_file
