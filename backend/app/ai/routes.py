from fastapi import APIRouter
from pydantic import BaseModel
from .keras_model import infer_kpi
from .nlp import summarize_text, extract_entities

router = APIRouter()

class KPIIn(BaseModel):
    values: list[float]

class TextIn(BaseModel):
    text: str

@router.post("/kpi/infer")
def kpi_infer(payload: KPIIn):
    return infer_kpi(payload.values)

@router.post("/nlp/summarize")
def nlp_summarize(payload: TextIn):
    return {"summary": summarize_text(payload.text)}

@router.post("/nlp/ner")
def nlp_ner(payload: TextIn):
    return {"entities": extract_entities(payload.text)}
