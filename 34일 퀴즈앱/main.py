from question_model import Question
from data import question_data
from quiz_brain import QuizBrain
from ui import QuizInterface


question_bank = []
#api와 연결해서 question_data를 받아오고 이를 Question클래스를 통해 질문과 답으로 나누어준다.
for question in question_data:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)
    # print(new_question.text) #['text'] bracket은 오류가 나는데 .text 는 사용 가능  그이유는 사용자정의클래스 에는 getitem 메서드가 없어서 대괄호 기능 사용 안됨.

quiz = QuizBrain(question_bank) #QUizBrain 클래스 init에 q_list를 인자로 받는다.
print(type(quiz))
quiz_ui = QuizInterface(quiz)

while quiz.still_has_questions():
    quiz.next_question()

print("You've completed the quiz")
print(f"Your final score was: {quiz.score}/{quiz.question_number}")
