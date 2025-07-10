import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

# Tela Fixa 
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("🐍 Cobrinha com Ranking, Obstáculos e Fases")

# Cores 
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

#  Bloco 
TAMANHO_BLOCO = 20
FONTE = pygame.font.SysFont(None, 35)
clock = pygame.time.Clock()

#  Imagens 
imagem_cabeca = pygame.transform.scale(pygame.image.load("cobra.jpg"), (TAMANHO_BLOCO, TAMANHO_BLOCO))
imagem_corpo = pygame.transform.scale(pygame.image.load("cobra_corpo.png"), (TAMANHO_BLOCO, TAMANHO_BLOCO))
imagem_maca = pygame.transform.scale(pygame.image.load("apple.png"), (TAMANHO_BLOCO, TAMANHO_BLOCO))
imagem_maca_dourada = pygame.transform.scale(pygame.image.load("gold_apple.png"), (TAMANHO_BLOCO, TAMANHO_BLOCO))

# Ranking 
def salvar_pontuacao(nome, pontos):
    with open("ranking.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{nome} - {pontos}\n")

def carregar_ranking():
    try:
        with open("ranking.txt", "r", encoding="utf-8") as arquivo:
            pontuacoes = []
            for linha in arquivo:
                if "-" in linha:
                    nome, pts = linha.strip().rsplit("-", 1)
                    pontuacoes.append((nome.strip(), int(pts.strip())))
            return sorted(pontuacoes, key=lambda x: x[1], reverse=True)[:5]
    except:
        return []

def desenhar_texto(texto, cor, y, centralizar=True):
    render = FONTE.render(texto, True, cor)
    x = (LARGURA - render.get_width()) // 2 if centralizar else 10
    TELA.blit(render, (x, y))

