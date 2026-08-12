import os
import sys

from Quiz import Quiz
from QuizGame import QuizGame
from Storage import Storage

storage = Storage()


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_valid_int(prompt, min_value, max_value):
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


def run_quiz():
    data = storage.load()

    if not data["questions"]:
        print("\n[알림] 등록된 문제가 없습니다. 문제를 먼저 추가해주세요!")
        input("\n엔터를 누르면 메뉴로 돌아갑니다...")
        return

    question_bank = []
    for q in data["questions"]:
        question_bank.append(Quiz(q["question"], q["choices"], q["answer"]))

    quiz = QuizGame(question_bank)
    while quiz.still_has_questions():
        quiz.next_question()

    print("\n" + "="*30)
    print(f"퀴즈 종료! 최종 점수: {quiz.score}/{len(question_bank)}")

    if quiz.score > data["high_score"]:
        print(f"최고 점수 갱신! ({data['high_score']} -> {quiz.score})")
        data["high_score"] = quiz.score
        storage.save(data)

    print("="*30)
    input("\n엔터를 누르면 메뉴로 돌아갑니다...")


def add_new_question():
    clear_screen()
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

    answer = get_valid_int("정답 번호를 입력하세요 (1-4): ", 1, 4)

    data = storage.load()
    new_q = {"question": question, "choices": choices, "answer": answer}
    data["questions"].append(new_q)
    storage.save(data)

    print("\n문제가 성공적으로 추가되었습니다!")
    input("\n엔터를 누르면 메뉴로 돌아갑니다...")


def view_question_list():
    clear_screen()
    data = storage.load()
    print("[등록된 퀴즈 목록]")

    if not data["questions"]:
        print("등록된 문제가 없습니다.")
    else:
        number = 1
        for q in data["questions"]:
            print(f"{number}. {q['question']} (정답: {q['answer']}번)")
            number += 1

    print("-" * 30)
    input("\n엔터를 누르면 메뉴로 돌아갑니다...")


def show_high_score():
    clear_screen()
    data = storage.load()
    print("[현재 최고 점수]")
    print(f"\n현재까지의 최고 기록은 {data['high_score']}점입니다.")
    print("\n더 높은 점수에 도전해보세요!")
    print("-" * 30)
    input("\n엔터를 누르면 메뉴로 돌아갑니다...")


def main_menu():
    while True:
        clear_screen()
        print("="*40)
        print("      세계 문학 작가 퀴즈")
        print("="*40)
        print("  1. 퀴즈 시작")
        print("  2. 퀴즈 추가")
        print("  3. 퀴즈 목록 보기")
        print("  4. 최고 점수 확인")
        print("  5. 종료")
        print("-"*40)

        choice = get_valid_int("메뉴를 선택하세요 (1-5): ", 1, 5)

        if choice == 1:
            run_quiz()
        elif choice == 2:
            add_new_question()
        elif choice == 3:
            view_question_list()
        elif choice == 4:
            show_high_score()
        elif choice == 5:
            print("\n게임을 종료합니다. 이용해주셔서 감사합니다!")
            break


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n[알림] 강제 종료 신호(Ctrl+C)를 감지했습니다. 안전하게 종료합니다.")
        sys.exit(0)
    except EOFError:
        print("\n\n[알림] 입력이 종료되어 프로그램을 안전하게 종료합니다.")
        sys.exit(0)
