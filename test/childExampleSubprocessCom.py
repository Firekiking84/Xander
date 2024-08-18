import sys
import json

# Lecture des données envoyées depuis le script principal via stdin
input_data = sys.stdin.read()

# Reconstruction du dictionnaire à partir de la chaîne JSON
received_dict = json.loads(input_data)

# Traitement des données (par exemple, création d'une chaîne à partir du dictionnaire)
output_data = f"Received name: {received_dict['name']}, Age: {received_dict['age']}, City: {received_dict['city']}"

# Envoi de la réponse au script principal via stdout
sys.stdout.write(output_data)
