class QuizGame:
    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        current_question = self.question_list[self.question_number]
        self.question_number += 1

        print(f"\nQ.{self.question_number}: {current_question.question}")

        number = 1
        for choice in current_question.choices:
            print(f"   {number}) {choice}")
            number += 1

        while True:
            user_answer = input("\n정답을 입력하세요 (1-4): ").strip()
            if user_answer == "":
                print("[알림] 입력이 비어 있습니다. 1번부터 4번 사이의 숫자를 입력해주세요.")
                continue
            if user_answer not in ["1", "2", "3", "4"]:
                print("[알림] 잘못된 입력입니다. 1번부터 4번 사이의 숫자를 입력해주세요.")
                continue
            break

        self.check_answer(user_answer, current_question.answer)

    def check_answer(self, user_answer, correct_answer):
        if user_answer == str(correct_answer):
            self.score += 1
            print("정답입니다!")
        else:
            print("틀렸습니다.")
            print(f"정답은 {correct_answer}번이었습니다.")

        print(f"현재 점수: {self.score}/{self.question_number}")
