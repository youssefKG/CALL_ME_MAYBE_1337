"""Predict valid function-name continuations using a trie over token IDs."""

from src.cache.cache import Cache
from enum import Enum, auto


class FunctionNameState(Enum):
    START = auto()
    CONTENT = auto()
    ESCAPE = auto()
    FINAL = auto()


class TrieNode:
    """Node in a token trie used for constrained function-name decoding.

    Attributes:
        val: The token ID associated with this node (None for root).
        children: Mapping of token IDs to child TrieNode instances.
        is_end: Whether this node represents the end of a valid name.
    """

    def __init__(self, val: int | None = None) -> None:
        """Initialize a trie node.

        Args:
            val: Optional token ID for this node (None for root node).
        """
        self.val: int | None = val
        self.children: dict[int, TrieNode] = dict()
        self.is_end: bool = False


class Trie:
    """Simple prefix tree for matching valid function-name token sequences.

    Stores tokenized function names in a trie structure to efficiently
    validate and predict valid next tokens during constrained decoding.
    """

    def __init__(self) -> None:
        """Initialize the trie with an empty root node."""
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

        Validates that the full sequence exists in the trie and marks the
        final node as an end-of-name node.

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

        Traverses the trie following the prefix and returns all valid
        immediate child tokens.

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
    """Expose trie-based next-token predictions for function-name decoding.

    Uses a trie structure to constrain token generation to known function
    names and provide real-time validation during decoding.

    Attributes:
        __fns_names_ids_trie: Trie structure holding tokenized names.
        __cache: Reference to the shared token cache.
    """

    def __init__(
        self,
    ) -> None:
        """Initialize the predictor with empty state.

        Creates a new trie and obtains the singleton cache reference.
        """
        self.__fns_names_ids_trie: Trie = Trie()
        self.__cache: Cache = Cache()

    def set_fns_names_ids_trie(self, fns_names_ids: list[list[int]]) -> None:
        """Build the trie from the available function-name token sequences.

        Populates the internal trie with all known function name token
        sequences, enabling constraint-based decoding.

        Args:
            fns_names_ids: Token-ID lists for each known function name.
        """
        for fn_ids in fns_names_ids:
            self.__fns_names_ids_trie.add(fn_ids)

    def get_next_predictions_ids(
        self, ids: list[int], generated_function_name: str
    ) -> list[int]:
        """Return the next allowed token IDs for a prefix.

        Queries the trie to get valid continuation tokens for the current
        prefix, constraining the model's output during generation.

        Args:
            ids: Current prefix token IDs.

        Returns:
            list[int]: Candidate next-token IDs.
        """
        next_possible_tokens: list[int] = (
            self.__fns_names_ids_trie.get_children(ids)
        )
        function_name_state: FunctionNameState = self.function_name_state(
            generated_function_name
        )
        match function_name_state:
            case FunctionNameState.START:
                next_possible_tokens.append(self.__cache.get_token_id('"'))
            case FunctionNameState.CONTENT:
                next_possible_tokens.append(self.__cache.get_token_id('"'))
            case FunctionNameState.FINAL:
                return [self.__cache.get_token_id(",")]
            case FunctionNameState.ESCAPE:
                return next_possible_tokens

        next_possible_tokens.append(self.__cache.get_token_id('"'))
        next_possible_tokens.append(self.__cache.get_token_id(","))
        return next_possible_tokens

    def function_name_state(self, function_name: str) -> FunctionNameState:
        function_name_state: FunctionNameState = FunctionNameState.START
        for ch in function_name:
            match function_name_state:
                case FunctionNameState.START:
                    function_name_state = FunctionNameState.CONTENT
                case FunctionNameState.CONTENT:
                    if ch == '"':
                        function_name_state = FunctionNameState.FINAL
                    if ch == "\\":
                        function_name_state = FunctionNameState.ESCAPE
                case FunctionNameState.ESCAPE:
                    function_name_state = FunctionNameState.CONTENT
                case FunctionNameState.FINAL:
                    pass

        return function_name_state

    def is_completed(self, ids: list[int]) -> bool:
        """Check whether the current prefix is a completed function name.

        Validates that the token sequence represents a complete and valid
        function name, not just a valid prefix.

        Args:
            ids: Token IDs to evaluate.

        Returns:
            bool: True if this prefix equals a known function name.
        """
        return self.__fns_names_ids_trie.search(ids)
