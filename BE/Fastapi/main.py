from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from models.t5_recommendation import T5Recommender
from api.weather import WeatherAPI
from api.external import ExternalAPI

app = FastAPI()
templates = Jinja2Templates(directory="templates")  # 템플릿 디렉토리 설정
recommender = T5Recommender()
weather_api = WeatherAPI()
external_api = ExternalAPI()

class MoodInput(BaseModel):
    mood: str
    lat: float = 37.5665  # 기본값: 서울
    lon: float = 126.9780

@app.get("/")
async def get_form(request: Request):
    """기본 입력 폼을 표시"""
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/recommend")
async def recommend_food(request: Request, mood: str = Form(...)):
    """
    사용자가 입력한 기분을 받아 음식 추천 결과를 반환
    - mood: 폼에서 받은 기분 입력
    - 반환: HTML에 결과 포함
    """
    # 기분과 날씨를 결합해 T5로 추천
    weather = weather_api.get_weather(37.5665, 126.9780)  # 기본 위치 사용
    mood_with_weather = f"{mood}, weather: {weather}"
    food = recommender.recommend(mood_with_weather)

    # 외부 API에서 추가 정보 가져오기
    place = external_api.get_place(food, 37.5665, 126.9780)
    recipe_link = external_api.get_recipe_link(food)

    # 결과 데이터 구성
    result = {
        "mood": mood,
        "weather": weather,
        "recommended_food": food,
        "place": place,
        "recipe_link": recipe_link
    }

    # 템플릿에 결과 전달
    return templates.TemplateResponse("index.html", {"request": request, "result": result})

# 기존 JSON API도 유지 (프론트엔드 연동 대비)
@app.post("/api/recommend")
async def api_recommend_food(input: MoodInput):
    """JSON 형식으로 추천 결과를 반환 (프론트엔드용)"""
    weather = weather_api.get_weather(input.lat, input.lon)
    mood_with_weather = f"{input.mood}, weather: {weather}"
    food = recommender.recommend(mood_with_weather)
    place = external_api.get_place(food, input.lat, input.lon)
    recipe_link = external_api.get_recipe_link(food)
    return {
        "mood": input.mood,
        "weather": weather,
        "recommended_food": food,
        "place": place,
        "recipe_link": recipe_link
    }