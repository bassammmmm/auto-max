def user_listing_path(instance, filename):
    return f'users/user_{instance.seller.user.username} ({instance.seller.user.id})/listings/{filename}'