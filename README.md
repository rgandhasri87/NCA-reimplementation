### Setup ###
Note: installation of dependencies on a machine with a GPU may be slightly more involved. The user likely needs to add a `[[tool.uv.index]]` element to `pyproject.toml` with the correct pytorch source wheel.

On CPU-only machines, setup is as simple as:
1. Install `uv` (see [installation docs](https://docs.astral.sh/uv/getting-started/installation/))
2. Clone the repo
3. Run `uv sync`