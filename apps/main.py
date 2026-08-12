# json: state.json 파일을 파이썬 dict/list ↔ 텍스트로 변환할 때 사용
# os: 운영체제별 화면 지우기 명령을 실행할 때 사용
# sys: 프로그램을 정상 종료(exit code 0)시킬 때 사용
import json
import os
import sys

# 같은 apps 폴더에 있는 Quiz.py, QuizGame.py에서 각각 클래스를 가져온다
from Quiz import Quiz
from QuizGame import QuizGame

# state.json은 "상대경로"로 열기 때문에, 반드시 apps 폴더 안에서
# `python main.py`를 실행해야 정상적으로 파일을 찾을 수 있다
DATA_PATH = "state.json"


def get_default_data():
    """state.json이 없거나(첫 실행) 손상된 경우 사용할 기본 퀴즈 데이터 (5개 이상).

    반환값은 항상 state.json과 동일한 구조(dict)를 따른다:
    {
        "high_score": 최고 점수(int),
        "questions": [ {question, options, answer} 형태의 딕셔너리들의 리스트 ]
    }
    """
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


def clear_screen():
    """터미널 화면을 지운다.

    운영체제마다 화면을 지우는 명령이 다르기 때문에 os.name으로 구분한다.
    - Windows(os.name == 'nt')는 'cls'
    - macOS/Linux는 'clear'
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def get_valid_int(prompt, min_value, max_value):
    """사용자로부터 min_value ~ max_value 사이의 정수를 입력받는다.

    아래 4가지 잘못된 입력 케이스를 모두 걸러내고, 올바른 값이 나올 때까지
    while True 반복문으로 계속 다시 물어본다.
    1) 빈 입력(엔터만 입력)
    2) 숫자로 변환할 수 없는 문자(예: "abc")
    3) 허용 범위를 벗어난 숫자(예: 1~5 범위인데 9를 입력)
    4) 입력값 앞뒤 공백(예: " 1 ")은 strip()으로 미리 제거하고 검사한다

    Args:
        prompt: 사용자에게 보여줄 안내 문구
        min_value: 허용하는 최솟값(포함)
        max_value: 허용하는 최댓값(포함)

    Returns:
        검증을 통과한 정수값
    """
    while True:
        # strip()으로 입력 앞뒤 공백을 제거한다 (예: " 1 " -> "1")
        raw = input(prompt).strip()

        # 1) 빈 입력 처리: 공백을 제거하고 나니 빈 문자열이면 다시 입력받는다
        if raw == "":
            print("[알림] 입력이 비어 있습니다. 다시 입력해주세요.")
            continue

        # 2) 숫자 변환 실패 처리: "abc"처럼 숫자가 아닌 값은 int()에서 ValueError 발생
        try:
            value = int(raw)
        except ValueError:
            print("[알림] 숫자만 입력 가능합니다.")
            continue

        # 3) 범위 초과 처리: 변환은 됐지만 허용 범위 밖의 숫자인 경우
        if value < min_value or value > max_value:
            print(f"[알림] {min_value}~{max_value} 사이의 숫자를 입력해주세요.")
            continue

        # 위 3가지 검증을 모두 통과한 경우에만 반복문을 빠져나가며 값을 반환한다
        return value


def load_data():
    """state.json 파일을 읽어서 dict로 반환한다.

    파일이 없거나(첫 실행) 내용이 손상되어 있으면, 프로그램이 그대로
    멈추지 않도록 기본 퀴즈 데이터(get_default_data())로 대체한다.
    """
    try:
        # "r": 읽기 모드로 파일을 연다. encoding="utf-8"은 한글이 깨지지 않게 하기 위함
        with open(DATA_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)  # JSON 텍스트 -> 파이썬 dict로 변환

        # 파일은 존재하지만 필수 키(high_score, questions)가 없는 경우도
        # "손상된 데이터"로 간주하여 아래 except 블록에서 처리하도록 만든다
        if "high_score" not in data or "questions" not in data:
            raise ValueError("state.json 구조가 올바르지 않습니다.")

        return data

    except FileNotFoundError:
        # 프로그램을 처음 실행해서 state.json이 아직 만들어지지 않은 경우
        return get_default_data()

    except (json.JSONDecodeError, ValueError):
        # 파일은 있지만 JSON 형식이 깨졌거나(JSONDecodeError),
        # 구조가 올바르지 않은 경우(위에서 직접 발생시킨 ValueError)
        print("\n[알림] 데이터 파일이 손상되어 기본 퀴즈 데이터로 초기화합니다.")
        recovered = get_default_data()
        save_data(recovered)  # 복구한 기본 데이터를 파일에도 다시 저장해 둔다
        return recovered


def save_data(data):
    """dict 형태의 데이터를 state.json 파일에 저장한다.

    Args:
        data: {"high_score": int, "questions": [...]} 형태의 딕셔너리
    """
    # "w": 쓰기 모드로 파일을 연다. 기존 내용은 덮어쓰기 된다
    with open(DATA_PATH, "w", encoding="utf-8") as file:
        # ensure_ascii=False: 한글을 유니코드 이스케이프(\uXXXX)가 아닌 그대로 저장
        # indent=4: 사람이 읽기 쉽게 4칸 들여쓰기로 예쁘게 저장
        json.dump(data, file, ensure_ascii=False, indent=4)


def run_quiz():
    """[메뉴 1] 퀴즈를 시작해서 모든 문제를 풀고, 점수를 계산·표시한다."""
    data = load_data()

    # 등록된 문제가 하나도 없으면 퀴즈를 진행할 수 없으므로 안내 후 메뉴로 복귀
    if not data["questions"]:
        print("\n[알림] 등록된 문제가 없습니다. 문제를 먼저 추가해주세요!")
        input("\n엔터를 누르면 메뉴로 돌아갑니다...")
        return

    # state.json에서 읽은 dict 리스트를 Quiz 객체 리스트로 변환한다
    # (Quiz는 문제 하나의 데이터만 담당하고, 파일 형식은 전혀 알지 못한다)
    question_bank = []
    for q in data["questions"]:
        question_bank.append(Quiz(q["question"], q["options"], q["answer"]))

    # QuizGame이 문제 출제 순서, 점수 계산 등 실제 게임 진행을 담당한다
    quiz = QuizGame(question_bank)
    while quiz.still_has_questions():
        quiz.next_question()

    # 모든 문제를 다 풀었으면 최종 점수를 출력한다
    print("\n" + "="*30)
    print(f"퀴즈 종료! 최종 점수: {quiz.score}/{len(question_bank)}")

    # 이번 점수가 기존 최고 점수보다 높으면 갱신하고 파일에 즉시 저장한다
    if quiz.score > data["high_score"]:
        print(f"최고 점수 갱신! ({data['high_score']} -> {quiz.score})")
        data["high_score"] = quiz.score
        save_data(data)

    print("="*30)
    input("\n엔터를 누르면 메뉴로 돌아갑니다...")


def add_new_question():
    """[메뉴 2] 새 문제를 입력받아 state.json에 추가한다."""
    clear_screen()
    print("[새 문제 추가]")

    # 문제 내용: 빈 문자열이 입력되는 동안 계속 재입력을 요구한다
    question = input("문제 내용을 입력하세요: ").strip()
    while question == "":
        print("[알림] 문제 내용은 비어 있을 수 없습니다.")
        question = input("문제 내용을 입력하세요: ").strip()

    # 보기 4개를 순서대로 입력받는다 (1번 ~ 4번)
    options = []
    for i in range(1, 5):
        opt = input(f"보기 {i}번을 입력하세요: ").strip()
        while opt == "":
            print("[알림] 보기 내용은 비어 있을 수 없습니다.")
            opt = input(f"보기 {i}번을 입력하세요: ").strip()
        options.append(opt)

    # 정답 번호는 반드시 1~4 사이의 숫자여야 하므로 get_valid_int()로 검증한다
    answer = get_valid_int("정답 번호를 입력하세요 (1-4): ", 1, 4)

    # 기존 데이터를 불러온 뒤, 새 문제를 questions 리스트 맨 뒤에 추가하고 저장한다
    data = load_data()
    new_q = {"question": question, "options": options, "answer": answer}
    data["questions"].append(new_q)
    save_data(data)

    print("\n문제가 성공적으로 추가되었습니다!")
    input("\n엔터를 누르면 메뉴로 돌아갑니다...")


def view_question_list():
    """[메뉴 3] 등록된 모든 문제와 정답 번호를 목록으로 보여준다."""
    clear_screen()
    data = load_data()
    print("[등록된 퀴즈 목록]")

    if not data["questions"]:
        print("등록된 문제가 없습니다.")
    else:
        # 1번부터 순서대로 번호를 매기며 문제와 정답을 출력한다
        number = 1
        for q in data["questions"]:
            print(f"{number}. {q['question']} (정답: {q['answer']}번)")
            number += 1

    print("-" * 30)
    input("\n엔터를 누르면 메뉴로 돌아갑니다...")


def show_high_score():
    """[메뉴 4] 지금까지 기록된 최고 점수를 보여준다."""
    clear_screen()
    data = load_data()
    print("[현재 최고 점수]")
    print(f"\n현재까지의 최고 기록은 {data['high_score']}점입니다.")
    print("\n더 높은 점수에 도전해보세요!")
    print("-" * 30)
    input("\n엔터를 누르면 메뉴로 돌아갑니다...")


def main_menu():
    """프로그램의 메인 메뉴 화면. 사용자가 5번(종료)을 선택할 때까지 반복한다."""
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

        # 1~5 사이의 숫자만 허용하며, 그 외 입력은 get_valid_int() 내부에서 재입력을 요구한다
        choice = get_valid_int("메뉴를 선택하세요 (1-5): ", 1, 5)

        # 선택한 번호에 맞는 기능 함수를 호출한다
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
            break  # while True 반복문을 빠져나가며 프로그램 종료


# 이 파일을 직접 실행했을 때만(다른 파일에서 import 했을 때는 실행되지 않음) 아래 코드가 동작한다
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        # 사용자가 Ctrl+C를 눌러 강제 종료를 시도한 경우
        # 에러 트레이스백을 그대로 보여주지 않고, 안내 메시지 후 안전하게 종료한다
        print("\n\n[알림] 강제 종료 신호(Ctrl+C)를 감지했습니다. 안전하게 종료합니다.")
        sys.exit(0)
    except EOFError:
        # 입력 스트림이 예기치 않게 끊긴 경우(예: 파이프로 실행하다 입력이 바닥난 경우)
        print("\n\n[알림] 입력이 종료되어 프로그램을 안전하게 종료합니다.")
        sys.exit(0)
