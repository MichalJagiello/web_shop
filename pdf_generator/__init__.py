import pdfkit


def generate(html):
    return pdfkit.from_string(html, False, options={'encoding': "UTF-8"})