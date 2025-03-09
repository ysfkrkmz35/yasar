from django import template

from system.params import PRMS

register = template.Library()

# Check authorisation

@register.filter
def chk_aut(user, type, auth):
    member = None
    if type == PRMS['EMP_MEMBER'] and hasattr(user, 'employee'): member = user.employee

    if member is not None and member.role == auth: return True
    return False

# Check for employee

@register.filter
def is_emp_mgr(user):
    return chk_aut(user, PRMS['EMP_MEMBER'], PRMS['AUT_MGR'])

@register.filter
def is_emp_sup(user):
    if chk_aut(user, PRMS['EMP_MEMBER'], PRMS['AUT_SUP']): return True
    return is_emp_mgr(user)

@register.filter
def is_emp_usr(user):
    if chk_aut(user, PRMS['EMP_MEMBER'], PRMS['AUT_USR']): return True
    return is_emp_sup(user)

@register.filter
def is_emp_gst(user):
    if chk_aut(user, PRMS['EMP_MEMBER'], PRMS['AUT_GST']): return True
    return is_emp_usr(user)

# Check for generic member

@register.filter
def is_mbr_aut(user, type, auth):
    if type == PRMS['EMP_MEMBER']:
        if auth == PRMS['AUT_MGR']: return is_emp_mgr(user)
        if auth == PRMS['AUT_SUP']: return is_emp_sup(user)
        if auth == PRMS['AUT_USR']: return is_emp_usr(user)
        if auth == PRMS['AUT_GST']: return is_emp_gst(user)

    return False

@register.filter
def is_mbr_mgr(user, type):
    return is_mbr_aut(user, type, PRMS['AUT_MGR'])

@register.filter
def is_mbr_sup(user, type):
    return is_mbr_aut(user, type, PRMS['AUT_SUP'])

@register.filter
def is_mbr_usr(user, type):
    return is_mbr_aut(user, type, PRMS['AUT_USR'])

@register.filter
def is_mbr_gst(user, type):
    return is_mbr_aut(user, type, PRMS['AUT_GST'])

# Toggle row color
@register.filter
def row_tint_color(index):
    if int(index/2)*2 == index: return 'white'
    else:
        return '#f0f0f0'

# Get a particular item from a collection
@register.filter
def get_item(list, item):
    return list[item]

# Get a particular item from a tuple
@register.filter
def get_from_tuple(tuple, key):
    return next((y for x, y in tuple if x == key), None)

# Get a loop counter
@register.filter
def filter_range(start, end):
    return range(start, end)
