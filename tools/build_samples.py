"""Materialize authored content; rendering/review are explicit separate steps."""
import importlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/omni-learning-anything/scripts'))
import omni_core as c
from content.catalog import DATE,SOURCES,META,CAPTIONS
from content.objectives import OBJECTIVES
PHASES={
 'technology':['系统与证据','数字技术基础','人工智能','生命科学','能源与大型工程','技术与社会'],
 'economics':['个人选择与市场','企业与市场失灵','宏观指标','货币与政策','国际与分配','证据与综合解释'],
 'music':['主动聆听','声音组织','人声与乐器','西方风格入口','多元音乐经验','比较与表达'],
 'agent-product':['任务与控制','模型与信息','需求与验收','体验与风险','架构与商业','案例与面试'],
 'architecture':['古典与观察方法','中世纪','文艺复兴到巴洛克','工业时代','现代建筑','比较与遗产'],
 'ming-history':['明初与读史方法','国家制度','经济生活','社会文化','中后期变化','转折与综合论证']}
PUBLISHED={
 'https://www.metmuseum.org/essays/architecture-in-ancient-greece':'2003-10-01',
 'https://www.metmuseum.org/essays/theater-and-amphitheater-in-the-roman-world':'2006-10-01',
 'https://www.metmuseum.org/essays/ming-dynasty-1368-1644':'2002-10-01',
 'https://www.anthropic.com/engineering/building-effective-agents':'2024-12-19',
 'https://www.anthropic.com/engineering/writing-tools-for-agents':'2025-09-11',
 'https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents':'2026-01-09',
 'https://modelcontextprotocol.io/specification/2025-06-18':'2025-06-18（指定版本）'}
for slug,(topic,baseline,goal,prompt,topics) in META.items():
 root=ROOT/'examples'/slug
 if (root/'state.json').exists() and c.read(root/'state.json')['lessons']: raise SystemExit('Refusing to overwrite delivered samples: '+slug)
 objectives=OBJECTIVES[slug].split('|'); assert len(topics)==len(objectives)==30
 sources=[dict(id=f'S{i+1}',title=t,url=u,publisher=p,published_at=PUBLISHED.get(u,'未标注'),checked_at=DATE,note=n) for i,(t,u,p,n) in enumerate(SOURCES[slug])]
 figure=dict(path='assets/teaching.png',caption=CAPTIONS[slug],credit='AI生成教学示意，非实物照片、原始史料或官方架构。生成方式：内置文生图；提示词见仓库 docs/image-prompts.json。')
 config=dict(topic=topic,goal=goal,baseline=baseline,daily_minutes=15,timezone='Asia/Shanghai',time='10:00',weekdays=['MO','TU','WE','TH','FR','SA','SU'],language='zh',immediate_day01=True,sample_mode=True)
 days=[dict(day=i+1,topic=t,objective=objectives[i]) for i,t in enumerate(topics)]
 sections=[
 dict(title='学习者与目标',body=f'适合：{baseline}。\n\n本轮目标：{goal}。30天用于建立入门框架与方法，不承诺掌握整个学科。除明确说明的基础外，不假设学习者的行业经历。原始启动句：“{prompt}”'),
 dict(title='学习方式与时间安排',body='每天预计10–15分钟：正文与读图约8分钟，回忆和练习约3分钟，可用余下时间复述。学习速度存在差异，时间为估计值；扩展阅读不计入必做量。每天10:00（Asia/Shanghai，含周末）开始生成，检查完成后交付。计划确认后可立即生成Day01。\n\n本文件是公开演示样例：30天完整课纲，配套展示Day01–Day03；试跑不创建真实定时任务。图中A、B、C分别对应前三天的观察重点。'),
 dict(title='课程依据与学习成果',body=f'先从{topics[0]}进入，逐渐引入领域概念，再通过案例与复盘连接。来源[S1]和[S2]提供起点知识；其他链接扩展相关视角。课程排序是本项目的教学设计，不是来源机构为本项目背书。\n\n完成时应能：{objectives[0]}；{objectives[14]}；{objectives[29]}。每五天安排一次回顾或整合，检查能否脱离正文解释，不以“收到PDF”代替学会。')]
 for phase,name in enumerate(PHASES[slug]):
  rows=[f"Day{d['day']:02d}  {d['topic']}\n目标：{d['objective']}。" for d in days[phase*5:phase*5+5]]
  sections.append(dict(title=f'阶段{phase+1}：{name}',body='\n\n'.join(rows)))
 sections.append(dict(title='自测、调整与确认',body='每天先尝试作答，再看参考要点；答不出来时记录具体概念，不据此给自己贴能力标签。每五天用一张卡整理“已经能解释／仍不确定／需要查证”。若学习量过大，优先缩小每日范围并保留主线，不靠减小字体压缩材料。\n\n真实使用时，请确认目标、基础、周期、每天用时、执行时间、时区与输出目录。批准当前计划后才创建任务；修改已开始的课程时保留旧档案并建立新版本。到期漏跑则继续最早未交付课程，不按日期跳课。'))
 plan=dict(topic=topic,title=topic+'：30天学习计划',days=days,sections=sections,sources=sources,figure=figure)
 if not (root/'state.json').exists(): c.initialize(root,config,plan)
 lessons=importlib.import_module('content.'+slug.replace('-','_')).LESSONS
 for i,parts in enumerate(lessons,1):
  doc=dict(day=i,title=topics[i-1],reading_minutes=8,practice_minutes=3,sections=[dict(title=t,body=b) for t,b in parts],sources=sources,figure={**figure,'caption':f'本课重点看 {"ABC"[i-1]} 区。'+CAPTIONS[slug]})
  c.save(root/'data'/f'Day{i:02d}.json',doc)
 c.save(root/'intake.json',{'user_prompt':prompt,'answers':config,'approval_mode':'simulated for explicitly requested public examples','source_check_date':DATE,'search_performed':True,'verification_note':'Key pages read with web tool; Palace Museum page read directly from official HTML after web-tool fetch failure. No real learner data.'})
 print(slug,[sum(len(s['body']) for s in d['sections']) for d in [plan,*[c.read(root/'data'/f'Day{i:02d}.json') for i in range(1,4)]]])
