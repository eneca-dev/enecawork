def password_comparison(password: str, password_confirm: str) -> bool:
    if password != password_confirm:
        return False
    return True