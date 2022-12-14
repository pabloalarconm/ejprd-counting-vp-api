from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from querySelection import QuerySelection


app = FastAPI()
service = QuerySelection()


# Input classes:

class Filters(BaseModel):
    type: str
    id: str
    operator: str

class Query(BaseModel):
    description: str
    filters: List[Filters]

class Properties(BaseModel):
    query: Query

class Input(BaseModel):
    description: str
    properties: Properties


# Output classes:

class ResponseSummary(BaseModel):
    numTotalResults: int
    exists: bool

class Response(BaseModel):
    responseSummary: ResponseSummary


# Protocols:

@app.get("/")
def apiRunning():
    return {"message": "API running"} 

@app.post("/individuals")
def countingIndividuals(input_data:Input):
    """
    Counting for individuals, creates modular SPARQL queries based on EJP CDE semantic models. Parameters are passed as request body where you define what data elements are you searching for. \n
    Specifications can be found here: https://github.com/ejp-rd-vp/vp-api-specs \n
    It retrieves JSON object that defines counted individuals as {"count" : nº of individuals} \n
    """

    count_result = service.individualsCountingQuery(input_data=input_data)
    does_data_exist = False
    if count_result is not None:
        does_data_exist = True
    else:
        count_result = 0
    return Response(responseSummary={'numTotalResults': count_result, 'exists': does_data_exist})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)