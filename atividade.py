# Sistema Especialista - Diagnóstico de Problemas em Computadores
# Cauã Lionel Xavier Nunes e Gustavo Silva dos Santos

PERGUNTAS = [
    ("liga", "O computador liga (algum sinal de energia)?"),
    ("luzes_acendem", "Alguma luz do gabinete/placa-mãe acende?"),
    ("ventoinhas_giram", "As ventoinhas/coolers giram?"),
    ("emite_bipes", "O computador emite bipes (beep code) na inicialização?"),
    ("tela_liga", "O monitor exibe alguma imagem?"),
    ("sistema_inicia", "O sistema operacional chega a iniciar (carregar até a área de trabalho)?"),
    ("reinicia_sozinho", "O computador reinicia sozinho, sem motivo aparente?"),
    ("superaquecimento", "O gabinete/processador fica muito quente ao toque?"),
    ("tela_azul", "Aparece tela azul (BSOD) ou travamentos frequentes?"),
    ("barulho_estranho", "O HD faz barulhos estranhos (cliques, rangidos)?"),
    ("lentidao_extrema", "O computador está extremamente lento para abrir arquivos/programas?"),
    ("sem_internet", "O computador está sem conexão à internet/rede?"),
    ("luz_rede_acesa", "A luz da placa de rede (ou do cabo de rede) está acesa?"),
]


def perguntar_sim_nao(pergunta):
    while True:
        resposta = input(pergunta + " (s/n/naosei): ").strip().lower()

        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        if resposta in ("naosei", "não sei", "nao sei", "?"):
            return None

        print("Resposta inválida. Digite 's', 'n' ou 'naosei'.")


