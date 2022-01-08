from django.utils.translation import gettext_lazy as _


# CSS Classes
INPUT_CLASS = {'class': 'form-input'}
TEXTAREA_CLASS = {'class': 'form-textarea'}
CUSTOM_TEXTAREA_CLASS = {'class': 'form-textarea w-full h-48'}
SELECT_CLASS = {'class': 'form-select'}
RADIO_CLASS = {'class': 'form-radio'}
CHECKBOX_CLASS = {'class': 'form-checkbox'}
HIDDEN_CLASS = {'class': 'form-input hidden'}
INPUT_CLASS_DISABLED = {'class': 'form-input', 'disabled': 'true'}

# Model Constants
GENDER_CHOICES = (
    ("f", _("Female")),
    ("m", _("Male")),
)
HAIR_CHOICES = (
    ('brown', _('brown')),
    ('yellow', _('yellow')),
    ('other', _('other'))
)
EYES_CHOICES = (
    ('brown', _('brown')),
    ('yellow', _('yellow')),
    ('other', _('other'))
)
HEIGHT_CHOICES = (
    ('1.40-1.60', '1.40-1.60'),
    ('1.60-1.80', '1.60-1.80'),
    ('1.80-2.00', '1.80-2.00'),
)
CITY_CHOICES = (('Marrakech', 'Marrakech'), ('Fes', 'Fès'))
COUNTRY_CHOICES = (('Morocco', 'Maroc'), ('France', 'France'))

AGREEMENT_CHOICES = (
    ('y', 'Oui'),
    ('n', 'Non'),
)
