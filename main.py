from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import os
import re
 
porta = int(os.environ.get("PORT", 5000))
app = Flask(__name__)
CORS(app)  # libera acesso de qualquer origem (ajuste com origins=[...] se quiser restringir)
 
NOME_DA_IA = "RuleAI"
 
# Palavras banidas checadas por PALAVRA INTEIRA (evita falso positivo tipo "cu" em "cultura")
PALAVRAS_PROIBIDAS = ["cu", "xoxota", "xereca", "roubar", "bunda"]
 
 
def contem_palavra_proibida(frase):
    for palavra in PALAVRAS_PROIBIDAS:
        if re.search(r"\b" + re.escape(palavra) + r"\b", frase):
            return True
    return False
 
 
def GerarTotal(frase, emocao):
    frasesFeliz = ["Claro! Vamos nessa.", "Mandou bem! Bora lá.", "Opa! Bora nessa?"]
    frasesRaiva = ["Certo.", "Entendi.", "Entendido."]
 
    if emocao == "feliz":
        fraseCool = random.choice(frasesFeliz)
        return fraseCool + " " + frase + "."
    elif emocao == "raiva":
        escolhida = random.choice(frasesRaiva)
        return escolhida + " " + frase + "."
    else:
        # Fallback para nunca retornar None
        return frase + "."
 
 
def GerarFraseInicial(emocao, nomeDaIA):
    frasesFeliz = [
        "Olá! Eu sou a (NOME) IA, sua nova IA baseada em regras. Em que posso te ajudar hoje?",
        "Olá! Meu nome é (NOME), a sua nova IA baseada em regras. O que você procura?",
        "Olá! Sou a (NOME), em que posso te ajudar hoje?",
        "Oi! Sou a (NOME), tô aqui pra ajudar. O que você precisa?",
        "E aí! Sou a (NOME), sua IA baseada em regras. Qual é a boa?",
        "Salve! Sou a (NOME). Me conta o que você tá procurando!",
        "Opa, tudo certo? Sou a (NOME), em que posso ser útil hoje?",
        "Oi! Eu sou a (NOME), pronta pra ajudar. O que manda?",
        "Fala aí! Sou a (NOME), sua IA de regras. No que posso ajudar?",
        "Olá, tudo bem? Sou a (NOME). Diz aí o que você precisa!"
    ]
 
    frasesRAIVA = [
        "Olá, eu sou a (NOME). Para que eu possa te ajudar, me diga o que você está procurando.",
        "Ok, sem estresse. Em que posso ajudar?",
        "Entendi, vou direto ao ponto. O que você precisa?",
        "Certo, sem enrolação. Me diz o que você quer.",
        "Beleza, vamos ser rápidos. Qual é a demanda?",
        "Ok. Sem rodeios — em que posso ajudar?",
        "Certo, sem mais delongas. O que você precisa?",
        "Beleza, direto ao assunto. Qual é a sua?",
        "Ok, sem enrolar. Manda o que você quer.",
        "Entendido, vamos logo. Do que você precisa?",
        "Sem problema, sem demora. O que manda?",
        "Certo. Já vamos nessa. O que você quer resolver?"
    ]
 
    if emocao == "feliz":
        return random.choice(frasesFeliz).replace("(NOME)", nomeDaIA)
    elif emocao == "raiva":
        return random.choice(frasesRAIVA).replace("(NOME)", nomeDaIA)
    else:
        return f"Olá, eu sou a {nomeDaIA}. Em que posso te ajudar hoje?"
 
 
