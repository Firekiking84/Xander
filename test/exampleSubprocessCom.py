import subprocess
import json

# Le script à exécuter
script_to_run = 'childExampleSubprocessCom.py'

# Commande pour exécuter le script avec Python
command = ['python3', script_to_run]

# Dictionnaire à envoyer
my_dict = {
    'name': 'Alice',
    'age': 30,
    'city': 'Paris'
}

# Conversion du dictionnaire en JSON
input_data = json.dumps(my_dict)

# Exécution du script enfant avec subprocess.run() et communication via PIPE
result = subprocess.run(command, input=input_data, capture_output=True, text=True)

# Vérification du retour de l'exécution
if result.returncode == 0:
    print("Output from child script:")
    print(result.stdout)
else:
    print("An error occurred:")
    print(result.stderr)