#  Menus 
def menu_inicial():
    botoes = {
        "Jogar": pygame.Rect(LARGURA//2 - 100, ALTURA//3, 200, 50),
        "Ranking": pygame.Rect(LARGURA//2 - 100, ALTURA//3 + 70, 200, 50),
        "Sair": pygame.Rect(LARGURA//2 - 100, ALTURA//3 + 140, 200, 50)
    }

    while True:
        TELA.fill(BRANCO)
        desenhar_texto("🐍 Jogo da Cobrinha", VERDE, ALTURA//5)

        for nome, botao in botoes.items():
            pygame.draw.rect(TELA, PRETO, botao, border_radius=8)
            texto = FONTE.render(nome, True, BRANCO)
            TELA.blit(texto, (botao.x + (botao.width - texto.get_width())//2, botao.y + 10))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botoes["Jogar"].collidepoint(evento.pos):
                    nome_jogador = pedir_nome()
                    main(nome_jogador)
                if botoes["Ranking"].collidepoint(evento.pos):
                    menu_ranking()
                if botoes["Sair"].collidepoint(evento.pos):
                    pygame.quit(); sys.exit()

def menu_ranking():
    ranking = carregar_ranking()
    while True:
        TELA.fill(BRANCO)
        desenhar_texto("🏆 TOP 5 PONTUAÇÕES", PRETO, ALTURA//5)
        for i, (nome, score) in enumerate(ranking):
            desenhar_texto(f"{i+1}º - {nome}: {score}", PRETO, ALTURA//5 + 40 + i * 40)

        desenhar_texto("Pressione ESC para voltar", PRETO, ALTURA - 60)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return

def pedir_nome():
    nome = ""
    input_ativo = True
    while input_ativo:
        TELA.fill(BRANCO)
        desenhar_texto("Digite seu nome e pressione ENTER:", PRETO, ALTURA//3)
        caixa = pygame.Rect(LARGURA//2 - 150, ALTURA//2 - 25, 300, 50)
        pygame.draw.rect(TELA, PRETO, caixa, 2)
        texto = FONTE.render(nome, True, PRETO)
        TELA.blit(texto, (caixa.x + 10, caixa.y + 10))
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nome.strip():
                    return nome.strip()
                elif evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                else:
                    if len(nome) < 20:
                        nome += evento.unicode

def tela_game_over(nome, pontos):
    salvar_pontuacao(nome, pontos)
    botoes = {
        "Jogar Novamente": pygame.Rect(LARGURA//2 - 120, ALTURA//2, 240, 50),
        "Menu": pygame.Rect(LARGURA//2 - 120, ALTURA//2 + 70, 240, 50)
    }
    while True:
        TELA.fill(BRANCO)
        desenhar_texto("FIM DE JOGO", VERMELHO, ALTURA//4)
        desenhar_texto(f"Pontuação: {pontos}", PRETO, ALTURA//4 + 40)
        for nome_btn, rect in botoes.items():
            pygame.draw.rect(TELA, PRETO, rect, border_radius=8)
            texto = FONTE.render(nome_btn, True, BRANCO)
            TELA.blit(texto, (rect.x + (rect.width - texto.get_width())//2, rect.y + 10))
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: pygame.quit(); sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botoes["Jogar Novamente"].collidepoint(evento.pos):
                    main(nome)
                if botoes["Menu"].collidepoint(evento.pos):
                    return

# Jogo
def main(nome):
    x = LARGURA // 2
    y = ALTURA // 2
    dx, dy = 0, 0
    corpo = []
    comp = 1
    comida_x = random.randrange(0, LARGURA, TAMANHO_BLOCO)
    comida_y = random.randrange(0, ALTURA, TAMANHO_BLOCO)
    maca_dourada_ativa = False
    maca_dourada_x = maca_dourada_y = maca_dourada_timer = 0
    fase = 1
    velocidade = 10

    obstaculos_por_fase = {
        2: [pygame.Rect(200, 200, TAMANHO_BLOCO*5, TAMANHO_BLOCO)],
        3: [pygame.Rect(100, 100, TAMANHO_BLOCO*3, TAMANHO_BLOCO), pygame.Rect(500, 300, TAMANHO_BLOCO*3, TAMANHO_BLOCO)]
    }
    obstaculos = []

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT and dx == 0: dx, dy = -TAMANHO_BLOCO, 0
                if e.key == pygame.K_RIGHT and dx == 0: dx, dy = TAMANHO_BLOCO, 0
                if e.key == pygame.K_UP and dy == 0: dx, dy = 0, -TAMANHO_BLOCO
                if e.key == pygame.K_DOWN and dy == 0: dx, dy = 0, TAMANHO_BLOCO

        x += dx
        y += dy

        if x < 0 or x >= LARGURA or y < 0 or y >= ALTURA:
            tela_game_over(nome, comp - 1)
            return

        TELA.fill(BRANCO)

        if fase in obstaculos_por_fase:
            obstaculos = obstaculos_por_fase[fase]
        for ob in obstaculos:
            pygame.draw.rect(TELA, VERMELHO, ob)
            if pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO).colliderect(ob):
                tela_game_over(nome, comp - 1)
                return

        TELA.blit(imagem_maca, (comida_x, comida_y))
        if maca_dourada_ativa:
            TELA.blit(imagem_maca_dourada, (maca_dourada_x, maca_dourada_y))
            maca_dourada_timer -= 1
            if maca_dourada_timer <= 0:
                maca_dourada_ativa = False

        corpo.append([x, y])
        if len(corpo) > comp:
            del corpo[0]

        for s in corpo[:-1]:
            if s == [x, y]:
                tela_game_over(nome, comp - 1)
                return

        # Desenhar apenas a cabeça no início
        if comp == 1:
            TELA.blit(imagem_cabeca, corpo[-1])
        else:
            for i, s in enumerate(corpo):
                if i == len(corpo) - 1:
                    TELA.blit(imagem_cabeca, s)
                else:
                    TELA.blit(imagem_corpo, s)

        desenhar_texto(f"Pontos: {comp - 1} | Fase {fase}", PRETO, 10, centralizar=False)

        cobra_rect = pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO)
        comida_rect = pygame.Rect(comida_x, comida_y, TAMANHO_BLOCO, TAMANHO_BLOCO)
        if cobra_rect.colliderect(comida_rect):
            comp += 1
            comida_x = random.randrange(0, LARGURA, TAMANHO_BLOCO)
            comida_y = random.randrange(0, ALTURA, TAMANHO_BLOCO)
            if random.randint(1, 5) == 1:
                maca_dourada_ativa = True
                maca_dourada_timer = 100
                maca_dourada_x = random.randrange(0, LARGURA, TAMANHO_BLOCO)
                maca_dourada_y = random.randrange(0, ALTURA, TAMANHO_BLOCO)

        if maca_dourada_ativa:
            dourada_rect = pygame.Rect(maca_dourada_x, maca_dourada_y, TAMANHO_BLOCO, TAMANHO_BLOCO)
            if cobra_rect.colliderect(dourada_rect):
                comp += 5
                maca_dourada_ativa = False

        if comp > 10:
            fase = 2
            velocidade = 12
        if comp > 20:
            fase = 3
            velocidade = 15

        pygame.display.update()
        clock.tick(velocidade)


menu_inicial()
