# Verifying an archive

Inspect the console for page-fetch and file-write errors. In the output
directory, open sample image files and load their sidecars as JSON. Check
that the filename ID matches the sidecar ID and that the Flickr page URL
identifies the same photo. Inspect unpaired sidecars for a
`download_error` value. A missing or unreadable sidecar also warrants
checking the console because a write error is reported independently of
the image download counters.

The available-size map records Flickr's labels and source URLs at lookup
time. Additional sidecar fields describe the listing entry, including
description, tags, date taken, view count, media type, and any available
coordinates and location accuracy. These fields reflect the API response
and can be absent or empty. The sidecar does not record the selected size
label or a checksum of the downloaded image.
