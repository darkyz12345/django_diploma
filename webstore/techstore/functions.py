from googletrans import Translator


def translate(text, src, dest):
    translator = Translator()
    return translator.translate(text, src=src, dest=dest).text