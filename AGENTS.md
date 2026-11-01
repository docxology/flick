# AGENTS.md — flick

Guidance for agents working in this repository.

## What this repository is

A single-script archiver for a public Flickr photostream. `flickr_scraper.py` walks the
photostream in pages of 100, downloads every photo at the largest available size, and writes
a JSON sidecar next to each image so the copy is self-describing: title, description, tags,
machine tags, capture date, owner, view count, media type, GPS coordinates and the available
size list. A `download_error` field records any photo that could not be retrieved.

Only publicly visible photos are retrieved.

## Commands

```bash
pip install -r requirements.txt
python flickr_scraper.py
```

Credentials come from a local `.env` file (`FLICKR_API_KEY`, `FLICKR_API_SECRET`), created at
https://www.flickr.com/services/apps/create/. The target photostream is set by the
`TARGET_USERNAME` and `TARGET_URL` constants near the top of `flickr_scraper.py`; editing them
is how you point it at another account.

Output lands in `flickr_output/<username>/`, two files per photo:

```
flickr_output/daniel_friedman/
  54321012345_A day at the coast.jpg
  54321012345_A day at the coast_metadata.json
```

Filenames combine the photo ID with a sanitized 50-character slug of the title, so they stay
unique and readable. The script pauses one second after each photo — each one costs a sizes
lookup plus a download — to stay inside Flickr's rate limits. It requests `X-Large` and falls
back to the largest size the API reports.

## Layout

| Path | Role |
|---|---|
| `flickr_scraper.py` | The whole program: constants, API client, paginator, size fallback, sidecar writer |
| `requirements.txt` | `flickrapi`, `requests`, `python-dotenv` |
| `docs/AGENTS.md` | Notes on the `docs/` folder itself |

There is no package manifest beyond `requirements.txt`, no test suite and no CI workflow.

## Working here

- **Never commit credentials or `flickr_output/`.** A `.gitignore` covers the output tree;
  keep it that way.
- Verify the sidecar field list against the script before documenting it — the README and any
  notes must not drift from what the code actually writes.
- The script has no automated checks. If you change the pagination, the size fallback or the
  filename scheme, say in your report what you changed and how you convinced yourself it
  still works; there is no gate that will catch a regression for you.

## Relationship to `docs/AGENTS.md`

`docs/AGENTS.md` documents the `docs/` folder only. This file is the repository-level entry
point; the two should not restate each other.
