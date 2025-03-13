from transformers import T5Tokenizer, T5ForConditionalGeneration
import requests

class T5Recommender:
    def __init__(self):
        self.tokenizer = T5Tokenizer.from_pretrained("t5-small")  # 초기 테스트용 small 모델
        self.model = T5ForConditionalGeneration.from_pretrained("t5-small")
        
        # 임시 음식 데이터 사용시
        self.foods = ["치킨", "핫초코", "김치찌개", "피자", "떡볶이"]
        
        # 음식목록 api 호출시 사용
        # self.food_api_url = "http://localhost:8000/api/foods" # api 호출시

        # def fetch_foods(self):
        # # 음식 데이터를 외부 API에서 가져옴
        #     try:
        #         response = requests.get(self.food_api_url)
        #         response.raise_for_status()
        #         return response.json().get("foods", ["치킨", "핫초코"])  # 기본값 제공
        #     except requests.RequestException as e:
        #         print(f"Error fetching foods: {e}")
        #         return ["치킨", "핫초코"]  # API 실패 시 기본값


    def recommend(self, mood_input: str) -> str:
        # T5 입력 형식: "recommend food for: <mood>"
        # foods = self.fetch_foods()  # API에서 음식 목록 가져오기 # 음식목록 API 호출시 사용
        input_text = f"recommend food for: {mood_input}"
        inputs = self.tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
        outputs = self.model.generate(inputs["input_ids"], max_length=50, num_beams=5)
        recommendation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # T5 출력이 음식 이름과 맞지 않을 경우 기본 매핑으로 보정
        for food in self.foods:
            if food in recommendation:
                return food
        return self.foods[0]  # 기본값 (예: "치킨")

# 테스트
if __name__ == "__main__":
    recommender = T5Recommender()
    print(recommender.recommend("나 오늘 너무 힘들어"))  # "치킨" 등 출력 기대


# 파인튜닝 관련
# Google Colab vs 로컬 개발
# Google Colab:
# 장점: 무료 GPU/TPU로 T5 파인튜닝 가능, 초기 테스트 용이.
# 단점: 배포 준비 시 로컬 환경과 달라 추가 조정 필요.
# 로컬 개발 (Mac M1):
# 장점: 배포 환경(AWS EC2)과 유사, 전체 개발 흐름 일관성 유지.
# 단점: GPU 없으므로 파인튜닝 속도 느림.
# 배포 시: AWS EC2에서 Docker로 직접 배포하므로 로컬에서 개발 후 바로 컨테이너화 가능.
# 제안: 로컬에서 개발 시작하고, 파인튜닝 필요 시 Colab 활용 후 모델 파일(pytorch_model.bin)을 로컬로 가져와 통합.

# 사양 요구
# Mac M1:
# 16GB RAM 이상이면 t5-small 문제없음. t5-base도 실행 가능하지만 느림.
# AWS EC2:
# t5-small: t2.medium (2 vCPU, 4GB RAM)으로 충분.
# t5-base: t2.large (2 vCPU, 8GB RAM) 추천. GPU 필요 시 g4dn.xlarge (4 vCPU, 16GB RAM, T4 GPU).
# AWS 가능 여부
# 충분히 가능. CPU만으로도 t5-small 실행 가능하며, 파인튜닝 후 추론만 할 경우 t2.medium으로도 무난.