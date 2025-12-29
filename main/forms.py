from django import forms


class ProfileForm(forms.Form):
    """User profile information form."""
    name = forms.CharField(max_length=120, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Your full name',
        'class': 'form-control'
    }))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'placeholder': 'your.email@example.com',
        'class': 'form-control'
    }))
    location = forms.CharField(max_length=120, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'City, Country',
        'class': 'form-control'
    }))
    education = forms.CharField(max_length=120, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'e.g., Bachelor of Technology',
        'class': 'form-control'
    }))
    experience = forms.IntegerField(required=False, min_value=0, widget=forms.NumberInput(attrs={
        'placeholder': 'Years of experience',
        'class': 'form-control'
    }))
    skills = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Skills (comma-separated): Python, SQL, Machine Learning',
        'rows': 4,
        'class': 'form-control'
    }), required=False, help_text='Enter skills separated by commas')


class ResumeForm(forms.Form):
    """Professional resume builder form."""
    name = forms.CharField(max_length=120, required=True, label="Full Name", widget=forms.TextInput(attrs={
        'placeholder': 'Your full name',
        'class': 'form-control'
    }))
    summary = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Professional summary (2-3 sentences about yourself)',
            'rows': 4,
            'class': 'form-control'
        }), 
        required=False,
        label="Professional Summary"
    )
    experiences = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'List your work experiences. Separate multiple entries with "---"\nExample:\nCompany Name | Job Title | Jan 2020 - Present | Description of role',
            'rows': 6,
            'class': 'form-control'
        }), 
        required=False,
        label="Work Experience",
        help_text='Separate multiple entries with "---"'
    )
    education = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Your educational background. Separate entries with "---"\nExample:\nUniversity Name | Degree | Field of Study | 2020',
            'rows': 4,
            'class': 'form-control'
        }), 
        required=False,
        label="Education",
        help_text='Separate multiple entries with "---"'
    )
    skills = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Your professional skills (comma-separated)\nExample: Python, SQL, JavaScript, React, Machine Learning, AWS',
            'rows': 3,
            'class': 'form-control'
        }), 
        required=False,
        label="Skills"
    )
    certifications = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Certifications and credentials. Separate entries with "---"\nExample: AWS Solutions Architect | Amazon Web Services | Jan 2023',
            'rows': 3,
            'class': 'form-control'
        }), 
        required=False,
        label="Certifications",
        help_text='Separate multiple entries with "---"'
    )


class CoverLetterForm(forms.Form):
    """Cover letter generation form."""
    name = forms.CharField(max_length=120, required=True, label="Your Name", widget=forms.TextInput(attrs={
        'placeholder': 'John Doe',
        'class': 'form-control'
    }))
    role = forms.CharField(max_length=120, required=True, label="Target Role", widget=forms.TextInput(attrs={
        'placeholder': 'Software Engineer',
        'class': 'form-control'
    }))
    company = forms.CharField(max_length=120, required=False, label="Company Name", widget=forms.TextInput(attrs={
        'placeholder': 'E.g., Google, Microsoft',
        'class': 'form-control'
    }))
    context = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Additional context: Why are you interested in this role? Your experience highlights?',
            'rows': 5,
            'class': 'form-control'
        }), 
        required=False,
        label="Additional Context"
    )
