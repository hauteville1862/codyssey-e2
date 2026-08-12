class Quiz:
    """퀴즈 문제 하나를 표현하는 값 객체.

    이 클래스는 문제 내용/보기/정답이라는 "데이터"만 가지고 있을 뿐,
    화면에 출력하거나 파일에 저장하는 등의 동작은 전혀 하지 않는다.
    (문제를 출제하고 점수를 매기는 실제 진행 로직은 QuizGame이 담당한다)
    """

    def __init__(self, question, choices, answer):
        """Quiz 객체를 생성한다.

        Args:
            question: 문제 내용 문자열 (예: "'1984'를 쓴 작가는?")
            choices: 보기 문자열 4개가 담긴 리스트 (예: ["조지 오웰", ...])
            answer: 정답에 해당하는 보기 번호 (1~4 사이의 정수)
        """
        self.question = question
        self.choices = choices  # 보기 리스트 추가
        self.answer = answer    # 정답 (숫자 1~4)
