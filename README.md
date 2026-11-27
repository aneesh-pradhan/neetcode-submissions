# NeetCode Solutions

This repository is my NeetCode practice. Each file is a solution I wrote for a problem on [NeetCode](https://neetcode.io), kept as its own submission so a reader can open the approach (and later attempts) directly. The solution code is mine, and the repository is licensed under the MIT License.

## Languages

Python (`.py`).

## Layout

NeetCode's GitHub sync stores every attempt as its own file:

```text
<topic>/<problem-id>/submission-<n>.<ext>
```

The topic folder is the category. The problem folder is the problem id. `submission-<n>` counts attempts for that problem, starting at 0. The tree currently has one topic, `Data Structures & Algorithms`, and three problems: `anagram-groups`, `duplicate-integer`, and `is-anagram`.

Difficulty is recorded in the index only when a folder or file name contains `easy`, `medium`, or `hard`. These paths do not, so that column is blank.

## Run a solution locally

Python 3 is the only toolchain these files need. From the repository root, syntax-check every solution:

```bash
python3 -m compileall -q "Data Structures & Algorithms"
```

Syntax-check one file:

```bash
python3 -m py_compile "Data Structures & Algorithms/is-anagram/submission-0.py"
```

The `is-anagram` files import cleanly. This runs `submission-0.py` against two pairs and prints `True`, then `False`:

```bash
python3 - << 'PY'
import importlib.util

path = "Data Structures & Algorithms/is-anagram/submission-0.py"
spec = importlib.util.spec_from_file_location("solution", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print(module.Solution().isAnagram("anagram", "nagaram"))
print(module.Solution().isAnagram("rat", "car"))
PY
```

`submission-1.py` is the same call. `submission-2.py` and `submission-3.py` use the same method with a character-count implementation; point `path` at either file and run the same snippet.

`anagram-groups` and `duplicate-integer` annotate parameters with `List` and do not import it. `python3 -m py_compile` accepts those files. Importing them raises `NameError: name 'List' is not defined`.

After new solution files land, rebuild the table below:

```bash
python3 scripts/gen_index.py
```

`python3 scripts/gen_index.py --check` exits with an error when the table does not match the tree.

## Problems

`scripts/gen_index.py` generates this table from the files in the repository. Problem is the problem-folder name with `-` and `_` written as spaces. Category is the topic folder. Difficulty stays blank when the path does not include `easy`, `medium`, or `hard`. Language comes from the file extension.

<!-- INDEX:START -->

| Problem | Category | Difficulty | Language | Solution |
| --- | --- | --- | --- | --- |
| Anagram Groups | Data Structures & Algorithms |  | Python | [submission-0.py](Data%20Structures%20%26%20Algorithms/anagram-groups/submission-0.py) |
| Duplicate Integer | Data Structures & Algorithms |  | Python | [submission-0.py](Data%20Structures%20%26%20Algorithms/duplicate-integer/submission-0.py) |
| Duplicate Integer | Data Structures & Algorithms |  | Python | [submission-1.py](Data%20Structures%20%26%20Algorithms/duplicate-integer/submission-1.py) |
| Duplicate Integer | Data Structures & Algorithms |  | Python | [submission-2.py](Data%20Structures%20%26%20Algorithms/duplicate-integer/submission-2.py) |
| Duplicate Integer | Data Structures & Algorithms |  | Python | [submission-3.py](Data%20Structures%20%26%20Algorithms/duplicate-integer/submission-3.py) |
| Is Anagram | Data Structures & Algorithms |  | Python | [submission-0.py](Data%20Structures%20%26%20Algorithms/is-anagram/submission-0.py) |
| Is Anagram | Data Structures & Algorithms |  | Python | [submission-1.py](Data%20Structures%20%26%20Algorithms/is-anagram/submission-1.py) |
| Is Anagram | Data Structures & Algorithms |  | Python | [submission-2.py](Data%20Structures%20%26%20Algorithms/is-anagram/submission-2.py) |
| Is Anagram | Data Structures & Algorithms |  | Python | [submission-3.py](Data%20Structures%20%26%20Algorithms/is-anagram/submission-3.py) |

<!-- INDEX:END -->

## License

[MIT License](LICENSE). Copyright (c) 2026 Aneesh Pradhan.
