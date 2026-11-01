"""Source-grounded, originally authored multilingual course samples for v3.0.0.

The six-day routes cover only the first three catalog groups.  Explanations,
worked examples and questions are our teaching material, not lecture transcripts.
"""

CHECKED_AT = "2026-11-01"


def _sections(items):
    return [{"title": title, "body": body.strip()} for title, body in items]


def _days(items):
    return [{"day": i, "topic": topic, "course_units": [f"u{(i + 1) // 2:02d}"],
             "objective": objective} for i, (topic, objective) in enumerate(items, 1)]


def _source(id, title, url, publisher, note, published_at):
    return dict(id=id, title=title, url=url, publisher=publisher, note=note,
                checked_at=CHECKED_AT, published_at=published_at)


SAMPLES = [
    {
        "slug": "positive-psychology-zh", "course_id": "harvard-positive-psychology",
        "language": "zh", "title": "积极心理学：从好问题开始",
        "days": _days([
            ("把幸福感变成可以研究的问题", "区分个人体验、可检验的问题和过度承诺。"),
            ("为什么需要积极心理学", "在关注困难之外提出关于优势与良好生活的问题。"),
            ("基本前提：从口号到假设", "把宽泛的信念改写为带条件的可检验判断。"),
            ("信念如何进入行动循环", "用假设情境区分预期、行为与结果。"),
            ("注意焦点：观察到了什么", "发现选择性观察可能遗漏的信息。"),
            ("改变：提出一个小检验", "设计低负担观察并承认因果推断的局限。"),
        ]),
        "plan_sections": _sections([
            ("课程版本与这六天的边界", """本路线依据 Tal Ben-Shahar 的 Harvard PSYCHOLOGY 1504 — POSITIVE PSYCHOLOGY，2006 年春季教学大纲。大纲保存在宾夕法尼亚大学积极心理学中心网站，列明课程主题与日期。[S1] 我们只选前三个目录分组：课程起点与积极心理学、基本前提与信念、注意焦点与改变。六天是局部入门，不等于修完原课，也不涵盖后面的健康、目标、关系等全部内容。
本页没有取得并核实该课第一讲的官方逐字稿。因此，第一天以独立学术来源建立研究视角；解释、虚构情境与问题均为本指南原创，不冒充教授讲义。阅读时请把“大纲确认的课程安排”和“本指南帮助理解的教学示例”分开。"""),
            ("每天十分钟怎样使用", """每天七分钟读一小节并看图，三分钟做两道轻问题。可以口头回答，不需要长日记、公开个人经历或上传记录。读得慢时，只保留当天的概念和一个例子，原始材料放在额外时间打开。十分钟是本指南的学习预算，不是原课课时换算，也不包含完整视频、论文与原课作业。
建议把一个小问题留到第二天：今天的说法究竟是定义、观察，还是对原因的猜测？这个问题能连接全部六天。遇到令人困惑的结论，先用问号标记，不必立刻接受或反对。"""),
            ("第一、二天：学会问一个可研究的问题", """第一天“把幸福感变成可以研究的问题”属于 u01，先区别短暂感受与研究对象，用虚构的学习小组练习提问。第二天“为什么需要积极心理学”仍属于 u01，将困难、已有能力和环境支持放在同一张观察表里。你只需选出一个可以比较的问题，说明比较的对象与时间；不需要给自己打一个“幸福总分”。
完成这两天的标志，是能把“每个人都应该更快乐”改写为一个有范围的问题，并说清楚这个问题暂时回答不了什么。"""),
            ("第三至六天：沿原课前段继续", """第三天“基本前提：从口号到假设”和第四天“信念如何进入行动循环”对应 u02。我们会用本指南编写的例子，把一句断言拆成预期、行动和反馈，而不是把成功归结为态度。第五天“注意焦点：观察到了什么”和第六天“改变：提出一个小检验”对应 u03；重点是辨认遗漏、考虑另一种解释，再提出可撤回的小观察。这些日题是微学习切口，不是原课讲次标题，也不保证覆盖所在分组的所有内容。
六天结束只做一次口头复述：我在研究什么、我凭什么这样说、什么证据会让我修改判断。若第三个问题答不上来，就把它作为下一轮学习的起点。"""),
            ("怎样判断学到了，而不只是觉得受鼓舞", """采用三个朴素标准：能区分陈述类型；能指出例子里未控制的因素；能提出比原来更具体的问题。一次心情改善是值得珍惜的经历，但不能单独证明某方法对所有人有效。反过来，一天没有变化也不能推翻整个研究方向。我们的练习用于理解研究问题，不是筛查、诊断或疗效测试。
图中的三层视角是原创组织工具。它提醒我们：主观体验、个人行动与社会环境可以成为不同的研究层次。图中没有因果箭头、分数和“最佳人生”排名。讨论某人的体验时，允许对方不分享；你可以始终使用虚构人物。"""),
            ("原始材料与继续学习", """[S1] 用于核对 2006 年大纲及前段顺序。[S2] 是 Seligman 与 Csikszentmihalyi 2000 年论文的作者机构资源入口，[S3] 提供该原始论文的书目信息与摘要。它们支持积极心理学作为研究议程的背景，不能证明本指南的虚构案例是有效干预。所有网页核查日期为 2026-11-01。
有额外时间时，先看大纲，再通过作者机构入口寻找论文；全文阅读单独计时。继续原课时，回到相应讲次和阅读安排。六天只是一条进入前三组的路径，后续主题和原课考核仍需要另行学习。"""),
        ]),
        "lesson_sections": _sections([
            ("今天的入口：七分钟阅读，三分钟练习", """今天只做一件事：把一句关于幸福的话，变成一个更清楚、可以讨论证据的问题。本课原版是 Harvard PSY1504，2006 年春季；大纲的开头安排导论、为何需要积极心理学与基本前提。[S1] 我们从 u01 的一个小切口进入，不复述未核实的第一讲。下面的讲解和情境由本指南编写，学术背景另引 [S2][S3]。"""),
            ("研究对象比“开心一点”更宽", """积极心理学的早期研究纲领关注积极的主观体验、个人特征及支持良好生活的制度环境。[S3] 今天把它理解为拓宽问题范围：除了问“哪里出了困难”，也问“哪些条件帮助人持续投入、与别人合作、觉得生活有价值”。这不是要求人随时保持愉快，更不是把困境解释成个人不够努力。
请区分三种话：“我今天轻松一些”是一份体验报告；“参加小组的人平均更愿意继续学习”是一个待核实的比较判断；“参加小组使所有人幸福”则同时扩大了因果力度与适用范围。说得更肯定，并不会使证据更强。"""),
            ("原创例子：一间安静的自习室", """设想两组虚构学习者。甲组每周有一次安静自习时间，乙组时间相同，但每次结束前互相问一个学习问题。一个月后，有人说乙组“看起来更积极”。我们不能从这句话直接认定提问提高了幸福感。“看起来”由谁判断？两组原来的熟悉程度是否相同？更愿意发言的人是否本来就更愿意参加乙组？这些都可能影响观察。
一个更好的问题是：在这两组参与者中，四周后愿意继续参加的人数是否不同？这个问题仍不等于幸福本身，却明确了对象、时间与观察指标。假设甲组有八人愿意继续，乙组有九人，组员人数却分别是十人与二十人，那么只比较人数还会误导；比例与参加条件也要交代。
这个算例不是实验结果，不来自教授课堂。它帮助我们看到，研究之前先把问题说清楚，本身就是一种进步。"""),
            ("图怎样读：三个观察层次", """图中三个相连但不带方向的区域分别代表体验、行动和环境。体验可以是一个人当下觉得专注；行动可以是他是否愿意继续参与；环境可以是是否有安静空间与同伴支持。把三者分开，是为了避免把所有变化都塞进一个模糊的“幸福”标签。
区域相邻不表示某一层必然导致另一层。一个人愿意继续参加，可能喜欢活动，也可能只是时间方便；一次自评轻松，也可能受当天睡眠影响。图是本指南的概念示意，不是原课图片，不含研究数据。读图时试着指出：我们的自习室问题实际观测了哪一层，还有哪两层没有测到？"""),
            ("三分钟轻练习", """1. 哪个问题更适合今天的研究视角？A. 怎样保证所有人永远快乐？B. 同一活动持续四周后，参加者愿意继续参与的比例有何变化？C. 哪一类人最值得拥有幸福？
2. 有人说：“乙组更愿意继续，所以提问一定让人更幸福。”用一句话指出其中一个跳步。你可以只想一想，不必写下个人经历。
3. 若只能增加一项背景信息，你想了解两组原来的关系、场地，还是参与条件？任选一个，并说出它为什么可能改变解释。没有要求你设计完整实验。"""),
            ("参考答案与提示：先自己想，再看这里", """第 1 题选 B。它有对象、时间和较明确的指标；它仍需要说明如何记录与比较，并不因此自动成为可靠的因果研究。第 2 题可以答：“继续参加不等于幸福，而且差异可能来自组员原有特点。”指出其中一处就足够。第 3 题没有唯一答案；关键是把信息与另一种解释连接起来。例如，原来认识的同伴可能让人更愿意留下，而非最后那一个提问本身造成变化。
如果选了 A，可以保留它作为愿望，再缩小成一个可以观察的问题。学习的目标是改善问题，不是给自己的感受判对错。"""),
            ("明天与来源边界", """明天仍在 u01，讨论为什么要在困难之外观察已有的能力与支持条件。今天结束时只记住一句自己的话：我希望了解的变化是什么，我准备用什么观察它。无需开始长篇记录。
[S1] 核实的是原课范围；[S2][S3] 核实的是独立的学术背景。它们不支持“这个自习室方法已经被验证”的说法。可选原始阅读不计入今天十分钟，本指南也不声称完成了 Harvard 课程或获得任何学分。"""),
        ]),
        "sources": [
            _source("S1", "PSYCHOLOGY 1504 — POSITIVE PSYCHOLOGY", "https://ppc.sas.upenn.edu/sites/default/files/ppsyllabusschachar.pdf", "宾夕法尼亚大学积极心理学中心（保存哈佛课程大纲）", "2006 年春季原课大纲；仅支持课程主题、日期与安排，不代表已核实官方讲课全文。", "2006 春季"),
            _source("S2", "Positive Psychology: An Introduction", "https://www.authentichappiness.sas.upenn.edu/resources/positive-psychology-introduction", "宾夕法尼亚大学 Authentic Happiness", "作者机构的论文入口；提供作者及年份，链接的论文全文本次未能获取。", "2000（论文；入口页未标日期）"),
            _source("S3", "Positive psychology. An introduction", "https://pubmed.ncbi.nlm.nih.gov/11392865/", "美国国家医学图书馆；原论文作者 Seligman 与 Csikszentmihalyi", "原始论文摘要与书目记录，2000 年 1 月，55(1):5–14；只使用摘要中的研究框架。", "2000-01"),
        ],
        "figure": {"caption": "同一情境的三个观察层次：体验、行动、环境；相邻关系不等于因果关系。", "credit": "本指南原创教学示意；不含研究数据，非哈佛原课图。", "concept": "Three equally weighted overlapping translucent circles: subjective experience, action, environment; no arrows or numeric data. Chinese labels 体验、行动、环境. Quiet paperlike background; educational conceptual diagram."},
    },
    {
        "slug": "cs50x-en", "course_id": "harvard-cs50x", "language": "en",
        "title": "CS50x: think clearly before you code",
        "days": _days([
            ("From a problem to an unambiguous procedure", "Identify inputs, outputs and a terminating procedure."),
            ("Decisions and repetition in Scratch", "Trace one condition and one loop without building a project."),
            ("From blocks to C and arrays", "Recognize variables and indexed collections in a short trace."),
            ("Checking a small array calculation", "Find an off-by-one mistake through a concrete example."),
            ("Comparing ways to search", "Explain how a search strategy depends on the input."),
            ("Memory and the limits of a model", "Distinguish a stored value from the place that stores it."),
        ]),
        "plan_sections": _sections([
            ("Edition and partial scope", """This guide selects the first three catalog groups for Harvard CS50x 2026: Week 0; Weeks 1–2; and Weeks 3–4. The requested 2026 official URLs redirected to the current CS50x pages when checked on 1 November 2026. We retain the requested edition label and disclose that behavior rather than treating the pages as a frozen archive. [S1][S2] Six brief days introduce selected ideas in those groups; they do not complete the groups or the course. The remaining weeks and final project sit outside this sample.
The official materials provide the course context. The parcel-sorting example, diagram and light questions here are original teaching material, not claims about what David Malan demonstrated in his lecture."""),
            ("A ten-minute routine", """Reserve seven minutes for the day's explanation and diagram, then three minutes for a short trace or choice question. You can answer aloud. No IDE, account, API key, paid service or project submission is needed. If a trace takes longer, stop after finding the first uncertain step and begin there next time. A useful learning record can be a single sentence describing what changed in your understanding.
Watching a full original lecture or doing an official problem set is optional work outside this ten-minute budget. The original course has a substantially larger workflow, including problem sets and a final project. [S1] A micro lesson is a starting point for that work, not a compressed claim of equivalent credit."""),
            ("Days 1 and 2: Week 0", """Day 1, “From a problem to an unambiguous procedure,” takes one subsection of u01. You will distinguish the item a procedure receives, the decision it makes, and the result it returns. Day 2, “Decisions and repetition in Scratch,” stays in u01 and connects the same reasoning to blocks. The goal is to predict a small behavior before running it, including what happens when there are no items.
Keep the examples tiny. Three parcels are enough to expose an unclear rule. Extra complexity can hide a misunderstanding behind mechanical work. Success means explaining why the procedure stops and giving one input on which a vague alternative fails."""),
            ("Days 3–6: a route through two more groups", """Days 3 and 4 belong to u02, C and arrays. “From blocks to C and arrays” introduces how a value and a position can be tracked; “Checking a small array calculation” uses a short trace to locate an indexing error. Days 5 and 6 belong to u03, algorithms and memory. “Comparing ways to search” asks how the arrangement of input affects the strategy. “Memory and the limits of a model” introduces the distinction between a value and its storage location.
These titles name our selected learning tasks, not replacements for official week titles. Reading about a loop once is not the same as being able to write and debug a program. At the end of six days, decide which group deserves another pass before moving forward."""),
            ("How to check understanding", """For each example, ask three things: What would count as the right answer? Which step makes progress? What could go wrong at the boundary? Try a normal case and an empty case before inventing a complicated one. If two readers execute your instructions differently, identify the ambiguous phrase and improve it. This is a more informative result than merely saying the instructions seem sensible.
The lesson diagram contains no benchmark data. Its arrows represent the order of an original toy procedure. Read those arrows as control flow, not as evidence that every computer program has exactly this structure. Later programs can keep running, accept new input, or make several outputs."""),
            ("Sources and the next step", """Use [S2] to locate Lecture 0 topics and [S1] for the wider course and learning workflow. Both are official Harvard CS50 pages checked on 1 November 2026; their resolved URLs are recorded in the source notes. We paraphrase a small amount of their framing and teach with our own example. No professor quotations or lecture screenshots are reproduced.
After Day 6, return to the original week that felt least secure and give it a separate study session. Completing this route means you have practiced asking precise questions about programs; certification and original assessments remain separate."""),
        ]),
        "lesson_sections": _sections([
            ("Today's place in the course", """Today is a seven-minute reading followed by three minutes of light practice. We take one small part of u01, CS50x Week 0: expressing a problem as a procedure. The official Lecture 0 notes include problem solving, algorithms, pseudocode, and Scratch. [S2] You will not need to install anything. The example below is invented for this guide, and you can execute it with your finger on the page.
By the end, explain an input, an output, and a reason that a small procedure finishes. That is a narrower, more useful target than “understand programming” in ten minutes."""),
            ("First decide what counts as an answer", """Imagine a volunteer sorting parcels into two trays. For this teaching example, each parcel has a destination label that is either LOCAL or OTHER. The desired output is two trays with every parcel placed according to its label. We assume the labels are readable and valid. Those assumptions matter: if a label is missing, the rules below do not yet say what to do.
An input is the information or material the procedure receives. An output is the result required by the task. A procedure supplies steps linking them. “Sort carefully” states an intention but leaves decisions unspecified. “If the label is LOCAL, put the parcel in tray L; otherwise put it in tray O” gives the reader an executable decision under our assumptions."""),
            ("Worked example: three parcels and an empty pile", """Use this original pseudocode: while an unprocessed parcel remains, take one parcel; read its label; if the label is LOCAL, put it in L; otherwise put it in O. When no parcel remains, stop. Pseudocode lets us discuss the logic without committing to a particular programming language.
Trace the labels OTHER, LOCAL, OTHER. At first both trays are empty and three parcels remain. After the first step, O contains one parcel and two remain. After the second, L contains one and one remains. After the third, O contains two, L contains one, and none remain. The loop test now fails, so the procedure finishes. Each successful pass removes exactly one item from the unprocessed pile.
Now try zero parcels. The loop test fails immediately. Both trays stay empty, which is a sensible result for an empty input. A rule saying “take the first parcel” before checking the pile would fail here. Boundary cases are small enough to reason about and often reveal a hidden assumption quickly."""),
            ("Read the figure as a trace of decisions", """The diagram starts with the unprocessed pile, checks whether an item remains, and branches on its label. Both tray paths return to the pile check. The exit branch ends when the pile is empty. Follow the arrows for just one parcel before trying all three; the drawing represents repeated control flow, not three separate copies of the instructions.
The diagram is our own teaching illustration. It does not show a real warehouse system, timing measurement or original CS50 slide. A real service might need rules for damaged labels, duplicate items and new arrivals. We deliberately freeze those complications so that you can see the core decision. A model becomes useful when its assumptions are visible."""),
            ("Three minutes: predict before checking", """1. Which instruction removes the ambiguity in “sort carefully”? A. Work faster. B. Read the label and choose L for LOCAL, otherwise O. C. Think about both trays.
2. Start with labels LOCAL, OTHER, LOCAL. How many items end in each tray? A short mental trace is enough.
3. Name one condition under which our rules need extending. One phrase is sufficient; there is no request to write a program or a long explanation. If you have time left, point to the exact step where that condition becomes a problem."""),
            ("Suggested answers and a useful distinction", """For 1, choose B: it specifies an observable test and an action for each permitted result. For 2, L receives two parcels and O receives one. The answer is checked against each label, not inferred from the shape of the diagram. For 3, a missing label is a good example: our “otherwise” would accidentally treat it as OTHER unless we introduce validation or a separate review tray.
Stopping and correctness are different questions. A procedure can finish after putting every item in the wrong tray. Our progress argument explains why it stops for a finite, fixed pile; the label rule explains why each placement matches the specification. Keep both explanations available."""),
            ("Next: express the same idea in blocks", """Tomorrow stays in u01 and looks at decisions and repetition through Scratch. Bring the idea of a condition that can be true or false, plus a step that makes progress. You do not need to complete the official Scratch project today.
The course context comes from official materials [S1][S2]. Our parcel example is not an attributed lecture demonstration. The 2026 links currently redirect to the main course pages; optional lecture viewing takes additional time beyond today's ten minutes."""),
        ]),
        "sources": [
            _source("S1", "CS50x 2026", "https://cs50.harvard.edu/x/2026/", "Harvard University · CS50", "Requested 2026 course URL redirects to https://cs50.harvard.edu/x/; official course context, week sequence and wider workflow, not a frozen archive.", "2026 edition label; page undated"),
            _source("S2", "Lecture 0 — CS50x 2026", "https://cs50.harvard.edu/x/2026/notes/0/", "Harvard University · CS50", "Requested 2026 notes redirect to https://cs50.harvard.edu/x/notes/0/; verified topic headings and introductory concepts. Parcel example is original to this guide.", "2026 edition label; page undated"),
        ],
        "figure": {"caption": "An original parcel-sorting loop: check the pile, test a label, choose a tray, and repeat.", "credit": "Original teaching diagram for this guide; not a CS50 slide or measured system.", "concept": "Clean flowchart with English labels: Any parcels left? no -> Stop; yes -> Read label -> LOCAL? yes Tray L, no Tray O; both return to Any parcels left. Correct arrow directions. Small parcel and tray icons, no data graphics."},
    },
    {
        "slug": "linear-algebra-ja", "course_id": "mit-linear-algebra", "language": "ja",
        "title": "線形代数：同じ方程式を二つの図で見る",
        "days": _days([
            ("連立方程式を行と列から見る", "同じ解を直線の交点と列ベクトルの組合せで確かめる。"),
            ("消去で何を残すのか", "簡単な行操作が解を保存する理由を説明する。"),
            ("列空間と到達できるベクトル", "列の組合せで表せる右辺を見分ける。"),
            ("零空間と解の自由度", "同次方程式の解が何を表すかを小さな例で読む。"),
            ("基底と次元を数える", "独立性と生成を区別して基底の役割を説明する。"),
            ("最初の範囲を口頭で点検する", "基底と解の見方を復習し、原課の試験範囲を確認する。"),
        ]),
        "plan_sections": _sections([
            ("版と学習範囲", """対象は MIT OpenCourseWare の 18.06 Linear Algebra、2010 年春学期版です。担当は Gilbert Strang。公開ページでは講義映像自体は 1999 年秋に収録されたと説明されています。学期版と収録年を混同しないでください。[S1][S2] この六日間は最初の三つの目録群だけを使う部分的な導入で、全課程修了を意味しません。
第一群は方程式と消去、第二群は部分空間と解、第三群は基底と最初の確認までです。後の直交性、固有値などをこの日程で学び切るとは約束しません。以下の数値例と図は本ガイドが作成したもので、教授の板書を再現したものではありません。

元のコースの前提科目は 18.02（多変数微積分）です。MIT のシラバスに明記されています [S2]。本サンプルの初日では、代入・基本的な式変形・座標の読み取りだけを使います。これは前提科目を不要にするという意味ではありません。先の単元で不足する知識が見つかったら、補習する範囲を相談します。"""),
            ("一日十分の使い方", """七分で説明と図を読み、三分で小さな計算や選択問題を確かめます。紙を使っても構いませんが、長い証明や課題提出は不要です。式を追い切れないときは、各座標に数字を代入するだけでも十分な出発点になります。速く計算するより、どの量が未知数でどの量が固定されているかを言葉にしましょう。
原課のシラバスには複数回の授業、演習と宿題があり、この十分はその代替ではありません。[S2] 元の映像や教科書を読む時間は別枠です。日ごとに一つ、説明できなかった箇所に印を付ければ、次に原教材のどこへ戻るかを決められます。"""),
            ("一、二日目：最初の方程式群", """一日目「連立方程式を行と列から見る」は u01 の冒頭だけを扱います。交点を求める見方と、列ベクトルを組み合わせる見方が同じ数値を与えることを確かめます。二日目「消去で何を残すのか」も u01 です。式から別の式の倍を引く操作を使い、数字を変えても解が保存される条件を考えます。
ここでの到達点は一問の正解だけではありません。行の絵では点が未知数を表し、列の絵では矢印の係数が未知数を表す、と区別して説明できることです。図の色を覚える必要はありません。"""),
            ("三日目から六日目の道筋", """三日目「列空間と到達できるベクトル」と四日目「零空間と解の自由度」は u02 に対応します。右辺が与えられたとき到達できるか、また同じ右辺へ至る係数が複数あるか、という二つの問いを分けます。計算を少なくして、意味の違いを先に確かめます。
五日目「基底と次元を数える」と六日目「最初の範囲を口頭で点検する」は u03 です。独立な向きと必要な本数を考え、原課の最初の試験を含む群の位置を確認します。ガイド内の軽い確認は原課試験ではありません。各群に二日を置くのは閲覧のための配分で、元の授業回数を二回に圧縮したという意味ではありません。"""),
            ("理解を確認する三つの問い", """答えを得たら、元の式に戻して両方の行を満たすか確かめます。次に、図のどの部分がその答えに対応するかを指します。最後に、係数や右辺を一つ変えたら同じ答えが通用するかを考えます。この三段階なら、たまたま数字が合っただけの理解を見つけやすくなります。
図は二つの別の座標平面を使います。左の点と右の矢印は役割が異なるため、重ねて一枚の空間として読むと混乱します。最初はそれぞれの軸が何を表すか、声に出してから眺めてください。図に統計値や実験結果はありません。"""),
            ("出典と六日後の続き", """[S1] は第一講 The geometry of linear equations の公式ページで、行・列・行列という見方の位置付けを確認できます。[S2] は 2010 年春学期のシラバスです。教材は英語ですが、本ガイドの説明、問題、ヒントは日本語で独自に執筆しました。確認日は 2026-11-01 です。
追加の時間があれば第一講を開き、自分の例と同じ見方がどこで現れるか探してください。六日後は理解が弱かった群へ戻り、原課の演習を別に進めます。十分で全部を見ることより、短い式を二つの見方で説明できることを最初の成果にしましょう。"""),
        ]),
        "lesson_sections": _sections([
            ("今日の小さな目標", """七分の読解と三分の練習で、二本の式を二つの仕方で読むことを目指します。MIT 18.06 の 2010 年春学期版の第一講は、行・列・行列による連立方程式の見方を導入します。[S1] 今日扱うのは u01 の最初の一部分です。次の数値例は本ガイドの独自例で、原講義の具体例や板書の引用ではありません。"""),
            ("行を見る：両方の条件を満たす点", """次の連立方程式を考えます。x + y = 3、x + 2y = 4。x と y は、両方の条件に同時に入る未知数です。最初の式だけなら、例えば (3,0) も (1,2) も条件を満たします。しかしそのどちらも二番目の式を満たすとは限りません。
二番目の式から最初の式を引くと y = 1、これを最初の式へ戻すと x = 2 です。必ず元の両方で確認します。2 + 1 = 3、2 + 2×1 = 4。行の見方では各式は x,y 平面上の直線であり、解 (2,1) は二本の交点です。「点が線の近くにある」ではなく、同時に二つの条件を満たすことが要点です。"""),
            ("列を見る：係数を選んで目標へ届く", """同じ式を縦に並べ、x の係数だけを集めると (1,1)、y の係数だけを集めると (1,2) になります。右辺を縦に集めた目標は (3,4) です。したがって同じ問題は、x(1,1) + y(1,2) = (3,4) と書けます。ここでは (第一成分, 第二成分) の順に横書きしています。
先ほどの x=2、y=1 を使うと、2(1,1) = (2,2) と 1(1,2) = (1,2)。成分ごとに足すと (3,4) へ届きます。行の見方で「交点の座標」だった二つの数が、列の見方では「それぞれの矢印を何倍するか」になります。未知数を変えたのではなく、同じ未知数の役割を別の絵で説明しています。
行列の記法 Ax=b はこの情報をまとめる容器です。今日、記号を暗記しなくても構いません。まず二本の列を二倍と一倍で組み合わせる手順が、二本の式を同時に満たすことと一致する、と確かめてください。"""),
            ("図の読み方：二枚を混ぜない", """左側は x,y 平面です。二本の直線 x+y=3 と x+2y=4 の交点 (2,1) を示します。右側は成分を表す別の平面です。(1,1) の二倍を描き、その先端から (1,2) を足すと (3,4) に着きます。右側の目標点は左側の解の座標と同じではありません。
矢印を先端と始点がつながるように置くのは、ベクトルの和を示すためです。原点からの薄い矢印が列、長い矢印がその倍、最後の点が右辺です。この図は独自の説明用で、物体の移動を測ったデータでも、原講義の画像でもありません。どちらも数学的関係を可視化していますが、軸の意味を別々に読んでください。
左で一方の式だけを満たす点を選ぶことと、右で一方の列だけを使って偶然近くまで行くことは、どちらも解の確認には不足します。目標の二成分を両方確かめる必要があります。"""),
            ("三分の軽い練習", """1. x+y=3、x+2y=4 の解はどれですか。A. (1,2)、B. (2,1)、C. (3,0)。図の印だけでなく元の式で確かめてください。
2. 2(1,1)+(1,2) の第一成分と第二成分をそれぞれ計算してください。答えは数字二つで十分です。
3. 列の見方における x=2 は何を表しますか。A. 目標点の第一成分が必ず 2、B. 第一の列を二倍する、C. 方程式が二本ある。直感で選んだ後、式のどこに 2 が入るか指してみましょう。"""),
            ("答えとヒント", """1 は B です。A は最初の式を満たしますが二番目は 5 になります。C も最初だけを満たし、二番目は 3 です。二つの条件を別々に確認すれば、選択肢の形に頼らず判断できます。
2 は (3,4)。第一成分は 2×1+1、第二成分は 2×1+2 です。3 は B。x は第一列の係数であり、目標 (3,4) の第一成分そのものではありません。
もし二つの平面を混同したら、紙に「未知数の座標」と「式の結果の成分」と別々に書いてください。違いが言えれば、計算が少し遅くても今日の目標に近づいています。"""),
            ("明日へ持ち越す問い", """明日も u01 で、式から式を引く消去が何を保存するかを見ます。今日の式を一度だけ見直し、「なぜ引いてよいのか」を自分の言葉で予想してください。長い証明はまだ必要ありません。
[S1] は講義の概念的位置付け、[S2] は原課の学習範囲と負担を確認する資料です。元の映像は 1999 年秋収録、公開コースの版は 2010 年春です。原教材の視聴や宿題は別の学習時間であり、この一ページで第一群全部を終えたとは数えません。"""),
        ]),
        "sources": [
            _source("S1", "Lecture 1: The geometry of linear equations", "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-1-the-geometry-of-linear-equations/", "MIT OpenCourseWare", "行・列・行列の見方を確認。ページは映像の収録を 1999 年秋と明記。数値例は本ガイド独自。", "コース 2010 年春；映像 1999 年秋"),
            _source("S2", "Syllabus — Linear Algebra", "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/syllabus/", "MIT OpenCourseWare", "2010 年春版の目標、前提、授業・宿題・評価の位置付けを確認。", "2010 年春"),
        ],
        "figure": {"caption": "左：二直線の交点 (2,1)。右：2(1,1)+(1,2)=(3,4)。二つの平面は役割が異なる。", "credit": "本ガイド独自の数学説明図。MIT の原講義画像ではない。", "concept": "Two distinct mathematically accurate panels. Left xy axes lines x+y=3 and x+2y=4 intersection (2,1). Right vector component plane: arrow origin to (2,2) labelled 2(1,1), arrow (2,2) to (3,4) labelled (1,2), resulting arrow origin to (3,4). Japanese panel labels 行の見方 and 列の見方. Clear tick marks and no decorative data."},
    },
    {
        "slug": "listening-music-fr", "course_id": "yale-listening-music", "language": "fr",
        "title": "Écouter la musique : décrire ce qui change",
        "days": _days([
            ("Écouter activement : suivre une couche sonore", "Distinguer une observation sonore d'une impression générale."),
            ("Instruments, œuvre et genre", "Employer un vocabulaire précis sans deviner un instrument à tout prix."),
            ("Pulsation et organisation du temps", "Distinguer la pulsation régulière des événements rythmiques."),
            ("Suivre une idée mélodique", "Repérer le retour ou la transformation d'un petit contour."),
            ("Entendre plusieurs sons ensemble", "Distinguer la dimension harmonique d'une ligne mélodique."),
            ("Suivre la basse et faire le bilan", "Décrire le rôle d'une couche grave dans un court passage."),
        ]),
        "plan_sections": _sections([
            ("Version et périmètre partiel", """Ce parcours prend pour point de départ Listening to Music, MUSI 112, de Craig Wright à Yale, édition de l'automne 2008. Il sélectionne trois groupes du catalogue : initiation et instruments (leçons 1–2), rythme et mélodie (3–6), puis harmonie et basse (7–8). Les pages originales des deux premières leçons ont été consultées le 1 novembre 2026. [S1][S2] Six journées ne couvrent ni ces groupes dans leur intégralité, ni l'ensemble du cours.
Les explications, le petit scénario sonore et les questions sont écrits pour ce guide. Aucun extrait enregistré, exercice noté ou exemple attribué au professeur n'est reproduit. La première journée développe une seule idée de l'introduction : rendre son écoute plus attentive et plus descriptive."""),
            ("Dix minutes, sans devoir lourd", """Chaque journée prévoit sept minutes de lecture et d'observation d'une figure, puis trois minutes pour une ou deux réponses brèves. On peut répondre oralement. Il n'est pas nécessaire de lire une partition, de reconnaître une œuvre célèbre ou de disposer d'un instrument. Pour le premier exemple, une séquence imaginaire suffit ; un simple tapotement peut rendre la différence plus concrète.
Regarder une leçon originale entière, écouter ses nombreux extraits ou consulter le manuel prend du temps supplémentaire. Ces activités restent possibles en dehors du budget de dix minutes. Si vous choisissez votre propre musique, prenez un passage très court et revenez deux fois au même endroit, au lieu d'enchaîner des morceaux sans comparaison."""),
            ("Jours 1 et 2 : installer des repères", """Le jour 1, « Écouter activement : suivre une couche sonore », appartient à u01. Il demande de séparer ce qu'on peut décrire d'une impression globale. Le jour 2, « Instruments, œuvre et genre », reste dans u01. Il introduit un vocabulaire permettant de préciser ce qu'on entend, sans transformer l'écoute en concours d'identification.
Un résultat suffisant est une phrase comme « une ligne aiguë entre après les frappes régulières ». Elle contient un événement vérifiable dans le passage. « C'est magnifique » peut rester votre appréciation ; ajoutez simplement une observation qui explique où votre attention s'est portée. On peut apprécier une musique sans savoir encore nommer sa structure."""),
            ("Jours 3 à 6 : avancer par couches", """Les jours 3 et 4 correspondent à u02. « Pulsation et organisation du temps » distingue un repère régulier des événements qui s'y placent. « Suivre une idée mélodique » fait reconnaître un petit contour et son retour. Les jours 5 et 6 correspondent à u03 : « Entendre plusieurs sons ensemble », puis « Suivre la basse et faire le bilan ». Vous déplacerez l'attention d'une couche à l'autre au lieu d'essayer de tout entendre simultanément.
Nos intitulés indiquent un objectif réduit ; ils ne sont pas les titres officiels des leçons. Deux journées par groupe constituent une route d'entrée. Une notion difficile peut demander une nouvelle écoute séparée avant de poursuivre. Il n'y a pas de promesse de maîtriser l'harmonie au cinquième jour."""),
            ("Une manière légère de vérifier ses progrès", """À la fin d'une séance, indiquez un événement, son emplacement relatif et la couche concernée. Essayez ensuite de distinguer une observation certaine d'une hypothèse : vous pouvez entendre un son grave sans identifier l'instrument qui le produit. Cette différence protège l'écoute d'une fausse précision. Un doute bien localisé donne une meilleure question pour la prochaine séance.
Les figures de ce guide sont des cartes pédagogiques originales. Leurs lignes représentent l'ordre d'événements inventés ; elles ne mesurent ni fréquence réelle ni intensité et ne remplacent pas la musique. Comparez la carte à la description, puis revenez au son lorsque vous utilisez un enregistrement choisi par vous."""),
            ("Retour aux sources et suite", """L'introduction originale [S1] présente l'écoute comme une activité attentive ; la deuxième leçon [S2] apporte un cadre de vocabulaire, de genres et d'instruments. Ces pages donnent accès au contexte du cours et à ses transcriptions. La page générale du cours a renvoyé une erreur d'accès pendant la vérification ; les pages des leçons ont bien été consultées directement.
Après six jours, choisissez le groupe où vos descriptions restent les plus vagues et ouvrez une ressource originale pour un temps plus long. Le but de cet échantillon est de préparer une écoute mieux orientée. Il ne remplace pas les évaluations du cours et ne délivre aucun résultat universitaire."""),
        ]),
        "lesson_sections": _sections([
            ("Un objectif précis pour aujourd'hui", """Nous entrons dans u01 de Listening to Music, le cours MUSI 112 de Yale, automne 2008. Dans son introduction, Craig Wright présente l'écoute comme une activité qui peut devenir plus active grâce à l'attention aux éléments musicaux. [S1] Aujourd'hui, choisissez une couche sonore et décrivez ce qu'elle fait. Sept minutes pour lire et regarder la figure, puis trois pour les questions suffisent.
Notre exemple est une construction pédagogique originale. Il ne transcrit aucune œuvre et ne reprend pas une démonstration du professeur. Vous pouvez le suivre sans fichier audio ni connaissances de solfège."""),
            ("Impression et observation peuvent coexister", """« Ce passage m'apaise » décrit votre expérience. « Des sons graves reviennent régulièrement pendant qu'une ligne aiguë monte » décrit des relations dans le passage. La seconde phrase ne prouve pas la première et ne la rend pas plus légitime : elles répondent à deux questions différentes. On peut conserver son plaisir tout en apprenant à préciser ce qui attire l'oreille.
Pour commencer, limitez volontairement votre attention. Une fois, suivez les attaques régulières. Une autre fois, suivez la ligne la plus aiguë. La difficulté n'est pas forcément un manque d'oreille ; plusieurs événements simultanés se disputent votre attention. Une consigne étroite rend la comparaison possible."""),
            ("Exemple original : huit repères et trois entrées", """Imaginez huit frappes également espacées : 1, 2, 3, 4, 5, 6, 7, 8. Elles servent de repères temporels dans notre exemple. Au repère 1 commence aussi un son grave tenu jusqu'au repère 4. Au repère 5 commence un autre son grave, tenu jusqu'à la fin. Enfin, une petite ligne aiguë apparaît aux repères 3, 4 et 5 ; ses trois sons vont du plus bas au plus haut.
Première écoute imaginaire : comptez seulement les huit frappes. Deuxième passage : oubliez les frappes autant que possible et suivez le grave ; il change au repère 5. Troisième passage : suivez la ligne aiguë ; elle commence après le début et monte. Les mêmes événements permettent donc plusieurs descriptions utiles selon la couche choisie.
On ne peut pas en déduire que la musique accélère au repère 3. Davantage d'événements se superposent, mais nos frappes restent également espacées. On ne peut pas non plus identifier un violon à partir de la seule position aiguë d'un son. Nous n'avons décrit ni sa couleur ni sa production. Ces limites sont aussi instructives que les observations positives."""),
            ("Ce que montre la figure", """La carte comporte trois bandes : frappes, grave et ligne aiguë. Les huit colonnes sont des repères successifs. Un trait long dans la bande grave représente un son tenu, tandis que trois points qui montent dans la bande aiguë indiquent l'ordre relatif des hauteurs. Il s'agit d'un dessin conceptuel, pas d'une partition jouable avec des notes exactes.
Lisez d'abord horizontalement une seule bande. Regardez ensuite verticalement le repère 5 : une frappe, un nouveau son grave et le dernier son aigu y coïncident. Cette coïncidence donne un emplacement précis à votre phrase. Elle ne démontre pas une émotion universelle chez les auditeurs.
La figure est originale et sans données mesurées. Ses espacements illustrent notre scénario, non une analyse acoustique. Aucun son n'est intégré à la page : la description, et éventuellement votre tapotement, sert de support à ce premier exercice."""),
            ("Trois minutes de pratique légère", """1. Au repère 3, une ligne aiguë entre mais les frappes restent régulièrement espacées. Quelle conclusion est justifiée ? A. Le tempo a nécessairement doublé. B. Une couche s'ajoute sans changement prévu des repères. C. L'instrument est nécessairement un violon.
2. Complétez oralement : « Le son grave change au repère… » Puis indiquez une chose que le dessin ne permet pas de savoir.
3. Si vous écoutiez un passage réel deux fois, quelle couche choisiriez-vous pour la seconde écoute ? Une réponse et une raison très brèves suffisent ; aucun compte rendu long n'est attendu."""),
            ("Réponses suggérées et indice", """Pour 1, choisissez B. L'ajout d'une couche et l'accélération sont deux descriptions différentes. Pour 2, le grave change au repère 5. Le dessin ne permet pas de connaître le timbre exact, le nom de l'instrument ou la réaction de tous les auditeurs. Pour 3, plusieurs choix conviennent : suivre le grave après avoir suivi les frappes permet par exemple d'observer une relation nouvelle.
Si vous avez surtout retenu « cela monte », précisez quelle couche monte et à quel moment. Si vous n'arrivez pas encore à séparer les couches, reprenez seulement les deux premières bandes. Réduire le nombre d'éléments observés peut être une bonne stratégie d'apprentissage."""),
            ("Demain et lecture facultative", """Demain, toujours dans u01, nous préciserons des mots pour parler d'œuvres, de genres et d'instruments. La leçon originale 2 traite notamment de ce vocabulaire. [S2] Aujourd'hui, une observation localisée suffit : vous n'avez pas à reconnaître une symphonie ni à analyser une œuvre entière.
Pour prolonger, ouvrez [S1] et choisissez un passage de la leçon originale pendant une séance distincte. L'idée d'écoute active vient du cadre original ; la carte à huit repères est notre outil d'explication. Cette première journée n'achève ni u01 ni le cours de Yale."""),
        ]),
        "sources": [
            _source("S1", "MUSI 112 — Lecture 1 — Introduction", "https://oyc.yale.edu/music/musi-112/lecture-1", "Yale University · Open Yale Courses", "Page originale et transcription consultées ; cadre de l'écoute active. La page générale était inaccessible ; le scénario à huit repères est original au guide.", "Automne 2008 (édition du cours)"),
            _source("S2", "MUSI 112 — Lecture 2 — Introduction to Instruments and Musical Genres", "https://oyc.yale.edu/music/musi-112/lecture-2", "Yale University · Open Yale Courses", "Page originale et transcription ; confirme le vocabulaire, les genres et les instruments du début de cours, sans reproduire les exemples musicaux.", "Automne 2008 (édition du cours)"),
        ],
        "figure": {"caption": "Une carte inventée : huit frappes régulières, deux sons graves tenus et trois sons aigus ascendants.", "credit": "Schéma pédagogique original du guide ; aucune partition ou donnée sonore de Yale n'est reproduite.", "concept": "French labeled timeline with eight equal columns1–8 and three rows Frappes, Grave, Aigu. Frappes eight equal dots. Grave one horizontal segment columns1–4 and second5–8. Aigu rising three dots columns3,4,5. Minimal original conceptual listening map, not score or waveform."},
    },
    {
        "slug": "financial-markets-es", "course_id": "yale-financial-markets", "language": "es",
        "title": "Mercados financieros: recursos, tiempo y riesgo",
        "days": _days([
            ("Las finanzas como coordinación a través del tiempo", "Distinguir financiación, resultado y reparto del riesgo."),
            ("Riesgo, crisis e innovación", "Reconocer incertidumbre sin confundir una herramienta con una garantía."),
            ("Diversificación y sus límites", "Explicar por qué repartir exposiciones puede cambiar algunos riesgos."),
            ("Seguros e instituciones", "Distinguir la función de un seguro del contexto de una charla invitada."),
            ("Qué pregunta plantea la eficiencia del mercado", "Separar una hipótesis sobre precios de una promesa de beneficio."),
            ("Deuda y primera revisión del recorrido", "Describir una obligación de pago y ubicar el primer examen original."),
        ]),
        "plan_sections": _sections([
            ("Edición y alcance parcial", """Este recorrido usa Financial Markets, ECON 252 de Robert J. Shiller en Yale, primavera de 2011. La página del curso identifica esa edición y sus sesiones. [S1] Elegimos solo los tres primeros grupos del catálogo: propósito, riesgo e innovación (clases 1–3); diversificación, seguros y una intervención invitada (4–6); eficiencia y deuda (7–8), con el primer examen situado entre esas últimas clases. Seis días constituyen una entrada parcial; no completan esos grupos ni el curso entero.
Las explicaciones y el ejemplo de un taller son originales de esta guía. No son una cita del profesor ni un caso observado. Estudiamos funciones de las instituciones, sin formular decisiones de inversión personales ni presentar la edición de 2011 como descripción de la regulación actual.

El programa original exige familiaridad con álgebra elemental y cálculo, según el syllabus de Yale [S1]. El primer día de esta muestra solo usa una resta y el orden temporal de los pagos. Esta entrada accesible no elimina los requisitos del curso completo; si faltan bases para las siguientes unidades, acordaremos una preparación específica."""),
            ("Cómo usar diez minutos", """Cada día dedica siete minutos a leer una explicación y mirar un diagrama, y tres a preguntas breves. Puedes contestar de palabra; no necesitas hoja de cálculo, cuenta financiera ni datos privados. Si una palabra resulta nueva, anota una definición tentativa y un ejemplo. Es mejor conservar una distinción clara que acumular términos que todavía se confunden.
Ver las clases completas y resolver los ejercicios originales requiere tiempo adicional. La página del curso incluye requisitos y evaluaciones que esta guía no sustituye. [S1] No intentamos convertir los minutos de lectura en equivalentes de créditos. Las fuentes se ofrecen para ampliar o comprobar, y su consulta extensa queda fuera del presupuesto diario."""),
            ("Días 1 y 2: el primer grupo", """El día 1, « Las finanzas como coordinación a través del tiempo », toma una pequeña parte de u01. Identifica quién aporta recursos ahora, quién promete algo después y quién soporta un resultado incierto. El día 2, « Riesgo, crisis e innovación », permanece en u01 y pregunta qué cambia una herramienta y qué incertidumbre permanece.
El objetivo no es aprender a seleccionar productos. Basta con describir una relación entre participantes y distinguir una obligación de un resultado. En el primer ejemplo, recibir recursos para producir no demuestra que el proyecto vaya a vender; esa diferencia prepara la conversación sobre riesgo."""),
            ("Días 3 a 6: dos grupos más", """Los días 3 y 4 corresponden a u02. « Diversificación y sus límites » examina un reparto sencillo de exposiciones; « Seguros e instituciones » separa una función institucional del contexto de una charla invitada. No usamos la presencia de un invitado en el programa como prueba de que sus opiniones sean recomendaciones actuales.
Los días 5 y 6 corresponden a u03: « Qué pregunta plantea la eficiencia del mercado » y « Deuda y primera revisión del recorrido ». Ubicaremos el examen original sin reproducirlo como una prueba de tres minutos. Dos días por grupo indican selección y ritmo de la guía, no cobertura exhaustiva. Las clases posteriores sobre acciones, inmuebles, banca y otros temas exigen otro recorrido."""),
            ("Una comprobación que no depende de memorizar", """Para cada situación, señala tres cosas: el recurso que se mueve, el momento en que se mueve y el compromiso asociado. Después pregunta qué podría ocurrir de forma distinta de la prevista. Si no puedes identificar quién asume una pérdida, falta una pieza del modelo. Si todos parecen obtener un resultado seguro, revisa qué supuesto has introducido sin explicarlo.
Los números de la primera lección son inventados para hacer visibles las relaciones. No son tipos de interés, precios actuales ni rendimientos estimados. El diagrama tampoco representa una recomendación o una simulación de mercado. Puedes cambiar el tamaño del taller y comprobar qué relaciones se conservan; no necesitas aumentar la dificultad numérica."""),
            ("Fuentes y continuación", """La página original del curso [S1] permite comprobar la edición, la estructura y el orden. La primera clase [S2] presenta las finanzas dentro de una visión amplia de organización de recursos y gestión del riesgo. Ambas se verificaron el 1 de noviembre de 2026. La segunda es contenido original de clase, no solo un índice, y se usa para situar la pregunta del día.
Al terminar seis días, vuelve al grupo cuya distinción resulte menos clara y reserva una sesión larga para sus materiales originales. Haber seguido esta ruta significa haber practicado un vocabulario de análisis; no equivale a superar los exámenes de Yale ni a poder evaluar cualquier contrato real."""),
        ]),
        "lesson_sections": _sections([
            ("El objetivo de hoy", """Hoy usamos siete minutos de lectura y tres de preguntas para describir una función sencilla de las finanzas: conectar recursos presentes con actividades y compromisos futuros. Estamos en una subsección de u01 de Financial Markets, Yale, primavera de 2011. La primera clase presenta una perspectiva amplia que incluye asignación de recursos y gestión de riesgos. [S2] Nuestro taller imaginario es una explicación propia, no un ejemplo atribuido a Shiller.
Al terminar, deberías poder separar « recibió recursos », « prometió un pago » y « consiguió el resultado esperado ». Son tres afirmaciones distintas."""),
            ("Primero, las relaciones", """Imagina un taller ficticio que puede producir mesas, pero necesita materiales antes de entregarlas. Las personas que desean las mesas las recibirían dentro de un mes. El taller dispone de habilidades y tiempo, pero hoy carece de materiales suficientes. Tenemos una diferencia entre el momento de la necesidad y el momento del posible ingreso.
Una relación financiera puede ayudar a cruzar esa diferencia. Eso no fabrica madera ni asegura compradores: organiza derechos, recursos y obligaciones entre participantes. Para entenderla conviene preguntar quién entrega qué, cuándo lo entrega y a cambio de qué. La palabra « financiar » por sí sola todavía deja abiertas esas preguntas."""),
            ("Ejemplo original: materiales hoy, compromiso después", """Supón, solo para aprender, que los materiales cuestan 100 unidades y que el taller recibe esas 100 de un prestamista. Se acuerda devolver 105 al cabo de un mes. Los números no representan condiciones reales ni una recomendación. Al inicio, el prestamista entrega recursos y el taller adquiere una obligación; el cliente todavía no tiene la mesa.
Considera dos resultados inventados. En el primero, los clientes pagan 140 unidades y el taller puede atender el pago acordado de 105. La diferencia de 35 no puede llamarse automáticamente beneficio: hemos omitido trabajo, transporte y otros costes. En el segundo, las ventas ingresan 80. La promesa sigue siendo 105 según nuestro supuesto, pero los ingresos por sí solos no alcanzan. La forma de resolver ese incumplimiento no está especificada en el ejemplo.
Así, el mismo acuerdo puede facilitar la producción y dejar incertidumbre sobre el pago. No hace falta calcular una probabilidad para reconocer esa incertidumbre. Tampoco podemos concluir, a partir de dos escenarios escogidos, cuál será el resultado más frecuente. Las posibilidades ilustran una pregunta, no estiman un mercado."""),
            ("Cómo leer el diagrama", """El dibujo distingue dos momentos. En « hoy », una flecha de 100 va del prestamista al taller. En « dentro de un mes », otra flecha indica el pago prometido de 105 en sentido inverso. Una rama aparte muestra ingresos posibles de 140 u 80 desde los clientes. La promesa debe llevar una etiqueta distinta del resultado posible para que no parezcan equivalentes.
El diagrama es conceptual y original. No muestra probabilidades, garantías ni un contrato jurídicamente completo. En particular, que una flecha aparezca dibujada no demuestra que el pago se realice. Lee la etiqueta antes de interpretar la línea.
Si quisieras hacer el modelo más realista, tendrías que agregar costes, condiciones de pago y otras relaciones. Hoy no necesitamos resolverlas: señalar su ausencia es una parte válida de comprender el modelo. Una explicación pequeña resulta más útil cuando reconoce exactamente lo que deja fuera."""),
            ("Tres minutos de preguntas", """1. ¿Qué afirmación está justificada por el ejemplo? A. Conseguir financiación elimina el riesgo de ventas. B. El acuerdo conecta recursos presentes con una obligación futura. C. Un ingreso de 140 garantiza un beneficio de 35.
2. Si solo ingresan 80 y el pago prometido es 105, ¿qué diferencia queda sin cubrir por esos ingresos? Una operación mental basta.
3. Nombra un dato omitido que impediría evaluar el taller como negocio real. No hace falta buscar precios ni escribir un informe. Puedes responder con dos o tres palabras y explicar qué parte del razonamiento cambiaría."""),
            ("Respuestas sugeridas y un matiz", """La primera respuesta es B. El acuerdo modifica cuándo están disponibles los recursos, pero no garantiza las ventas. En la segunda, faltan 25 unidades respecto del pago prometido. Esto no demuestra por sí solo qué pérdida final sufrirá cada parte: pueden existir otros recursos o condiciones que el ejemplo no incluye. Para la tercera sirven, entre otros, el coste del trabajo o las condiciones de incumplimiento.
Si elegiste C, detectaste una diferencia aritmética correcta, pero la nombraste demasiado pronto. Ingreso menos un único pago no equivale necesariamente a beneficio. Aprender a limitar la conclusión a los datos disponibles es una habilidad central del análisis."""),
            ("Mañana y fuentes", """Mañana seguimos en u01 con riesgo, crisis e innovación. Conserva la pregunta « ¿qué cambia este acuerdo y qué permanece incierto? ». Puedes contestarla usando el mismo taller sin añadir cálculos complejos.
[S1] identifica la edición y el programa. [S2] sostiene el encuadre amplio de la primera clase; no documenta las cifras de nuestro ejemplo. Consultar una clase completa es una ampliación fuera de estos diez minutos. Hoy has trabajado una distinción inicial, no completado las tres clases de u01 ni el curso de Yale."""),
        ]),
        "sources": [
            _source("S1", "Financial Markets (2011)", "https://oyc.yale.edu/economics/econ-252", "Yale University · Open Yale Courses", "Página original del curso: edición de primavera de 2011, programa y evaluaciones. La dirección econ-252-11 del índice no respondió; esta es la página verificada.", "Primavera de 2011"),
            _source("S2", "ECON 252 (2011) — Lecture 1 — Introduction and What this Course Will Do for You and Your Purposes", "https://oyc.yale.edu/economics/econ-252-11/lecture-1", "Yale University · Open Yale Courses", "Página y transcripción originales; encuadre de recursos, tiempo y riesgo. El taller y todas sus cifras son ejemplos propios de la guía.", "Primavera de 2011"),
        ],
        "figure": {"caption": "Ejemplo inventado: 100 unidades hoy, una promesa de 105 después e ingresos que pueden ser distintos.", "credit": "Diagrama conceptual original de esta guía; no es una imagen de Yale ni contiene datos de mercado.", "concept": "Spanish two-date conceptual cashflow: Hoy lender Prestamista gives100 to Taller; Dentro de un mes Taller promises105 back labelled Pago prometido. Separate Clientes arrow possible ingresos140 or80, explicit Posibilidades, no probabilities. Original minimalist time and resource diagram."},
    },
    {
        "slug": "death-ar", "course_id": "yale-death", "language": "ar",
        "title": "فلسفة الموت: توضيح السؤال قبل الحكم",
        "days": _days([
            ("تمييز سؤال الوجود من سؤال القيمة", "تصنيف سؤال فلسفي وبيان نوع الحجة التي يحتاج إليها."),
            ("ما الشخص؟ الثنائية والمذهب الفيزيائي", "عرض موقفين عن طبيعة الشخص دون افتراض صحة أحدهما."),
            ("ما الذي يجعل القول حجة؟", "فصل المقدمة عن النتيجة في مناقشة وجود النفس."),
            ("فحص تفسيرين متنافسين", "تحديد ما يحتاج إليه الانتقال من ظاهرة إلى تفسير ميتافيزيقي."),
            ("قراءة حجة عن النفس عند أفلاطون", "تمييز بناء الحجة من مجرد الاتفاق مع نتيجتها."),
            ("الخلود: ما الذي تدعمه الحجة؟", "تحديد نطاق نتيجة فلسفية وصياغة اعتراض قصير."),
        ]),
        "plan_sections": _sections([
            ("نسخة المقرر وحدود هذا المسار", """ينطلق هذا المسار من مقرر Death، ورمزه PHIL 176، الذي قدّمه Shelly Kagan في جامعة ييل في ربيع 2007. تؤكد الصفحة الأصلية هذه النسخة، وتتيح برنامج المقرر وجلساته. [S1] نختار هنا المجموعات الثلاث الأولى فقط: أسئلة الموت وطبيعة الأشخاص، ثم حجج النفس، ثم أفلاطون والخلود. ستة أيام لا تعني إتمام هذه المجموعات أو المقرر كله، ولا تمنح رصيداً جامعياً.
اليوم الأول مدخل صغير إلى طريقة طرح الأسئلة في المحاضرة الأولى. الأمثلة والشروح والأسئلة في هذه الصفحات من تأليف الدليل، وليست اقتباسات من الأستاذ أو نقلاً لأمثلته. ندرس تمييزاً فلسفياً محدداً قبل الانتقال إلى اختلاف المواقف والاعتراضات عليها. ولا نفترض أن معرفة عنوان الموقف تكفي لفهم حجته."""),
            ("عشر دقائق وطريقة عملية للقراءة", """خصص سبع دقائق لقراءة الفكرة والنظر في الرسم، ثم ثلاث دقائق لإجابة قصيرة أو اختيار من متعدد. يمكن الإجابة شفوياً؛ لا حاجة إلى مقالة طويلة أو سرد تجربة شخصية أو مشاركة معلومات خاصة. إذا تعثرت عند مصطلح، اكتب أو قل مثالاً بسيطاً له قبل مواصلة القراءة. الغاية أن تتضح علاقة واحدة، لا أن تحفظ قائمة من أسماء الفلاسفة.
مشاهدة محاضرة ييل كاملة وقراءة النصوص المقررة نشاط إضافي خارج هذه الدقائق. يضم المقرر الأصلي قراءات ونقاشات وواجبات كتابية؛ هذا المسار ليس بديلاً عنها. [S1] يمكن العودة إلى المصدر عند توفر وقت أطول. احتفظ بسؤال واحد لم تجب عنه اليوم، ليكون نقطة دخولك إلى القراءة التالية بدلاً من محاولة حل جميع المسائل دفعة واحدة."""),
            ("اليومان الأول والثاني: توضيح موضوع السؤال", """اليوم الأول، «تمييز سؤال الوجود من سؤال القيمة»، يتبع المجموعة u01. ستتعرف إلى الفرق بين السؤال عما يوجد أو يستمر، والسؤال عما هو مرغوب أو ذو قيمة. اليوم الثاني، «ما الشخص؟ الثنائية والمذهب الفيزيائي»، يبقى في u01 وينتقل إلى موقفين تتناولهما المحاضرة الثانية. [S3] المطلوب عرض الفكرة بأمانة، لا إعلان موقف نهائي خلال عشر دقائق.
علامة التقدم هي أن تستطيع القول: هذا السؤال يحتاج إلى توضيح معنى الشخص أو البقاء، وذلك السؤال يحتاج إلى سبب يبيّن قيمة نتيجة ما. قد يرتبط السؤالان، لكن الإجابة عن أحدهما لا تحسم الآخر تلقائياً. استخدم مثال الدليل المتخيل إذا لم ترغب في مناقشة حالة واقعية."""),
            ("الأيام من الثالث إلى السادس", """اليومان الثالث والرابع يتبعان u02. في «ما الذي يجعل القول حجة؟» نفصل المقدمات عن النتيجة. وفي «فحص تفسيرين متنافسين» نسأل عن الدليل المطلوب للانتقال من ظاهرة إلى تفسير عن طبيعة الشخص. لا نعامل أسماء المواقف على أنها أدلة، ولا نعد مجرد إمكان تصور شيء برهاناً على وجوده.
اليومان الخامس والسادس يتبعان u03: «قراءة حجة عن النفس عند أفلاطون»، ثم «الخلود: ما الذي تدعمه الحجة؟». الهدف قراءة بنية محدودة للحجة واختبار نطاق نتيجتها. هذه عناوين تعلم صغناها للدليل وليست عناوين المحاضرات الأصلية. تخصيص يومين لكل مجموعة يحدد وتيرة العينة، ولا يدّعي تلخيص كل محاضرات المجموعة في حصتين قصيرتين. تبقى موضوعات لاحقة كثيرة خارج هذا المسار."""),
            ("كيف تتحقق من فهمك؟", """جرّب ثلاثة أفعال بسيطة: أعد صياغة السؤال بكلماتك، واذكر مقدمة قد يعتمد عليها جواب محتمل، ثم قل ما الذي سيبقى غير محسوم حتى لو قبلت تلك المقدمة. إذا استطعت فعل ذلك، فقد تقدمت حتى لو لم تختَر موقفاً. وإذا خالفت نتيجة ما، حاول أن تحدد موضع الخلاف في الاستدلال بدلاً من وصفها بأنها غريبة فحسب.
الرسم في اليوم الأول خريطة مفاهيم أصلية، وليس قياساً أو تصنيفاً رسمياً للفلاسفة. فروعه تساعد على تحديد نوع السؤال، ولا تمثل ترتيباً لقيمة المواقف أو مساراً مفروضاً للاعتقاد. يمكن أن يكون السؤال الواحد مركباً؛ عندئذ نفصله إلى سؤالين أصغر قبل محاولة الإجابة. هذا الفصل وسيلة للعمل، لا جداراً يمنع الترابط بين الموضوعات."""),
            ("المصادر والخطوة اللاحقة", """تتيح [S1] التحقق من نسخة المقرر وبرنامجه. توضح المحاضرة الأولى [S2] انتقال المقرر بين مسائل ميتافيزيقية ومسائل القيمة، وتعرض الثانية [S3] الثنائية والمذهب الفيزيائي. جرى الاطلاع على الصفحات الأصلية في 2026-11-01. نذكر العناوين الأصلية لسهولة العثور عليها، أما الشرح والملاحظات والأسئلة هنا فمكتوبة بالعربية لهذا الدليل.
بعد اليوم السادس، عد إلى المجموعة التي يصعب عليك شرح حجتها، واختر قراءة أصلية في جلسة أطول. نجاح هذه العينة يعني امتلاك أسئلة أوضح وطريقة أولية لفحص الحجة، وليس الحصول على إجابة نهائية عن الموت أو إنهاء مقرر ييل. ليس مطلوباً أن تتفق مع الأستاذ كي تقرأ موقفه بدقة."""),
        ]),
        "lesson_sections": _sections([
            ("مدخل اليوم: سؤال واحد أوضح", """نبدأ من جزء صغير في u01 من مقرر Death، في جامعة ييل، ربيع 2007. تميز المحاضرة الافتتاحية بين البحث في طبيعة الموت والأشخاص وبين البحث في مسائل القيمة. [S2] سنقرأ سبع دقائق ثم نجيب عن أسئلة خفيفة خلال ثلاث دقائق. هدف اليوم أن تعرف نوع السؤال الذي تطرحه قبل أن تحاول الإجابة عنه.
الأمثلة التالية من تأليف هذا الدليل. لا نقدمها بوصفها أمثلة الأستاذ أو خلاصات حرفية لمحاضرته. ولن نحتاج إلى قصة شخصية أو إلى كتابة نص طويل: يكفي أن نفصل بين ادعاءين يبدوان متشابهين في الكلام اليومي."""),
            ("ما الذي يوجد، وما الذي نريده؟", """اسأل أولاً: «هل يستمر هذا الشيء نفسه بعد تغير معين؟». هذا سؤال عن الوجود أو الهوية عبر الزمن. ثم اسأل: «لو استمر، هل سيكون استمراره أمراً جيداً؟». هذا سؤال عن القيمة. الإجابة بنعم عن الثاني لا تثبت نعم في الأول؛ فقد نرغب في شيء لا يحدث. وكذلك إثبات إمكان أمر ما لا يثبت أنه مرغوب.
يساعد هذا الفصل في قراءة النقاش الفلسفي. عندما يقول شخص «أود أن يكون هذا صحيحاً»، نفهم تفضيله، لكننا لا نملك بعد سبباً يثبت صدق القضية. وعندما يقول «هذا ممكن»، يبقى علينا أن نسأل: ما الدليل على تحققه فعلاً؟ ثم نسأل على نحو مستقل عما يجعله جيداً أو سيئاً. ليست هذه الأسئلة متعارضة؛ لكل منها عمل مختلف."""),
            ("مثال أصلي: دفتر ونُسخة مطابقة", """تخيل نادياً للقراءة يحتفظ بدفتر ورقي يسجل فيه نقاشاته. صوّر الأعضاء جميع الصفحات، ثم جمعوا الصور في ملف مطابق من حيث الكلمات والترتيب. قال عضو: «صار لدينا الدفتر نفسه». وقال آخر: «حفظ هذه المناقشات أمر ذو قيمة». الجملتان قد تبدوان متفقتين، لكنهما لا تجيبان عن السؤال نفسه.
في الجملة الأولى نحتاج إلى تحديد المقصود بعبارة «الدفتر نفسه». هل نعني الجسم الورقي الذي يمكن حمله؟ أم المحتوى الذي يمكن قراءته؟ الملف لا يملك الأوراق نفسها، لكنه قد يحفظ الكلمات. يعتمد الحكم على معيار الهوية الذي نستعمله. أما الجملة الثانية فتحتاج إلى سبب يوضح قيمة الحفظ، مثل إمكان رجوع أعضاء النادي إلى أفكارهم السابقة.
لنفرض أن لدينا سبباً جيداً لحفظ المحتوى. لا يلزم من ذلك أن الملف هو الجسم الورقي ذاته. ولنفرض أن النسخ مطابق تماماً في المحتوى. لا يلزم من ذلك أن حفظه أهم من كل استخدام آخر للوقت. يختبر المثال طريقة الانتقال بين أنواع الادعاءات، لا يحسم نظرية عن الأشخاص. الإنسان ليس دفتراً؛ التشابه هنا في بنية السؤال فقط، ولا يجوز تحويله إلى برهان عن طبيعة الإنسان أو بقائه."""),
            ("معنى الرسم وحدوده", """يبدأ الرسم بسؤال عام، ثم يفتح فرعين. الفرع الأول يسأل عن الوجود والاستمرار والهوية. الفرع الثاني يسأل عن القيمة وما يستحق التفضيل. وتحت كل فرع مساحة صغيرة لنوع السبب المطلوب. لا توجد أسهم تجعل الرغبة سبباً كافياً للوجود، ولا درجات تضع أحد الفرعين فوق الآخر.
هذه خريطة تعليمية أصلية للدليل وليست صورة من محاضرات ييل. تساعدك على وضع عبارتك في موضع مبدئي، لكنها لا تحتوي أجوبة أو نتائج بحثية. إذا كانت عبارتك «هل البقاء ممكن ومرغوب؟» فضع جزءها الأول في فرع الإمكان، والثاني في فرع القيمة. ثم ابحث عن الحجة الخاصة بكل جزء.
لاحظ أيضاً أن السهم في الخريطة يعني تفكيك السؤال، لا استنتاج الجواب. قد نحتاج لاحقاً إلى ربط الفرعين: لتقييم أمر ما علينا فهمه أولاً. لكن فهم طبيعته وحده لا يعطينا جميع أسباب تقييمه. الاحتفاظ بهذا الفرق يقلل الخلط دون أن يلغي الروابط بين المسائل."""),
            ("ثلاث دقائق من الأسئلة الخفيفة", """1. أي عبارة تتناول القيمة مباشرة؟ أ. مم يتكون الشخص؟ ب. ما الذي يجعل الشخص اليوم هو نفسه غداً؟ ج. هل سيكون استمرار الوجود مرغوباً؟
2. قال عضو النادي: «أريد أن تبقى المناقشات، إذن الملف هو الدفتر الورقي نفسه». ما الخطوة غير المبررة؟ تكفي جملة قصيرة؛ لا حاجة إلى مقالة.
3. ضع سؤالاً واحداً من اختيارك في أحد فرعي الرسم. يمكنك البقاء داخل مثال الدفتر. إذا كان السؤال مركباً، قسمه إلى سؤالين. لا يُطلب منك تقديم إجابة نهائية أو الإفصاح عن معتقد شخصي."""),
            ("إجابات مقترحة وتلميح", """الإجابة الأولى هي ج؛ فهي تسأل عن كون الاستمرار مرغوباً، لا عن تركيبة الشخص أو معيار هويته. في الثانية، انتقل العضو من رغبة في الحفظ إلى حكم عن هوية جسمين. الرغبة لا تحدد ما إذا كان الملف والجسم الورقي شيئاً واحداً. يمكن أن تكون الرغبة مفهومة بينما تبقى دعوى الهوية محتاجة إلى توضيح مستقل.
في الثالثة لا توجد صياغة وحيدة لازمة. مثلاً «هل الملف يحفظ الكلمات نفسها؟» سؤال عن خاصية يمكن فحصها في المثال، و«هل يستحق الاحتفاظ به وقتاً إضافياً؟» سؤال عن التقييم. إن اختلطا عليك، ضع خطاً تحت الكلمة التي تحتاج إلى تعريف، مثل «نفسه»، أو تحت كلمة التفضيل، مثل «يستحق». تحديد موضع الالتباس جزء من الإجابة الجيدة."""),
            ("الخطوة التالية وحدود المصدر", """غداً نبقى في u01 وننظر في عرض موقفين عن طبيعة الشخص: الثنائية والمذهب الفيزيائي، كما تقدمهما المحاضرة الثانية. [S3] يكفي اليوم أن تحمل معك سؤالاً واضحاً، وأن تتذكر أن الاتفاق مع نتيجة لا يغني عن فحص الطريق إليها.
تثبت [S1] نسخة المقرر، وتدعم [S2] التمييز العام الذي بدأنا منه. أما الدفتر والخريطة والأسئلة فمن تأليف الدليل، وليست دليلاً مستمداً من أبحاث عن بقاء الأشخاص. مشاهدة المحاضرات وقراءة النصوص الأصلية تحتاج إلى وقت إضافي، ولم نتم اليوم المجموعة الأولى أو المقرر كله."""),
        ]),
        "sources": [
            _source("S1", "Death — PHIL 176", "https://oyc.yale.edu/death/phil-176", "جامعة ييل · المقررات المفتوحة", "الصفحة الأصلية لنسخة ربيع 2007 وبرنامج المقرر؛ تأكدت أيضاً إحالة العنوان القديم philosophy/phil-176 إليها.", "ربيع 2007"),
            _source("S2", "PHIL 176 — Lecture 1 — Course Introduction", "https://oyc.yale.edu/philosophy/phil-176/lecture-1", "جامعة ييل · المقررات المفتوحة", "صفحة المحاضرة الأصلية ونصها؛ تدعم التمييز العام بين الميتافيزيقا ومسائل القيمة. مثال الدفتر من تأليف الدليل.", "ربيع 2007"),
            _source("S3", "PHIL 176 — Lecture 2 — The Nature of Persons: Dualism vs. Physicalism", "https://oyc.yale.edu/philosophy/phil-176/lecture-2", "جامعة ييل · المقررات المفتوحة", "صفحة المحاضرة الأصلية ونصها؛ للتحقق من موضوع الخطوة التالية، دون عرضها كإجابة نهائية في اليوم الأول.", "ربيع 2007"),
        ],
        "figure": {"caption": "خريطة سؤال أصلية: فرع للوجود والهوية، وفرع للقيمة؛ لا تكفي الرغبة وحدها لإثبات الوجود.", "credit": "رسم مفاهيمي مستقل أُعد لهذا الدليل، وليس صورة من جامعة ييل أو نتيجة بحثية.", "concept": "Arabic RTL conceptual question tree: central السؤال branches into الوجود والهوية and القيمة. Under first ما الذي يستمر؟ under second هل هو مرغوب؟ Balanced branches, no causal cross arrow, no human mortality scenes. Plain readable diagram with correctly shaped logical Arabic."},
    },
]
