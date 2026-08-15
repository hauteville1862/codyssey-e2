class QuizGame:
    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def get_current_question(self):
        return self.question_list[self.question_number]

    def submit_answer(self, user_answer):
        is_correct = user_answer == self.get_current_question().answer
        self.question_number += 1

        if is_correct:
            self.score += 1

        return is_correct
