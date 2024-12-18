from fastapi import FastAPI
from pydantic import BaseModel
from app.llm_utils import summarize_match
from app.data_utils import get_player_stats

app = FastAPI()

class MatchSummaryRequest(BaseModel):
    match_id: int

class PlayerProfileRequest(BaseModel):
    match_id: int
    player_name: str

@app.post("/match_summary")
def match_summary(request: MatchSummaryRequest):
    summary = summarize_match(request.match_id)
    return {"summary": summary}

@app.post("/player_profile")
def player_profile(request: PlayerProfileRequest):
    stats = get_player_stats(request.match_id, request.player_name)
    return {"player_profile": stats}
