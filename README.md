_This project has been created as part of the 42 curriculum by totib._

# CALL_ME_MAYBE_1337

## Description

This project is a lightweight experimental pipeline for function-calling with a local language model. It reads a set of user prompts and available function definitions, then generates structured function calls instead of free-form text. The goal is to make the model produce valid, parseable outputs by constraining generation at the token level.

The program is built around a simple but effective idea: first select a valid function name from the known set, then generate the required arguments while enforcing the expected type for each field. The result is written to a JSON file that can be consumed by another system or executed directly.

### What the project does

- Parses prompt and function-definition data from JSON files.
- Uses a transformer-based model to propose the next token.
- Restricts generation to tokens that preserve a valid function name or parameter format.
- Produces structured function calls for strings, numbers, and booleans.
- Saves the generated output and keeps logs for debugging and recovery.

## Instructions

### Prerequisites

- Python 3.10 or newer
- `uv` (recommended) or `pip`
- Internet access for the first run so the selected Hugging Face model can be downloaded

### Installation

Using `uv`:

```bash
uv sync
uv pip install -e llm_sdk
```

Using plain `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e llm_sdk
pip install -e .
```

### Execution

Run the pipeline from the repository root:

```bash
uv run python -m src \
  --input data/input/function_calling_tests.json \
  --output output.json \
  --functions_definition data/input/functions_definition.json \
  --model_name Qwen/Qwen3-0.6B
```

You can swap the input file, output file, function-definition file, or model name to suit your own dataset.

## Algorithm explanation

The constrained decoding approach is implemented in two layers.

1. Function-name generation
   - The available function names are encoded and inserted into a trie structure.
   - During generation, the model is only allowed to continue with tokens that keep the current prefix compatible with at least one known function name.
   - The generator also allows the punctuation needed to complete the name, such as quotes or commas, so the output stays parseable.

2. Argument generation
   - Each argument is handled independently with a small deterministic state machine.
   - For numbers, the state machine enforces a legal numeric pattern: optional sign, integer part, optional fraction, and termination at a comma.
   - For strings, the state machine ensures the argument remains inside quotes and closes correctly.
   - For booleans, generation is limited to the two valid tokens `true` and `false`.
   - At every decoding step, the model scores the allowed candidates, and the system picks the highest-scoring legal token.

This design keeps the model creative while preventing it from drifting into invalid syntax. The result is a structured, JSON-like function call that is easier to parse and safer to execute.

## Design decisions

Several architectural choices were made to keep the project understandable and modular:

- Separation of concerns: a dedicated parser, prompt generator, predictor layer, and output generator keep the data pipeline and decoding logic independent.
- Deterministic state machines: these are used for numbers, strings, and booleans so that type validity is enforced without a full grammar engine.
- Trie-based function-name filtering: this makes function-name selection both efficient and simple to reason about.
- Cache layer for token IDs: repeated prompt and static-token lookups are reused to reduce overhead.
- Pydantic-backed validation: prompt and function-definition data are validated before generation starts.

These choices make the project easier to extend with new argument types or additional constrained decoding rules.

## Performance analysis

The current solution is a practical prototype rather than a production-grade inference engine.

- Accuracy: it performs well on short, well-specified prompts and simple function definitions. Accuracy decreases when the prompt is ambiguous or when the model is uncertain about the intended function.
- Speed: generation is slower than unconstrained decoding because each step requires both model inference and token filtering. However, the overhead remains acceptable for small batches and simple tasks.
- Reliability: the constrained decoding loop significantly improves syntactic validity, and the error-recovery layer helps the pipeline continue when a generation fails. Reliability is still dependent on the underlying model quality and tokenizer behavior.

## Challenges faced

A few difficulties shaped the implementation:

- Tokenization mismatch: the model works with token IDs, while the state machine operates on human-readable characters. This required careful bridging between token-level decoding and string-level validation.
- Partial-output correctness: a model may start a valid prefix and then drift later, so the generator needed a way to stop and repair malformed continuations.
- Type-specific generation: numbers, strings, and booleans each require slightly different constraints, so the decoding logic had to remain flexible without becoming too permissive.
- Recovery from invalid calls: when the model produced an unsupported function name or malformed parameters, the project needed a graceful fallback path instead of a hard crash.

The project solved these by combining token masking, simple automata, and an explicit recovery pipeline.

## Testing strategy

The implementation was validated with a combination of schema checks, fixture-based runs, and inspection of the generated output.

- The repository includes sample input files under `data/input/` for prompts and function definitions.
- The parser and Pydantic models validate the JSON structure before generation begins.
- The generated function-call output is checked for structural correctness and compatibility with the declared function definitions.
- Logs and recovery logic were used to inspect failures and refine the constraint rules.

In other words, the project was validated by running it on representative examples and ensuring that the produced calls were both parseable and consistent with the function schema.

## Example usage

A simple example is shown below:

```bash
uv run python -m src \
  --input data/input/function_calling_tests.json \
  --output output.json \
  --functions_definition data/input/functions_definition.json \
  --model_name Qwen/Qwen3-0.6B
```

The generated output is written as a JSON array of function calls. Each entry contains the resolved function name and its parameters.

## Resources

https://medium.com/@adimodi96/from-logits-to-tokens-9a36feab9cab

## # how LLM work:

how llm work: https://martinfowler.com/articles/function-call-LLM.html

## constraint decoding:

https://www.salmanq.com/blog/llm-constrained-sampling/#
https://mbrenndoerfer.com/writing/constrained-decoding-structured-llm-output

### best format for constraint decoding

https://mbrenndoerfer.com/writing/constrained-decoding-structured-llm-output#the-mathematical-formulation

### end

### Prefix tree:

https://polaris000.medium.com/understanding-prefix-trees-13da74b3cafb

fine tuning = https://comfyai.app/article/llm-hands-on-practice/qwen3-ift

### constraint decoding json:

https://pr1nt.dev/posts/constrained-json-decoding/

### x grammar: https://xgrammar.mlc.ai/docs/structural_tag/tool_calling_and_reasoning.html

### ollam that generate constraint decoding based on pydantic model

https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md

### constriant decoding:

https://mbrenndoerfer.com/writing/constrained-decoding-structured-llm-output

### how to use tools like Finite state machine and context free grammar to generate structered output

### Finite state machine for generating floating number

https://ifnotnil.com/t/finite-state-machines/323

### Temerature simpling:

https://mbrenndoerfer.com/writing/hallucination-mitigation

### soft max:

https://mbrenndoerfer.com/writing/decoding-temperature-language-model-generation
