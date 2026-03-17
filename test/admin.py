from django.contrib import admin
from django.utils.html import format_html
# Register your models here.
from django_summernote.admin import SummernoteModelAdmin,SummernoteInlineModelAdmin
from .settings import VIEW_KEY
from .models import Client,Concept, QuestionBank, QuizResponse, QuestionBankOption, UserQuiz, Quiz, QuizConcept


# Question Options
class QBankOptionAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
admin.site.register(QuestionBankOption, QBankOptionAdmin)

# Question and the admin models
class OptionInline(admin.TabularInline,SummernoteInlineModelAdmin):
    model = QuestionBankOption
    max_num = 4
    extra = 4
class QuestionBankAdmin(SummernoteModelAdmin):
    inlines = [OptionInline]
    list_display = ('concept','short_desc','is_active','sme_note','view_html')
    summernote_fields = '__all__'
    list_filter = ('concept__display_name',)
    def view_html(self, obj):
        return format_html('<button class="button" target="_blank" onclick="window.open(\'/assessment/question_view/' + VIEW_KEY + '/' + str(obj.id) + '\');" type="button">&nbsp; View &nbsp;</button>')

admin.site.register(QuestionBank,QuestionBankAdmin)

admin.site.register(Concept)

class QuizConceptInline(admin.TabularInline):
    model = QuizConcept
    extra = 1

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuizConceptInline]
    list_display = ('name','display_name','is_timed','time_min','create_dummy')
    def create_dummy(self,obj):
        return format_html('<a class="button" target="_blank" href="/assessment/create_dummy/' + obj.name + '">Test Ride</a>')
admin.site.register(Quiz,QuizAdmin)

class UserQuizAdmin(admin.ModelAdmin):
    list_display = ('__str__','quiz','client','has_passed','num_correct','num_questions','started_at','view_responses')
    list_filter = ('client','started_at',)
    readonly_fields = ['client','quiz','id_pub','has_passed','num_correct','num_questions','started_at','submitted_at']
    fields = ['client','quiz','id_pub','has_passed','num_correct','num_questions','started_at','submitted_at']
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return True

    def has_passed(self,obj):
        if obj.num_correct/obj.num_questions > 0.5:
            return True
        else:
            return False
    has_passed.boolean = True
    def view_responses(self,obj):
        return format_html('<a class="button" target="_blank" href="/assessment/user_quiz_view/' + obj.id_pub + '/' + obj.key + '">View</a>')

admin.site.register(UserQuiz,UserQuizAdmin)

admin.site.register(Client)
