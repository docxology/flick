# Limitations

The program stops paging after an error escapes the page-processing loop,
leaving the files already written. Its reported failed/skipped count can
include two increments for a photo when the size lookup fails, so that
counter is not a count of distinct failed photo IDs. A later run starts at
page one and may overwrite files with matching names.

The archive captures selected fields from a public API response. It omits
other material such as album organization and photo comments. Listing
contents and download availability can change between or during runs.
Credentials and download permissions can also affect what can be
retrieved. The workflow diagram summarizes control flow from source code.
No live-archive coverage or performance measurement is presented here.
