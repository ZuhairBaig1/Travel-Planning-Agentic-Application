from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from Agents.agentic_workflow import GraphBuilder
from utils.text_extraction import extract_text_from_message
import os

app = FastAPI()

class QueryRequest(BaseModel):
    query: str


@app.post("/query")
async def query_travel_agent(query:QueryRequest):
    try:
        print(query)
        graph = GraphBuilder() #model_provider = "groq" ??
        react_app = graph()   #graph.build_graph()

        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png","wb") as f:      # wb (write binary), to write text image into file
            f.write(png_graph)
        
        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")

        messages = {"messages":[query.query]}    # query.query ?
        output = react_app.invoke(messages)
        
        final_output = extract_text_from_message(output['messages'][-1].content)

        return {'answer': final_output}
    except Exception as e:
        return JSONResponse(status_code=500, content= {"error":str(e)})



