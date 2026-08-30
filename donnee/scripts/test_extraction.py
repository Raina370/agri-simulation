import pdfplumber

chemin_pdf = "donnee/pdf_source/Fiche Arachide.pdf"

with pdfplumber.open(chemin_pdf) as pdf:
    premiere_page = pdf.pages[0]
    texte = premiere_page.extract_text()
    print(texte)