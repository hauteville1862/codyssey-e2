class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices  # 보기 리스트 추가
        self.answer = answer    # 정답 (숫자 1~4)