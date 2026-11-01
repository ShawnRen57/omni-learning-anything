# University course catalog: sources and verification

Checked: **2026-11-01**. This ledger accompanies `skills/omni-learning-anything/references/course-catalog.json` (schema 1). It covers twelve deliberately selected courses, not a ranking or a claim about popularity.

## What the catalog represents

Course identity, named edition, published order, and original workload statements are grounded in the linked university or instructor pages. Unit titles and focus statements are concise, original Chinese paraphrases for navigation. Grouping into 6–12 units, audience suggestions, and learning preparation explicitly marked as recommendations are editorial adaptations. They are approximate learning blueprints, not transcripts, exact teacher quotations, university endorsements, credit-bearing enrollment, or a replacement for the original assignments.

Every unit preserves a contiguous portion of its source sequence. A locator names the original lecture, calendar session, week, or dated syllabus rows; `source_id` points to a source within that course. In a grouped unit spanning several music pages, the locator also lists the related source IDs. Session numbering is never silently treated as video numbering. Exams, guest sessions and reviews remain in their published positions where the source lists them.

`syllabus_and_sessions` means a syllabus or course/requirements description and an ordered session schedule were inspected. It does not mean every recording, reading or assignment was reviewed. `syllabus_only` means the published tentative schedule was inspected but an actual delivered session sequence was not established. `checked_at` is the source-check date, not a guarantee that a live URL will remain unchanged.

## Evidence by course

### Positive Psychology — PSY 1504 (Spring 2006)

The two-page Spring 2006 PSYCHOLOGY 1504 syllabus names Tal Ben-Shahar. This is a Harvard syllabus hosted by the University of Pennsylvania Positive Psychology Center, hence `university_archive`. The tentative schedule has **25 dated entries** from February 2 to May 4, including the March 21 midterm and March 23 review. It is grouped into twelve units without dropping either entry. Spring break stays between review and perfectionism. The final project and final exam are grading requirements; the document does not date the final exam. No claim is made that a circulating video playlist has exactly these sessions.

