# -*- coding: utf-8 -*-

import re
from wtforms import Form, BooleanField, TextField, TextAreaField, validators, ValidationError
from wtfrecaptcha.fields import RecaptchaField

RECAPTCHA_PUB_KEY = ""
RECAPTCHA_PRIV_KEY = ""


def validate_entry(form, field):
    if not re.match(ur"^[a-zA-Z0-9\s_-áéíóúñÁÉÍÓÚÑ]+$", field.data):
        raise ValidationError("Solo letras, numeros y espacios por favor.")


class DefinitionForm(Form):
    captcha = RecaptchaField(
            public_key=RECAPTCHA_PUB_KEY,
            private_key=RECAPTCHA_PRIV_KEY, secure=True
    )

    entry = TextField('Termino*',
                      [validate_entry,
                       validators.Length(
                              message=u'Debe tener entre 3 y 50 caractacteres.',
                              min=3,
                              max=50,)
                      ])

    definition = TextAreaField('Definici&oacute;n*',
                               [validators.Length(
                                   message=u'Debe tener entre 15 y 300 caracteres.',
                                   min=15,
                                   max=300)
                               ])

    example = TextAreaField('Ejemplo (Opcional)',
                            [validators.Length(
                                message=u'No puede tener mas de 300 caracteres',
                                min=0,
                                max=300)
                            ])
