# flick — Documentation

`flick` is a single-script bulk archiver for a public Flickr photostream: every
photo at the largest available size, each paired with a JSON sidecar holding
its full metadata (title, tags, dates, GPS, views).

## Repository map

- `flickr_scraper.py` — the entire tool (target account configured via
  `TARGET_USERNAME` / `TARGET_URL` constants near the top)
- `requirements.txt` — `flickrapi`, `requests`, `python-dotenv`
- `flickr_output/<username>/` — generated at runtime: one image (the size
  Flickr serves, `.jpg` by default) + one `_metadata.json` per photo

## Running

```bash
pip install -r requirements.txt
# create a Flickr API credentials file per root README (key + secret)
python flickr_scraper.py
```

Only publicly visible photos are retrieved. Details of rate-limit behavior,
size fallback, and sidecar fields: root `README.md`.
