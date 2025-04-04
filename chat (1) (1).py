# -*- coding: utf-8 -*-
# /content/info.txt is the  data

!pip install huggingface_hub
!pip install transformers
!pip install langchain
!pip install gradio
!pip install langchain_community

from langchain_community.llms import HuggingFaceHub
from langchain import HuggingFaceHub ,LLMChain
import os
from getpass import getpass
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.document_loaders import TextLoader
from langchain.schema.messages import HumanMessage, SystemMessage
import gradio as gr

def eliminer_double_sauts(texte):
    lignes = texte.split("\n\n")
    texte_modifie = " ".join(lignes)
    return texte_modifie

def extract_text_after_word(paragraph, word):
    index = paragraph.find(word)
    if index!= -1:
        return paragraph[index + len(word):].strip()
    else:
        return ""

def get_response(msg):
    HUGGINGFACEHUB_API_TOKEN="api"
    os.environ['HUGGINGFACEHUB_API_TOKEN']=HUGGINGFACEHUB_API_TOKEN

    model_id="mistralai/Mistral-7B-Instruct-v0.2"
    llm= HuggingFaceHub( huggingfacehub_api_token=os.environ['HUGGINGFACEHUB_API_TOKEN'],
                            repo_id=model_id,
                            model_kwargs={"temperature":0.5,"max_new_tokens":1000}
                              )
    prompt_template = PromptTemplate.from_template(
          "<s>[INST] your are an enthusiastic and friendly AI assistant, designed to provide helpful answers to user queries. your responses are designed to be concise, cheerful, and always aimed at answering the question of the user effectively and efficiently: {query} .</s> [INST]"
    )
    filled_prompt = prompt_template.format( query = msg )

    loader = TextLoader("intentes.txt")
    document = loader.load()
    page_content = tuple(document[0])[0][1]
    messages = [
        SystemMessage(content=str(prompt_template + page_content)),
        HumanMessage(content="<s>[INST] "+ msg +"</s> [INST]"),
    ]
    response = llm.invoke(messages)
    ch=eliminer_double_sauts(extract_text_after_word(extract_text_after_word(response,"</s> [INST]"),"</s> [INST]"))
    return ch

if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)
