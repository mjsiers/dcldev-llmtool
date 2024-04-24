#!/bin/bash

model_name="phi3"
custom_model_name="crewai-phi3"
custom_model_file="./phi3-modelfile"

# get the base model
ollama pull $model_name

# create the model using the model file
ollama create $custom_model_name -f $custom_model_file
