# Flick technical manuscript

This directory contains the canonical source for *Flick: Archiving a Public
Flickr Photostream*, a software methods manuscript. The renderer assembles
the numbered Markdown files in order, reads `config.yaml` and `preamble.md`,
and uses `references.bib` for citations. The workflow figure is a checked-in
PNG with its Graphviz source under [assets](assets/).

To regenerate the figure after editing its source, run Graphviz from this
directory.

```bash
dot -Tpng assets/archive-workflow.dot -o assets/archive-workflow.png
```

## Render and validate

Use a fresh Git checkout named `flick` and a separate checkout of the
[pinned template](https://github.com/docxology/template/tree/87704feae0a4490ef7dad9c931d268e8c30273c2).
Install Git, uv, Pandoc, XeLaTeX, and the TeX packages listed in the template's
[setup guide](https://github.com/docxology/template/blob/87704feae0a4490ef7dad9c931d268e8c30273c2/docs/guides/startup-and-setup.md).
The manuscript build uses the template's Python environment and requires
neither Flickr credentials nor downloaded photos.

Run the following from the root of the Flick checkout you want to render.

```bash
flick_checkout="$(pwd -P)"
mkdir -p output/figures
cp docs/manuscript/assets/archive-workflow.png output/figures/

template_checkout="$(mktemp -d)/template"
git clone https://github.com/docxology/template.git "$template_checkout"
git -C "$template_checkout" checkout --detach 87704feae0a4490ef7dad9c931d268e8c30273c2
cd "$template_checkout"
uv sync --locked
mkdir -p projects/working
ln -s "$flick_checkout" projects/working/flick
uv run --no-sync python scripts/pipeline/stage_03_render.py --project working/flick
uv run --no-sync python scripts/pipeline/stage_04_validate.py --project working/flick
```

The copy stages the authored workflow image where the PDF renderer looks
for figures. The registered checkout resolves directly to `docs/manuscript/`. The PDF
lands in `output/pdf/` in the Flick checkout, with the assembled edition
named `*_combined.pdf`. Open it and check the abstract, archiving method,
verification and limitations sections, the workflow figure, and the three
references. Check the validation result before sharing the PDF.
