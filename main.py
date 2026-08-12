import pygame
import random
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da Tela
LARGURA = 800
ALTURA = 400
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo do Dinossauro")
RELOGIO = pygame.time.Clock()

# Cores (RGB)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (100, 100, 100)
VERDE = (34, 139, 34)

# Classe do Dinossauro
class Dinossauro:
    def __init__(self):
        self.largura = 40
        self.altura = 50
        self.x = 80
        self.y_chao = ALTURA - self.altura - 30
        self.y = self.y_chao
        self.velocidade_y = 0
        self.gravidade = 0.8
        self.no_chao = True

    def pular(self):
        if self.no_chao:
            self.velocidade_y = -14
            self.no_chao = False

    def atualizar(self):
        self.velocidade_y += self.gravidade
        self.y += self.velocidade_y

        # Limite do chão
        if self.y >= self.y_chao:
            self.y = self.y_chao
            self.velocidade_y = 0
            self.no_chao = True

    def desenhar(self):
        # Desenha o dinossauro (retângulo verde simples)
        rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        pygame.draw.rect(TELA, VERDE, rect)
        
        # Olho do dinossauro
        pygame.draw.rect(TELA, BRANCO, (self.x + 25, self.y + 8, 6, 6))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

# Classe dos Cactos (Obstáculos)
class Cacto:
    def __init__(self, velocidade):
        self.largura = random.choice([20, 30, 40])
        self.altura = random.randint(35, 65)
        self.x = LARGURA
        self.y = ALTURA - self.altura - 30
        self.velocidade = velocidade

    def atualizar(self):
        self.x -= self.velocidade

    def desenhar(self):
        rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        pygame.draw.rect(TELA, PRETO, rect)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

# Função Principal
def jogo():
    dino = Dinossauro()
    cactos = []
    tempo_ultimo_cacto = pygame.time.get_ticks()
    
    pontuacao = 0
    velocidade_jogo = 6
    rodando = True
    game_over = False

    fonte = pygame.font.SysFont("Arial", 22)
    fonte_game_over = pygame.font.SysFont("Arial", 36, bold=True)

    while rodando:
        TELA.fill(BRANCO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE or evento.key == pygame.K_UP:
                    if game_over:
                        jogo() # Reinicia o jogo
                    else:
                        dino.pular()

        if not game_over:
            # Atualiza Dinossauro
            dino.atualizar()

            # Gera Cactos dinamicamente
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - tempo_ultimo_cacto > random.randint(1200, 2200):
                cactos.append(Cacto(velocidade_jogo))
                tempo_ultimo_cacto = tempo_atual

            # Atualiza e limpa Cactos
            for cacto in list(cactos):
                cacto.atualizar()
                
                # Checa colisão
                if dino.get_rect().colliderect(cacto.get_rect()):
                    game_over = True

                # Remove cactos que saíram da tela
                if cacto.x < -cacto.largura:
                    cactos.remove(cacto)

            # Pontuação e Aumento de Dificuldade
            pontuacao += 1
            if pontuacao % 300 == 0:
                velocidade_jogo += 0.5

        # --- Desenho dos Elementos na Tela ---
        
        # Desenha a Linha do Chão
        pygame.draw.line(TELA, CINZA, (0, ALTURA - 30), (LARGURA, ALTURA - 30), 2)

        dino.desenhar()

        for cacto in cactos:
            cacto.desenhar()

        # Desenha a Pontuação
        texto_pontos = fonte.render(f"Pontos: {pontuacao // 5}", True, PRETO)
        TELA.blit(texto_pontos, (LARGURA - 150, 20))

        # Mensagem de Game Over
        if game_over:
            texto_go = fonte_game_over.render("GAME OVER", True, PRETO)
            texto_reiniciar = fonte.render("Pressione ESPAÇO para reiniciar", True, CINZA)
            TELA.blit(texto_go, (LARGURA // 2 - 100, ALTURA // 2 - 40))
            TELA.blit(texto_reiniciar, (LARGURA // 2 - 150, ALTURA // 2 + 10))

        pygame.display.flip()
        RELOGIO.tick(60)

if __name__ == "__main__":
    jogo()