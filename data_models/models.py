from pydantic import BaseModel

class RagToolSchema(BaseModel):
    question:str 
    
    
class WeatherApiSchema(BaseModel):
    city: str
    
    
class QuestionRequest(BaseModel):
    question: str