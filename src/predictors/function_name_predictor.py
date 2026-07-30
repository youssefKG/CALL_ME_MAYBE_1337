"""Predict valid function-name continuations using a trie over token IDs."""

from src.cache.cache import Cache


class TrieNode:
    """Node in a token trie used for constrained function-name decoding."""

    def __init__(self, val: int | None = None) -> None:
        self.val: int | None = val
        self.children: dict[int, TrieNode] = dict()
        self.is_end: bool = False


class Trie:
    """Simple prefix tree for matching valid function-name token sequences."""

    def __init__(self):
        self.root_node: TrieNode = TrieNode()

    def add(self, ids: list[int]) -> None:
        """Insert a token sequence into the trie.

        Args:
            ids: Token IDs for one known function name.
        """
        current_node: TrieNode = self.root_node
        for id in ids:
            if id not in current_node.children:
                current_node.children[id] = TrieNode(id)
            current_node = current_node.children[id]
        current_node.is_end = True

    def search(self, ids: list[int]) -> bool:
        """Check whether a token sequence is a complete known function name.

        Args:
            ids: Token IDs to test.

        Returns:
            bool: True when the prefix forms a complete function name.
        """
        current_node: TrieNode = self.root_node
        for id in ids:
            if id not in current_node.children:
                return False
            current_node = current_node.children[id]
        return current_node.is_end

    def get_children(self, ids: list[int]) -> list[int]:
        """Get the valid next-token IDs for the given prefix.

        Args:
            ids: Current prefix token IDs.

        Returns:
            list[int]: Child token IDs that extend the prefix.
        """
        curr_node: TrieNode = self.root_node
        for id in ids:
            if id not in curr_node.children:
                return []
            curr_node = curr_node.children[id]
        return [x for x in curr_node.children.keys()]


class FunctionNamePredictor:
    """Expose trie-based next-token predictions for function-name decoding."""

    def __init__(
        self,
    ) -> None:
        self.__fns_names_ids_trie: Trie = Trie()
        self.__cache: Cache = Cache()

    def set_fns_names_ids_trie(self, fns_names_ids: list[list[int]]) -> None:
        """Build the trie from the available function-name token sequences.

        Args:
            fns_names_ids: Token-ID lists for each known function name.
        """
        for fn_ids in fns_names_ids:
            self.__fns_names_ids_trie.add(fn_ids)

    def get_next_predictions_ids(self, ids: list[int]) -> list[int]:
        """Return the next allowed token IDs for a prefix.

        Args:
            ids: Current prefix token IDs.

        Returns:
            list[int]: Candidate next-token IDs.
        """
        next_possible_tokens: list[int] = self.__fns_names_ids_trie.get_children(ids)
        return next_possible_tokens

    def is_completed(self, ids: list[int]) -> bool:
        """Check whether the current prefix is a completed function name.

        Args:
            ids: Token IDs to evaluate.

        Returns:
            bool: True if this prefix equals a known function name.
        """
        return self.__fns_names_ids_trie.search(ids)
