# sdrpanel

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0f5086f247974a8f98c9a590905b23b4)](https://app.codacy.com/app/xkill/sdrpanel?utm_source=github.com&utm_medium=referral&utm_content=SambaDaRua/sdrpanel&utm_campaign=Badge_Grade_Settings)

Panel de gestión de actuaciones, pensado para blocos samberos.

# Devel running

1. Run

```bash
pip install django
./manage.py migrate
./manage.py collectstatic
./manage.py createsuperuser
./manage.py runserver
```

2. Open http://127.0.0.1:8000
