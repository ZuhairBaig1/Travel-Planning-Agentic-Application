import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class ConfigLoader:                         # loading dependencies from config.yaml
    def __init__(self):
        print(f"loaded config....")
        self.config=load_config()

    def __getitem__(self, key):
        return self.config[key]
    

class ModelLoader(BaseModel):
    model_provider: Literal["groq", "gemini"] = "gemini"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any)-> None:  # This is a specific name reserved by Pydantic. Pydantic promises to call this method automatically after it finishes creating and validating your object, using thid means parent class's (BaseModel) __init__ is not overwritten
        self.config = ConfigLoader()

    class Config:                                      # Allows pydantic to accept ConfigLoader object type, only reason we are doing this is because pydantic does not recognise "configloader" as a valid data type, this can be overcome if we defined config loader class by inheriting BaseModel 
        arbitrary_types_allowed=True

    def load_llm(self):
        print("llm loading...")
        print(f"Loading model from provider: {self.model_provider}")
        if self.model_provider == "groq":
            print("Loading LLM from Groq..........")
            groq_api_key = os.getenv("GROQ_API_KEY")
            model_name=self.config["llm"]["groq"]["model_name"]
            llm=ChatGroq(model=model_name, api_key=groq_api_key)
        elif self.model_provider ==  "gemini":
            print("Loading LLM from Google.......")
            gemini_api_key = os.getenv("GEMINI_API_KEY")
            model_name=self.config["llm"]["gemini"]["model_name"]
            llm=ChatGoogleGenerativeAI(model=model_name, api_key=gemini_api_key)

        return llm
