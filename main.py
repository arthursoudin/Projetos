from flask import Flask, render_template, request, send_file
from datetime import date

# Importando o dicionário e a função geradora de outros arquivos
from produtos import produtos_cadastrados
from relatorio import gerar_relatorio

# 1. ESTA LINHA É OBRIGATÓRIA E DEVE FICAR AQUI:
app = Flask(__name__)

@app.route("/")
def hub():
    return render_template("hub.html")

@app.route("/relatorio-avaria")
def relatorio_avaria():
    return render_template("avaria.html") 

@app.route("/gerar-relatorio", methods=["POST"])
def gerar():
    ordem = request.form["ordem"]
    redespacho = request.form["redespacho"]
    operador = request.form["operador"]
    motorista = request.form["motorista"]
    transportadora = request.form["transportadora"]
    placa = request.form["placa"]
    cpf = request.form["cpf"]

    quantidades = request.form.getlist("quantidade[]")
    codigos = request.form.getlist("codigo[]")
    motivos = request.form.getlist("motivo[]")
    notas_fiscais = request.form.getlist("nota_fiscal[]")

    produtos = [
        ["QUANTIDADE", "PRODUTO", "MOTIVO", "NOTA FISCAL"]
    ]

    for i in range(len(codigos)):
        cod = codigos[i]
        
        if cod in produtos_cadastrados:
            nome_produto = produtos_cadastrados[cod]
        else:
            nome_produto = f"Cód. não encontrado ({cod})"
            
        produtos.append([quantidades[i], nome_produto, motivos[i], notas_fiscais[i]])

    arquivo = gerar_relatorio(
        redespacho=redespacho,
        ordem_carga=ordem,
        data=date.today(),
        operador=operador,
        motorista=motorista,
        transportadora=transportadora,
        placa=placa,
        cpf=cpf,
        produtos=produtos
    )

    return send_file(
        arquivo,
        as_attachment=True,
        download_name=f"relatorio_avaria_{ordem}.pdf"
    )


# 3. O arranque do servidor fica sempre no final
if __name__ == "__main__":
    print("SERVIDOR INICIANDO...")
    app.run(debug=True)