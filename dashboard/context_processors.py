def display_name(request):
    user = request.user
    if user.is_authenticated:
        display_name = user.username
        social_accounts = getattr(user, 'socialaccount_set', None)
        if social_accounts:
            accounts = social_accounts.all()
            if accounts:
                display_name = accounts[0].extra_data.get('given_name', user.username)
        return {'display_name': display_name}
    return {}
       