# Teaching figures

Choose an image after deciding what the learner should discover by looking at it. Define a question with a visible answer. If the reader could cover the picture and lose no evidence, choose a better example or visual form.

| What the learner needs to do | Suitable visual | What must be visible |
| --- | --- | --- |
| Compare two cases | Aligned comparison or a small chart | Comparable features, units or contrasting forms on the same row |
| Follow a process or transformation | Labeled sequence | Order, change at each step and the meaning of the arrows |
| Interpret a map, painting, artifact or photo | A relevant original or licensed reproduction | A recognizable detail, where to look and why that detail matters |
| Read a textbook or inspect source material | The verified original page crop | The specific marks or relationships used in the explanation, with original provenance |
| Understand a numerical relationship | A plot from checked values, axes with units and legend when needed | Scale, denominator, source and visible trend; distinguish observed data from a constructed example |
| Learn a language | Aligned sentence patterns, pronunciation contrasts or a labeled scene for concrete words | The target form connected to its meaning or use; preserve diacritics and scripts |

**Authoring.** For new courses use `"visual_guides": true` in config. In every plan and lesson include `figure.reading`. Its `question` tells the reader what to look for, `observation` explains how a particular mark, label or comparison answers it, and `source_ids` names real entries in the same document. The reading guide appears next to the figure in PDF, HTML, DOCX and Markdown. In strict material courses use selected material references; for textbooks cite the crop's actual page. Use course-language labels and the learner's target script where relevant. Add an in-text reference pointing back to a specific feature of the figure.

**Draw or acquire.** Use `figure-build` for concise comparisons, sequences and aligned fraction bars. It produces a PNG locally using Pillow. For quantitative plots use a suitable charting tool; for visual analysis use a real artifact or photograph with documented reuse rights. Use a host image model for a scene when the learner needs to observe its objects or spatial relationships. Check AI artwork against teaching sources, and retain prompt provenance and disclosure. Do not rely on a generated painting, map or scientific reconstruction as original evidence. In textbook mode always use `textbooks figure` for the unaltered original crop and attach the reading guide to its returned JSON. A diagram cannot replace that crop.

## Draw a teaching figure

Write a small JSON spec, then run:

```sh
python scripts/omni_learning.py --project /actual/course figure-build --input /actual/diagram.json
```

For a comparison include two or three column labels, and one to four rows with exactly one value per column. For a sequence replace columns and rows with two to four `steps`, each with `label` and `detail`. Choose the left-to-right sequence only for material that is naturally read that way. Use a suitable host renderer when the lesson needs different geometry. Write labels short enough to stay legible. For example:

```json
{
  "layout": "comparison",
  "title": "One sentence in two forms",
  "columns": ["Statement", "Yes/no question"],
  "rows": [
    {"label": "They", "values": ["They sing.", "Do they sing?"]},
    {"label": "She", "values": ["She sings.", "Does she sing?"]}
  ],
  "credit": "Original examples based on the cited grammar reference.",
  "reading": {
    "question": "Follow the second row. Which word marks the change to a singular subject in the question?",
    "observation": "Compare ‘sings’ in the statement with ‘Does ... sing’ in the question. The question carries the distinction on its auxiliary.",
    "source_ids": ["S1"]
  }
}
```

Use a real reference in the document, such as the [British Council grammar reference](https://learnenglish.britishcouncil.org/free-resources/grammar/english-grammar-reference/present-simple) for this example. Copy the returned figure object into the document. The PNG is content-addressed inside the course assets directory. For multilingual labels the helper checks installed font coverage. Use `--font /path/to/installed/font.ttf` if needed. Right-to-left and complex-script labels such as Arabic and Devanagari require Pillow with libraqm. Where a suitable font or renderer is unavailable, acquire or render a verified diagram through another host tool.

For a comparison of parts of the same whole, choose `"layout": "fraction-bars"`. Put the shared whole and unit in `unit` (for example, “Every full strip is one metre”). Supply two to four `bars`, each with integer `numerator` and `denominator`. A denominator of 1–16 keeps equal subdivisions legible. The numerator may range from zero to the denominator. For example, use `[{"numerator":1,"denominator":2},{"numerator":2,"denominator":4}]` to show how different partitions end at the same midpoint. All bars share endpoints 0 and 1. The generator draws the midpoint guide, computes the fraction labels and uses the stated denominator to place subdivisions.

**Review the finished page.** Inspect the export at its normal reading size. Read the question using the figure alone, then check the answer and every relation against the cited material. Confirm arrows point the right way, quantities and scales agree, distinct categories can be read without color, and labels are legible without clipping or missing glyphs. Write in the review note the feature you inspected and the inference it supports. A passed file or metadata check establishes neither visual accuracy nor learning value.
