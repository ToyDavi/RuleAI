from flask import Flask, request, jsonify
import random
import os

porta = int(os.environ.get("PORT", 5000))
app = Flask(__name__)

NOME_DA_IA = "RuleAI"
def GerarTotal(frase, emocao):
    frasesFeliz = ["Claro! Vamos nessa.", "Mandou bem! Bora lá.", "Opa! Bora nessa?"]
    frasesRaiva = ["Certo.", "Entendi.", "Entendido."]

    if emocao == "feliz":
        fraseCool = random.choice(frasesFeliz)
        fraseTotal = fraseCool + " " + frase + "."
        return fraseTotal
    elif emocao == "raiva":
        fraseRaiva = random.choice(frasesRaiva)
        fraseCu = fraseRaiva + " " + frase + "."
        return fraseCu


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
        fraseF = random.choice(frasesFeliz).replace("(NOME)", nomeDaIA)
        return fraseF
    elif emocao == "raiva":
        fraseR = random.choice(frasesRAIVA).replace("(NOME)", nomeDaIA)
        return fraseR
    else:
        return "Olá, eu sou a (NOME). Em que posso te ajudar hoje?" # Fallback para a IA não crashar caso o programador digite o nome da emoção errado ou uma que não existe.
    

def GerarFrase(prompt):
    frase = prompt.lower()
    print(frase + " <VERSÃO 1>")
    for caractere in ["!", "?", ".", "[", "]", "{", "}", "%", "$"]:
        frase = frase.replace(caractere, "")
    
    print(frase + "<VERSÃO 2>")

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
    # Contrações e variações de escrita
    "eai", "e ai", "eaí", "iai", "koe", "ola",
    
    # Formais / profissionais
    "prezado", "prezada", "caro", "cara senhora", "bom te ver",
    "boa te encontrar", "seja bem vindo", "seja bem vinda",
    
    # Perguntas de abertura comuns
    "posso te perguntar", "gostaria de saber", "queria saber",
    "me tira uma dúvida", "cadê você", "kd voce", "kd vc",
    
    # Internet / abreviações
    "sextou", "partiu", "bora", "borah", "vamo que vamo",
    "fmz mano", "suave na nave", "de boa contigo",
    
    # Regionais adicionais
    "e aí parceiro", "diacho", "arre", "bah tchê", "tchê",
    "oxe", "vixe", "eita", "égua doido",
    
    # Cumprimentos por horário (variações)
    "bom dia pessoal", "boa tarde galera", "boa noite pessoal",
    
    # Expressões de retorno/reencontro
    "quanto tempo", "há quanto tempo", "sumido", "sumida",
    "voltei", "cheguei"
    ]

    if any(palavra in frase for palavra in saudacoes):
        lista.append("alegre")
    
    if "vai logo" in frase or "chato" in frase or "lento" in frase or "pressa" in frase:
        lista.append("raiva")
    if "cu" in frase or "xoxota" in frase or "xereca" in frase or "roubar" in frase or "bunda" in frase:
        lista.append("violação")
    
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
        
        # Aqui eu não coloquei IFS, porque mesmo se for CRIAR ou se for só JOGO, de qualquer jeito seria:
        # "Um jogo de RPG" ou "Vou criar um jogo de RPG"
    
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

    if "alegre" in lista and jaTemEmocao == False:
        jaTemEmocao = True
        fraseComEmocao = GerarTotal(gerado, "feliz")
    
    if "raiva" in lista and jaTemEmocao == False:
        jaTemEmocao = True
        fraseComEmocao = GerarTotal(gerado, "raiva")
    
    if jaTemEmocao == False:
        fraseComEmocao = gerado

    if "violação" in lista:
        fraseComEmocao = "Sou apenas uma Inteligência Artificial baseada em regras e não posso ajudar com isso."
    

    if lista == ["alegre"]:
        fraseComEmocao = GerarFraseInicial("feliz", NOME_DA_IA)
    
    if lista == ["raiva"]:
        fraseComEmocao = GerarFraseInicial("raiva", NOME_DA_IA)
    

    return fraseComEmocao

@app.route("/gerar", methods=["POST"])
def gerar():
    data = request.get_json()
    prompt = data.get("prompt", "")
    
    if prompt.strip() == "":
        return jsonify({"erro": "prompt vazio"}), 400
    
    resposta = GerarFrase(prompt)
    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(port=porta)