from django import forms
from actuaciones.models import samberos
from django.contrib.auth import authenticate


class samberoForm(forms.ModelForm):
    oldpassword = forms.CharField(max_length=20,
                                  required=False,
                                  label='Contraseña anterior',
                                  widget=forms.TextInput(attrs={'type': 'password'}),
                                  help_text='''Escribe tu contraseña y la contraseña nueva para cambiar la contraseña.
                                  <br/>Deja los campos de contraseña en blanco para no cambiar la contraseña.'''
                                  )
    newpassword1 = forms.CharField(max_length=20,
                                   required=False,
                                   label='Contraseña Nueva',
                                   widget=forms.TextInput(attrs={'type': 'password'})
                                   )
    newpassword2 = forms.CharField(max_length=20,
                                   required=False,
                                   label='Repetir Contraseña Nueva',
                                   widget=forms.TextInput(attrs={'type': 'password'})
                                   )
    username = forms.CharField(disabled=True,
                               label="Nombre de usuario")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        username = None
        if self.request:
            username = self.request.user.username
        oldpassword = self.cleaned_data.get('oldpassword')
        newpassword1 = self.cleaned_data.get('newpassword1')
        newpassword2 = self.cleaned_data.get('newpassword2')
        if newpassword1 != newpassword2:
                self.add_error('newpassword2', forms.ValidationError('Las dos contraseñas nuevas no coinciden.',
                                                                     code='new_passwords_dont_match'))
        elif not newpassword2 and oldpassword:
                self.add_error('newpassword2', forms.ValidationError('La contraseña nueva no puede estar vacía',
                                                                     code='new_passwords_blank'))
        elif newpassword1 and newpassword2 and newpassword1 == newpassword2:
            userauth = authenticate(username=username, password=oldpassword)
            if userauth is None:
                self.add_error('oldpassword', forms.ValidationError('Contraseña incorrecta.', code='wrong_password'))

    class Meta:
        model = samberos
        fields = ['username', 'first_name', 'last_name',
                  'dni', 'phone', 'movil', 'email', 'instrumento',
                  'backstage', 'notification_email',
                  'oldpassword', 'newpassword1', 'newpassword2']


class RemoveDisableAccountForm(forms.Form):
    disable_account = forms.BooleanField(initial=True, label="Desactivar cuenta", required=False,
                                         help_text='''Desactivas la cuenta, pero seguirás contando como que estuviste en
                                         Samba da Rua y las actuaciones, tus datos seguiran en el panel, si quieres
                                         borrar esos datos puedes cambiarlos manualmente antes de desactivar la cuenta,
                                         de esta manera solo quedará tu nombre de usuario (mejor si dejas el email para
                                         que podamos contactar contigo en el futuro, quién sabe si hacemos una mega
                                         quedada sambera). Otra opción es borrar tu cuenta, pero así todos tus datos
                                         serán borrados.''')
    remove_account = forms.BooleanField(label="Borrar cuenta", required=False,
                                        help_text='''Se borrara tu cuenta y todos los datos. ¡¡Una pena, ya no podremos
                                        saber nada de ti, ni las actuaciones en las que estubiste, ni nada... Mejor si
                                        en vez de borrar la cuenta solo la desactivas y si no quieres que Samba da Rua
                                        tenga datos tuyos, pues antes de desactivar la cuenta borra los datos que
                                        quieras.''')
