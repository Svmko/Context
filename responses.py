from random import choice, randint

def get_reponse(uinput: str) -> str:
    lowered: str = uinput.lower()

    if lowered == '':
        return 'Might wanna try that again :/'
    elif 'hello' in lowered:
        return 'it works!'