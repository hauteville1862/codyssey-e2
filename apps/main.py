import sys

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")

from quiz_cli import QuizCLI


if __name__ == "__main__":
    app = QuizCLI()
    try:
        app.main_menu()
    except KeyboardInterrupt:
        print("\n\n[알림] 강제 종료 신호(Ctrl+C)를 감지했습니다. 안전하게 종료합니다.")
        sys.exit(0)
    except EOFError:
        print("\n\n[알림] 입력이 종료되어 프로그램을 안전하게 종료합니다.")
        sys.exit(0)
