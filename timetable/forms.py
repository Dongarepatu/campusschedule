from django import forms
from .models import TimetableEntry, Faculty

class TimetableForm(forms.ModelForm):
    lab_faculty = forms.ModelMultipleChoiceField(
        queryset=Faculty.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'style': 'height: 150px;'
        }),
        label="Lab Faculty (Multiple)"
    )
    
    # Change from BooleanField to CharField
    is_lab = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),  # Hidden since we handle it with radio buttons
        initial='lecture'
    )
    
    class Meta:
        model = TimetableEntry
        fields = ['department', 'semester', 'day', 'start_time', 'end_time', 'subject', 'faculty']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'day': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter subject name'
            }),
            'faculty': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make day field optional with special placeholder
        self.fields['day'].required = False
        self.fields['day'].widget.choices = [
            ('', 'Select Day (Optional for Recess)'),
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
        ]
        
        # Make faculty optional initially
        self.fields['faculty'].required = False
        self.fields['faculty'].label = "Theory Faculty (Single)"
        
        # Set default semester to Semester 1
        if not self.instance.pk:  # Only for new entries
            self.fields['semester'].initial = 'Semester 1'
    
    def clean(self):
        cleaned_data = super().clean()
        
        subject = cleaned_data.get('subject', '').lower()
        faculty = cleaned_data.get('faculty')
        lab_faculty = cleaned_data.get('lab_faculty')
        day = cleaned_data.get('day')
        
        # Get is_lab from data (not cleaned_data since it's a hidden field)
        is_lab = self.data.get('is_lab', 'lecture')  # 'lab' or 'lecture'
        
        # Store it in cleaned_data for later use
        cleaned_data['is_lab'] = is_lab
        
        # Check if it's a recess/break/lunch
        is_break = any(x in subject for x in ['recess', 'lunch', 'break', 'interval'])
        
        # For breaks
        if is_break:
            # If day is not provided for break, that's OK
            # Faculty should be None for breaks
            if faculty:
                self.add_error('faculty', 'Faculty should not be selected for recess/break entries')
                cleaned_data['faculty'] = None
            # Clear lab_faculty for breaks
            if lab_faculty:
                self.add_error('lab_faculty', 'Lab faculty should not be selected for recess/break entries')
                cleaned_data['lab_faculty'] = None
        else:
            # For non-break entries
            if not day:
                self.add_error('day', 'Day is required for all non-break entries')
            
            # Check faculty selection based on mode
            if is_lab == 'lab':
                # Lab mode - require lab_faculty, not single faculty
                if not lab_faculty:
                    self.add_error('lab_faculty', 'Please select at least one Lab Faculty for lab sessions')
                # Clear single faculty if lab mode is selected
                if faculty:
                    self.add_error('faculty', 'Theory faculty should not be selected for lab sessions. Use the "Lab Faculty" field below.')
                    cleaned_data['faculty'] = None
            else:
                # Lecture mode - require single faculty, not lab_faculty
                if not faculty:
                    self.add_error('faculty', 'Please select a Theory Faculty for lecture sessions')
                # Clear lab_faculty if lecture mode is selected
                if lab_faculty:
                    self.add_error('lab_faculty', 'Lab faculty should not be selected for lecture sessions. Use the "Theory Faculty" field above.')
                    cleaned_data['lab_faculty'] = None
        
        return cleaned_data
    
    def save(self, commit=True):
        # Don't save directly - we'll handle saving in the view
        instance = super().save(commit=False)
        
        # Check if it's a break
        subject = self.cleaned_data.get('subject', '').lower()
        is_break = any(x in subject for x in ['recess', 'lunch', 'break', 'interval'])
        
        # For breaks, ensure faculty is None
        if is_break:
            instance.faculty = None
        
        if commit:
            instance.save()
        
        return instance