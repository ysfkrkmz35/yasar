from django import forms

from entity.models import Member, Employee

class MemberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Member
        exclude = []
        widgets = {}

class MemberFilterRequestForm(forms.Form):
    member = forms.CharField(max_length=32, required=False)

class EmployeeForm(MemberForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)

    class Meta(MemberForm.Meta):
        model = Employee

class EmployeeFilterRequestForm(MemberFilterRequestForm):
    pass

