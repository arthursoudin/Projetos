from flask import Flask, render_template, request, send_file, redirect, url_for, flash, jsonify
from datetime import date

from produtos import produtos_cadastrados, atualizar_produtos_via_excel
from relatorio import gerar_relatorio

app = Flask(__name__)
# Chave secreta necessária para enviar mensagens (flash) do Python para o HTML
app.secret_key = "chave_super_secreta_avaria" 

# --- ROTAS DE PÁGINAS ---
@app.route("/")
def hub():
    return render_template("hub.html")

@app.route("/relatorio-avaria")
def relatorio_avaria():
    return render_template("avaria.html")


# --- NOVAS ROTAS (SISTEMA V2.5) ---

# 1. Rota para receber o arquivo Excel do Hub
@app.route("/upload-produtos", methods=["POST"])
def upload_produtos():
    if 'arquivo_excel' not in request.files:
        flash("Nenhum arquivo enviado.", "erro")
        return redirect(url_for('hub'))
    
    arquivo = request.files['arquivo_excel']
    if arquivo.filename == '':
        flash("Nenhum arquivo selecionado.", "erro")
        return redirect(url_for('hub'))
        
    if not arquivo.filename.endswith(('.xls', '.xlsx')):
        flash("Formato inválido. Envie um arquivo .xlsx ou .xls", "erro")
        return redirect(url_for('hub'))
        
    sucesso, mensagem = atualizar_produtos_via_excel(arquivo)
    if sucesso:
        flash(mensagem, "sucesso")
    else:
        flash(mensagem, "erro")
        
    return redirect(url_for('hub'))

# 2. Rota invisível que o formulário chama enquanto você digita
@app.route("/api/produto/<codigo>")
def buscar_produto(codigo):
    # Procura no dicionário. Se não achar, retorna "Não encontrado"
    nome = produtos_cadastrados.get(codigo, "Não encontrado")
    return jsonify({"nome": nome})

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