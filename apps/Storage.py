import json


class Storage:
    def __init__(self, path="state.json"):
        self.path = path

    def get_default_data(self):
        return {
            "high_score": 0,
            "questions": [
                {
                    "question": "'레 미제라블'의 저자로 프랑스의 대문호인 작가는?",
                    "options": ["빅토르 위고", "에밀 졸라", "기 드 모파상", "알베르 카뮈"],
                    "answer": 1,
                },
                {
                    "question": "소설 '1984'와 '동물농장'을 쓴 영국 작가는?",
                    "options": ["올더스 헉슬리", "조지 오웰", "버지니아 울프", "제임스 조이스"],
                    "answer": 2,
                },
                {
                    "question": "1946년 노벨 문학상을 수상했으며, '데미안', '수레바퀴 아래서' 등을 집필한 독일의 작가는?",
                    "options": ["요한 볼프강 폰 괴테", "헤르만 헤세", "라이너 마리아 릴케", "프란츠 카프카"],
                    "answer": 2,
                },
                {
                    "question": "미국 잃어버린 세대의 대표 작가로 '위대한 개츠비'를 쓴 사람은?",
                    "options": ["윌리엄 포크너", "어니스트 헤밍웨이", "존 스타인벡", "F. 스콧 피츠제럴드"],
                    "answer": 4,
                },
                {
                    "question": "러시아 문학의 거장으로 '죄와 벌'을 집필한 작가는?",
                    "options": ["표도르 도스토옙스키", "레프 톨스토이", "안톤 체호프", "이반 투르게네프"],
                    "answer": 1,
                },
            ],
        }

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if "high_score" not in data or "questions" not in data:
                raise ValueError("state.json 구조가 올바르지 않습니다.")

            return data

        except FileNotFoundError:
            return self.get_default_data()

        except (json.JSONDecodeError, ValueError):
            print("\n[알림] 데이터 파일이 손상되어 기본 퀴즈 데이터로 초기화합니다.")
            recovered = self.get_default_data()
            self.save(recovered)
            return recovered

    def save(self, data):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
