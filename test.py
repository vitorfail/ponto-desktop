import PyPDF2
from reportlab.pdfgen import canvas
from win32 import win32print

def imprimir_arquivo(nome_arquivo, impressora=None):
    if impressora is None:
        impressora = win32print.GetDefaultPrinter()

    # Configurar as propriedades da impressão
    properties = {
        "DesiredAccess": win32print.PRINTER_ALL_ACCESS,
    }

    # Abrir a impressora
    hPrinter = win32print.OpenPrinter(impressora, properties)

    try:
        # Inicializar o objeto de dados de impressão
        hJob = win32print.StartDocPrinter(hPrinter, 1, (nome_arquivo, None, "RAW"))

        try:
            # Iniciar a página de impressão
            win32print.StartPagePrinter(hPrinter)
            
            # Ler o conteúdo do arquivo e enviá-lo para a impressora
            with open(nome_arquivo, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for pagina_num in range(len(pdf_reader.pages)):
                    pagina = pdf_reader.pages[pagina_num]
                    texto_pagina = pagina.extract_text()
                    win32print.WritePrinter(hPrinter, bytes(texto_pagina, 'utf-8'))        
        finally:
            # Finalizar a página de impressão
            win32print.EndPagePrinter(hPrinter)

            # Finalizar o trabalho de impressão
            win32print.EndDocPrinter(hPrinter)
            print("Impressão concluída com sucesso.")
    except Exception as e:
        print(f"Erro ao imprimir: {e}")
    finally:
        # Fechar a impressora
        win32print.ClosePrinter(hPrinter)
imprimir_arquivo("TEXTE.pdf")
def criar_pdf_cupom(nome_arquivo, conteudo):
    # Configurar o tamanho da página para um tíquete de cupom padrão
    largura, altura = 200, 200
    c = canvas.Canvas(nome_arquivo, pagesize=(largura, altura))
    espacamento_linhas = 14

    c.setFont("Courier", 12)
    linhas = conteudo.split('\n')
    altura_total = len(linhas) * espacamento_linhas

    # Calcular a posição central na página
    y_posicao_central = 180

    # Adicionar as linhas ao PDF com quebra de linha e centralizando
    for linha in linhas:
        largura_texto = c.stringWidth(linha, "Courier", 12)
        x_posicao_central = (largura - largura_texto) / 2
        c.drawString(x_posicao_central, y_posicao_central, linha)
        y_posicao_central -= espacamento_linhas

    # Salvar o PDF
    c.save()
