"""
HSE-IT — Health Safety Executive Indicator Tool
35 perguntas, escala Likert:
  1 = Nunca | 2 = Raramente | 3 = Às vezes | 4 = Frequentemente | 5 = Sempre

Dimensões (conforme Anexo 2):
  DEMANDAS        → 03, 06, 09, 12, 16, 18, 20, 22
  CONTROLE        → 02, 10, 15, 19, 25, 30
  APOIO DA CHEFIA → 08, 23, 29, 33, 35
  APOIO DOS COLEGAS → 07, 24, 27, 31
  RELACIONAMENTOS → 05, 14, 21, 34
  CARGO           → 01, 04, 11, 13, 17
  COMUNICAÇÃO E MUDANÇAS → 26, 28, 32
"""

QUESTIONNAIRE_CODE = "HSE-IT"

LIKERT_CHOICES = [
    ("1", "1 – Nunca"),
    ("2", "2 – Raramente"),
    ("3", "3 – Às vezes"),
    ("4", "4 – Frequentemente"),
    ("5", "5 – Sempre"),
]

# Dimensões e os números das perguntas que as compõem
DIMENSIONS = {
    "DEMANDAS":              [3, 6, 9, 12, 16, 18, 20, 22],
    "CONTROLE":              [2, 10, 15, 19, 25, 30],
    "APOIO DA CHEFIA":      [8, 23, 29, 33, 35],
    "APOIO DOS COLEGAS":    [7, 24, 27, 31],
    "RELACIONAMENTOS":       [5, 14, 21, 34],
    "CARGO":                 [1, 4, 11, 13, 17],
    "COMUNICAÇÃO E MUDANÇAS": [26, 28, 32],
}

# Textos das perguntas na mesma ordem do HSE-IT (1–35)
QUESTION_TEXTS = [
    "Tenho clareza sobre o que se espera do meu trabalho.",                                          # 01
    "Posso decidir quando fazer uma pausa.",                                                          # 02
    "As exigências de trabalho feitas por colegas e supervisores são difíceis de combinar.",          # 03
    "Eu sei como fazer o meu trabalho.",                                                             # 04
    "Falam ou se comportam comigo de forma dura.",                                                   # 05
    "Tenho prazos inatingíveis.",                                                                    # 06
    "Quando o trabalho se torna difícil, posso contar com ajuda dos colegas.",                       # 07
    "Recebo informações e suporte que me ajudam no trabalho que eu faço.",                           # 08
    "Devo trabalhar muito intensamente.",                                                            # 09
    "Consideram a minha opinião sobre a velocidade do meu trabalho.",                                # 10
    "Estão claras as minhas tarefas e responsabilidades.",                                           # 11
    "Eu não tenho algumas tarefas porque tenho muita coisa para fazer.",                             # 12
    "Os objetivos e metas do meu setor são claros para mim.",                                       # 13
    "Existem conflitos entre os colegas.",                                                           # 14
    "Tenho liberdade de escolha de como fazer meu trabalho.",                                        # 15
    "Não tenho possibilidade de fazer pausas suficientes.",                                          # 16
    "Eu vejo como o meu trabalho se encaixa nos objetivos da empresa.",                              # 17
    "Recebo pressão para trabalhar em outro horário.",                                               # 18
    "Tenho liberdade de escolha para decidir o que fazer no meu trabalho.",                          # 19
    "Tenho que fazer meu trabalho com muita rapidez.",                                               # 20
    "Sinto que sou perseguido(a) no trabalho.",                                                     # 21
    "As pausas temporárias são impossíveis de cumprir.",                                             # 22
    "Posso confiar no meu chefe quando eu tiver problemas no trabalho.",                             # 23
    "Meus colegas me ajudam e me dão apoio quando eu preciso.",                                      # 24
    "Minhas sugestões são consideradas sobre como fazer meu trabalho.",                              # 25
    "Tenho oportunidades para pedir explicações ao chefe sobre as mudanças relacionadas ao meu trabalho.", # 26
    "No trabalho os meus colegas demonstram o respeito que mereço.",                                 # 27
    "As pessoas são sempre consultadas sobre as mudanças no trabalho.",                              # 28
    "Quando algo no trabalho me perturba ou irrita, posso falar com meu chefe.",                     # 29
    "O meu horário de trabalho pode ser flexível.",                                                  # 30
    "Os colegas estão disponíveis para escutar os meus problemas de trabalho.",                      # 31
    "Quando há mudanças, faço o meu trabalho com o mesmo carinho.",                                  # 32
    "Tenho suportado trabalhos emocionalmente exigentes.",                                           # 33
    "As relações no trabalho são tensas.",                                                           # 34
    "Meu chefe me incentiva no trabalho.",                                                           # 35
]

QUESTION_DEFINITIONS = [
    {
        "number": i + 1,
        "text": QUESTION_TEXTS[i],
        "options": LIKERT_CHOICES,
    }
    for i in range(35)
]
