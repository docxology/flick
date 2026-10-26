# flick — Agent Guide

## Layout

Single-module script repository. `flickr_scraper.py` contains configuration
constants (`TARGET_USERNAME`, `TARGET_URL`), the Flickr API client, the
paginator (100 per page, 1s after each photo), size fallback (X-Large → largest
available), and the metadata sidecar writer.

## Conventions observed

- No package manifest: dependencies are `requirements.txt`
  (`flickrapi`, `requests`, `python-dotenv`); credentials come from a local
  environment file documented in the root `README.md`.
- Output is self-describing: each image file has a same-stem
  `_metadata.json` sidecar; filenames are `<photo_id>_<50-char title slug>`.

## How docs here are maintained

Root `README.md` is the user reference. Keep `docs/README.md` a short pointer
to it plus the real install/run commands; update both together if the script's
constants or output layout change.

## Notes for agents

- Never commit credentials files or `flickr_output/` output.
- Verify field lists against the script before documenting sidecar contents.
