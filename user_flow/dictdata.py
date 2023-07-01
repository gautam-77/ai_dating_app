def textreplay(text):
    data = {"What's up?":"I am good","Hey!":"hyyy","Send":"just a wait","I chat":"Sure"}
    x = data[text] 
    return x 


from .models import CustomToken

def generate_custom_token(user):
    token = CustomToken(user=user)
    token.save()
    print("-=-===--=-=0=-=")
    return token.key