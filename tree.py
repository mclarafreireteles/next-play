#Maria Clara e Guilherme Bessa - Sistema de Recomendação de Board
#Game: Crie um sistema de recomendação de jogos de tabuleiro que utilize
#listas para armazenar os jogos, pilhas para guardar o histórico de
#recomendações dos usuários e uma árvore de decisão binária para sugerir
#jogos com base nas preferências dos usuários. A árvore deve possuir ordem
#6, pelo menos.

import random

games = [
    ("Carcassonne", "Construção", "curto", "2-5", "Construa uma paisagem medieval colocando peças e dominando cidades e estradas."),
    ("Suburbia", "Construção", "médio", "2-4", "Planeje e desenvolva sua cidade otimizando bairros e infraestrutura."),
    ("Between Two Cities", "Construção", "curto", "3-7", "Trabalho cooperativo para criar cidades equilibradas e prósperas."),
    ("The Castles of Burgundy", "Construção", "médio", "2-4", "Expanda seu território na França medieval através de estratégias de desenvolvimento."),
    ("7 Wonders", "Cartas", "curto", "3-7", "Desenvolva uma civilização e construa maravilhas icônicas através de um draft de cartas."),
    ("Dominion", "Cartas", "médio", "2-4", "Construa seu baralho e implemente estratégias para acumular pontos de vitória."),
    ("Love Letter", "Cartas", "curto", "2-4", "Jogo de dedução e blefe onde você tenta enviar mensagens secretas à princesa."),
    ("Exploding Kittens", "Cartas", "curto", "2-5", "Jogo de cartas caótico e engraçado onde você evita explodir enquanto atrapalha seus amigos."),
    ("Catan", "Estratégia", "longo", "3-4", "Comércio e construção de assentamentos para dominar a ilha de Catan."),
    ("Terraforming Mars", "Estratégia", "longo", "1-5", "Transforme Marte em um planeta habitável através de engenharia e pesquisa."),
    ("Splendor", "Estratégia", "médio", "2-4", "Colete gemas, expanda seu comércio e conquiste a admiração da nobreza renascentista."),
    ("Small World", "Estratégia", "médio", "2-5", "Controle raças fantásticas e expanda seu domínio em um mundo pequeno demais para todos."),
    ("Concordia", "Estratégia", "médio", "2-5", "Expanda seu império comercial na Roma Antiga através de planejamento estratégico."),
    ("Ticket to Ride", "Família", "curto", "2-5", "Viaje pelo mundo construindo rotas de trem e conectando cidades antes dos adversários."),
    ("Azul", "Família", "curto", "2-4", "Monte mosaicos com azulejos coloridos para criar padrões e conquistar pontos."),
    ("Kingdomino", "Família", "curto", "2-4", "Construa um reino combinando terrenos e competindo por espaço estratégico."),
    ("Patchwork", "Família", "curto", "2", "Jogo de quebra-cabeça estratégico onde você monta uma colcha de retalhos."),
    ("Pandemic", "Cooperativo", "longo", "2-4", "Salve o mundo de surtos de doenças mortais antes que se espalhem."),
    ("The Crew", "Cooperativo", "curto", "2-5", "Jogo de vaza cooperativo onde a tripulação deve completar missões no espaço."),
    ("Spirit Island", "Cooperativo", "longo", "1-4", "Espíritos da ilha devem proteger a natureza contra invasores coloniais usando poderes elementais."),
    ("Gloomhaven", "RPG", "longo", "1-4", "Campanha épica com combate tático e evolução de personagens."),
    ("Dungeons & Dragons", "RPG", "longo", "2+", "Narração e interpretação em um universo de fantasia infinita."),
    ("Mice and Mystics", "RPG", "médio", "1-4", "Ratinhos guerreiros lutam contra forças do mal para salvar seu reino.")
]

class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []  # Lista de nomes dos jogos
        self.children = []  # Lista de filhos

class BTree:
    def __init__(self, t=3):  # Ordem 6 (máximo 2t-1 chaves)
        self.root = BTreeNode(True)
        self.t = t
    
    def insert(self, key):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            new_root = BTreeNode(False)
            new_root.children.append(root)
            self.split_child(new_root, 0, root)
            self.root = new_root
        self.insert_non_full(self.root, key)
    
    def insert_non_full(self, node, key):
        if node.leaf:
            node.keys.append(key)
            node.keys.sort()
        else:
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.t) - 1:
                self.split_child(node, i, node.children[i])
                if key > node.keys[i]:
                    i += 1
            self.insert_non_full(node.children[i], key)
    
    def split_child(self, parent, i, child):
        new_node = BTreeNode(child.leaf)
        mid = self.t - 1
        parent.keys.insert(i, child.keys[mid])
        new_node.keys = child.keys[mid + 1:]
        child.keys = child.keys[:mid]
        if not child.leaf:
            new_node.children = child.children[mid + 1:]
            child.children = child.children[:mid + 1]
        parent.children.insert(i + 1, new_node)
    
    def search(self, key, node=None):
        node = node or self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return node.keys[i]
        elif node.leaf:
            return None
        else:
            return self.search(key, node.children[i])

