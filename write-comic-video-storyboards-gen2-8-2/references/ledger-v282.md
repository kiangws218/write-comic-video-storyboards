# V3 台账：2.8.2 存储与工具

规则见 core，本文件只定义格式。原记录仍用 V3，加 `skill_version: "2.8.2"`，不另建分轮事实账。旧 V3 未声明新版时走旧校验，修改版本号不能完成迁移。

## 各轮记录与版本对照

沿用一份V3工作台账：第一遍准备观察／原文／资料与初译，第二遍纠错、理解并完整写原镜六字段、局部表演和基本计时；适用P镜保留原表演卡。story_context沿用字符串数组，段首格写连贯事件与因果，其余格按需补充，不另起剧情表。

第二遍完成后保存台账和完整原镜底稿的只读版本快照（例如second-pass目录），工作台账继续迭代。快照是同一记录的版本，不是第二套持续维护的事实真值；保留快照文件SHA-256供对照。来源冻结只锁原作事实／全文，不锁最终镜号、时间或全部六字段。

第三轮在原镜底稿基础上创作，补齐最终映射／发声切分／邻接／分片；正式验证器检查最终成稿，不用于迫使第二轮先凑出最终剪辑。director_review沿用现有对象，在node_arrivals结论中写清与第二遍及原图对照后的原镜主动作／关键构图／表情与状态保留情况，不另增通用通过表。机器不能独立判断语义保真。

## 来源和对白锁

第一次精读对新段明确标记 requires_route_confirmation:true/false。关键动作段使用 action_routes:[{id,source_images,path,user_confirmation:{quote,sha256}}]；source_images按原格顺序，path为实际向用户展示的完整简明路径，quote如实引用用户明确确认或已给出的路径解释。先用 `python scripts/authoring.py ledger.json --route-digest 路径ID` 打印提案指纹；得到用户明确确认后才记录quote和该指纹。工具只算指纹，不确认路径；新提案改动后原确认失效。确认覆盖不到的原作路径必须另问，不能伪造用户原话。冻结、渲染与最终校验均拒绝待确认或已变更路径；旧记录缺字段仍兼容，不表示程序能自动发现未登记的关键动作。

根：version、skill_version、source_language、look（场景色彩基准）、panels、shots、performance、character_registry、source_lock、director_review。

每个 panel：

- image：唯一真实原格文件名，多格文件使用诚实裁图与原文件溯源。
- renderable_visual：布尔值；source_bubble_count 与 bubbles 行数一致。
- viewed_at_drafting、drafting_resolution（720p/1080p/original）、放大时 resolution_escalation_reason、bubble_audit：保留真实工作记录，不由工具代填。
- composition_lock、source_facts.entities/actions/relations、background：第一次观察，第二次纠错；不得被导演设计覆盖。
- node_state：已知原作节点的简短世界状态键值，如 `董白.持剑手: 右`、`董白.阶段: 腾空`；只放已知必要内容。
- anchor_target：承载本格节点的 `片段N/分镜N`；连续格合镜时可相同。
- narrative_kind：action/mixed/dialogue/state；动作／混合格 action_reading 包含 summary、phase、world_motion、screen_motion、grounding、basis，uncertainty 可选。它是动作理解，不将上下文判断冒充 source_facts；有此记录便纳入来源锁。旧2.8.2记录未分类会提醒补查。
- bubbles：每行 id、speaker、kind（dialogue/inner/narration）、source_text、锁定 script_text、status:mapped；不支持 omitted。
- 发声可用自身 target/start/seconds，或 segments 数组，每段 target/script_text/start/seconds；start 为本镜开头起的实际秒数。整段顺序拼回必须等于完整 script_text，声音归属和类型不变。原作确有重叠才登记 bubble.overlap:true。

纯拟声格 page_overlays 中的 sfx：kind/source_text/render:false/audio_meaning/target/audio_excerpt；audio_excerpt 必须实际写在目标【声音设计】。纯文字旁白仍走 bubbles 完整映射，不创建虚假原作视觉镜头。

