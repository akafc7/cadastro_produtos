from reportlab.pdfgen import canvas
import mysql.connector
from PyQt5 import QtWidgets, uic

banco = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='cadastro_produtos'
)


def salvar_produtos():
    global numero_id
    cod = editar_produtos.lineEdit_2.text()
    desc = editar_produtos.lineEdit_3.text()
    preço = editar_produtos.lineEdit_4.text()
    cat = editar_produtos.lineEdit_5.text()
    cursor = banco.cursor()
    comando_SQL = f"UPDATE produtos SET codigo = '{cod}', descrição = '{desc}', preço = '{preço}', categoria = '{cat}' WHERE id='{numero_id}'"
    cursor.execute(comando_SQL)
    editar_produtos.close()
    lista_produtos.close()
    chama_lista_produtos()


def menu_editar():
    global numero_id

    editar_produtos.show()
    linha = lista_produtos.tableWidget.currentRow()
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute(f"SELECT * FROM produtos WHERE id=" + str(valor_id))
    produto = cursor.fetchall()
    editar_produtos.lineEdit.setText(str(produto[0][0]))
    editar_produtos.lineEdit_2.setText(str(produto[0][1]))
    editar_produtos.lineEdit_3.setText(str(produto[0][2]))
    editar_produtos.lineEdit_4.setText(str(produto[0][3]))
    editar_produtos.lineEdit_5.setText(str(produto[0][4]))
    numero_id = valor_id


def excluir_produtos():
    linha = lista_produtos.tableWidget.currentRow()
    lista_produtos.tableWidget.removeRow(linha)
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute(f"DELETE FROM produtos WHERE id={valor_id}")
    banco.commit()
    print(valor_id)


def gerar_pdf():
    cursor = banco.cursor()
    comando_SQL = 'SELECT * FROM produtos'
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Produtos Cadastrados")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(10, 750, "ID")
    pdf.drawString(110, 750, "CÓDIGO")
    pdf.drawString(210, 750, "PRODUTO")
    pdf.drawString(310, 750, "PREÇO")
    pdf.drawString(410, 750, "CATEGORIA")

    for i in range(0, len(dados_lidos)):
        y += 50
        pdf.drawString(10, 750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110, 750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210, 750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310, 750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410, 750 - y, str(dados_lidos[i][4]))

    pdf.save()
    print("PDF GERADO.")


def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()

    categoria = ""

    if formulario.checkBox.isChecked():
        print("Categoria: Informática")
        categoria = "Informática"
    elif formulario.checkBox_2.isChecked():
        print('Categoria: Alimentos')
        categoria = "Alimentos"
    else:
        print("Categoria: Eletrodomésticos")
        categoria = "Eletrodomésticos"

    print(f"Código: {linha1}")
    print(f"Descrição: {linha2}")
    print(f"Preço: {linha3}")

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo, descrição, preço, categoria) VALUES (%s, %s, %s, %s)"
    dados = (str(linha1), str(linha2), str(linha3), categoria)
    cursor.execute(comando_SQL, dados)
    banco.commit()
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")


def chama_lista_produtos():
    lista_produtos.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    lista_produtos.tableWidget.setRowCount(len(dados_lidos))
    lista_produtos.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            lista_produtos.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


app = QtWidgets.QApplication([])
formulario = uic.loadUi("formulario.ui")
lista_produtos = uic.loadUi("lista_produtos.ui")
editar_produtos = uic.loadUi("editar_produtos.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chama_lista_produtos)
lista_produtos.pushButton.clicked.connect(gerar_pdf)
lista_produtos.pushButton_2.clicked.connect(excluir_produtos)
lista_produtos.pushButton_3.clicked.connect(menu_editar)
editar_produtos.pushButton.clicked.connect(salvar_produtos)

formulario.show()
app.exec()
