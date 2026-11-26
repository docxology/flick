# AGENTS.md — flick

`flickr_scraper.py` is the single program module. Its dependencies are listed
in `requirements.txt`. The repository has no automated tests or CI workflow.

- [User guide](docs/README.md) documents setup, run configuration, and outputs.
- [Manuscript guide](docs/manuscript/README.md) documents the canonical
  manuscript source and render workflow.

Never commit credentials or `flickr_output/`. Check changes to pagination,
size selection, filenames, or the sidecar schema against the implementation
and exercise the relevant path when modifying it.
