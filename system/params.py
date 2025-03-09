from datetime import date

from dateutil.relativedelta import relativedelta

# Various global parameters

RCD_PER_PAG = 25

# Member types and authorization levels

EMP_MEMBER = 'EMP_MEMBER'

AUT_GST = 'AUT_GST'
AUT_USR = 'AUT_USR'
AUT_SUP = 'AUT_SUP'
AUT_MGR = 'AUT_MGR'

DEF_AUT_LVL = AUT_GST

AUT_LVLS = (
    (AUT_GST, 'Konuk'),
    (AUT_USR, 'Kullanıcı'),
    (AUT_SUP, 'Şef'),
    (AUT_MGR, 'Yönetici'),
)

# Defaults for name search

DEF_EMP = ''

# Sort types

SRT_NAM = 'NAM'
SRT_AUT = 'AUT'
SRT_TPC = 'TPC'
SRT_LAN = 'LAN'
SRT_PRD = 'PRD'
SRT_RID = 'RID'

DEF_SRT = SRT_NAM

SRTS = (
    (SRT_NAM, 'Eser Adı'),
    (SRT_AUT, 'Eser Sahibi'),
    (SRT_TPC, 'Etiket'),
    (SRT_LAN, 'Dil'),
    (SRT_PRD, 'Tür'),
    (SRT_RID, 'Kayıt No'),
)

# Borrowing Sort types

BRW_SRT_REV = 'REV'
BRW_SRT_FWD = 'FWD'

BRW_DEF_SRT = BRW_SRT_REV

BRW_SRTS = (
    (BRW_SRT_REV, 'Sondan Başa'),
    (BRW_SRT_FWD, 'Baştan Sona'),
)

BRW_DEF_BWR = 0

str_date = date(year=2024,month=10,day=1)
BRW_DEF_STR_DAT = str_date.strftime("%Y-%m-%d")

end_date = date.today()
end_date += relativedelta(days=1)
BRW_DEF_END_DAT = end_date.strftime("%Y-%m-%d")

# Order status

ORD_STA_ALL = '**'
ORD_STA_ALL_TXT = "Tüm Durumlar"

ORD_REQ = 'REQ'
ORD_RJT = 'RJT'
ORD_ASN = 'ASN'
ORD_EXA = 'EXA'
ORD_QTD = 'QTD'
ORD_DFR = 'DFR'
ORD_DCL = 'DCL'
ORD_APR = 'APR'
ORD_STR = 'STR'
ORD_FIN = 'FIN'
ORD_ACC = 'ACC'
ORD_BIL = 'BIL'
ORD_PAY = 'PAY'
ORD_CLO = 'CLO'

DEF_ORD_STA = ORD_REQ

ORD_STAS = (
    (ORD_REQ, 'İstendi'),
    (ORD_RJT, 'Reddedildi'),
    (ORD_ASN, 'Atandı'),
    (ORD_EXA, 'İncelendi'),
    (ORD_QTD, 'Önerildi'),
    (ORD_DFR, 'Ertelendi'),
    (ORD_DCL, 'Vazgeçildi'),
    (ORD_APR, 'Onaylandı'),
    (ORD_STR, 'Başlandı'),
    (ORD_FIN, 'Tamamlandı'),
    (ORD_ACC, 'Kabul Edildi'),
    (ORD_BIL, 'Faturalandı'),
    (ORD_PAY, 'Ödendi'),
    (ORD_CLO, 'Kapandı'),
)

ALL_ORD_STAS = ((ORD_STA_ALL,ORD_STA_ALL_TXT),)

for sta in ORD_STAS:
    ALL_ORD_STAS += ((sta[0], sta[1]),)

RDRS_PAG_NO = 1
AUTS_PAG_NO = 1
DNRS_PAG_NO = 1
PRDS_PAG_NO = 1
BRWS_PAG_NO = 1
EVTS_PAG_NO = 1
PRTS_PAG_NO = 1
EMPS_PAG_NO = 1
ODRS_PAG_NO = 1

PRMS =  {
    'RCD_PER_PAG' : RCD_PER_PAG,

    'EMP_MEMBER' : EMP_MEMBER,

    'AUT_GST' : AUT_GST,
    'AUT_USR' : AUT_USR,
    'AUT_SUP' : AUT_SUP,
    'AUT_MGR' : AUT_MGR,

    'DEF_AUT_LVL' : DEF_AUT_LVL,

    'AUT_LVLS' : AUT_LVLS,

    'DEF_EMP' : DEF_EMP,

    'SRT_NAM' : SRT_NAM,
    'SRT_AUT' : SRT_AUT,
    'SRT_TPC' : SRT_TPC,
    'SRT_PRD' : SRT_PRD,
    'SRT_LAN' : SRT_LAN,
    'SRT_RID' : SRT_RID,

    'DEF_SRT' : DEF_SRT,

    'SRTS' : SRTS,

    'BRW_SRT_REV' : BRW_SRT_REV,
    'BRW_SRT_FWD' : BRW_SRT_FWD,

    'BRW_DEF_SRT' : BRW_DEF_SRT,

    'BRW_SRTS' : BRW_SRTS,

    'BRW_DEF_BWR' : BRW_DEF_BWR,
    'BRW_DEF_STR_DAT' : BRW_DEF_STR_DAT,
    'BRW_DEF_END_DAT' : BRW_DEF_END_DAT,

    'ORD_STA_ALL' : ORD_STA_ALL,
    'ORD_REQ' : ORD_REQ,
    'ORD_RJT' : ORD_RJT,
    'ORD_ASN' : ORD_ASN,
    'ORD_EXA' : ORD_EXA,
    'ORD_QTD' : ORD_QTD,
    'ORD_DFR' : ORD_DFR,
    'ORD_DCL' : ORD_DCL,
    'ORD_APR' : ORD_APR,
    'ORD_STR' : ORD_STR,
    'ORD_FIN' : ORD_FIN,
    'ORD_ACC' : ORD_ACC,
    'ORD_BIL' : ORD_BIL,
    'ORD_PAY' : ORD_PAY,
    'ORD_CLO' : ORD_CLO,

    'DEF_ORD_STA' : DEF_ORD_STA,

    'ORD_STAS' : ORD_STAS,
    'ALL_ORD_STAS' : ALL_ORD_STAS,

    'RDRS_PAG_NO' : RDRS_PAG_NO,
    'AUTS_PAG_NO' : AUTS_PAG_NO,
    'DNRS_PAG_NO' : DNRS_PAG_NO,
    'PRDS_PAG_NO' : PRDS_PAG_NO,
    'BRWS_PAG_NO' : BRWS_PAG_NO,
    'EVTS_PAG_NO' : EVTS_PAG_NO,
    'PRTS_PAG_NO' : PRTS_PAG_NO,
    'EMPS_PAG_NO' : EMPS_PAG_NO,
    'ODRS_PAG_NO' : ODRS_PAG_NO,
    }
