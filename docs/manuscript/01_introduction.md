# Introduction

A directory of downloaded images retains the file bytes but often lacks the
titles, tags, and page URLs used to find those images on Flickr. Flick stores
a JSON file beside each downloaded image to keep selected Flickr fields
available for local inspection. The photo ID anchors the pair. The title
serves as a human-readable filename component and is also stored in full in
the sidecar [@flick-software].

The scope is the public listing exposed by the Flickr API. The utility
operates with an application key and secret and does not perform a user
OAuth sign-in. Its output represents what Flickr exposes and what the
script can retrieve during a run.
