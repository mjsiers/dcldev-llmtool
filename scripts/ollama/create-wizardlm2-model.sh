#!/bin/bash

model_name="wizardlm2:7b"
custom_model_name="crewai-wizardlm2"
custom_model_file="./wizardlm2-modelfile"

# get the base model
ollama pull $model_name

# create the model using the model file
ollama create $custom_model_name -f $custom_model_file
