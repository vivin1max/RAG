from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from pydantic import BaseModel
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.query_pipeline import QueryPipeline
from prompts import context, code_parser_template
from code_reader import code_reader
from dotenv import load_dotenv
import os
import ast
import json
import re

load_dotenv()
llm = Ollama(model="llama3.1", request_timeout=150.0)
parser = LlamaParse(result_type="markdown")
file_extractor = {".pdf": parser}
documents = SimpleDirectoryReader("./data", file_extractor=file_extractor).load_data()
embed_model = resolve_embed_model("local:BAAI/bge-m3")


vector_index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
query_engine = vector_index.as_query_engine(llm=llm)

tools = [
    QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="api_documentation",
            description="this gives documentation about code for an API. Use this for reading docs for the API",
        ),
    ),
    code_reader,
]

code_llm = Ollama(model="codellama",request_timeout=150.0)
agent = ReActAgent.from_tools(tools, llm=code_llm, verbose=True, context=context)


class CodeOutput(BaseModel):
    code: str
    description: str
    filename: str


parser = PydanticOutputParser(CodeOutput)
json_prompt_str = parser.format(code_parser_template)
json_prompt_tmpl = PromptTemplate(json_prompt_str)
output_pipeline = QueryPipeline(chain=[json_prompt_tmpl, llm])

while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    retries = 0

    while retries < 3:
        try:
            result = agent.query(prompt)
            next_result = output_pipeline.run(response=result)
            print("done")
            print(next_result)
           
            raw_response = str(next_result)
            json_str = raw_response.replace("assistant: Here is the parsed response in the requested JSON format:", "").strip()
            json_match = re.search(r'({.*})', json_str, re.DOTALL)
            print("done")
            print(json_match)

            if json_str:
                print("done")
                json_str = json_match.group(0)
                try:
                    print("done")
                    cleaned_json = json.loads(json_str)
                    print("Cleaned JSON:", cleaned_json)
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e} in output: '{json_str}'")
            else:
                print("No valid JSON found in the response.")

            break
     

        except Exception as e:
            print(f"Error encountered: {e}")
            retries += 1
            if retries == 3:
                print("Max retries reached. Moving to next prompt.")

    if cleaned_json:
        
            print("Code generated:")
            print(cleaned_json['code'])  # Access code within 'properties'
            print("\n\nDescription:", cleaned_json['description'])  # Access description within 'properties'
            filename = cleaned_json["filename"]
            try:
                with open(os.path.join("output", filename), "w") as f:
                    f.write(cleaned_json["code"])
                print("Saved file", filename)
            except:
                print("Error saving file...")
        
        

    

    