class RecommendationSystem:
    def __init__(self):
        # Dicionário de jogos categorizados.
        # Cada jogo é uma tupla: (nome, duração, jogadores, descrição)
        self.games = {}
        self.history = []  # Pilha para histórico de recomendações
        self.tree = BTree(3)  # Árvore B de ordem 6
        self.category_feedback = {}  # Feedback (pontuação) para cada categoria
    
    @staticmethod
    def player_matches(game_players, input_players):
        """
        Verifica se o número informado de jogadores (input_players)
        se encaixa na faixa definida em game_players.
        game_players pode ser:
          - Um intervalo, ex.: '2-5'
          - Um valor exato, ex.: '2'
          - Um valor com '+', ex.: '2+' (dois ou mais)
        """
        try:
            input_players = int(input_players)
        except ValueError:
            # Se não for número, faz comparação literal
            return game_players.lower() == input_players.lower()
        
        if '-' in game_players:
            parts = game_players.split('-')
            try:
                lower_bound = int(parts[0])
                upper_bound = int(parts[1])
            except ValueError:
                return False
            return lower_bound <= input_players <= upper_bound
        elif game_players.endswith('+'):
            try:
                bound = int(game_players[:-1])
            except ValueError:
                return False
            return input_players >= bound
        else:
            try:
                game_num = int(game_players)
            except ValueError:
                return False
            return input_players == game_num
    
    def add_game(self, game, category, duration, players, description):
        if category not in self.games:
            self.games[category] = []
        self.games[category].append((game, duration, players, description))
        self.tree.insert(game)
    
    def recommend_game(self, category, duration, players):
        candidate_matches = []
        best_score = -1
        
        # Se a categoria existir, utiliza os jogos dela; senão, busca em todas.
        if category in self.games:
            game_list = self.games[category]
        else:
            game_list = []
            for cat in self.games:
                game_list.extend(self.games[cat])
        
        for game in game_list:
            score = 0
            # Comparação da duração (curto/médio/longo)
            if game[1].lower() == duration.lower():
                score += 1
            # Comparação do número de jogadores usando a função auxiliar
            if RecommendationSystem.player_matches(game[2], players):
                score += 1
            # Atualiza a lista de candidatos caso a pontuação seja melhor
            if score > best_score:
                best_score = score
                candidate_matches = [game]
            elif score == best_score:
                candidate_matches.append(game)
        
        if candidate_matches:
            selected_game = random.choice(candidate_matches)
            self.history.append((category, duration, players, selected_game[0], selected_game[3]))
            if best_score == 2:
                return f"Recomendamos: {selected_game[0]} - {selected_game[3]}"
            else:
                return f"Nenhum jogo encontrado com 100% dos critérios. Recomendamos o mais próximo: {selected_game[0]} - {selected_game[3]}"
        else:
            return "Nenhum jogo encontrado com esses critérios."
    
    def show_history(self):
        if not self.history:
            return 'Nenhuma recomendação realizada ainda.'
        return "\n".join(
            [f"Categoria: {h[0]}, Duração: {h[1]}, Jogadores: {h[2]} -> Jogo: {h[3]} - {h[4]}" for h in reversed(self.history)]
        )
    
    def interactive_mode(self):
        print("Bem-vindo ao sistema de recomendação de jogos de tabuleiro!")
        while True:
            print("\nResponda às perguntas para receber uma recomendação ou digite 'sair' a qualquer momento para encerrar.")
            
            category = input("Qual seu estilo de jogo preferido? (Ex: Estratégia, RPG, Cartas, Construção, Família, Cooperativo, etc.): ")
            if category.lower() == 'sair':
                break
            
            if category in self.category_feedback and self.category_feedback[category] < 0:
                continuar = input("Você tem dado feedback negativo para recomendações desse estilo. Deseja continuar mesmo assim? (sim/nao): ")
                if continuar.lower() != 'sim':
                    print("Tente escolher outro estilo para recomendação.")
                    continue
            
            duration = input("Prefere jogos curtos, médios ou longos? (curto/médio/longo): ")
            if duration.lower() == 'sair':
                break
            
            players = input("Quantas pessoas vão jogar? (informe um número): ")
            if players.lower() == 'sair':
                break
            
            recommendation = self.recommend_game(category, duration, players)
            print("\n" + recommendation)
            
            feedback = input("Avalie a recomendação (digite 'p' para positiva ou 'n' para negativa): ")
            if category not in self.category_feedback:
                self.category_feedback[category] = 0
            if feedback.lower() == 'p':
                self.category_feedback[category] += 1
                print("Feedback positivo registrado. Continuaremos recomendando jogos desse estilo!")
            elif feedback.lower() == 'n':
                self.category_feedback[category] -= 1
                print("Feedback negativo registrado. Analisaremos recomendações futuras para esse estilo.")
            else:
                print("Feedback inválido. Nenhuma alteração no feedback.")
            
            print("\nHistórico de preferências e recomendações:")
            print(self.show_history())

# Exemplo de uso e adição de jogos com informações detalhadas:

recommendation_system = RecommendationSystem()
for game in games:
    recommendation_system.add_game(*game)

recommendation_system.interactive_mode()
