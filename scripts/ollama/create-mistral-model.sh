#!/bin/bash

model_name="mistral:7b"
custom_model_name="crewai-mistral"
custom_model_file="./mistral-modelfile"

# get the base model
ollama pull $model_name

# create the model using the model file
ollama create $custom_model_name -f $custom_model_file
