# kit-builder

A LADO kit that helps you build and evaluate LADO kits. Work in progress: the full README
(install, start, flows) comes with the first release.

Requires LADO 0.23 or newer.

## Tests

The complexity budget script (`skills/kit-budget/scripts/kit_budget.py`) has tests on small
fixture kits. Run them from the repository root with `uv`:

```bash
uv run --with pyyaml python -m unittest discover -s tests -v
```
