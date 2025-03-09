from django import forms
from .models import Attendants, Decisions

class AttendantForm(forms.ModelForm):
    class Meta:
        model = Attendants
        fields = ['member']
        labels = {
            'member': 'Katılımcı',
        }

class DecisionForm(forms.ModelForm):
    class Meta:
        model = Decisions
        fields = ['topic_group', 'decision_status', 'decision_text']
        labels = {
            'topic_group': 'Konu Grubu',
            'decision_status': 'Karar Durumu',
            'decision_text': 'Karar Metni',
        }