第二次精读核对后运行 `python scripts/freeze_storyboard.py ledger.json`。工具写入 source_lock 的版本、来源／全文指纹与原格清单，不设置看图／语义通过。锁涵盖原格顺序、可视性、构图、事实、背景、node_state，以及原文、译文、归属和类型；不锁镜头数量、分段、target、时长或发声切分。

已冻结不允许覆盖。真实原文／翻译纠错先回图核对，再用 `--correction-reason "具体纠错原因"`；保存旧锁和原因，清除已过期最终审查，不能用该选项给导演改词背书。

## 镜头记录

### 默认精简写作格式

根增加 authoring_format:"compact-2.8.2"，仍为V3、2.8.2。来源panels、对白及六字段保持原格式，各只写一份。以下仅改变存储方式，原作、表演与差异门槛不变：

- 根 initial_state 写一次本段起始的必要世界状态；每镜 state_changes 只写镜内发生变化的键值，未改变可省略。工具继承上镜尾作为本镜头起点，合入变化作为镜尾；不自动推断动作或原格状态。必须人工对照动作正文、源节点与到达状态，继承不等于证明连续。需要时间省略重置时可用下面的完整格式，不混用两套状态字段。
- 根 cuts 每个实际切点只写一项记录：`{from:"片段1/分镜1",to:"片段1/分镜2",changes:[{dimension:"scale",description:"从双人中景切到听者眼部特写，反应成为重点",shot:"片段1/分镜2",field:"镜头设计"}]}`。有新增镜头的一侧必须覆盖；两侧均新增也只登记一次。工具给实际前后邻镜各绑定这一记录，以实际字段解析摘录；显著性仍须人工判断，不由景别标签或字符串不同保证。无变化、引用其他镜头、非实际邻接不成立。
- 表演卡写在所需镜头的 performance:{card,details,intervals} 内，不另建根performance和重复target。卡先规划，details只摘实际动作中的必要短句，不能复制整段充当计划；工具只搬运到既有检查格式，不代写卡或计时。
- 其他原格映射、anchors、meaning_excerpt、看图和审查记录仍如实保留；机械工具不代填viewed、pass、用户确认、剧情解释、重要动作或显著差异。

`render_storyboard.py`、`freeze_storyboard.py`和`validate_storyboard.py`直接接收精简台账，无需手工展开。排障才运行 `python scripts/authoring.py ledger.json --expand compiled-ledger.json`；展开文件为派生产物，不回写创作台账、不让模型通读、不建立第二套维护记录。最终正文由渲染器输出；只读取本次问题和受影响片段，避免成稿、全台账与逐镜审查报告三份来回复述。模块首次按阶段读取，后续查相关段落，脚本直接执行；两次真实精读保留。

### 完整兼容格式

每镜 target、duration（正整数秒）、role、source_images、purpose、characters（在场人物名称数组）、risk_flags（D/P/G 数组）、risk_basis、state_in、state_out、fields。

fields 为六个中文字段名对应的实际正文字符串，不含字段标签。正式每条发声单独一行，例如 `人物（画外音）：“锁定原句的实际片段”（语气）。` 内心／旁白写在角色括号里；本例文字不是可复制到成稿的占位。

