from dataclasses import dataclass


@dataclass
class PredictionResult:
    is_found: bool
    possible_predicted_tokens: set[str]
    predicted_token: str


class TrieNode:
    def __init__(self, val: int | None = None) -> None:
        self.val: int | None = val
        self.children: dict[int, TrieNode] = dict()
        self.is_end: bool = False

class Trie:
    def __init__(self):
        self.root_node: TrieNode = TrieNode()

    def add(self, ids: list[int]) -> None:
        current_node: TrieNode = self.root_node
        for id in ids:
            if id not in current_node.children:
                current_node.children[id] = TrieNode(id)
            current_node = current_node.children[id]
        current_node.is_end = True

    def search(self, ids: list[int]) -> bool:
        current_node: TrieNode = self.root_node
        for id in ids:
            if id not in current_node.children:
                return False
            current_node = current_node.children[id]
        return current_node.is_end;

    def get_children(self, ids: list[int]) -> list[int]:
        curr_node: TrieNode = self.root_node
        for id in ids:
            if id not in curr_node.children:
                return []
            curr_node = curr_node.children[id]
        return [x for x in curr_node.children.keys()]


def test_prefix_triee() -> None:
    tree = Trie()
    tree.add([1, 2, 3, 4, 5])
    tree.add([1, 2, 3, 5, 6])
    print(tree.search([3, 5, 8, 1, 5]))
    print(tree.search([3, 5]))
    print(tree.get_children([1, 2, 3]))


if __name__ == "__main__":
    test_prefix_triee()


"""
class TrieNode:
    def __init__(self):
        # Associe un caractère à son nœud enfant correspondant
        self.children = {}
        # Compte combien de fois ce chemin a été emprunté
        self.frequency = 0

class PrefixTreePredictor:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.frequency += 1  # Incrémente la popularité de ce chemin

    def predict_next_characters(self, prefix: str):
        node = self.root
        
        # 1. Navigation jusqu'au bout du préfixe donné
        for char in prefix:
            if char not in node.children:
                return []  # Le préfixe n'existe pas dans l'arbre
            node = node.children[char]

        # 2. Extraction et tri des enfants par fréquence décroissante
        sorted_predictions = sorted(
            node.children.items(), 
            key=lambda item: item[1].frequency, 
            reverse=True
        )

        # 3. Retourne une liste de tuples (caractère, score de fréquence)
        return [(char, child.frequency) for char, child in sorted_predictions]

# ==========================================
# Exemple d'utilisation :
# ==========================================
predictor = PrefixTreePredictor()

# Entraînement de l'arbre avec un corpus de mots
corpus = ["chat", "chapeau", "château", "chien", "chasse", "chat"]
for word in corpus:
    predictor.insert(word)

# Prédiction après le préfixe "cha"
prefixe_test = "cha"
predictions = predictor.predict_next_characters(prefixe_test)

print(f"Après '{prefixe_test}', les caractères les plus probables sont :")
for char, freq in predictions:
    print(f"  -> '{char}' (vu {freq} fois)")

"""
