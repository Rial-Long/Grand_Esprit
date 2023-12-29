from macro import CHANNEL_INCANTATION, CHANNEL_TEST

def is_channel(message):  # Permet de vérifier si le message a été écrit dans le salon test ou incantation
    if message.channel.id == CHANNEL_INCANTATION or message.channel.id == CHANNEL_TEST:
        return True
    else:
        return False
