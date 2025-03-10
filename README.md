# Projet Bot Stat

## Pour commencer le projet

```bash
PYTHONPATH=src python main.py
```

### Créer l'environnement virtuel

```bash
python3 -m venv .venv
```

### Puis Activer l'environnement virtuel

```bash
source .venv/bin/activate
```

```bash
.venv\Scripts\activate.bat
```

### Pour arrêter (ou désactiver) l'environnement virtuel, il te suffit de taper la commande suivante dans ton terminal

```bash
deactivate
```

### Puis il faut install les dependans

```bash
pip install -r requirements.txt
```

### Mettre à jour le fichier `requirements.txt`

```bash
pip freeze > requirements.txt
```

### Formatage du code

```bash
black src/ && isort src/ && blackdoc src/ && pylint src/ && darglint src/
```
