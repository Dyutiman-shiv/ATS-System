import secrets, string, random
from django.db import models

def token_alphanum(size):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))
def token_alphanum32():
    return token_alphanum(32)
def token_alphanum16():
    return token_alphanum(16)
def token_alphanum8():
    return token_alphanum(8)
def token_alphanum6():
    return token_alphanum(6)

# This class represents clients who are authorized to create assessements
class Client(models.Model):
    username = models.CharField(unique=True,max_length=16)
    display_name = models.CharField(default='noName.com',max_length=16)
    display_header = models.CharField(default='noName.com OTP Psychometric Test',max_length=128)
    api_key = models.CharField(unique=True,default=token_alphanum8,max_length=16)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.username

# The concepts are related to questions.
class Concept(models.Model):
    name = models.CharField(unique=True,null=False,max_length=128,help_text='unique id for the concept')
    display_name = models.CharField(null=True,max_length=256,help_text='display name for the concept')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.display_name

# This question bank
class QuestionBank(models.Model):
    concept = models.ForeignKey(Concept,null=False,on_delete=models.PROTECT)
    tags = models.CharField(null=True,blank=True, max_length=1024,help_text='comma seperated tags for the question')
    type = models.CharField(default='mcq',max_length=32,help_text='type of question like MCQ etc')
    html = models.TextField(null=False,help_text='question html')
    is_active = models.BooleanField(default=False, help_text='make active only after quality check')
    sme_note = models.TextField(null=True, blank=True, help_text='SME can write a note for other reviewers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'assessment_question_bank'
    @property
    def short_desc(self):
        return self.html[:100]
    def __str__(self):
        return self.html[:20]

# This will store options if the question type is MCQ
class QuestionBankOption(models.Model):
    question = models.ForeignKey(QuestionBank,on_delete=models.CASCADE)
    html = models.TextField(help_text='option html')
    is_correct = models.BooleanField(default=False,help_text='True if the option is correct')
    sequence = models.PositiveSmallIntegerField(help_text='order in which the options will be displayed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'assessment_question_bank_option'
    def __str__(self):
        return self.html[0:20]

# Quiz Class
class Quiz(models.Model):
    name = models.CharField(unique=True, max_length=128, help_text='unique id for the quiz')
    display_name = models.CharField(max_length=256, help_text='display text for quiz')
    is_timed = models.BooleanField(default=False)
    time_min = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

# Select all the concepts from here and then get questions for UserQuiz
class QuizConcept(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.PROTECT)
    concept = models.ForeignKey(Concept,on_delete=models.PROTECT)
    num_questions = models.IntegerField()
    class Meta:
        db_table = 'assessment_quiz_concept'

# This is an instance of Quiz
class UserQuiz(models.Model):
    client = models.ForeignKey(Client,null=False,on_delete=models.PROTECT)
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT)
    id_pub = models.CharField(unique=True, default=token_alphanum16 , max_length=32, help_text='public id')
    key = models.CharField(unique=True,default=token_alphanum16, max_length=32, help_text='secret key')
    num_questions = models.PositiveSmallIntegerField(null=True,help_text='total number of questions')
    num_correct = models.PositiveSmallIntegerField(default=0,help_text='number of correct answers. will be calculated after submit')
    update_url = models.CharField(null=True,blank=True,max_length=1024,help_text='url where quiz result will be POSTed')
    forward_url = models.CharField(null=False, max_length=1024, help_text= 'forward to this url after test is submitted')
    var = models.CharField(null=True,max_length=64,help_text='optional variable to be passed back to the client')
    started_at = models.DateTimeField(null=True, help_text='time at which the quiz started')
    expires_at = models.DateTimeField(null=True, help_text='time at which the quiz expires')
    submitted_at = models.DateTimeField(null=True,help_text='time at which quiz is submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'assessment_user_quiz'
    def __str__(self):
        return self.id_pub

# This will include Quiz questions and response from the user
# We create all rows as soon as UserQuiz is created
# When the quiz is submitted, we calculate and update UserQuiz
class QuizResponse(models.Model):
    user_quiz = models.ForeignKey(UserQuiz,on_delete=models.PROTECT)
    sequence = models.PositiveSmallIntegerField(null=False,help_text='sequence in which questions will be displayed')
    question = models.ForeignKey(QuestionBank,on_delete=models.PROTECT)
    selected_index = models.PositiveSmallIntegerField(null=True, help_text='index which is selected')
    is_correct = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False,help_text='user can flag a question for review during quiz')
    submitted_at = models.DateTimeField(null=True, help_text='time at which the question is submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'assessment_quiz_response'


