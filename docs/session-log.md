# 세션 기록 — 2026-08-14

Claude와 함께 `apps` 코드를 학습·리뷰·리팩터링한 세션 요약. 다음 대화를 시작할 때 이 문서를
먼저 참고하면 맥락을 다시 설명할 필요가 줄어든다.

## 이번 세션에서 한 일

1. `main.py`를 함수 단위로 끊어 한 줄씩 학습 (`get_valid_int`, `run_quiz`, `add_new_question`,
   `view_question_list`, `show_high_score`, `main_menu`, `if __name__ == "__main__":` 진입점)
2. `apps` 폴더 전체 클래스 구조 개괄 (`Quiz`/`QuizGame`/`Storage`의 책임 분리, `QuizGame`이
   `Quiz`를 import 없이 덕 타이핑으로만 사용하는 점 등)
3. "숙련된 개발자 관점"의 코드 리뷰를 여러 차례 진행하고, 그중 일부를 실제로 리팩터링
4. 전체 코드가 실제로 정상 동작하는지 격리된 테스트 폴더에서 시나리오를 돌려 검증(메뉴 흐름,
   입력 검증, 손상된 파일 복구, `EOFError` 처리 등)

## 진행된 리팩터링 (커밋 순서)

| 커밋 | 내용 |
|---|---|
| `de64d86` | 모듈 파일명을 PEP8 관례에 맞게 소문자로 변경 (`Quiz.py`→`quiz.py`, `QuizGame.py`→`quiz_game.py`, `Storage.py`→`storage.py`) |
| `dd5a889` | 파일명 변경에 맞춰 import 경로 수정 + `sys.stdin`/`stdout` UTF-8 강제 설정 추가 (cp949 콘솔에서 한글 문제 추가 시 `UnicodeEncodeError`로 죽는 버그를 재현 후 수정) |
| `2fd241f` | `QuizGame` 책임 분리 — `next_question`/`check_answer`(입출력 포함)를 없애고 `get_current_question`/`submit_answer`(순수 로직)로 교체. 화면 출력·입력 검증은 `main.py`(`get_valid_int` 재사용)로 이동 |
| `007bfd3` | `main.py`에 흩어져 있던 함수 5개 + 전역 변수 `storage`를 `QuizCLI` 클래스로 묶음. `storage`는 `self.storage` 인스턴스 상태가 됨 |
| `6545663` | `QuizCLI` 클래스를 `apps/quiz_cli.py`로 분리. `main.py`는 `QuizCLI`를 생성해 실행·예외 처리만 하는 얇은 진입점으로 남음 |
| `e2242ab` | (사용자 요청으로) UTF-8 강제 설정 제거 — **cp949 콘솔에서 한글 문제 추가 시 크래시가 재발할 수 있는 상태로 되돌아감. 의도적인 트레이드오프.** |

## 현재 파일 구조

```
apps/
├── main.py       # 진입점: QuizCLI 생성 + main_menu() 실행 + Ctrl+C/EOF 처리
├── quiz_cli.py   # QuizCLI: 메뉴 출력, 입력 검증(get_valid_int), 모든 화면 입출력
├── quiz_game.py  # QuizGame: 순수 게임 진행 로직 (print/input 없음, 테스트하기 쉬움)
├── quiz.py       # Quiz: 문제 하나(question/choices/answer)를 표현하는 값 객체
└── storage.py    # Storage: state.json 로드/저장, 기본 퀴즈 데이터 제공
```

의존 방향: `main.py` → `QuizCLI` → (`Quiz`, `QuizGame`, `Storage`). `Quiz`/`QuizGame`/`Storage`는
서로의 존재를 모른다.

## 알려진 이슈 (미해결, 임팩트 순)

1. **[크래시 위험]** `main.py`에서 UTF-8 강제 설정을 되돌려서, cp949 콘솔 환경에서 한글 문제를
   추가하면 `storage.save()`에서 `UnicodeEncodeError`로 죽을 수 있음(`e2242ab`에서 의도적으로
   되돌린 상태).
2. **`storage.py`**
   - 상대경로 의존(`path="state.json"`) — 실행 위치(cwd)에 따라 다른 파일을 봄
   - `save()`에 예외 처리 없음 — `OSError` 발생 시 트레이스백과 함께 죽음
   - 손상된 파일을 백업 없이 바로 기본 데이터로 덮어씀
   - `questions` 내부 스키마(보기 4개, 정답 1~4) 검증 없음 — 수동 편집으로 깨진 데이터가
     `load()`는 통과하고 한참 뒤 퀴즈 진행 중 `IndexError`/`KeyError`로 죽을 수 있음
   - `get_default_data()`가 도메인 콘텐츠(퀴즈 5개)를 하드코딩하고 있어 단일 책임 원칙에서
     벗어남
3. **`quiz_cli.py`**
   - `"엔터를 누르면 메뉴로 돌아갑니다..."` 문자열이 5곳에 중복
   - 메뉴 선택마다 `self.storage.load()`를 독립적으로 호출(캐싱 없음 — 트레이드오프로 남겨둠)
4. **`quiz_game.py`**
   - `question_number`가 "다음 인덱스"와 "지금까지 푼 문제 수" 두 의미로 쓰여 읽기 헷갈릴 수 있음
   - `submit_answer()`가 `still_has_questions()` 확인 없이 호출되면 `IndexError` (현재 유일한
     호출부는 안전하게 쓰고 있어 실사용에는 문제없음)
5. **`quiz.py`**
   - 생성자에 값 검증 없음 (보기 개수, 정답 범위 등)
   - `self.choices = choices`가 리스트를 참조로 공유(방어적 복사 없음)

## 의도적으로 하지 않기로 한 것

- **자동화된 테스트(`unittest`) 추가**: 리뷰에서 제안했지만 사용자가 명시적으로 거절함
  ("최대한 코드를 간결하게 해야 내가 설명하기 쉽잖아"). 앞으로도 리뷰 시 제안은 하되 먼저
  나서서 구현하지 않을 것.

## 다음 대화 참고사항

- 이 프로젝트는 `docs/mission-2.md`(미션 과제)와 `docs/evaluations.md`(평가기준, 특히 항목 2
  코드 구조 설명·항목 4 심층 인터뷰)에 맞춰 진행 중.
- 사용자는 파이썬 초보자이며, 최종 목표는 이 코드를 스스로 남에게 설명할 수 있게 되는 것(평가가
  인터뷰 형식 포함).
- 설명/리뷰 진행 시 선호 스타일: 함수 단위로 끊어서 진행, 다음 단계로 넘어가기 전에 확인 질문,
  12년차 시니어 개발자 관점의 통찰 포함.
