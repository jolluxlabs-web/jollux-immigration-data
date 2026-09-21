# Contributing

1. Open an issue before making a large schema or public API change.
2. Create a focused branch and keep unrelated website or deployment code out of this repository.
3. Add tests using synthetic records only.
4. Run `pytest` before submitting a pull request.
5. Document new source columns, normalization behavior, and compatibility assumptions.

Do not submit credentials, environment files, private records, production exports, or bulk DOL datasets. Small fixtures must be invented and must not reproduce real cases.
