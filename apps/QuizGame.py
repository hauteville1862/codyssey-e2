class QuizGame:
    """퀴즈 한 판의 진행(출제 순서, 정답 판정, 점수 계산)을 담당하는 클래스.

    Quiz 객체들의 리스트를 받아서, 문제를 하나씩 순서대로 출제하고
    사용자 입력을 검증한 뒤 정답 여부를 판정하며 점수를 누적한다.
    파일 저장/불러오기는 이 클래스가 아니라 main.py가 담당한다.
    """

    def __init__(self, q_list):
        """QuizGame 객체를 생성하고 진행 상태를 초기화한다.

        Args:
            q_list: 이번 판에서 풀 Quiz 객체들의 리스트
        """
        self.question_number = 0  # 지금까지 출제한 문제 수 (동시에 다음 문제의 인덱스 역할)
        self.score = 0            # 맞힌 문제 수
        self.question_list = q_list  # 풀어야 할 전체 Quiz 객체 리스트

    def still_has_questions(self):
        """아직 풀지 않은 문제가 남아 있는지 확인한다.

        question_number(지금까지 출제한 문제 수)가 전체 문제 수보다 작으면
        아직 남은 문제가 있다는 뜻이다. main.py의 run_quiz()에서
        `while quiz.still_has_questions():` 형태로 반복 조건에 사용된다.

        Returns:
            남은 문제가 있으면 True, 모두 풀었으면 False
        """
        return self.question_number < len(self.question_list)

    def next_question(self):
        """다음 문제를 출제하고, 사용자 입력을 받아 정답을 판정한다."""
        # question_number를 인덱스로 사용해 아직 출제하지 않은 다음 문제를 가져온다
        current_question = self.question_list[self.question_number]
        self.question_number += 1  # 출제했으므로 다음 문제를 가리키도록 1 증가

        print(f"\nQ.{self.question_number}: {current_question.question}")

        # 보기 출력 (1. 보기1, 2. 보기2...)
        number = 1
        for choice in current_question.choices:
            print(f"   {number}) {choice}")
            number += 1

        # 사용자 입력 및 유효성 검사 (공백 제거, 빈 입력, 범위 초과 처리)
        # 올바른 입력(1~4 중 하나)이 나올 때까지 반복해서 다시 물어본다
        while True:
            user_answer = input("\n정답을 입력하세요 (1-4): ").strip()
            if user_answer == "":
                print("[알림] 입력이 비어 있습니다. 1번부터 4번 사이의 숫자를 입력해주세요.")
                continue
            if user_answer not in ["1", "2", "3", "4"]:
                print("[알림] 잘못된 입력입니다. 1번부터 4번 사이의 숫자를 입력해주세요.")
                continue
            break

        # 검증을 통과한 사용자 입력과 정답을 비교해 채점한다
        self.check_answer(user_answer, current_question.answer)

    def check_answer(self, user_answer, correct_answer):
        """사용자의 답과 정답을 비교해 점수를 갱신하고 결과를 출력한다.

        Args:
            user_answer: 사용자가 입력한 값 (문자열, 예: "2")
            correct_answer: 정답 번호 (정수, 예: 2)
        """
        # JSON의 answer는 숫자(int)이므로 문자열로 변환하여 비교
        if user_answer == str(correct_answer):
            self.score += 1
            print("정답입니다!")
        else:
            print("틀렸습니다.")
            print(f"정답은 {correct_answer}번이었습니다.")

        print(f"현재 점수: {self.score}/{self.question_number}")
