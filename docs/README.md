# flick user guide

Flick is a Python script for archiving publicly visible photos from a Flickr
photostream. It saves image files alongside selected API metadata in JSON.

- [Setup and run](#setup-and-run)
- [Output and verification](#output-and-verification)
- [Technical manuscript and build instructions](manuscript/README.md)

## Setup and run

You need Python 3, internet access, and a [Flickr API key and secret](https://www.flickr.com/services/apps/create/).
From the repository root, create a virtual environment and install the dependencies.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Set `FLICKR_API_KEY` and `FLICKR_API_SECRET` in your shell environment or
put them in an untracked `.env` file at the repository root.

```dotenv
FLICKR_API_KEY=your_key
FLICKR_API_SECRET=your_secret
```

To target another account, edit both `TARGET_USERNAME` and `TARGET_URL` in
[`flickr_scraper.py`](../flickr_scraper.py). The script looks up the username
first. If that lookup fails, it attempts to resolve the URL. The configured
username also determines the output folder name.

```bash
python flickr_scraper.py
```

The script requests up to 100 items per page and sleeps one second after each
processed item. It uses the first size label Flickr returns from the priority
list `X-Large`, `Large 2048`, `Large 1600`, `Large`, `Original`. If
none match, it uses the last returned entry, assuming Flickr ordered the list
by size. Set `X_LARGE_SIZE_LABEL` to change the first preference. The script
does not compare image dimensions.

## Output and verification

By default, files appear in `flickr_output/<TARGET_USERNAME>/` relative to the
working directory. An image and its sidecar share the stem
`<photo_id>_<sanitized_title>`. The title segment is capped at 50 characters.
The image extension comes from the download URL, with `.jpg` as the default.

Sidecars contain `id`, `title`, `description`, `tags`, `machine_tags`,
`date_taken`, `owner_name`, `views`, `media`, `latitude`, `longitude`,
`accuracy` and `flickr_url`. The size lookup adds an `available_sizes`
mapping from Flickr's labels to source URLs when the mapping can be built.
A failed size lookup or download can leave a sidecar with `download_error`
and no usable image. Tags are split on whitespace, and absent coordinates and
accuracy are stored as JSON `null`.

Check the console for page-fetch, download, and metadata-write errors. A failed
page fetch stops the loop and leaves files from earlier pages in place. A size
lookup failure can increment the failed/skipped counter twice, and a sidecar
write error is logged separately from the download counters. Reruns fetch
pages again and can overwrite files with matching names.

Open an image and inspect its matching sidecar. For example, substitute a real
sidecar path in this command and confirm that the `id` and `flickr_url`
identify the expected photo.

```bash
python -m json.tool "flickr_output/<username>/<photo_id>_<title>_metadata.json"
```

Keep credentials and downloaded files outside commits. Sidecars can include
coordinates from the public Flickr response.
