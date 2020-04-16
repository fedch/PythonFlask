from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    # Check is user is not None AND check if the password matches the one stored = is correct:
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
