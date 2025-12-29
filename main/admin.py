from django.contrib import admin
from .models import (Post, Profile, Conversation, Message, Recommendation, 
                     InterviewAttempt, Resume, CoverLetter)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'body')
    ordering = ('-created_at',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'location', 'created_at')
    list_filter = ('created_at', 'location')
    search_fields = ('name', 'email')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'location')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('title', 'message_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title',)
    readonly_fields = ('created_at',)
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = "Messages"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'role', 'preview_text', 'created_at')
    list_filter = ('role', 'created_at', 'conversation')
    search_fields = ('conversation__title', 'text')
    readonly_fields = ('created_at', 'full_text')
    
    def preview_text(self, obj):
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    preview_text.short_description = "Text Preview"
    
    def full_text(self, obj):
        return obj.text
    full_text.short_description = "Full Text"


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'roles_display', 'created_at')
    list_filter = ('created_at', 'profile')
    search_fields = ('profile__name', 'recommended_roles')
    readonly_fields = ('created_at',)
    
    def roles_display(self, obj):
        roles = obj.get_roles()
        return ', '.join(roles[:3]) + (f' +{len(roles)-3}' if len(roles) > 3 else '')
    roles_display.short_description = "Recommended Roles"


@admin.register(InterviewAttempt)
class InterviewAttemptAdmin(admin.ModelAdmin):
    list_display = ('role', 'question_count', 'score_display', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('role',)
    readonly_fields = ('created_at', 'questions_json_display', 'answers_json_display')
    
    fieldsets = (
        ('Interview Details', {
            'fields': ('role', 'score', 'created_at')
        }),
        ('Questions & Answers', {
            'fields': ('questions_json_display', 'answers_json_display'),
            'classes': ('collapse',)
        }),
    )
    
    def question_count(self, obj):
        import json
        try:
            qs = json.loads(obj.questions)
            return len(qs)
        except:
            return 0
    question_count.short_description = "Questions"
    
    def score_display(self, obj):
        if obj.score:
            return f"{obj.score:.1f}/10"
        return "Not scored"
    score_display.short_description = "Score"
    
    def questions_json_display(self, obj):
        import json
        try:
            qs = json.loads(obj.questions)
            return '\n\n'.join([f"{i+1}. {q}" for i, q in enumerate(qs)])
        except:
            return obj.questions
    questions_json_display.short_description = "Questions"
    
    def answers_json_display(self, obj):
        if not obj.answers:
            return "No answers submitted"
        import json
        try:
            ans = json.loads(obj.answers)
            return '\n\n'.join([f"{i+1}. {a}" for i, a in enumerate(ans)])
        except:
            return obj.answers
    answers_json_display.short_description = "Answers"


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'data_preview')
    list_filter = ('created_at',)
    search_fields = ('name',)
    readonly_fields = ('created_at', 'data_json_display')
    
    fieldsets = (
        ('Resume Information', {
            'fields': ('name', 'created_at')
        }),
        ('Resume Data', {
            'fields': ('data_json_display',),
            'classes': ('collapse',)
        }),
    )
    
    def data_preview(self, obj):
        import json
        try:
            data = json.loads(obj.data_json)
            summary = data.get('summary', '')[:50]
            return summary + '...' if summary else 'No summary'
        except:
            return 'Error reading data'
    data_preview.short_description = "Preview"
    
    def data_json_display(self, obj):
        import json
        try:
            data = json.loads(obj.data_json)
            return json.dumps(data, indent=2)
        except:
            return obj.data_json
    data_json_display.short_description = "Full Data"


@admin.register(CoverLetter)
class CoverLetterAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'created_at', 'body_preview')
    list_filter = ('role', 'created_at')
    search_fields = ('name', 'role', 'body')
    readonly_fields = ('created_at', 'full_body')
    
    fieldsets = (
        ('Letter Information', {
            'fields': ('name', 'role', 'created_at')
        }),
        ('Cover Letter Content', {
            'fields': ('full_body',),
        }),
    )
    
    def body_preview(self, obj):
        return obj.body[:100] + '...' if len(obj.body) > 100 else obj.body
    body_preview.short_description = "Preview"
    
    def full_body(self, obj):
        return obj.body
    full_body.short_description = "Full Letter"