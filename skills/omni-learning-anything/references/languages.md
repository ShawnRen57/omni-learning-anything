# Learn a foreign language through your own language

Use this route for “我是零基础，用中文带我学日语”, “Teach me German in English”, or an agreed continuation of a foreign-language course. Translate a one-off sentence directly if that was the whole request. Keep the usual plan, approval and local delivery flow. No rich cards, account, special launcher or extra model are required.

## Build the route

Ask which language the learner already understands, which language/variety they want to use, their starting point and one concrete situation. Reuse anything already said. Agree the available days and minutes. For a true beginner, let them start with zero knowledge. If their level is uncertain offer one short example or self-placement. Choose actual sources in the target variety and verify the expressions, meanings and register. For a low-resource pair or a regional variety, seek credible material or a learner-provided reference and narrow the scope to what can be checked.

Use the native language for explanations and task instructions, and the target language in its normal script for examples and answers. Store real language names in `config.language_course`; the existing `config.language` controls document labels. If those labels are unavailable for the native language, agree on a supported label language while keeping the authored explanations in the requested native language. Check script shaping, font coverage, direction, and mixed-script punctuation in the actual output.

```json
{"language":"zh","language_course":{"native":"中文","target":"日本語","starting_point":"零基础","goal":"能在第一次参加日语课时问候、介绍自己并请求重复"}}
```

With the learner's goal, make a path of manageable blocks. Assign each day a `can_do` statement in the native language next to its normal day number/topic. Include the visible day-by-day outcomes, review opportunities and a final task in the plan's rendered sections. Adapt the number of days and amount of new material to the learner's time. A short travel block may stop after independently completing a small exchange.

| Block | Teaching and practice | Evidence to carry into the next block |
| --- | --- | --- |
| First encounter | Recognize a few high-utility forms. Show script direction, how to segment one expression, and where a sound or writing convention differs from the learner's language. Use transliteration only when it helps, alongside the original form. | Select the appropriate expression in a familiar situation, then produce another from a native-language cue. |
| First independent exchange | Vary one part of a short dialogue, such as a name, quantity or formality level. Revisit earlier expressions after time has passed. | Perform a short task without a phrase bank. Keep reading, writing, listening and speaking evidence distinct. |
| Everyday combinations | Combine known functions into a new situation. Teach any additional prerequisite before testing it. Fade translation as the learner requests and can handle. | Respond to a change in a scenario, ask for clarification, or repair a misunderstanding. |
| Next domain or level | Upon agreement, extend to a personally relevant domain using authentic, source-located input, longer turns and feedback. Reuse the normal continuation/proposal workflow. | Record specific tasks and assistance, compare against the next goal, and show the new plan for approval. |

Use CEFR can-do descriptors when useful for scoping. The learner selects a practical outcome. A completed block, a count of lessons or one translated sentence cannot establish a whole CEFR level. [Council of Europe framework and descriptors](https://www.coe.int/en/web/common-european-framework-reference-languages/cefr-descriptors)

## Teach one lesson

1. Open with one achievable situation and a small dialogue or reading. Cite the checked usage or source passage in the visible teaching section. Write the target expression, its contextual native meaning and one usage clue. Add a specific cue for pronunciation, writing or register when it changes understanding. Use starting-script supports, then fade them. Separate approximate romanization from audio evidence.
2. Make the figure answer a specific question, e.g. which greeting fits each point in the day, which part of the sentence changes with the speaker, or which mouth position distinguishes two sounds. Include the exact contrast in its labels and caption. In textbook mode keep the bound original illustration.
3. Record one or more reviewed expressions in the lesson JSON. Select a small enough set for the actual session time. Each form, contextual meaning and source marker must appear together in the referenced teaching section. Include enough context in the meaning to distinguish register or grammatical forms; explain legitimate variants in prose.
4. Give a recognition task (target → native), then ask for productive recall on a *different* expression (native → target). Keep the sheet apart from the model answers. For a one-item mini-lesson, reverse direction on a later day. Revisit previous delivered material using the same archive.
5. Offer a separate situational check. Prepare ordinary source-bound `quiz` questions with a new scenario; use the real learner's request before starting. Give open production questions a meaning/usage rubric that accepts equivalent forms, spelling conventions and culturally appropriate variants. Count pronunciation or comprehension of audio only when the learner actually heard/replied to a verified recording and there is evidence for the specific skill. Do not score oral proficiency from typed answers or infer practice from opening a worksheet.

```json
{"sections":[{"title":"早上遇见老师","body":"おはようございます 表示礼貌的早上好。朝刚认识的老师问好时，可以用这一句。[S1]"}],
 "language_items":[{"form":"おはようございます","meaning":"礼貌的早上好","section_index":0,"source_id":"S1"}]}
```

Render and review through the normal course commands. Then generate an answer-free Markdown worksheet, which works in a text editor or a printable document. The answer key is produced separately when requested. Earlier days must have actual delivery records and the requested current lesson must be reviewed. These commands leave lesson delivery and learner observations intact. The worksheet only tests expressions already taught. If you need new situations, use the reviewed quiz flow.

```sh
OMNI language worksheet --key Day01
OMNI language answer-key --key Day01
OMNI language worksheet --key Day01 --reverse
OMNI language answer-key --key Day01 --reverse
OMNI language worksheet --key Day04 --review-from Day01 --review-from Day03
OMNI language answer-key --key Day04 --review-from Day01 --review-from Day03
```

Use `--reverse` for a second pass on the same expressions in the opposite direction; generate the corresponding key with the same arguments. Each command returns its file path under the course's local `learning/` directory. Send only the worksheet before the learner attempts it. When the learner requests feedback, open the corresponding key and compare meaning and register with the source. A key gives model responses, so accept equivalent valid answers. Optional listening can use an appropriate source recording. If the host has a matching system voice, the separate `language-audio --locale ja-JP --text 'おはようございます。' --output audio/listening-01.wav` command can produce a local synthesized model. Keep answer transcripts separate from listening prompts. Offer text exercises when audio is unavailable.

**Mixed-script PDFs.** Inspect the actual exported page wherever native explanations meet target-language text. For Arabic, read a whole phrase and check its right-to-left word order inside the sentence. For Japanese and Korean, check the exact kanji, kana or Hangul used, including headings. The PDF renderer selects fonts and direction for these runs. Other writing systems, such as Devanagari, need a font and layout engine that cover the script. When a required glyph, mark or shaping feature fails, use a verified readable HTML or DOCX for that lesson after agreeing the format with the learner, or configure and retest a suitable PDF template. Keep the authored original script in every format.
