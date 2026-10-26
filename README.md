# flick

Bulk-archive a public Flickr photostream — every photo at the largest available size, each one paired with a JSON sidecar holding its full metadata.

Useful when you want a local, self-describing copy of a photostream rather than a folder of anonymous JPEGs: titles, tags, capture dates, GPS coordinates, and view counts all travel with the image.

## Requirements

```bash
pip install -r requirements.txt
```

Create a `.env` file with credentials from https://www.flickr.com/services/apps/create/:

```
FLICKR_API_KEY=your_key
FLICKR_API_SECRET=your_secret
```

## Usage

```bash
python flickr_scraper.py
```

The target photostream is set by the `TARGET_USERNAME` and `TARGET_URL` constants near the top of `flickr_scraper.py` — edit those to archive a different account.

## Output

Files land in `flickr_output/<username>/`, two per photo:

```
flickr_output/daniel_friedman/
  54321012345_A day at the coast.jpg
  54321012345_A day at the coast_metadata.json
```

Each sidecar records:

`id`, `title`, `description`, `tags`, `machine_tags`, `date_taken`, `owner_name`, `views`, `media`, `latitude`, `longitude`, `accuracy`, `flickr_url`, `available_sizes` — plus `download_error` if a photo could not be retrieved.

## Behavior

Photos are fetched in pages of 100 and the script pauses one second after each photo (each one costs a sizes lookup plus a download) to stay well inside Flickr's rate limits. It requests the `X-Large` size and falls back to the largest size the API reports as available. Filenames combine the photo ID with a sanitized, 50-character slug of the title, so they stay unique and readable.

Only publicly visible photos are retrieved.
