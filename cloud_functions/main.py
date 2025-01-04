# main.py (in cloud_functions)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import jsonify

# Initialisiere Firebase Admin SDK
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': 'aiprompt-openlibrary',
    'storageBucket': 'aiprompt-openlibrary.appspot.com'  # Optional: Falls du Cloud Storage verwendest
})
db = firestore.client()

def getFolders(request):
    """
    Ruft alle Ordner eines Benutzers ab.

    Args:
        request (flask.Request): Die HTTP-Anfrage. Muss einen gültigen Firebase-Authentifizierungs-Token im Authorization-Header enthalten.

    Returns:
        flask.Response: Eine HTTP-Antwort mit den Ordnerdaten im JSON-Format.
    """
    try:
        # Authentifizierung prüfen (hier vereinfacht, in der Praxis muss der Token validiert werden)
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Unauthorized'}), 401

        # Extrahiere die User-ID aus dem Token (Annahme: Der Token enthält die User-ID im Feld 'user_id')
        # In der Praxis würdest du den Token mit firebase_admin.auth.verify_id_token() validieren
        user_id = auth_header.split(' ')[1]

        # Alle Ordner des Benutzers abrufen
        folders_ref = db.collection('folders')
        query = folders_ref.where('userId', '==', user_id).order_by('createdAt')
        folders = query.stream()

        # Ordnerdaten in ein JSON-Array konvertieren
        folders_list = []
        for folder in folders:
            folder_data = folder.to_dict()
            folder_data['id'] = folder.id
            folders_list.append(folder_data)

        # Antwort zurückgeben
        return jsonify(folders_list), 200

    except Exception as e:
        print(f"Error in getFolders: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500