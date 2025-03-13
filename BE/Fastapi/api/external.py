class ExternalAPI:
    def get_place(self, food: str, lat: float, lon: float) -> dict:
        # 더미 데이터로 테스트 (실제 API 연동은 키 발급 후 진행)
        return {"place": f"{food} 맛집 근처", "distance": "1km"}

    def get_recipe_link(self, food: str) -> str:
        return f"https://www.google.com/search?q={food}+레시피"