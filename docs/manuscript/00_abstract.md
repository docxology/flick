# Abstract

Flick is a Python utility that pairs files downloaded from a public Flickr
photostream with JSON sidecars. Its workflow resolves an account, lists public
photos in pages, and selects a download URL from the sizes returned for
each photo. The sidecar preserves selected listing fields and can record an
error even when the image is unavailable. This technical manuscript describes
the implementation, the decisions that shape the archive, and checks an
operator can perform on the resulting files.
