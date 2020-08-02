from importlib import import_module

from backend.models import UserConnection


def get_activities(user_id, all_time=False):
    connections = UserConnection.objects.filter(user_id=user_id)
    for user_connection in connections:
        connection = user_connection.connection
        module = import_module(connection.library)
        Lib = getattr(module, connection.class_str)
        connect = Lib()
        connect.get_data(user_connection.id, all_time)
