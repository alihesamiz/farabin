# 1️⃣ Import modules
from datetime import datetime
from django.utils import timezone
from apps.company.models import CompanyProfile
from apps.questionnaire.models import (
    Question, QuestionChoice, QuestionMetric,
    Questionnaire, QuestionnaireQuestion,
    CompanyQuestionnaire, CompanyAnswer
)

# 2️⃣ Create Questions
q1 = Question.objects.create(text="چقدر از خدمات ما رضایت دارید؟")
q2 = Question.objects.create(text="آیا محصولات ما را به دیگران توصیه می‌کنید؟")
q3 = Question.objects.create(text="چقدر احتمال دارد دوباره از محصولات ما استفاده کنید؟")
q4 = Question.objects.create(text="چقدر از فرآیندهای داخلی شرکت رضایت دارید؟")
q5 = Question.objects.create(text="آیا احساس می‌کنید همکاری تیمی در شرکت موثر است؟")

# 3️⃣ Create Question Choices
choices_satisfaction = [
    QuestionChoice.objects.create(question=q1, answer="خیلی راضی", points=5),
    QuestionChoice.objects.create(question=q1, answer="نسبتاً راضی", points=4),
    QuestionChoice.objects.create(question=q1, answer="متوسط", points=3),
    QuestionChoice.objects.create(question=q1, answer="ناراضی", points=2),
    QuestionChoice.objects.create(question=q1, answer="خیلی ناراضی", points=1),
]

# q2: Yes/No
choice_yes = QuestionChoice.objects.create(question=q2, answer="بله", points=1)
choice_no = QuestionChoice.objects.create(question=q2, answer="خیر", points=0)

# q3: Likelihood scale
choices_likelihood = [
    QuestionChoice.objects.create(question=q3, answer="حتماً", points=5),
    QuestionChoice.objects.create(question=q3, answer="احتمال زیاد", points=4),
    QuestionChoice.objects.create(question=q3, answer="ممکن است", points=3),
    QuestionChoice.objects.create(question=q3, answer="احتمال کم", points=2),
    QuestionChoice.objects.create(question=q3, answer="هرگز", points=1),
]

# q4: Internal satisfaction
QuestionChoice.objects.bulk_create([
    QuestionChoice(question=q4, answer="خیلی راضی", points=5),
    QuestionChoice(question=q4, answer="راضی", points=4),
    QuestionChoice(question=q4, answer="متوسط", points=3),
    QuestionChoice(question=q4, answer="ناراضی", points=2),
    QuestionChoice(question=q4, answer="خیلی ناراضی", points=1),
])

# q5: Team cooperation
QuestionChoice.objects.bulk_create([
    QuestionChoice(question=q5, answer="کاملاً موثر", points=5),
    QuestionChoice(question=q5, answer="موثر", points=4),
    QuestionChoice(question=q5, answer="متوسط", points=3),
    QuestionChoice(question=q5, answer="کم موثر", points=2),
    QuestionChoice(question=q5, answer="بی‌تاثیر", points=1),
])

# 4️⃣ Create Question Metrics
QuestionMetric.objects.create(question=q1, title="رضایت مشتری", weight=0.4)
QuestionMetric.objects.create(question=q2, title="توصیه به دیگران", weight=0.3)
QuestionMetric.objects.create(question=q3, title="احتمال بازگشت مشتری", weight=0.3)
QuestionMetric.objects.create(question=q4, title="رضایت داخلی", weight=0.5)
QuestionMetric.objects.create(question=q5, title="همکاری تیمی", weight=0.5)

# 5️⃣ Create a Questionnaire
questionnaire = Questionnaire.objects.create(
    id="business-01",
    name="نظرسنجی عملکرد و رضایت شرکت"
)

# 6️⃣ Link Questions to Questionnaire (only once)
QuestionnaireQuestion.objects.bulk_create([
    QuestionnaireQuestion(questionnaire=questionnaire, question=q1, order=1),
    QuestionnaireQuestion(questionnaire=questionnaire, question=q2, order=2),
    QuestionnaireQuestion(questionnaire=questionnaire, question=q3, order=3),
    QuestionnaireQuestion(questionnaire=questionnaire, question=q4, order=4),
    QuestionnaireQuestion(questionnaire=questionnaire, question=q5, order=5),
])

# 7️⃣ Save Questionnaire
questionnaire.save()

# 8️⃣ Create a Company
company = CompanyProfile.objects.create(title="شرکت نمونه")

# 9️⃣ Assign Questionnaire to Company
company_q = CompanyQuestionnaire.objects.create(
    company=company,
    questionnaire=questionnaire,
    submitted_at=timezone.now()
)

# 🔟 Add sample answers
CompanyAnswer.objects.create(company_questionnaire=company_q, question=q1, selected_choice=choices_satisfaction[0])
CompanyAnswer.objects.create(company_questionnaire=company_q, question=q2, selected_choice=choice_yes)
CompanyAnswer.objects.create(company_questionnaire=company_q, question=q3, selected_choice=choices_likelihood[1])
CompanyAnswer.objects.create(company_questionnaire=company_q, question=q4, selected_choice=QuestionChoice.objects.get(question=q4, answer="راضی"))
CompanyAnswer.objects.create(company_questionnaire=company_q, question=q5, selected_choice=QuestionChoice.objects.get(question=q5, answer="موثر"))

print("✅ Mock business survey data in Farsi inserted successfully!")
