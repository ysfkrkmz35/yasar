from datetime import datetime

from entity.models import Work

from ThirdSpring.templatetags.ThirdSpring_filters import get_from_tuple
from ThirdSpring.templatetags.ThirdSpring_filters import is_owner
from ThirdSpring.templatetags.ThirdSpring_filters import is_prt_usr, is_prt_sup, is_prt_mgr
from ThirdSpring.templatetags.ThirdSpring_filters import is_emp_usr, is_emp_sup, is_emp_mgr

# Get options from objects for a user that is filtered by func

def get_options(objects, all_opt, me_opt, parameter, func):
    options = ()
    if me_opt != 0:
        options += ((me_opt, 'Kendiniz'),)

    if all_opt == -1 or all_opt == -3:
        options += ((-1, 'Tümü'),)
    if all_opt == -2 or all_opt == -3:
        options += (('', '---------'),)

    if objects is not None:
        for object in objects:
            if func==None or func(object.user):
                if parameter == 'LIST_NAME':
                    options += ((int(object.id), object.list_name()),)
                elif parameter == 'PROP_NUMB':
                    options += ((int(object.id), str(object)),)
    return options

def get_order_states(order, action, user, PRMS):
    if action =='CREATE':
        return None

    options = ()

    is_user_owner = is_owner(user)
    is_user_prt_mgr = is_prt_mgr(user)
    is_user_emp_mgr = is_emp_mgr(user)
    is_user_emp_sup = is_emp_sup(user)
    is_user_emp_usr = is_emp_usr(user)

    if order.status == PRMS['ORD_REQ']:
        options += ((PRMS['ORD_REQ'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_REQ'])),)
        if is_user_prt_mgr or is_user_emp_mgr:
            options += ((PRMS['ORD_RJT'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_RJT'])),)
        if is_user_emp_sup:
            options += ((PRMS['ORD_ASN'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_ASN'])),)
        if is_user_owner or is_user_prt_mgr or is_user_emp_mgr:
            options += ((PRMS['ORD_DCL'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_DCL'])),)
    elif order.status == PRMS['ORD_RJT']:
        options += ((PRMS['ORD_RJT'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_RJT'])),)
        if is_user_owner or is_user_prt_mgr or is_user_emp_mgr:
            options += ((PRMS['ORD_REQ'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_REQ'])),)
        if is_user_owner:
            options += ((PRMS['ORD_CLO'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_CLO'])),)
    elif order.status == PRMS['ORD_ASN']:
        options += ((PRMS['ORD_ASN'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_ASN'])),)
        if is_user_emp_usr:
            options += ((PRMS['ORD_EXA'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_EXA'])),)
    elif order.status == PRMS['ORD_EXA']:
        options += ((PRMS['ORD_EXA'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_EXA'])),)
        if is_user_emp_mgr:
            options += ((PRMS['ORD_RJT'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_RJT'])),)
        if is_user_emp_sup:
            options += ((PRMS['ORD_QTD'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_QTD'])),)
    elif order.status == PRMS['ORD_QTD']:
        options += ((PRMS['ORD_QTD'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_QTD'])),)
        if is_user_owner:
            options += ((PRMS['ORD_DFR'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_DFR'])),)
        if is_user_owner:
            options += ((PRMS['ORD_DCL'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_DCL'])),)
        if is_user_owner:
            options += ((PRMS['ORD_APR'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_APR'])),)
    elif order.status == PRMS['ORD_DFR']:
        options += ((PRMS['ORD_DFR'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_DFR'])),)
        if is_owner or is_user_emp_mgr:
            options += ((PRMS['ORD_REQ'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_REQ'])),)
        if is_owner or is_user_emp_mgr:
            options += ((PRMS['ORD_DCL'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_DCL'])),)
        if is_user_emp_sup:
            options += ((PRMS['ORD_CLO'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_CLO'])),)
    elif order.status == PRMS['ORD_DCL']:
        options += ((PRMS['ORD_DCL'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_DCL'])),)
        if is_user_emp_sup:
            options += ((PRMS['ORD_CLO'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_CLO'])),)
    elif order.status == PRMS['ORD_APR']:
        options += ((PRMS['ORD_APR'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_APR'])),)
        if is_user_emp_sup:
            options += ((PRMS['ORD_STR'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_STR'])),)
    elif order.status == PRMS['ORD_STR']:
        options += ((PRMS['ORD_STR'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_STR'])),)
        if is_user_emp_usr:
            options += ((PRMS['ORD_FIN'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_FIN'])),)
    elif order.status == PRMS['ORD_FIN']:
        options += ((PRMS['ORD_FIN'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_FIN'])),)
        if is_user_owner:
            options += ((PRMS['ORD_ACC'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_ACC'])),)
    elif order.status == PRMS['ORD_ACC']:
        options += ((PRMS['ORD_ACC'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_ACC'])),)
        if is_user_emp_sup:
            options += ((PRMS['ORD_BIL'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_BIL'])),)
    elif order.status == PRMS['ORD_BIL']:
        options += ((PRMS['ORD_BIL'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_BIL'])),)
        if is_user_owner or is_user_emp_sup:
            options += ((PRMS['ORD_PAY'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_PAY'])),)
    elif order.status == PRMS['ORD_PAY']:
        options += ((PRMS['ORD_PAY'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_PAY'])),)
        if is_user_emp_sup:
            options += ((PRMS['ORD_CLO'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_CLO'])),)
    elif order.status == PRMS['ORD_CLO']:
        options += ((PRMS['ORD_CLO'], get_from_tuple(PRMS['ORD_STAS'], PRMS['ORD_CLO'])),)
    return options

def check_order(order, action, user, PRMS):
    err_no = 0
    err_msg = ''

    if order.status == PRMS['ORD_REQ']:
        pass
    elif order.status == PRMS['ORD_RJT']:
        if order.rejecter is None:
            order.rejecter = user
        if order.rejecter is None:
            order.reject_date = datetime.now()
    elif order.status == PRMS['ORD_ASN']:
        if order.assigner is None:
            order.assigner = user
        if order.assignment_date is None:
            order.assignment_date = datetime.now()
        if order.assigned1 is None and order.assigned2 is None:
            err_no = -1
            err_msg += 'En az bir çalışan atanmalı.'
    elif order.status == PRMS['ORD_EXA']:
        if order.examiner is None:
            order.examiner = user
        if order.examination_date is None:
            order.examination_date = datetime.now()
    elif order.status == PRMS['ORD_QTD']:
        works = Work.objects.filter(order__id=order.id)
        order.material_cost = 0
        order.labor_cost = 0
        for work in works:
            order.material_cost += work.material_cost * work.bill_mat_pc / 100
            order.labor_cost += work.labor_hours * work.bill_lab_pc * work.employee.hourly_rate / 100
        if order.quoter is None:
            order.quoter = user
        if order.quotation_date is None:
            order.quotation_date = datetime.now()
    elif order.status == PRMS['ORD_DFR']:
        if order.deferrer is None:
            order.deferrer = user
        if order.deferring_date is None:
            order.deferring_date = datetime.now()
    elif order.status == PRMS['ORD_DCL']:
        if order.decliner is None:
            order.decliner = user
        if order.declining_date is None:
            order.declining_date = datetime.now()
    elif order.status == PRMS['ORD_APR']:
        if order.approver is None:
            order.approver = user
        if order.approval_date is None:
            order.approval_date = datetime.now()
    elif order.status == PRMS['ORD_STR']:
        if order.starter is None:
            order.starter = user
        if order.starting_date is None:
            order.starting_date = datetime.now()
    elif order.status == PRMS['ORD_FIN']:
        if order.completer is None:
            order.completer = user
        if order.completion_date is None:
            order.completion_date = datetime.now()
    elif order.status == PRMS['ORD_ACC']:
        if order.acceptor is None:
            order.acceptor = user
        if order.acception_date is None:
            order.acception_date = datetime.now()
    elif order.status == PRMS['ORD_BIL']:
        if order.biller is None:
            order.biller = user
        if order.billing_date is None:
            order.billing_date = datetime.now()
    elif order.status == PRMS['ORD_PAY']:
        order.paid_amount = order.material_cost + order.labor_cost
        if order.payer is None:
            order.payer = user
        if order.paying_date is None:
            order.paying_date = datetime.now()
    elif order.status == PRMS['ORD_CLO']:
        if order.closer is None:
            order.closer = user
        if order.closing_date is None:
            order.closing_date = datetime.now()

    return (err_no, err_msg)

def check_work(work, action, user, PRMS):
    err_no = 0
    err_msg = ''

    work.updater = user
    work.last_update = datetime.now()

    return (err_no, err_msg)



