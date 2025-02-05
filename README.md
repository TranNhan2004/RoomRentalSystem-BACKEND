## 1. INSTALL THE VENV
```bash
python3.10 -m venv venv
```

## 2. ACTIVATE AND DEACTIVATE THE VENV
```bash
# activate
venv/Scripts/activate

# deactivate
deactivate
```

## 3. INSTALL THE DEPENDENCIES AND PACKAGES
```bash
pip install -r requirements.txt
```

## 4. MAKE MIGRATIONS AND MIGRATE
```bash
python manage.py makemigrations
python manage.py migrate
``` 

## 5. RUN THE SERVER
```bash
python manage.py runserver
```