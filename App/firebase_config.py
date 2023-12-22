import pyrebase

config = {
    "apiKey": "AIzaSyDUcV279efOnxcJq8zfNl3Qu_2YQlHySyw",
    "authDomain": "vista-76841.firebaseapp.com",
    "databaseURL": "https://vista-76841-default-rtdb.firebaseio.com",
    "projectId": "vista-76841",
    "storageBucket": "vista-76841.appspot.com",
    "messagingSenderId": "72376537978",
    "appId": "1:72376537978:web:87c4b50515630f89d6bcc3"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()


def get_user_info_from_firebase(token):
    try:
        # Obtener la información del usuario desde Firebase usando el token
        user_info = auth.get_account_info(token)

        # Devolver la información del usuario
        return user_info

    except Exception as e:
        # Manejar cualquier error que pueda ocurrir al interactuar con Firebase
        print(f"Error al obtener información del usuario de Firebase: {e}")

    # Si no se puede obtener la información, devolver None
    return None
