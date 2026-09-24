
import pandas as pd

produtos_cadastrados = {
    "001": "Doce de leite",
    "002": "Paçoca",
    "003": "Queijo Minas",
    "004": "Goiabada",
}

def atualizar_produtos_via_excel(arquivo_excel):
    global produtos_cadastrados
    try:
        df = pd.read_excel(arquivo_excel, dtype=str)
        novo_dicionario = {}
        
        for index, row in df.iterrows():
            codigo = str(row.iloc[0]).strip()
            nome = str(row.iloc[1]).strip()
            
            # Ignora linhas em branco
            if codigo.lower() != 'nan' and nome.lower() != 'nan':
                novo_dicionario[codigo] = nome
        
        # Atualiza a lista do sistema
        produtos_cadastrados.clear()
        produtos_cadastrados.update(novo_dicionario)
        
        return True, f"Sucesso! {len(novo_dicionario)} produtos foram carregados."
    
    except Exception as e:
        return False, f"Erro ao ler a planilha: Verifique se ela tem 2 colunas."