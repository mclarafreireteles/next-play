import random

# Lista de jogos pré-cadastrados
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

# Classe para os nós da árvore de decisão
class AVLTreeNode:
    def __init__(self, criterion=None, is_leaf=False):
        self.criterion = criterion  # Critério atual (ex: "Categoria", "Duração")
        self.is_leaf = is_leaf  # Indica se é um nó folha
        self.games = []  # Lista de jogos (só preenchida se for folha)
        self.children = {}  # Filhos do nó (chave: valor do critério, valor: nó filho)
        self.height = 1  # Altura do nó

class AVLTree:
    def __init__(self, criteria_order=["Categoria", "Duração", "Jogadores"]):
        self.root = AVLTreeNode(criterion=criteria_order[0])
        self.criteria_order = criteria_order  # Define a hierarquia dos critérios

    def insert(self, game):
        self.root = self._insert(self.root, game, 0)

    def _insert(self, node, game, depth):
        if depth >= len(self.criteria_order):
            node.games.append(game)
            return node

        criterion = self.criteria_order[depth]
        if criterion == "Categoria":
            value = game[1]
        elif criterion == "Duração":
            value = game[2]
        elif criterion == "Jogadores":
            value = game[3]

        if value not in node.children:
            is_leaf = (depth == len(self.criteria_order) - 1)
            node.children[value] = AVLTreeNode(
                criterion=self.criteria_order[depth + 1] if not is_leaf else None,
                is_leaf=is_leaf
            )

        node.children[value] = self._insert(node.children[value], game, depth + 1)

        # Atualiza a altura do nó atual
        node.height = 1 + max(self._get_height(child) for child in node.children.values())

        # Balanceia o nó
        balance = self._get_balance(node)

        # Casos de desbalanceamento
        if balance > 1:
            if self._get_balance(list(node.children.values())[0]) >= 0:
                return self._rotate_right(node)
            else:
                node.children[list(node.children.keys())[0]] = self._rotate_left(list(node.children.values())[0])
                return self._rotate_right(node)
        if balance < -1:
            if self._get_balance(list(node.children.values())[-1]) <= 0:
                return self._rotate_left(node)
            else:
                node.children[list(node.children.keys())[-1]] = self._rotate_right(list(node.children.values())[-1])
                return self._rotate_left(node)

        return node

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(list(node.children.values())[0]) - self._get_height(list(node.children.values())[-1])

    def _rotate_right(self, y):
        x = list(y.children.values())[0]
        T2 = x.children.get(list(x.children.keys())[-1], None)

        # Realiza a rotação
        x.children[list(x.children.keys())[-1]] = y
        y.children[list(y.children.keys())[0]] = T2

        # Atualiza alturas
        y.height = 1 + max(self._get_height(child) for child in y.children.values())
        x.height = 1 + max(self._get_height(child) for child in x.children.values())

        return x

    def _rotate_left(self, x):
        y = list(x.children.values())[-1]
        T2 = y.children.get(list(y.children.keys())[0], None)

        # Realiza a rotação
        y.children[list(y.children.keys())[0]] = x
        x.children[list(x.children.keys())[-1]] = T2

        # Atualiza alturas
        x.height = 1 + max(self._get_height(child) for child in x.children.values())
        y.height = 1 + max(self._get_height(child) for child in y.children.values())

        return y

    def recommend_from_tree(self, preferences):
        current_node = self.root
        path = []

        for criterion in self.criteria_order:
            value = preferences.get(criterion, "")
            if value in current_node.children:
                current_node = current_node.children[value]
                path.append(value)
            else:
                closest_match = self.find_closest_match(current_node, criterion, preferences)
                if closest_match:
                    current_node = current_node.children[closest_match]
                    path.append(closest_match)
                else:
                    return []

        return current_node.games

    def find_closest_match(self, node, criterion, preferences):
        if criterion == "Jogadores":
            input_players = int(preferences["Jogadores"])
            for key in node.children.keys():
                if self.player_matches(key, input_players):
                    return key
        return None

    @staticmethod
    def player_matches(game_players, input_players):
        if '-' in game_players:
            parts = game_players.split('-')
            lower_bound = int(parts[0])
            upper_bound = int(parts[1])
            return lower_bound <= input_players <= upper_bound
        elif game_players.endswith('+'):
            bound = int(game_players[:-1])
            return input_players >= bound
        else:
            game_num = int(game_players)
            return input_players == game_num

class RecommendationSystem:
    def __init__(self):
        self.history = []
        self.tree = AVLTree()
        self.category_feedback = {}

    def add_game(self, game):
        self.tree.insert(game)

    def recommend_game(self, category, duration, players):
        preferences = {
            "Categoria": category,
            "Duração": duration,
            "Jogadores": players
        }
        candidates = self.tree.recommend_from_tree(preferences)
        if candidates:
            selected = random.choice(candidates)
            self.history.append((category, duration, players, selected[0], selected[4]))
            return f"Recomendação: {selected[0]} - {selected[4]}"
        else:
            return "Nenhum jogo encontrado."

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

# Exemplo de uso
recommendation_system = RecommendationSystem()
for game in games:
    recommendation_system.add_game(game)

recommendation_system.interactive_mode()