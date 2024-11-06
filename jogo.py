import pygame
import random
from pygame.locals import *  # type: ignore
import sys
import os

LARGURA_TELA = 600
ALTURA_TELA = 600
COR_FUNDO = (255, 255, 255)
ALTURA_CABEÇALHO = 60
PIXEL = 30

class JogoDaCobrinha:
     
    """  Classe que representa o jogo da cobrinha (Snake).

    Atributos:
    posicoes_cobra (list[tuple[int, int]]): Lista de posições da cobra.
    posicao_maca (tuple[int, int]): Posição da maçã.
    direcao_cobra (int): Direção atual da cobra.
    pontuacao (int): Pontuação atual do jogo.
    nome (str): Nome do jogador."""
    
    
    def __init__(self)-> None:
        """ inicia o jogo, confiurando tela e posição. """
        pygame.init()
        pygame.display.set_caption('Jogo da Cobrinha')
        self.clock = pygame.time.Clock()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        self.font = pygame.font.match_font('arial')
        self.carregar_arquivos()
        self.mouse = pygame.mouse.get_pos()
        self.reiniciar_jogo()
        self.comando_direcao = K_LEFT
        self.direcao_cobra = self.comando_direcao


    def random_on_grid(self) -> tuple[int, int]:
        while True:
            
            """Gera uma posição aleatória para a maçã, que esteja dentro dos limites da tela.

            Retorna:
            tuple[int, int]: Coordenadas (x, y) da nova posição da maçã.
            """
            
            x  = random.randint(0, (LARGURA_TELA - PIXEL) // PIXEL) * PIXEL 
            y = random.randint(ALTURA_CABEÇALHO // PIXEL, (ALTURA_TELA - PIXEL) // PIXEL) * PIXEL 
            nova_posicao=(x, y) 
            if nova_posicao not in self.posicoes_cobra:
                self.posicao_maca = nova_posicao
                return nova_posicao
    
  

    def limite(self, posicao: tuple[int, int]) -> bool:
        """Verifica se a posição está fora dos limites da tela e/ou cabeçalho.

        Args:
            posicao (tuple[int, int]): Coordenadas (x, y) a serem verificadas.

        Retorna:
            bool: True se a posição estiver fora dos limites, False caso contrário.
        """
        
        return not (0 <= posicao[0] < LARGURA_TELA and ALTURA_CABEÇALHO <= posicao[1] < ALTURA_TELA)
    

    def criar_superficie_cobra(self) -> pygame.Surface:
        """Cria a superfície para desenhar a cobra.

        Retorna:
            pygame.Surface: Superfície com a cor verde para a cobra.
        """
        superficie_cobra = pygame.Surface((PIXEL, PIXEL))
        superficie_cobra.fill(((34, 139, 34)))
        return superficie_cobra
        
    def criar_superficie_maca(self) -> pygame.Surface:
        """Cria a superfície para desenhar a maçã.

        Retorna:
            pygame.Surface: Superfície para a maçã.
        """
        superficie_maca = pygame.Surface((PIXEL, PIXEL))

        return superficie_maca

    def collision(self, posicao_1: tuple[int, int], posicao_2: tuple[int, int]) -> bool:
        """Verifica se as duas posições colidiram.

        Args:
            posicao_1 (tuple[int, int]): Primeira posição (tupla).
            posicao_2 (tuple[int, int]): Segunda posição (tupla).

        Retorna:
            bool: True se as posições forem iguais, False caso sejam diferentes."""
        return posicao_1 == posicao_2
    

    def mover_cobra(self, tela: pygame.Surface) -> list[tuple[int, int]]:

        """Move a cobra de acordo com a direção atual e verifica colisões.

        Args:
            tela (pygame.Surface): Superfície do jogo.

        Retorna:
            list[tuple[int, int]]: Lista atualizada de posições da cobra.
        """
        # Move a cobra a partir da cabeça para trás
        for i in range(len(self.posicoes_cobra) - 1, 0, -1):
            self.posicoes_cobra[i] = self.posicoes_cobra[i - 1]

        # Atualiza a posição da cabeça da cobra de acordo com a direção
        if self.comando_direcao == K_UP and not self.direcao_cobra == K_DOWN:
            self.direcao_cobra = self.comando_direcao
        elif self.comando_direcao == K_DOWN and not self.direcao_cobra == K_UP:
            self.direcao_cobra = self.comando_direcao
        elif self.comando_direcao == K_LEFT and not self.direcao_cobra == K_RIGHT:
            self.direcao_cobra = self.comando_direcao
        elif self.comando_direcao == K_RIGHT and not self.direcao_cobra == K_LEFT:
            self.direcao_cobra = self.comando_direcao

        if self.direcao_cobra == K_UP:
            self.posicoes_cobra[0] = (self.posicoes_cobra[0][0], self.posicoes_cobra[0][1] - PIXEL)
        elif self.direcao_cobra == K_DOWN:
            self.posicoes_cobra[0] = (self.posicoes_cobra[0][0], self.posicoes_cobra[0][1] + PIXEL)
        elif self.direcao_cobra == K_LEFT:
            self.posicoes_cobra[0] = (self.posicoes_cobra[0][0] - PIXEL, self.posicoes_cobra[0][1])
        elif self.direcao_cobra == K_RIGHT:
            self.posicoes_cobra[0] = (self.posicoes_cobra[0][0] + PIXEL, self.posicoes_cobra[0][1])

        # Verifica se a cobra bateu nos limites da tela
        if self.limite(self.posicoes_cobra[0]):
            self.perder(tela)
            return self.posicoes_cobra

        # Verifica se a cobra colidiu com ela mesma
        for i in range(1, len(self.posicoes_cobra)):
            if self.posicoes_cobra[0] == self.posicoes_cobra[i]:
                self.perder(tela)
                return self.posicoes_cobra
        return self.posicoes_cobra

    def verificar_colisao_com_maca(self) -> tuple[int, int]:
        """Verifica se houve colisão com a maçã e atualiza a posição da maçã e a pontuação.

        Retorna:
            tuple[int, int]: Nova posição da maçã.
        """
        if self.collision(self.posicao_maca, self.posicoes_cobra[0]):
            self.posicoes_cobra.append((-30, -30))
            self.posicao_maca = self.random_on_grid()
            self.pontuacao += 1
        return self.posicao_maca
    
    def carregar_arquivos(self) -> None:
        """Carrega as imagens necessárias para o jogo."""
        diretorio_imagens = os.path.join(os.getcwd(),'imagens')
        self.fundo = pygame.image.load(os.path.join(diretorio_imagens, 'fundo.jpg')).convert()
        self.imagem_maca = pygame.image.load(os.path.join(diretorio_imagens, 'maca.png')).convert_alpha()
        self.exit= pygame.image.load(os.path.join(diretorio_imagens, 'exit_btn.png')).convert()
        self.start = pygame.image.load(os.path.join(diretorio_imagens, 'start_btn.png')).convert()
        self.cabeca_cobra = pygame.image.load(os.path.join(diretorio_imagens, 'cabeca_cobra.jpg')).convert()
        self.trofeu = pygame.image.load(os.path.join(diretorio_imagens, 'trofeu.png')).convert()

       

    def reiniciar_jogo(self) -> None:
        """Reinicia o jogo, configurando a posição inicial da cobra, da maçã e da pontuação."""

        """ Reinicia o jogo, configurando a posição inicial da cobra,da  maçã e da pontuação."""
        self.posicoes_cobra = [(270, 60), (300, 60), (330, 60)]
        self.posicao_maca = self.random_on_grid()
        self.direcao_cobra = K_LEFT
        self.pontuacao = 0

    
    def exibir_pontuacao(self, pontuacao_total: int) -> None:
        """Exibe a pontuação final e o troféu.

        Args:
            pontuacao_total (int): A pontuação total do jogador.
        """
        fonte = pygame.font.SysFont(None, 30)

        # Limpa a tela e exibe a pontuação total com o troféu
        self.tela.fill((0, 0, 0))
        self.tela.blit(self.trofeu, (175, 175))
        mensagem_3 = f'SUA PONTUAÇÃO TOTAL FOI: {pontuacao_total}'
        texto_3 = fonte.render(mensagem_3, True, (255, 255, 255))
        self.tela.blit(texto_3, (150, 120))
        pygame.display.update()

        # Delay para exibir a pontuação
        self.aguardar_tempo_exibicao(2500)  # Espera 2,5 segundos

    def aguardar_tempo_exibicao(self, tempo: int) -> None:
        """Aguarda um determinado tempo sem permitir entradas do jogador.

        Args:
            tempo (int): Tempo em milissegundos para aguardar.
        """
        inicio = pygame.time.get_ticks()  # Marca o tempo inicial

        while pygame.time.get_ticks() - inicio < tempo:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

    def perder(self, tela: pygame.Surface) -> None:
        """Pergunta se o jogador quer continuar ou sair após perder o jogo.

        Args:
            tela (pygame.Surface): A superfície onde o jogo está sendo desenhado.
        """
        pontuacao_total = self.salvar_pontuacao()
        self.exibir_pontuacao(pontuacao_total)

        fonte = pygame.font.SysFont(None, 30)
        texto_perder = fonte.render('Pressione S para sair ou C para continuar', True, (255, 255, 255))
        self.tela.fill((0, 0, 0))  
        self.tela.blit(texto_perder, (90, 250))
        pygame.display.flip()

        # Loop para esperar a decisão do jogador
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_s:
                        pygame.quit()
                        sys.exit()
                    elif event.key == K_c:
                        self.reiniciar_jogo()  # Reinicia o jogo
                        self.menu_inicial()  # Exibe o menu inicial
                        return  # Sai da função imediatamente

    def salvar_pontuacao(self)-> None:
        """Salva a pontuação do jogador em um arquivo de ranking.

        A função lê as pontuações existentes de um arquivo chamado 'ranking.txt',
        adiciona a pontuação atual do jogador, e escreve as pontuações em ordem
        decrescente de volta ao arquivo. Se o arquivo não existir, é criado um novo.

        Returns:
        int: A pontuação da rodada atual do jogador.
        """
        pontuacoes = []
        
        # Tenta ler o arquivo se existir
        try:
            with open('ranking.txt', 'r') as arquivo:
                for linha in arquivo:
                    linha = linha.strip()
                    if linha:  # Ignora linhas vazias
                        nome, pontos = linha.split(': ')
                        pontuacoes.append((nome, int(pontos.replace(' pontos', ''))))
        except FileNotFoundError:
            # O arquivo não existe, então começamos com uma lista vazia
            pass

        # Adiciona a nova pontuação
        pontuacoes.append((self.nome, self.pontuacao))

        for i in range(len(pontuacoes)):
            for j in range(i + 1, len(pontuacoes)):
                if pontuacoes[i][1] < pontuacoes[j][1]:
                    pontuacoes[i], pontuacoes[j] = pontuacoes[j], pontuacoes[i]

    
        with open('ranking.txt', 'w') as arquivo:
            for nome, pontos in pontuacoes:
                arquivo.write(f'{nome}: {pontos} pontos\n')

        return self.pontuacao # Retorna a pontuação da rodada atual
   
        
        
    def decisão(self) -> bool:
        """
        Espera pela decisão do jogador para continuar.

        O loop aguarda um evento de teclado ou a saída do jogo. 
        Se a tecla UP for pressionada, a função retorna True. 
        Se o jogo for encerrado, ela finaliza a execução.

        Returns:
            bool: Retorna True se a tecla UP foi pressionada, caso contrário, retorna False.
        """
        esperar = True
        while esperar:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    esperar = False
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        esperar = False
        return esperar
    
    #função do mouse
    def verificar_clique(self) -> bool:
        """Verifica se o mouse foi clicado em um dos botões da tela.

        Retorna:
            bool: Retorna True se o botão "Start" foi clicado, caso contrário, retorna False.
        """
        pos_mouse_x,pos_mouse_y = pygame.mouse.get_pos()
        clique = pygame.mouse.get_pressed()
        if clique[0]:
            if 20<=pos_mouse_x<=20 + self.exit.get_width() and 300 <= pos_mouse_y<= 300 +  self.exit.get_height():
                pygame.quit()
                sys.exit()
            elif 380 <= pos_mouse_x <= 300 + self.start.get_width() and 300 <= pos_mouse_y <= 300 + self.start.get_height():
                return True
        return False
    
    def menu_inicial(self) -> None:
        """Exibe o menu inicial do jogo, com opções para iniciar e sair.

        O usuário pode iniciar o jogo ou sair através de botões interativos.
        """
        fonte = pygame.font.SysFont(None, 45)
        mensagem = 'BEM VINDO AO SNAKE GAME!'
        texto = fonte.render(mensagem,True,(255,255,255))
        fonte_2 = pygame.font.SysFont(None, 30)
        mensagem_com = 'POR : MARIA LUÍZA E JOSÉ ABÍLIO'
        texto_com = fonte_2.render(mensagem_com, True, (255, 255, 255))
        nome = ""

    
        while True:

            self.tela.fill((0,0,0))
            self.tela.blit(texto, (80, 150))
            self.tela.blit(self.exit,(20,300))
            self.tela.blit(self.start,(300,300))
            self.tela.blit(texto_com, (120, 500))
        
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            if self.verificar_clique():
                # Se clicar no botão Start, mostra a tela de digitação do nome
                return self.digitar_nome()
            
    
    def digitar_nome(self) -> str:
        """
        Exibe a tela para o jogador digitar seu nome.

        Este método exibe uma tela onde o jogador pode inserir seu nome. O nome é atualizado
        em tempo real enquanto o jogador digita. Quando o jogador pressiona a tecla Enter,
        o nome é salvo e a função retorna o nome digitado.

        Retorno:
            str: O nome digitado pelo jogador.
        """
        fonte = pygame.font.SysFont(None, 45)
        mensagem_2 = 'DIGITE SEU NOME PARA INICIAR'
        texto_2 = fonte.render(mensagem_2, True, (255, 255, 255))
        mensagem_3 = 'POR MARIA LUÍZA E JOSÉ ABÍLIO'
        texto_3 = fonte.render(mensagem_3, True, (255, 255, 255))
        nome = ""
        while True:
            #boas vindas
            self.tela.fill((0, 0, 0))
            self.tela.blit(texto_2, (60, 150))
            #nome do usuario
            texto_nome = fonte.render(nome, True, (255, 255, 255))
            self.tela.blit(texto_nome, (200, 250))
            # aviso

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN and nome.strip():
                    # Se pressionar Enter e o nome não estiver vazio, sai do loop
                        self.nome = nome
                        return nome
                    
                    elif event.key == K_BACKSPACE:
                        # Apaga o último caractere do nome
                        nome = nome[:-1]
                    
                    elif len(nome) < 20 :
                        # Adiciona o caractere pressionado ao nome com limite de 20 caracteres
                        nome += event.unicode
       

    def principal(self)-> None:

        """
        Loop principal do jogo.

        Este método controla a lógica do jogo, atualiza a tela e responde a eventos do teclado.
        Ele inicia o loop do jogo, onde a cobra é movida, verifica se há colisão com a maçã
        e atualiza a tela com a cobra, maçã e pontuação.

        Retorno:
            None
        """
        superficie_cobra = self.criar_superficie_cobra()
        fonte = pygame.font.SysFont(None, 36)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                        # Trata o caso de o usuário tentar andar no sentido contrário do que a cobrinha está indo
                        self.comando_direcao = event.key

            # Move a cobra
            self.posicoes_cobra = self.mover_cobra(self.tela)

            # Verifica se a cobra comeu a maçã
            self.verificar_colisao_com_maca()

            self.tela.fill(COR_FUNDO)  

            self.tela.blit(self.fundo, (0, ALTURA_CABEÇALHO))

            self.tela.blit(self.cabeca_cobra, self.posicoes_cobra[0])

            for posicao in self.posicoes_cobra[1:]:  # Começa do segundo segmento
                self.tela.blit(superficie_cobra, posicao)
        
            self.tela.blit(self.imagem_maca, self.posicao_maca)

            # Desenha a linha do cabeçalho
            pygame.draw.line(self.tela, (0, 0, 0), (0, ALTURA_CABEÇALHO), (LARGURA_TELA, ALTURA_CABEÇALHO), 2)

            # Desenha a pontuação
            texto_pontuacao = fonte.render(f'Pontuação: {self.pontuacao}', True, (0, 0, 0))
            self.tela.blit(texto_pontuacao, (420, 20))

            pygame.display.flip()

            self.clock.tick(7)

def main()-> None:
    """
    Função principal que inicializa e executa o jogo da cobrinha.
        
    Esta função cria uma instância da classe JogoDaCobrinha, chama o método
    menu_inicial() para exibir o menu inicial e, em seguida, inicia o jogo
    chamando o método principal().
    """
    jogo = JogoDaCobrinha()
    jogo.menu_inicial()
    jogo.principal()

if __name__ == "__main__":
    """
    Ponto de entrada do programa.
            
    Verifica se o script está sendo executado diretamente e, caso esteja,
    chama a função main() para iniciar o jogo.
    """
    main()