- source_locked：source_images 为按顺序登记的真实可视原格。单格继续使用 anchor_phase（preparation/process/middle/contact/reaction/result/state/endpoint）、anchor_elements、anchor_state；有 action_reading 时 meaning_excerpt 必须摘录实际【可见动作】，人工比较其是否实现源含义。anchor_state 包含本格 node_state 的全部已知键并一致。viewed_while_writing/source_audit 如实；frame_adaptation 记录画幅适配，不重写源观察。
- 连续原格合镜：另有 merge_basis 说明为何是同一连续动画镜头；anchors 与 source_images 一一同序，每项 image/start/anchor_phase/anchor_elements/anchor_state/action_excerpt，以及适用的 meaning_excerpt。start 为该节点在本镜内经过的秒数，严格递增但不要求停住。各 action_excerpt 摘录实际动作正文，不能只写源图清单。镜头设计先写统一机位或连续运镜，再逐行使用 `- 参考 [a.jpg]（起势）：该阶段构图` 格式；合并不自动生成理由或审查结论。
- source_supported_phase、uncited_coverage：均是新增镜头，source_images:[]，无正式原镜引用，derived_from 关联本场相关原格，可多个，不限两个相邻证据。创作内容记录 creative_additions，缺证据不阻塞。purpose 说明演出作用，不需要台词。
- state_in/state_out：非空扁平对象，使用世界关系与稳定简写，公共键跨连续切点须相等。状态变化演在镜内，不写画面左右充当世界坐标。没有共同键时机械检查无法证明连续，需人工检验节点与连接。
- 真正场景／时间省略才使用 boundary:{from:前镜target,kind:"ellipsis",reason:具体理由}，会提示人工检查，不能借此掩盖普通动作跳变。
- 明确写出的沉默用 silences:[{start:0,seconds:2}]，与【台词与语气】中的 `（沉默2秒）` 一一对应，位置正确、不与发声重叠。纯“无台词”镜无需为全镜额外造沉默标记。

新镜头 neighbor_contrast.previous / next 各为对象：target 为最终紧邻镜头，changes 为非空数组，至少一条有 dimension、description、excerpt。dimension 为 subject/scale/viewpoint/composition/information/action_phase/emotion/rhythm/dramatic_function。excerpt 从当前或该邻镜的实际字段摘取；程序只能检查落实和邻接，显著性由导演审查，不由标签保证。首尾缺邻接的一侧不填写。

P 镜复用 performance 数组：target、card.opening/beats（非空字符串数组）/coupling/landing、details（动作字段准确摘录）、intervals（speech_seconds/acting_seconds/concurrent）。间隔依次发生，间隔内 concurrent:true 用最长时间，false 相加。不要为了填卡自动全镜并行，也不为物品镜硬造表演。

character_registry 是项目共享人物主档中本话出场条目的快照，不是独立维护的第二套设定。每项 id/canonical_name/aliases/identity_status、performance_profile:{baseline,source}；没有性格资料则基调明确写未确认、本场策略标注上下文，不编造恒定性格。character_registry_source 记录主档 path/version/读取日期，可附 sha256，进入最终审查指纹；新话及开导演轮前主动核对主档新版本，不声称工具会自动同步文件。

未识别角色 identity_status:"unidentified"，额外 color_prompt 与 color_basis：前者是交付用完整上色提示词，后者在台账中注明参考／沿用配色／生产设计的来源。渲染器将稳定ID、统一称呼与提示词集中放在脚本开头；缺提示或正式称呼使用已登记别称时校验报错。颜色未给定可作一致的生产设计，不要求用户逐色批准。具体维护边界见 [character-registry.md](character-registry.md)。

## 渲染和最终审查

`python scripts/render_storyboard.py ledger.json storyboard.md` 只输出已经规划的真实字段与时长／引用，不修改输入、不补对白、不默认角色、不发审查证明。输出后再实际对图与整段检查，修正记录后重新渲染。

director_review 是根对象，characters/pacing/node_arrivals/contrast 写具体结论，sha256 绑定最终文本、镜头／状态／表演、角色基准和来源锁。运行 `python scripts/freeze_storyboard.py ledger.json --review-digest storyboard.md` 只打印版本指纹；人工完成检查后把指纹与说明写入，不能用指纹声称完成读图、动态分镜或质量验证。

源观察不变的局部改动仍保留；文字、镜尾、邻接、时长或角色记录变化会使最终审查指纹失效。按 core 只重查相关内容，最终绑定实际版本。记录 revision_audit 真实范围；未实际播放写“文字前向检查”，不写成片通过。

使用统一入口：`python scripts/validate_storyboard.py storyboard.md --source-ledger ledger.json --require-source-ledger --image-dir proxies`。错误需修正；来源 warnings 可保留，不必逐项消警。程序检查完整性、字面一致性、时间与记录关系，无法独立发现所有翻译／视觉／角色／物理／艺术问题。
