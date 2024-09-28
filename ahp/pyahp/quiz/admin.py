from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  # Số lượng lựa chọn sẽ hiện trước khi có thêm lựa chọn mới

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]  # Đính kèm các lựa chọn vào câu hỏi
    list_display = ('question_text',)  # Hiển thị cột "question_text" trong danh sách các câu hỏi

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)