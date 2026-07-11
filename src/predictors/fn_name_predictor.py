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
        return current_node.is_end

    def get_children(self, ids: list[int]) -> list[int]:
        curr_node: TrieNode = self.root_node
        for id in ids:
            if id not in curr_node.children:
                return []
            curr_node = curr_node.children[id]
        return [x for x in curr_node.children.keys()]


class FunctionNamePredictor:
    def __init__(
        self,
    ) -> None:
        self.__fns_names_ids_trie: Trie = Trie()

    def set_fns_names_ids_trie(self, fns_names_ids: list[list[int]]) -> None:
        for fn_ids in fns_names_ids:
            self.__fns_names_ids_trie.add(fn_ids)

    def get_next_predictions_ids(self, ids: list[int]) -> list[int]:
        return self.__fns_names_ids_trie.get_children(ids)

    def is_completed(self, ids: list[int]) -> bool:
        return self.__fns_names_ids_trie.search(ids)
