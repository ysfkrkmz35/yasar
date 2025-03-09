from django.core.validators import RegexValidator
from django.utils.translation import gettext as _

# All validators in the system

author_name_validator = \
    [RegexValidator(regex = r'^[a-zA-ZÇçĞğİıÖöŞşÜü]{1}[ +-_.\'a-zA-ZÇçĞğİıÖöŞşÜü]{0,63}$',
                    message = _('Lütfen geçerli bir yazar adı girin.'),
                    code = 'invalid_author_name'),]

product_name_validator = \
    [RegexValidator(regex = r'^[0-9.\"\'a-zA-ZÇçĞğİıÖöŞşÜü]{1}[ +-_0-9.\"\'()a-zA-ZÇçĞğİıÖöŞşÜü]{0,63}$',
                    message = _('Lütfen geçerli bir eser adı girin.'),
                    code = 'invalid_artwork_name'),]

phone_country_validator = \
    [RegexValidator(regex = r'^[1-9]{1}[\d]{0,2}$',
                    message = _('Lütfen en çok üç basamaklı (geçerli) bir ülke kodu girin.'),
                    code = 'invalid_country_code'),]

phone_part2_validator = \
    [RegexValidator(regex = r'^[\d]{3}$',
                    message = _('Lütfen üc basamaklı bir sayı girin.'),
                    code = 'invalid_phone_part2'),]

phone_part4_validator = \
    [RegexValidator(regex = r'^[\d]{4}$',
                    message = _('Lütfen dört basamaklı bir sayı girin.'),
                    code = 'invalid_phone_part4'),]

residence_validator = \
    [RegexValidator(regex = r'^(([1-9]{1})|([1-8]{1}[0-8]{1})|((([8]{1}[9]{1})|([9]{1}[0-2]{1}))-(([0-9]{1})|([1]{1}[0-2]{1}))))$',
                    message = _('Lütfen geçerli bir konut numarası girin.'),
                    code = 'invalid_residence_no'),]

