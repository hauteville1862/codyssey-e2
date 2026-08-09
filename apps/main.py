import json
import os
import sys
from Quiz import Quiz
from QuizGame import QuizGame

# main.py와 같은 apps 폴더의 state.json을 사용한다 (실행 위치와 무관하게 동작)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "state.json")

def get_default_data():
    """파일이 없거나 손상된 경우 사용할 기본 퀴즈 데이터 (5개 이상). 호출마다 새 dict를 생성한다."""
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
    os.system('cls' if os.name == 'nt' else 'clear')

def get_valid_int(prompt, min_value, max_value):
    """공백 제거, 빈 입력, 숫자 변환 실패, 범위 초과를 모두 처리하는 정수 입력."""
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
        if not (min_value <= value <= max_value):
            print(f"[알림] {min_value}~{max_value} 사이의 숫자를 입력해주세요.")
            continue
        return value

def load_data():
    """파일에서 데이터를 로드합니다. 파일이 없거나 손상된 경우 기본 데이터로 대체합니다."""
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
        if "high_score" not in data or "questions" not in data:
            raise ValueError("state.json 구조가 올바르지 않습니다.")
        return data
    except FileNotFoundError:
        # 파일이 없을 경우 기본 퀴즈 데이터 사용
        return get_default_data()
    except (json.JSONDecodeError, ValueError):
        # 파일이 손상된 경우 기본 데이터로 복구
        print("\n[알림] 데이터 파일이 손상되어 기본 퀴즈 데이터로 초기화합니다.")
        recovered = get_default_data()
        save_data(recovered)
        return recovered

def save_data(data):
    """데이터를 파일에 저장합니다."""
    with open(DATA_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def run_quiz():
    """1. 퀴즈 시작"""
    data = load_data()
    if not data["questions"]:
        print("\n[알림] 등록된 문제가 없습니다. 문제를 먼저 추가해주세요!")
        input("\n엔터를 누르면 메뉴로 돌아갑니다...")
        return

    question_bank = []
    for q in data["questions"]:
        question_bank.append(Quiz(q["question"], q["options"], q["answer"]))

    quiz = QuizGame(question_bank)
    while quiz.still_has_questions():
        quiz.next_question()

    print("\n" + "="*30)
    print(f"퀴즈 종료! 최종 점수: {quiz.score}/{len(question_bank)}")

    if quiz.score > data["high_score"]:
        print(f"최고 점수 갱신! ({data['high_score']} -> {quiz.score})")
        data["high_score"] = quiz.score
        save_data(data)
    print("="*30)
    input("\n엔터를 누르면 메뉴로 돌아갑니다...")

def add_new_question():
    """2. 퀴즈 추가"""
    clear_screen()
    print("[새 문제 추가]")
    question = input("문제 내용을 입력하세요: ").strip()
    while question == "":
        print("[알림] 문제 내용은 비어 있을 수 없습니다.")
        question = input("문제 내용을 입력하세요: ").strip()

    options = []
    for i in range(1, 5):
        opt = input(f"보기 {i}번을 입력하세요: ").strip()
        while opt == "":
            print("[알림] 보기 내용은 비어 있을 수 없습니다.")
            opt = input(f"보기 {i}번을 입력하세요: ").strip()
        options.append(opt)

    answer = get_valid_int("정답 번호를 입력하세요 (1-4): ", 1, 4)

    data = load_data()
    new_q = {"question": question, "options": options, "answer": answer}
    data["questions"].append(new_q)
    save_data(data)
    print("\n문제가 성공적으로 추가되었습니다!")
    input("\n엔터를 누르면 메뉴로 돌아갑니다...")

def view_question_list():
    """3. 퀴즈 목록 보기"""
    clear_screen()
    data = load_data()
    print("[등록된 퀴즈 목록]")
    if not data["questions"]:
        print("등록된 문제가 없습니다.")
    else:
        for i, q in enumerate(data["questions"], 1):
            print(f"{i}. {q['question']} (정답: {q['answer']}번)")
    
    print("-" * 30)
    input("\n엔터를 누르면 메뉴로 돌아갑니다...")

def show_high_score():
    """4. 최고 점수 확인"""
    clear_screen()
    data = load_data()
    print("[현재 최고 점수]")
    print(f"\n현재까지의 최고 기록은 {data['high_score']}점입니다.")
    print("\n더 높은 점수에 도전해보세요!")
    print("-" * 30)
    input("\n엔터를 누르면 메뉴로 돌아갑니다...")

def main_menu():
    """메인 메뉴 화면"""
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