- **O1** [PSYCHOLOGY 1504 syllabus](https://ppc.sas.upenn.edu/sites/default/files/ppsyllabusschachar.pdf) — pp.1–2: Tentative Schedule; Grading; university_archive; checked 2026-11-01.

### CS50’s Introduction to Computer Science — CS50x (2026 (year URL redirects to current syllabus))

The requested 2026 URL redirects to `/x/syllabus/`; the fetched page identifies CS50x 2026. Preserve the year URL and check date because the redirect target can change. Week 0 through Week 10 and the separate AI supplement are retained; AI appears between SQL and Week 8. Ten problem sets and a final project are the published expectations. Grouping is editorial, not an eight-week university schedule.

- **O1** [CS50x 2026 syllabus](https://cs50.harvard.edu/x/2026/syllabus/) — Syllabus; navigation Weeks 0–10; Artificial Intelligence; Expectations; official; checked 2026-11-01.

### Justice — Justice (public lecture series) (Official 24-lecture sequence; term not stated on source)

The instructor’s Harvard page supplies a 24-lecture sequence with twelve paired video links and topic descriptions. It does not establish a semester or course code for this public series, so the edition and code fields say so instead of assigning an unverified year. Original credit-course meeting hours and assessments were not established from this page.

- **O1** [Justice — Michael J. Sandel](https://sandel.scholars.harvard.edu/justice) — Lectures 1–24, paired video links and descriptions; official; checked 2026-11-01.

### Introduction to Psychology — PSYC 110 (Spring 2007)

Open Yale Courses establishes Paul Bloom, Spring 2007 and PSYC 110. Its Sessions list includes twenty numbered lectures, two separately numbered guest lectures and two exams. Both guest entries and both exams remain in sequence. Requirements include reading responses, a book review and experimental participation, beyond watching the recordings.

- **O1** [PSYC 110 — Open Yale Courses](https://oyc.yale.edu/introduction-psychology/psyc-110) — Course Structure; Syllabus; Sessions; official; checked 2026-11-01.

### Financial Markets — ECON 252 (Spring 2011)

Use the **2011** ECON 252 offering, not the different 2008 edition. The page establishes Shiller, elementary algebra/calculus preparation and two midterms plus a final. All 23 numbered lectures, including guest speakers, and all three exam entries are covered. Historical financial examples and institutional descriptions are not current investment guidance.

- **O1** [ECON 252 (2011) — Open Yale Courses](https://oyc.yale.edu/economics/econ-252) — Course Structure; Requirements; Sessions; official; checked 2026-11-01.

### Game Theory — ECON 159 (Fall 2007)

The page establishes Ben Polak, Fall 2007 and ECON 159; it explicitly requires introductory microeconomics and uses calculus, probability and expectation. Its 24 lectures and two exams are covered. Intermediate microeconomics is recommended on the source, not a mandatory prerequisite.

- **O1** [ECON 159 — Open Yale Courses](https://oyc.yale.edu/economics/econ-159) — Requirements; Course Structure; Sessions; official; checked 2026-11-01.

### Death — PHIL 176 (Spring 2007)

The page establishes Shelly Kagan, Spring 2007 and PHIL 176. All 26 lectures remain in order. The original assessment is discussion plus three short papers, explicitly with no final exam. The concluding philosophical discussion of suicide is represented as an argument-analysis topic, not personal advice or an instruction to act.

- **O1** [PHIL 176 — Open Yale Courses](https://oyc.yale.edu/death/phil-176) — Course Structure; Requirements; Sessions; official; checked 2026-11-01.

### Listening to Music — MUSI 112 (Fall 2008)

The course landing URL returned HTTP 403 in the web fetcher and direct fetches. All **23 individual official lecture pages** were successfully inspected instead, including their numbered titles and overview/chapter sections. The official Lecture 1 HTML links to `/sites/default/files/courses/fall08/musi112/mp3/musi112_01_090408.mp3`, supporting the Fall 2008 edition without downloading the media. Lecture 1 also explains the listening exercises, textbook and course requirements; the landing-page weekly meeting hours were not independently rechecked. The YaleCourses video is an additional official distribution link; the fetched YouTube shell did not expose its description, so it is not the sole evidence for the edition. The final review, Lecture 23, is retained. Music recordings and images are linked, never redistributed.

- **O1** [MUSI 112 Lecture 1](https://oyc.yale.edu/music/musi-112/lecture-1) — Lecture 1: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O2** [MUSI 112 Lecture 2](https://oyc.yale.edu/music/musi-112/lecture-2) — Lecture 2: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O3** [MUSI 112 Lecture 3](https://oyc.yale.edu/music/musi-112/lecture-3) — Lecture 3: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O4** [MUSI 112 Lecture 4](https://oyc.yale.edu/music/musi-112/lecture-4) — Lecture 4: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O5** [MUSI 112 Lecture 5](https://oyc.yale.edu/music/musi-112/lecture-5) — Lecture 5: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O6** [MUSI 112 Lecture 6](https://oyc.yale.edu/music/musi-112/lecture-6) — Lecture 6: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O7** [MUSI 112 Lecture 7](https://oyc.yale.edu/music/musi-112/lecture-7) — Lecture 7: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O8** [MUSI 112 Lecture 8](https://oyc.yale.edu/music/musi-112/lecture-8) — Lecture 8: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O9** [MUSI 112 Lecture 9](https://oyc.yale.edu/music/musi-112/lecture-9) — Lecture 9: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O10** [MUSI 112 Lecture 10](https://oyc.yale.edu/music/musi-112/lecture-10) — Lecture 10: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O11** [MUSI 112 Lecture 11](https://oyc.yale.edu/music/musi-112/lecture-11) — Lecture 11: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O12** [MUSI 112 Lecture 12](https://oyc.yale.edu/music/musi-112/lecture-12) — Lecture 12: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O13** [MUSI 112 Lecture 13](https://oyc.yale.edu/music/musi-112/lecture-13) — Lecture 13: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O14** [MUSI 112 Lecture 14](https://oyc.yale.edu/music/musi-112/lecture-14) — Lecture 14: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O15** [MUSI 112 Lecture 15](https://oyc.yale.edu/music/musi-112/lecture-15) — Lecture 15: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O16** [MUSI 112 Lecture 16](https://oyc.yale.edu/music/musi-112/lecture-16) — Lecture 16: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O17** [MUSI 112 Lecture 17](https://oyc.yale.edu/music/musi-112/lecture-17) — Lecture 17: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O18** [MUSI 112 Lecture 18](https://oyc.yale.edu/music/musi-112/lecture-18) — Lecture 18: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O19** [MUSI 112 Lecture 19](https://oyc.yale.edu/music/musi-112/lecture-19) — Lecture 19: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O20** [MUSI 112 Lecture 20](https://oyc.yale.edu/music/musi-112/lecture-20) — Lecture 20: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O21** [MUSI 112 Lecture 21](https://oyc.yale.edu/music/musi-112/lecture-21) — Lecture 21: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O22** [MUSI 112 Lecture 22](https://oyc.yale.edu/music/musi-112/lecture-22) — Lecture 22: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O23** [MUSI 112 Lecture 23](https://oyc.yale.edu/music/musi-112/lecture-23) — Lecture 23: Overview; Lecture Chapters; transcript; official; checked 2026-11-01.
- **O24** [YaleCourses: 1. Introduction](https://www.youtube.com/watch?v=5_yOVARO2Oc) — Description: course recorded Fall 2008; official; checked 2026-11-01.

### Introduction to Computer Science and Programming in Python — 6.0001 (Fall 2016)

MIT OCW establishes Fall 2016, 6.0001, Ana Bell, Eric Grimson and John Guttag. The lecture gallery gives twelve lectures. The syllabus identifies a half-semester course using Python 3.5, six problem sets and two quizzes. Original software versions and assignment requirements are historical; modern execution may need adaptation.

- **O1** [6.0001 lecture videos](https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/video_galleries/lecture-videos/) — Lectures 1–12; Course Info; official; checked 2026-11-01.
- **O2** [6.0001 syllabus](https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/pages/syllabus/) — Course Meeting Times; Course Information; Problem Sets and Quizzes; official; checked 2026-11-01.

### Linear Algebra — 18.06 (Spring 2010)

MIT OCW establishes Gilbert Strang and Spring 2010. Units follow **Calendar SES 1–40**, including reviews and exams, rather than substituting the differently numbered video gallery. The syllabus lists 18.02 multivariable calculus as the original prerequisite and three in-class exams plus a final. Later textbook/video additions on OCW do not change the selected edition.

- **O1** [18.06 calendar](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/calendar/) — SES # 1–40; Course Info; official; checked 2026-11-01.
- **O2** [18.06 syllabus](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/syllabus/) — Meeting Times; Prerequisites; Homework; Exams; official; checked 2026-11-01.

### Classical Mechanics — 8.01SC (Fall 2016)

MIT OCW establishes the Fall 2016 8.01SC edition and its five listed instructors. The published sequence is vector review plus Weeks 1–12 / Lessons 0–37, including optional Deep Dives in their places. The syllabus specifies no prerequisites, with single-variable calculus as a corequisite. The catalog does not replace that statement with an invented high-school prerequisite.

- **O1** [8.01SC course sequence](https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/) — Review: Vectors; Weeks 1–12; Lessons 0–37; Course Info; official; checked 2026-11-01.
- **O2** [8.01SC syllabus](https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/pages/syllabus/) — Course Meeting Times; Prerequisites; Course Overview; official; checked 2026-11-01.

### Machine Learning — CS229 (Autumn 2018)

The Autumn 2018 schedule is the authority for Lectures 1–20, A0–A4, the November 7 take-home midterm and December project milestones. Lectures 3–4 share a topic cell in the published table; the catalog groups them rather than inventing a per-lecture split. The archived department schedule search result identifies CS229 instructor Ng, corroborated by Stanford Online’s official Autumn 2018 Lecture 1 listing. Department and syllabus meeting-time displays differ; the pace field follows the course syllabus. Programming/mathematics preparation is labeled an editorial recommendation because a 2018 admission-prerequisite page was not recovered. Piazza-only submission details were not accessed.

- **O1** [CS229 Autumn 2018 schedule](https://cs229.stanford.edu/syllabus-autumn2018.html) — Lectures 1–20; A0–A4; Midterm; Project; official; checked 2026-11-01.
- **O2** [Stanford CS Autumn 2018–2019 course schedule](https://legacy.cs.stanford.edu/courses/schedules/2018-2019.autumn.php) — CS229 row (Ng); used for instructor identity only; official; checked 2026-11-01.
- **O3** [Stanford Online: CS229 Lecture 1 (Autumn 2018)](https://www.youtube.com/watch?v=jGwO_UgTS7I) — Title and description identify Andrew Ng and edition; official; checked 2026-11-01.

## Reuse and maintenance

The repository stores only short original descriptions, factual identity metadata, locators and links. It does not copy lecture notes, transcripts, full syllabi, solutions, images or recordings. Public access to a source does not establish permission to redistribute third-party material inside it. External platform deadlines, certificates, software environments and present-day institutional facts should be rechecked before relying on them.

When updating a course, verify identity and edition first, then compare the full ordered schedule. Preserve the stable course ID; change the edition and evidence fields explicitly when adopting a different offering. Do not combine a newer syllabus with an older lecture order without documenting the difference. Do not fill a missing source with model recollection.