# Cada regra possui apenas os fatos necessários para o diagnóstico.
REGRAS = [
    {
        "nome": "fonte",
        "requer": ["liga", "luzes_acendem"],
        "condicao": lambda f: f["liga"] is False and f["luzes_acendem"] is False,
        "diagnostico": "Fonte de alimentação com defeito",
        "solucao": "Testar com outra fonte ou multímetro; verificar cabo de força e botão liga/desliga.",
        "prioridade": 3,
    },
    {
        "nome": "placa_mae",
        "requer": ["liga", "luzes_acendem"],
        "condicao": lambda f: f["liga"] is False and f["luzes_acendem"] is True,
        "diagnostico": "Possível defeito na placa-mãe",
        "solucao": "Verificar curtos-circuitos, capacitores estufados e reassentar os componentes (RAM e cabos).",
        "prioridade": 2,
    },
    {
        "nome": "coolers",
        "requer": ["ventoinhas_giram"],
        "condicao": lambda f: f["ventoinhas_giram"] is False,
        "diagnostico": "Falha nas ventoinhas/coolers",
        "solucao": "Verificar conexões e substituir as ventoinhas com defeito.",
        "prioridade": 2,
    },
    {
        "nome": "fonte_ou_coolers",
        "requer": ["liga", "ventoinhas_giram", "superaquecimento"],
        "condicao": lambda f: (
            f["liga"] is True
            and f["ventoinhas_giram"] is False
            and f["superaquecimento"] is False
        ),
        "diagnostico": "Falha na fonte ou nos coolers",
        "solucao": "Verificar conexões das ventoinhas e a capacidade/estado da fonte.",
        "prioridade": 2,
    },
    {
        "nome": "memoria_ram",
        "requer": ["emite_bipes"],
        "condicao": lambda f: f["emite_bipes"] is True,
        "diagnostico": "Problema na memória RAM",
        "solucao": "Reencaixar ou trocar os módulos de RAM; testar um pente por vez.",
        "prioridade": 3,
    },
    {
        "nome": "placa_video",
        "requer": ["liga", "emite_bipes", "tela_liga"],
        "condicao": lambda f: (
            f["liga"] is True
            and f["emite_bipes"] is False
            and f["tela_liga"] is False
        ),
        "diagnostico": "Problema na placa de vídeo ou no monitor",
        "solucao": "Testar outro monitor/cabo de vídeo; reencaixar a placa de vídeo.",
        "prioridade": 2,
    },
    {
        "nome": "disco_boot",
        "requer": ["tela_liga", "sistema_inicia"],
        "condicao": lambda f: (
            f["tela_liga"] is True and f["sistema_inicia"] is False
        ),
        "diagnostico": "Problema no HD/SSD ou corrupção do sistema de boot",
        "solucao": "Verificar o disco com uma ferramenta de diagnóstico e a ordem de boot na BIOS/UEFI.",
        "prioridade": 3,
    },
    {
        "nome": "superaquecimento",
        "requer": ["superaquecimento"],
        "condicao": lambda f: f["superaquecimento"] is True,
        "diagnostico": "Superaquecimento / falha na refrigeração",
        "solucao": "Limpar o gabinete, trocar a pasta térmica e verificar o funcionamento dos coolers.",
        "prioridade": 3,
    },
    {
        "nome": "reinicio",
        "requer": ["reinicia_sozinho"],
        "condicao": lambda f: f["reinicia_sozinho"] is True,
        "diagnostico": "Computador reiniciando sozinho",
        "solucao": "Verificar temperatura, memória RAM, fonte e possíveis falhas no sistema.",
        "prioridade": 2,
    },
    {
        "nome": "ram_ou_fonte_instavel",
        "requer": ["reinicia_sozinho", "superaquecimento"],
        "condicao": lambda f: (
            f["reinicia_sozinho"] is True
            and f["superaquecimento"] is False
        ),
        "diagnostico": "Possível instabilidade na memória RAM ou na fonte",
        "solucao": "Rodar um teste de memória (memtest) e verificar a tensão da fonte.",
        "prioridade": 2,
    },
    {
        "nome": "sistema_operacional",
        "requer": ["tela_azul"],
        "condicao": lambda f: f["tela_azul"] is True,
        "diagnostico": "Problema no sistema operacional ou em drivers",
        "solucao": "Atualizar/reinstalar drivers; verificar logs de erro e considerar reinstalar o sistema.",
        "prioridade": 2,
    },
    {
        "nome": "disco_mecanico",
        "requer": ["barulho_estranho", "lentidao_extrema"],
        "condicao": lambda f: (
            f["barulho_estranho"] is True and f["lentidao_extrema"] is True
        ),
        "diagnostico": "Falha mecânica no HD",
        "solucao": "Fazer backup imediato dos dados e substituir o disco o quanto antes.",
        "prioridade": 3,
    },
    {
        "nome": "lentidao",
        "requer": ["lentidao_extrema"],
        "condicao": lambda f: f["lentidao_extrema"] is True,
        "diagnostico": "Computador com desempenho muito baixo",
        "solucao": "Verificar uso de CPU, memória e disco e identificar programas que estão consumindo muitos recursos.",
        "prioridade": 1,
    },
    {
        "nome": "rede_hardware",
        "requer": ["sem_internet", "luz_rede_acesa"],
        "condicao": lambda f: (
            f["sem_internet"] is True and f["luz_rede_acesa"] is False
        ),
        "diagnostico": "Problema físico na placa de rede ou no cabo",
        "solucao": "Testar outro cabo de rede e, se possível, outra placa de rede.",
        "prioridade": 2,
    },
    {
        "nome": "rede_software",
        "requer": ["sem_internet", "luz_rede_acesa"],
        "condicao": lambda f: (
            f["sem_internet"] is True and f["luz_rede_acesa"] is True
        ),
        "diagnostico": "Problema de configuração de rede (software)",
        "solucao": "Verificar IP/DNS, reiniciar o roteador e checar configurações de rede do sistema.",
        "prioridade": 2,
    },
]


def regra_pode_ser_avaliada(regra, fatos):
    return all(chave in fatos and fatos[chave] is not None for chave in regra["requer"])


def main():
    print("=== SISTEMA ESPECIALISTA: Diagnóstico de Problemas em Computadores ===\n")

    fatos = {}
    encontrados = set()
    resultados = []

    for chave, pergunta in PERGUNTAS:
        fatos[chave] = perguntar_sim_nao(pergunta)

        for regra in REGRAS:
            if regra["nome"] in encontrados:
                continue

            if regra_pode_ser_avaliada(regra, fatos) and regra["condicao"](fatos):
                encontrados.add(regra["nome"])
                resultados.append((
                    regra["diagnostico"],
                    regra["solucao"],
                    regra["prioridade"]
                ))

                print(f"\n>> Possível causa identificada: {regra['diagnostico']}")
                print(f"   Solução sugerida: {regra['solucao']}\n")

    print("\n--- RESUMO DO DIAGNÓSTICO ---")

    if not resultados:
        print("Não há regras que se encaixem nos sintomas informados.")
        return

    resultados.sort(key=lambda r: r[2], reverse=True)

    print(f"Foram identificadas {len(resultados)} causas possíveis.\n")

    for diagnostico, solucao, _ in resultados:
        print(f"- {diagnostico}")
        print(f"  Solução: {solucao}")


if __name__ == "__main__":
    main()