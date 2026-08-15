from quiz import Quiz
from quiz_game import QuizGame
from storage import Storage


class QuizCLI:
    def __init__(self):
        self.storage = Storage()

    def get_valid_int(self, prompt, min_value, max_value):
        while True:
            raw = input(prompt).strip()

            if raw == "":
                print("[알림] 입력이 비어 있습니다. 다시 입력해주세요.")
                continue

            try:
                value = int(raw)
            except ValueError:
                print("[알림] 숫자만 입력 가능합니다.")
                continue

            if value < min_value or value > max_value:
                print(f"[알림] {min_value}~{max_value} 사이의 숫자를 입력해주세요.")
                continue

            return value

    def run_quiz(self):
        data = self.storage.load()

        if not data["questions"]:
            print("\n[알림] 등록된 문제가 없습니다. 문제를 먼저 추가해주세요!")
            input("\n엔터를 누르면 메뉴로 돌아갑니다...")
            return

        question_bank = []
        for q in data["questions"]:
            question_bank.append(Quiz(q["question"], q["choices"], q["answer"]))

        quiz = QuizGame(question_bank)
        while quiz.still_has_questions():
            current_question = quiz.get_current_question()

            print(f"\nQ.{quiz.question_number + 1}: {current_question.question}")
            for number, choice in enumerate(current_question.choices, 1):
                print(f"   {number}) {choice}")

            user_answer = self.get_valid_int("\n정답을 입력하세요 (1-4): ", 1, 4)

            if quiz.submit_answer(user_answer):
                print("정답입니다!")
            else:
                print("틀렸습니다.")
                print(f"정답은 {current_question.answer}번이었습니다.")

            print(f"현재 점수: {quiz.score}/{quiz.question_number}")

        print("\n" + "="*30)
        print(f"퀴즈 종료! 최종 점수: {quiz.score}/{len(question_bank)}")

        if quiz.score > data["high_score"]:
            print(f"최고 점수 갱신! ({data['high_score']} -> {quiz.score})")
            data["high_score"] = quiz.score
            self.storage.save(data)

        print("="*30)
        input("\n엔터를 누르면 메뉴로 돌아갑니다...")

    def add_new_question(self):
        print("[새 문제 추가]")

        question = input("문제 내용을 입력하세요: ").strip()
        while question == "":
            print("[알림] 문제 내용은 비어 있을 수 없습니다.")
            question = input("문제 내용을 입력하세요: ").strip()

        choices = []
        for i in range(1, 5):
            opt = input(f"보기 {i}번을 입력하세요: ").strip()
            while opt == "":
                print("[알림] 보기 내용은 비어 있을 수 없습니다.")
                opt = input(f"보기 {i}번을 입력하세요: ").strip()
            choices.append(opt)

        answer = self.get_valid_int("정답 번호를 입력하세요 (1-4): ", 1, 4)

        data = self.storage.load()
        data["questions"].append(
            {"question": question, "choices": choices, "answer": answer}
        )
        self.storage.save(data)

        print("\n문제가 성공적으로 추가되었습니다!")
        input("\n엔터를 누르면 메뉴로 돌아갑니다...")

    def view_question_list(self):
        data = self.storage.load()
        print("[등록된 퀴즈 목록]")

        if not data["questions"]:
            print("등록된 문제가 없습니다.")
        else:
            for number, q in enumerate(data["questions"], 1):
                print(f"{number}. {q['question']} (정답: {q['answer']}번)")

        print("-" * 30)
        input("\n엔터를 누르면 메뉴로 돌아갑니다...")

    def show_high_score(self):
        data = self.storage.load()
        print("[현재 최고 점수]")
        print(f"\n현재까지의 최고 기록은 {data['high_score']}점입니다.")
        print("\n더 높은 점수에 도전해보세요!")
        print("-" * 30)
        input("\n엔터를 누르면 메뉴로 돌아갑니다...")

    def main_menu(self):
        while True:
            print("="*40)
            print("      세계 문학 작가 퀴즈")
            print("="*40)
            print("  1. 퀴즈 시작")
            print("  2. 퀴즈 추가")
            print("  3. 퀴즈 목록 보기")
            print("  4. 최고 점수 확인")
            print("  5. 종료")
            print("-"*40)

            choice = self.get_valid_int("메뉴를 선택하세요 (1-5): ", 1, 5)

            if choice == 1:
                self.run_quiz()
            elif choice == 2:
                self.add_new_question()
            elif choice == 3:
                self.view_question_list()
            elif choice == 4:
                self.show_high_score()
            elif choice == 5:
                print("\n게임을 종료합니다. 이용해주셔서 감사합니다!")
                break
