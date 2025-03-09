def adjust_phone_fields(form):
    form.fields['phone_country'].widget.attrs['style'] = 'width:40px;'
    form.fields['phone_part2'].widget.attrs['style'] = 'width:40px;'
    form.fields['phone_part3'].widget.attrs['style'] = 'width:40px;'
    form.fields['phone_part4'].widget.attrs['style'] = 'width:50px;'

def check_phone_number(form):
    is_phone_entered = False
    is_phone_valid = True
    err_msg = ''

    if form.cleaned_data['phone_country'] is not None or \
        form.cleaned_data['phone_part2'] is not None or \
        form.cleaned_data['phone_part3'] is not None or \
        form.cleaned_data['phone_part4'] is not None:
        is_phone_entered = True

    phone_number = '(+'

    if form.cleaned_data['phone_country'] is not None:
        phone_number += form.cleaned_data['phone_country'] + ') '
    elif is_phone_entered:
        phone_number += '...' + ') '
        is_phone_valid = False
    if form.cleaned_data['phone_part2'] is not None:
        phone_number += form.cleaned_data['phone_part2'] + ' '
    elif is_phone_entered:
        phone_number += '...' + ' '
        is_phone_valid = False
    if form.cleaned_data['phone_part3'] is not None:
        phone_number += form.cleaned_data['phone_part3'] + ' '
    elif is_phone_entered:
        phone_number += '...' + ' '
        is_phone_valid = False
    if form.cleaned_data['phone_part4'] is not None:
        phone_number += form.cleaned_data['phone_part4']
    elif is_phone_entered:
        phone_number += '...'
        is_phone_valid = False

    if not is_phone_valid:
        err_msg = 'Geçersiz telefon numarası: \"' + phone_number + '\"'

    return (is_phone_valid, err_msg)
