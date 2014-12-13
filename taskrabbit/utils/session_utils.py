def check_session(request):
    if(request.session.get("user_id")):
        return True
    else:
        return False