def GerarFrase(prompt):
    frase = prompt.lower()
    for caractere in ["!", "?", ".", ",", ";", ":", "[", "]", "{", "}", "%", "$"]:
        frase = frase.replace(caractere, "")
 
    # Checagem de conteúdo proibido ANTES de qualquer outra lógica -> retorno imediato
    if contem_palavra_proibida(frase):
        return "Sou apenas uma Inteligência Artificial baseada em regras e não posso ajudar com isso."
 
    lista = []
    saudacoes = [
        "oi", "olá", "oii", "e aí", "eae", "eaew", "fala",
        "bom dia", "boa tarde", "boa noite", "tudo bem", "tudo bom",
        "como vai", "como você está",
        "salve", "salve salve", "opa", "e aí, tudo certo", "suave",
        "de boa", "tranquilo", "na paz", "tudo joia", "tudo tranquilo",
        "blz", "beleza",
        "oxente", "bah", "égua", "uai", "visse", "simbora",
        "mano", "cara", "véi", "parceiro", "brother", "mano véio",
        "bróder", "truta", "chapa", "parça",
        "coé", "e ae mano", "fala aê", "iae", "e aí, beleza",
        "fmz", "firmeza", "tudo firmeza",
        "eai", "e ai", "eaí", "iai", "koe", "ola",
        "prezado", "prezada", "caro", "cara senhora", "bom te ver",
        "boa te encontrar", "seja bem vindo", "seja bem vinda",
        "posso te perguntar", "gostaria de saber", "queria saber",
        "me tira uma dúvida", "cadê você", "kd voce", "kd vc",
        "sextou", "partiu", "bora", "borah", "vamo que vamo",
        "fmz mano", "suave na nave", "de boa contigo",
        "e aí parceiro", "diacho", "arre", "bah tchê", "tchê",
        "oxe", "vixe", "eita", "égua doido",
        "bom dia pessoal", "boa tarde galera", "boa noite pessoal",
        "quanto tempo", "há quanto tempo", "sumido", "sumida",
        "voltei", "cheguei"
    ]
 
    if any(palavra in frase for palavra in saudacoes):
        lista.append("alegre")
 
    if "vai logo" in frase or "chato" in frase or "lento" in frase or "pressa" in frase:
        lista.append("raiva")
 
    if "rpg" in frase:
        lista.append("rpg")
 
    if "jogo" in frase:
        lista.append("jogo")
 
    if "aventura" in frase:
        lista.append("aventura")
 
    if "criar" in frase or "crie" in frase or "cria" in frase:
        lista.append("criar")
 
    gerado = ""
    noPrompt = []
    if "criar" in lista:
        noPrompt.append("criar")
        gerado = "Vou criar"
 
    if "jogo" in lista:
        noPrompt.append("jogo")
        if "criar" in noPrompt:
            gerado = gerado + " um jogo"
        else:
            gerado = "Um jogo"
 
    if "rpg" in lista:
        noPrompt.append("rpg")
        gerado = gerado + " de RPG"
 
    if "aventura" in lista:
        noPrompt.append("aventura")
        if "rpg" in noPrompt:
            gerado = gerado + "/aventura"
        else:
            gerado = gerado + " de aventura"
 
    fraseComEmocao = ""
    jaTemEmocao = False
 
    if lista == []:
        jaTemEmocao = True
        fraseComEmocao = "Desculpe, não entendi sua pergunta."
 
    if "alegre" in lista and not jaTemEmocao:
        jaTemEmocao = True
        fraseComEmocao = GerarTotal(gerado, "feliz")
 
    if "raiva" in lista and not jaTemEmocao:
        jaTemEmocao = True
        fraseComEmocao = GerarTotal(gerado, "raiva")
 
    if not jaTemEmocao:
        fraseComEmocao = gerado
 
    if lista == ["alegre"]:
        fraseComEmocao = GerarFraseInicial("feliz", NOME_DA_IA)
 
    if lista == ["raiva"]:
        fraseComEmocao = GerarFraseInicial("raiva", NOME_DA_IA)
 
    return fraseComEmocao
 
 
@app.route("/gerar", methods=["POST"])
def gerar():
    try:
        data = request.get_json(silent=True) or {}
        prompt = data.get("prompt", "")
 
        if not isinstance(prompt, str) or prompt.strip() == "":
            return jsonify({"erro": "prompt vazio"}), 400
 
        resposta = GerarFrase(prompt)
        return jsonify({"resposta": resposta})
    except Exception as e:
        return jsonify({"erro": "erro interno", "detalhes": str(e)}), 500
 
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=porta)
 
