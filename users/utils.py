def user_directory_path(instance, filename):
    return f'users/user_{instance.user.username} ({instance.user.id})/{filename}'