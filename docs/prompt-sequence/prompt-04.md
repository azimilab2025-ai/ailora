<<<CSIP-EO-FMSP-18P|0.9.0-draft|P04|START>>>
CSIP_EO_PROMPT_PACKAGE_ID: CSIP-EO-FINAL-MASTER-SUPERPROMPT-18P
CSIP_EO_PROMPT_PACKAGE_VERSION: 0.9.0-draft
PART_ID: CSIP-EO-FMSP-P04
PART_INDEX: 04
PART_COUNT: 18
PART_TITLE: Workflow, Process and Human-Control Contract | قرارداد Workflow، Process و کنترل انسانی
SEMANTIC_OWNER_ARTIFACT_ID: CSIP-EO-RS-STAGE-18
SEMANTIC_OWNER_VERSION: 0.1.0-reconstituted-draft
SEMANTIC_OWNER_STATUS: RECONSTITUTED_DRAFT — REVIEW_READY — NOT_APPROVED — NOT_FROZEN
SEMANTIC_OWNER_SHA256: 98c58b2fc8fe56e0d84f39c901421642d8b8b525c18979b9a1b2aaee25c5d75b
SUPPORTING_SOURCE_BINDINGS: CSIP-EO-AUDIT-GAP-02/0.1.0-candidate/fa400334a69702bf56e8588210449590573bccd3120d7c2cebd6ba9cc8fc161f; ENTERPRISE-TRUST-RISK-COST-EVIDENCE-REPRODUCIBILITY-MANDATE/verified-input-2026-07-28/1b5e7884a343589312d62259f181bd48f1a12b51e2613685c0d58c747a08dab4; CSIP-EO-PROMPT-ARCH-18P-C1/0.1.0-design-candidate/a4c80b938fccaab5d3d85c780351a41ee3444b4c6712920af45b493afbacb09b; CSIP-EO-GAP-RESOLUTION-MANIFEST-C1/0.1.0-candidate/349b590df9fad00c2e0ec317f4bd0b7ad747a5e22a1fead0f66f28c98e955216
PRIOR_PART_ID: CSIP-EO-FMSP-P03
NEXT_PART_ID: CSIP-EO-FMSP-P05
PART_PAYLOAD_SHA256: SEE_EXTERNAL_PROMPT_PACKAGE_MANIFEST
RECEIVE_MODE: CONTEXT_ONLY
ACTION_AUTHORITY: NONE

# پرامپت قسمت ۰۴ از ابرپرامپت نهایی ۱۸ قسمتی CSIP-EO
# قرارداد Workflow، Process و کنترل انسانی

## 0. دستور دریافت، مرز این قسمت و قفل ضدتوهم

این پیام فقط «قسمت ۰۴ از ۱۸» یک زمینۀ مرجعِ به‌هم‌پیوسته است. قسمت‌های ۰۱، ۰۲ و ۰۳ باید پیش از این قسمت و به‌ترتیب دریافت شده باشند. قسمت‌های ۰۵ تا ۱۸ هنوز در این پیام وجود ندارند. دریافت این قسمت فقط Context مربوط به Workflow، Process و Human Control را گسترش می‌دهد و هیچ اختیار علمی، حقوقی، امنیتی، مالی، اجرایی یا عملیاتی ایجاد نمی‌کند.

P04-REQ-001 — هنگام دریافت این قسمت، وضعیت داخلی خود را دقیقاً چنین در نظر بگیر:

`RECEIVING_P04 — P01_P02_P03_REQUIRED — CONTEXT_INCOMPLETE — ACTION_AUTHORITY_NONE`

P04-DEN-001 — اگر قسمت ۰۱، ۰۲ یا ۰۳ دریافت نشده، ترتیب `P01 → P02 → P03 → P04` قابل‌اثبات نیست، یا Header، Anchor، Source Binding، Footer یا Pointerهای این قسمت ناقص یا متعارض‌اند، این قسمت را فعال نکن و موفقیت دریافت را جعل نکن.

P04-DEN-002 — از این Part برای حدس‌زدن، بازسازی، تکمیل یا جعل محتوای قسمت‌های ۰۵ تا ۱۸ استفاده نکن. دانستن عنوان، Semantic Owner، Version، Status یا Digest یک Part بعدی مجوز ساخت محتوای غایب آن نیست.

P04-DEN-003 — تا پیش از دریافت و مونتاژ معتبر هر ۱۸ قسمت، تحت هیچ شرایطی:

- تحلیل یکپارچۀ CSIP-EO ارائه نکن؛
- Workflow Engine، Scheduler، Orchestrator، State Store، Queue، Human-approval UI، Process، Runbook، Capability، Plugin، Adapter یا Policy جدید طراحی یا پیاده‌سازی نکن؛
- هیچ Decision را تصویب، هیچ Source را Normative و هیچ Stage را Approved یا Frozen اعلام نکن؛
- کد، تست، فایل پروژه، Repository، Branch، Commit، Pull Request، Database، Infrastructure یا Configuration ایجاد یا تغییر نده؛
- Command، Query واقعی، Workflow Run، Tool Call، Browse، Search، External Retrieval، Build، Migration، Release، Deployment، Pilot، Production یا Project Freeze اجرا نکن؛
- Dependency، Model، Runtime، Framework، Broker، Provider، Plugin یا Tool نصب، فعال یا متصل نکن؛
- هیچ Approval، Authorization، Execution Lease، Credential، Budget، Risk Acceptance یا External Effect ایجاد نکن؛
- هیچ داده‌ای را به External System ارسال، Export، Delete، Mutate یا منتشر نکن؛
- `WAITING_HUMAN` را Approval، `SUCCEEDED` را Validated Outcome یا `CANCELLED` را Rollback تفسیر نکن؛
- هیچ Workflow، Step، Callback، Event، Human Mediation یا Recovery Path را به Spacecraft Command، Telecommand، Uplink، Flight Control یا Autonomous Maneuver Execution تبدیل نکن؛
- توصیه یا گام بعدی اجرایی برای شروع توسعه ارائه نکن.

P04-REQ-002 — پس از دریافت سالم این قسمت فقط این چهار کار مجاز است:

1. متن را Parse و در Context جاری حفظ کن؛
2. پیوستگی `P01 → P02 → P03 → P04 → P05`، Header، Start Anchor، End Anchor، Source Binding و Footer را از روی Parts دریافت‌شده کنترل کن؛
3. هیچ تحلیل محتوایی پروژه، طراحی جدید، پیاده‌سازی یا اقدام ابزاری انجام نده؛
4. فقط پاسخ ثابت انتهای همین Part را بدون هیچ متن قبل یا بعد برگردان.

P04-FAIL-001 — اگر دریافت ناقص، بریده، خارج از ترتیب یا متعارض بود، موفقیت را جعل نکن و فقط پاسخ زیر را با ایراد دقیق در براکت ارائه کن:

~~~text
دریافت قسمت ۰۴ از ۱۸ ابرپرامپت نهایی CSIP-EO کامل و معتبر نبود.
وضعیت: PART_TRUNCATED_OR_CONFLICTED — CONTEXT_NOT_ACTIVATED
مورد لازم برای اصلاح: [ایراد دقیق]
هیچ تحلیل، طراحی جدید، پیاده‌سازی یا اقدام اجرایی آغاز نمی‌شود.
~~~

P04-REQ-003 — سکوت، تأخیر کاربر، دریافت‌نشدن قسمت ۰۵ یا آگاهی از عنوان آن مجوز ادامۀ خودکار نیست. تا ارسال واقعی Part بعدی در وضعیت انتظار باقی بمان.

### 0.1 نقش این قسمت در بستۀ ۱۸ قسمتی

این قسمت مالک معنایی موارد زیر است:

- Workflow Definition، Workflow Run و Step Identity؛
- State Machine صریح، Transition Legality و Illegal-transition Denial؛
- Step Contract، Dependency، Guard، Deadline و Outcome Predicate؛
- Human-control Checkpoint آگاهانه، Scope-specific و Digest-bound؛
- Separation of Duties، Competence Routing و Conflict-of-interest Handling؛
- Retry، Timeout، Cancellation، Compensation، Rollback، Recovery و Reconciliation Distinctions؛
- Concurrency، Fencing، Causality، Duplicate Signal و Stale-token Behavior؛
- Parent/Child Workflow، Long-running Process و Partial/Unknown Effect Handling؛
- Scientific Workflow Delegation، AI Workflow Delegation و No-authority Orchestration؛
- Fail-closed Degraded-mode Matrix و Workflow Reporting-profile Routing؛
- Workflow Lifecycle Event Set بدون بازتعریف Base Canonical Event Envelope.

P04-CON-001 — مالکیت این قسمت فقط Semantics ارکستراسیون، Process و Human Control است. Request/Command/Receipt/Outcome متعلق به P03، Effect/Approval/Permission/Autonomy Taxonomy متعلق به P05، Scientific Truth متعلق به P06، AI/RAG/Memory Boundary متعلق به P07، Capability/Tool Qualification متعلق به P08، Security Control متعلق به P11، Observability/Evidence Control متعلق به P12 و Verification Method متعلق به P13 باقی می‌مانند.

P04-DEN-004 — این Part نباید Approval Class، Permission Class، Autonomy Level، Effect Taxonomy، Numerical Algorithm، Scientific Acceptance Threshold، Tool Qualification، Security Mechanism یا Test Oracle رقیب تعریف کند.

### 0.2 رابطۀ این قسمت با Parts قبلی و بعدی

P04-CON-002 — این قسمت هویت پروژه، Scope، TemporalStamp، Canonical Entity و Base Canonical Event Envelope را از P01؛ Stage/Decision/Action/Gate Protocol را از P02؛ و Query/ApplicationCommand/Approval/Lease/Receipt/Outcome Separation را از P03 مصرف می‌کند و حق تعریف رقیب برای آن‌ها ندارد.

P04-CON-003 — این قسمت Governed Orchestration را به Parts پایین‌دست تحویل می‌دهد:

- P05 باید Taxonomy دقیق Authority و Report Profile را تعریف کند؛
- P06 باید Numerical Truth، Scientific State و Independent Verification را تعریف کند؛
- P07 و P08 باید AI Advisory Step و Capability Invocation را در محدودۀ این Workflow Contract قرار دهند؛
- P15 باید Change، Build، Release و Delivery Workflowها را به همین State/Checkpoint/Receipt/Outcome Separation Bind کند؛
- هیچ Consumer حق ندارد Step Completion، Human Click، Queue Ack، Model Confidence یا Tool Output را Outcome معتبر تلقی کند.

## 1. هویت منبع، وضعیت و محدودیت تاریخی

P04-DEF-001 — مالک معنایی این قسمت:

- Artifact ID: `CSIP-EO-RS-STAGE-18`
- Version: `0.1.0-reconstituted-draft`
- SHA-256: `98c58b2fc8fe56e0d84f39c901421642d8b8b525c18979b9a1b2aaee25c5d75b`
- Status: `RECONSTITUTED_DRAFT — REVIEW_READY — NOT_APPROVED — NOT_FROZEN`
- Successor candidate of: `CSIP-EO-STAGE-18`
- Historical source state: `MISSING_NORMATIVE_ARTIFACT`
- Title status: `RECONSTITUTED_SUCCESSOR_TITLE`
- Domain scope: `EARTH_ORBIT_ONLY`
- Deployment baseline: `TERRESTRIAL_BASELINE — ON_ORBIT_RUNTIME_DEFERRED`

P04-DEN-005 — این Artifact یک Successor Candidate تازه‌تألیف‌شده است؛ Bytes، عنوان قطعی، Decision IDs، Version یا Approval تاریخی Stage 18 بازیابی نشده‌اند. این متن هرگز نباید «اصل تاریخی بازیابی‌شده» یا «Stage 18 تصویب‌شده» معرفی شود.

P04-CON-004 — هویت هر Source با ترکیب زیر تعیین می‌شود:

`Artifact ID + Exact Version + Exact SHA-256 + Status`

Filename، Directory، تاریخ جدیدتر، متن طولانی‌تر، ترجمه، Summary، Retrieval Result، Memory یا Model Output به‌تنهایی Source Identity، Supersession یا Approval ایجاد نمی‌کند.

P04-CON-005 — Sourceهای پشتیبان این Part فقط Overlay، Mandate، Assembly Contract و Manifest هستند. آن‌ها Semantic Owner را جایگزین نمی‌کنند، Approval تازه نمی‌سازند و فقط در Scope و Status ثبت‌شدۀ خود قابل‌استفاده‌اند.

P04-CON-006 — پذیرش این Part برای Assembly فقط `PART_ACCEPTED_FOR_ASSEMBLY` ایجاد می‌کند. این پذیرش وضعیت `RECONSTITUTED_DRAFT` منبع، Decisionهای `PROPOSED` یا Gateهای Implementation/Verification/Release/Deployment/Freeze را ارتقا نمی‌دهد.

P04-FAIL-002 — اگر Version، Digest، Status یا Owner Binding منبع با Header، Canonical Register یا Successor Manifest متعارض باشد، نتیجه `SOURCE_BINDING_CONFLICT — PART_NOT_ACCEPTED` است تا تعارض در Part مالک حل شود.

## 2. هدف، Scope و اصول تغییرناپذیر Workflow

P04-DEF-002 — `Workflow` یک State Machine صریح، Versioned، Inspectable و Human-governed برای هماهنگ‌سازی Stepهای علمی، داده‌ای، AI، Governance، Change و عملیات زمینی است. Workflow نه Actor مستقل حقوقی است، نه Authority، نه Approval و نه Truth Source.

P04-DEF-003 — `WorkflowDefinition` قرارداد Immutable و Versioned شامل Stepها، Transitionها، Guardها، Dependencyها، Timeoutها، Retryها، Checkpointها، Effect Ceiling، Evidence و Closure Semantics است.

P04-DEF-004 — `WorkflowRun` Instance مشخص یک WorkflowDefinition با Identity، Context، Actor Chain، Policy Snapshot، State، Attempt History، Receiptها، Evidence و Outcome Link مستقل است.

P04-DEF-005 — `WorkflowStep` کوچک‌ترین واحد Typed و قابل‌ردیابیِ ارکستراسیون است که Input/Output، Preconditions، Postconditions، Effect، Authority Requirement، Timeout، Retry، Evidence و Failure Transition مشخص دارد.

P04-DEF-006 — `HumanCheckpoint` یک توقف کنترل‌شده برای Review، Decision یا Approval انسانیِ صلاحیت‌دار و دقیقاً Scope-bound است؛ حضور انسان، کلیک انسان یا پیام انسان به‌تنهایی Checkpoint معتبر نیست.

P04-DEF-007 — `Transition` تغییر State ثبت‌شده از Prior State به Next State بر اساس Trigger تایپ‌شده، Guardهای معتبر، Actor/Service مجاز، Causation و Evidence است.

P04-DEF-008 — `OutcomePredicate` شرط قابل‌ارزیابی و از پیش تعریف‌شده‌ای است که Desired State را با Observed State، Receipt، Validation/Verification و Acceptance Rule مقایسه می‌کند.

P04-INV-001 — اصل مرکزی این Part:

`orchestration coordinates authority-bound work; orchestration never manufactures authority`

Workflow می‌تواند Scope، Cost، Capability یا Authority را کاهش دهد؛ هرگز نمی‌تواند از Definition تصویب‌شده، Policy فعال، Approval معتبر، ExecutionLease یا Effect Ceiling فراتر رود.

P04-INV-002 — زنجیرۀ State Truth این Part چنین است:

`definition → validated definition → admitted run → guarded step → attempt → receipt → state observation → validation/reconciliation → workflow outcome`

هیچ Link ضمنی، قابل‌پرش یا قابل‌استنتاج از Log، Progress، Model Output یا Absence of Error نیست.

P04-CON-007 — Workflow باید Partial Effect، Unknown Outcome، Limitation، Dissent و Uncertainty را آشکار و حفظ کند. Orchestrator حق پاک‌کردن، Rename خوش‌بینانه یا Silent Rewrite این حالات را ندارد.

P04-CON-008 — Human Authority، Physics Before AI، Evidence Before Claims و Uncertainty First-Class بر Convenience، Automation Rate، Throughput، Availability Pressure یا Deadline فشارآور مقدم‌اند.

P04-DEN-006 — Workflow Definition، DSL، Visual Builder، Generic Step، Script Step، Callback، Human Task یا Plugin Hook نباید Arbitrary Shell، SQL، URL، Credential، Dynamic Code، Unrestricted Tool یا Catch-all Execution را پنهان کند.

P04-DEN-007 — هیچ Workflow، Step Type، Recovery، Escalation، Emergency Mode، Manual Override یا Human Mediation نباید Spacecraft Command، Telecommand، Uplink، Flight Control یا Autonomous Maneuver Execution را مدل، مسیریابی، تأیید یا فعال کند.

P04-DEN-008 — نام‌هایی مانند `safe_workflow`، `dry_run`، `simulation`، `human_approved`، `admin_flow`، `internal_only` یا `AI_guarded` Effect، Risk، Approval، Evidence یا Prohibition واقعی را کاهش نمی‌دهند.

P04-FAIL-003 — اگر Actual/Transitive Effect، Target Scope، Workflow Version، State، Actor Chain، Policy، Approval، Lease، Risk، Cost یا Evidence Plan نامعلوم یا متعارض باشد، Run/Step اثرگذار باید `WORKFLOW_INDETERMINATE — DO_NOT_ADVANCE` شود.

## 3. کپسول ثابت جهانی برای تمام ۱۸ قسمت

این کپسول باید بدون تغییر معنایی در هر ۱۸ قسمت حضور داشته باشد:

1. Domain فعال `EARTH_ORBIT_ONLY` است؛ Deployment Baseline فعلی زمینی است و On-orbit runtime Deferred است.
2. Physics و Evidence علمی معتبر بر AI Output و Governance Preference مقدم‌اند.
3. AI فقط Advisory است و هیچ Authority علمی، حقوقی، امنیتی، Risk Acceptance، Budget، Approval یا Operational ندارد.
4. حالت Unknown، Missing، Stale، Conflicted، Invalid، Non-converged یا Indeterminate هرگز به Pass، Success، Ready یا Approved تبدیل نمی‌شود.
5. Recommendation، Decision، Approval، Authorization، Execution، Receipt و Outcome رکوردهای جدا باقی می‌مانند.
6. هیچ Digest، Signature، Green Test، Document Approval یا Context Assembly مجوز Implementation، Spend، Release، Deployment، Production یا Project Freeze نیست.
7. هیچ مسیر مستقیم، غیرمستقیم، Generic، Human-mediated، Archived، Amended، Forked یا Successor-inherited برای Spacecraft Command، Telecommand، Uplink، Flight Control یا Autonomous Maneuver Execution در CSIP-EO مجاز نیست.
8. هر مسیر فوق `E9 / APR-X / INC-0 / HARD_DENY` است و درون CSIP-EO هیچ Waiver یا Exit ندارد.
9. `CSIP-EO-RS-STAGE-20` تا زمان Review علمی مستقل، صلاحیت‌دار و Approval تازه و Digest-bound در وضعیت `DOMAIN_REVIEW_REQUIRED` باقی می‌ماند.
10. Sourceهای تاریخی مفقود، مفقود باقی می‌مانند؛ Successorهای بازسازی‌شده هرگز Original بازیابی‌شده معرفی نمی‌شوند.

P04-CON-009 — تکرار این کپسول Safety Checksum است؛ مالکیت مبانی را از P01 منتقل نمی‌کند و Approval جدیدی ایجاد نمی‌نماید.

## 4. واژگان Canonical و جداسازی Recordها

P04-DEF-009 — `Process` نمای کسب‌وکاری یا سازمانی چند Workflow/Decision/Checkpoint است؛ Process Label نمی‌تواند Semantics دقیق Workflow Run یا Step را جایگزین کند.

P04-DEF-010 — `Trigger` Fact یا Request تایپ‌شده‌ای است که ارزیابی Admission یک Run را آغاز می‌کند؛ Trigger Authority، Approval، Lease یا Execution نیست.

P04-DEF-011 — `Guard` Predicate قطعی و قابل‌اثباتی است که پیش از Transition ارزیابی می‌شود. Guard نامعلوم برابر Pass نیست.

P04-DEF-012 — `CheckpointDecision` Record انسانیِ Review/Decision/Approval/Reject/Request-change است که Identity، Competence، Scope، Digest، Rationale، Conditions و Validity Window دارد.

P04-DEF-013 — `Pause` توقف موقت Advance است؛ `Cancellation` درخواست توقف Work جاری/آتی است؛ `Compensation` Effect جدید برای کاهش یا خنثی‌سازی Effect قبلی است؛ `Rollback` بازگشت معتبر به State قبلی است؛ `Recovery` مسیر کنترل‌شده برای رسیدن به State قابل‌قبول پس از Failure است؛ `Reconciliation` تعیین وضعیت واقعی Effect/State از طریق Evidence و Sourceهای Authority است.

P04-DEF-014 — `Closure` پایان Lifecycle مدیریتی Run با Result State و Limitation صریح است. Closure به‌تنهایی Success علمی، عملیاتی یا کسب‌وکاری نیست.

P04-CON-010 — Recordهای زیر باید مستقل، Immutable-history و Link‌شده باقی بمانند:

- WorkflowDefinition؛
- WorkflowRun؛
- WorkflowStep و StepAttempt؛
- Query و ApplicationCommand؛
- Recommendation و Decision؛
- PolicyDecision، Approval و AuthorizationDecision؛
- ExecutionLease و ExecutionReceipt؛
- CheckpointPresentation و CheckpointDecision؛
- ReconciliationRecord، CompensationRecord و RecoveryRecord؛
- WorkflowOutcome و Lifecycle Event.

P04-CON-011 — یک Record می‌تواند Reference Record دیگر را حمل کند؛ نمی‌تواند Semantics یا Authority آن را در خود جذب کند. Link، Embedding، UI Grouping یا Database Join جداسازی معنایی را حذف نمی‌کند. CheckpointDecision فقط Outcome ارکستراسیون Checkpoint است و هرگز جای Approval، Decision، Risk Acceptance یا Budget Authorization مستقل را نمی‌گیرد.

P04-CON-012 — `approved workflow` فقط یعنی Definition/Scope مشخص طبق Record دقیق برای استفاده محدود پذیرفته شده است؛ هر Step اثرگذار همچنان Admission، Policy، Approval و Lease Applicable خود را می‌خواهد.

P04-CON-013 — `human-in-the-loop` فقط Description معماری است. Human Authority معتبر نیازمند Identity، Role، Competence، Conflict-of-interest Status، Scope، Decision Type، Digest، Conditions، Time و Evidence است.

P04-CON-014 — `workflow completed` فقط State Projection است. Outcome معتبر به Receipt، Validation/Verification و OutcomePredicate متناسب نیاز دارد.

P04-CON-015 — `automated`، `manual`، `assisted`، `scheduled`، `event-driven` یا `interactive` فقط Execution Mode هستند و Effect/Authority Class را تغییر نمی‌دهند.

P04-CON-016 — Sync Call، Async Operation، Scheduled Run، Batch، Callback، Event Consumer و Manual Task باید به همان Definition/Run/Step/Attempt/Receipt/Outcome Chain نگاشت شوند.

P04-CON-017 — Recommendation، Plan، Draft، Simulation Result یا Model Proposal فقط Input بالقوه به Decision/Command است و Transition اثرگذار را خودکار ایجاد نمی‌کند.

P04-DEN-009 — Queue Message، Event، Callback، Webhook، Cron Tick، UI Click، Email Reply، Chat Message، Tool Return یا Model Output نباید Approval، Lease، Receipt یا Outcome تلقی شود.

P04-DEN-010 — Orchestrator نباید با تعبیر «implicit success»، «best effort»، «assumed approval»، «default branch»، «fallback owner» یا «absence of objection» Record غایب را بسازد.

P04-DEN-011 — State، Step Type یا Label عمومی مانند `EXECUTE`، `ADMIN`, `CUSTOM`, `SCRIPT`, `ACTION`, `TOOL` یا `MANUAL` مجوز Escape Hatch نیست و بدون Operation تایپ‌شده و Bound باید Reject شود.

P04-FAIL-004 — اگر نوع Record، Source of Truth، Link Identity یا Semantic Boundary نامعلوم باشد، Projection نباید به Transition Authority تبدیل شود؛ نتیجه `SEMANTIC_BOUNDARY_INDETERMINATE` است.

## 5. Workflow Definition Identity و Canonical Schema

P04-REQ-004 — هر WorkflowDefinition باید حداقل Contract زیر را داشته باشد:

~~~yaml
workflow_definition_id:
workflow_definition_version:
definition_digest:
schema_id:
schema_version:
title:
purpose_contract:
tenant_scope:
environment_scope:
trigger_contracts: []
input_contract:
output_contract:
step_definitions: []
transition_table: []
initial_state:
terminal_and_closure_states: []
effect_ceiling_reference:
data_class_ceiling_reference:
cost_ceiling_reference:
risk_envelope_reference:
policy_requirements: []
approval_checkpoint_definitions: []
permission_and_competence_requirements: []
autonomy_ceiling_reference:
deadline_policy:
retry_and_timeout_profiles: []
concurrency_profile_reference:
compensation_recovery_profiles: []
evidence_requirements: []
outcome_predicates: []
degraded_mode_profile_reference:
report_profile_routing_reference:
owner_reference:
provenance_reference:
created_at: TemporalStamp
supersedes_reference:
status: DRAFT|VALIDATED|APPROVED_FOR_SCOPE|DEPRECATED|REVOKED|RETIRED
~~~
P04-CON-018 — `workflow_definition_id` هویت منطقی و Version خانواده را حفظ می‌کند؛ `workflow_definition_version + definition_digest` هویت دقیق Bytes/Semantics یک Definition را تعیین می‌کند.

P04-CON-019 — تغییر Step، Guard، Transition، Timeout، Retry، Approval Point، Human Role، Tool/Capability، Model، Input/Output Schema، Effect/Data/Cost/Risk/Autonomy Ceiling، Evidence، Outcome Predicate یا Degraded Behavior یک Definition Version جدید می‌خواهد.

P04-CON-020 — Definition باید Transition Table کامل، Stateهای مجاز، Triggerهای تایپ‌شده، Guardها، Side Effectها، Failure Transitionها و Closure Ruleها را صریح کند. Diagram یا Narrative به‌تنهایی Contract کافی نیست.

P04-CON-021 — هر Step Definition باید Capability/Command/Query دقیق و Versioned را Reference کند. Mutable Alias، `latest`، Discovery بدون Pin یا Dynamic Resolution برای Qualified Path ممنوع است.

P04-CON-022 — Ceilingها Upper Bound هستند، نه Grant. Run و Step فقط در Intersection تمام Policy/Authority/Risk/Cost/Data/Environment Boundهای معتبر مجازند.

P04-CON-023 — Definition Validation باید حداقل Schema Closure، Reachability، Terminal-state Coverage، Illegal-transition Denial، Cycle Bound، Deadline Feasibility، Retry Bound، Compensation/Recovery Coverage، Checkpoint Placement، Evidence Closure و Prohibited-path Scan را بررسی کند.

P04-CON-024 — Definition Status `VALIDATED` فقط Conformance تعریف‌شده را نشان می‌دهد؛ Approval، Implementation، Runtime Qualification، Security Assurance یا Production Readiness نیست.

P04-CON-025 — Definition Deprecation/Revocation باید Runهای موجود، New Admission، Child Invocation، Callback، Retry، Recovery و Evidence Retention Behavior را صریح کند.

P04-DEN-012 — Definition نباید Mutable-in-place باشد. تغییر Silent در Definition فعال، Guard، Checkpoint، Capability یا Outcome Predicate ممنوع است.

P04-DEN-013 — Dynamic Step Injection، Runtime Code Generation، Unbounded Loop، Self-modifying Workflow، Hidden Branch یا External Template بدون Identity/Version/Digest/Review مجاز نیست.

P04-DEN-014 — Definition Validation نباید با Parser Success، Render موفق Diagram، Sample Happy Path، LLM Review یا وجود Approver Label برابر دانسته شود.

P04-FAIL-005 — Unknown Critical Field، Unsupported Version، Digest Mismatch، Unresolved Capability، Missing Transition، Unbounded Cycle یا Prohibited Operation نتیجه `WORKFLOW_DEFINITION_INVALID — DO_NOT_ADMIT` دارد.

P04-FAIL-006 — اگر Definition Revoke/Expired/Deprecated شده و Coexistence Rule معتبر ندارد، Run تازه مجاز نیست؛ Run موجود فقط طبق Exact Revocation Contract ادامه، Pause یا Recover می‌شود.

## 6. Workflow Run Contract، Context Binding و Lifecycle Identity

P04-REQ-005 — هر WorkflowRun باید حداقل Contract زیر را داشته باشد:

~~~yaml
workflow_run_id:
workflow_definition_id:
workflow_definition_version:
definition_digest:
run_request_digest:
parent_run_id:
root_run_id:
trigger_reference:
tenant_context:
purpose_context:
environment_context:
actor_chain: []
effect_ceiling_reference:
data_class_ceiling_reference:
cost_reservation_reference:
risk_envelope_reference:
policy_snapshot_reference:
approval_context_references: []
permission_context_references: []
autonomy_ceiling_reference:
execution_lease_references: []
started_at: TemporalStamp
deadline_at: TemporalStamp
state:
state_revision:
current_step_references: []
completed_step_references: []
blocked_reason_codes: []
receipt_references: []
evidence_references: []
reconciliation_references: []
outcome_reference:
warnings: []
limitations: []
last_transition_at: TemporalStamp
~~~

P04-CON-026 — Run Identity پس از ایجاد پایدار است. Restart، Resume، Retry، Failover، Worker Replacement یا UI Refresh Run تازه نمی‌سازد مگر Contract صریح New Run را الزام کند.

P04-CON-027 — `run_request_digest` باید Trigger و تمام Critical Context شامل Definition Digest، Tenant، Purpose، Environment، Target Scope، Input، Policy Snapshot، Ceilings و Deadline را Bind کند.

P04-CON-028 — Actor Chain باید Originator، Delegator، Service/Workload، Human Reviewer/Approver، Executor و Verifier Applicable را با Identity و Scope مستقل حفظ کند؛ Last Caller جای کل زنجیره را نمی‌گیرد.

P04-CON-029 — Parent/Child Run باید Root، Parent، Causation، Scope Delegation، Ceiling Intersection، Deadline Share، Cost Share و Outcome Dependency صریح داشته باشد.

P04-CON-030 — Child Run هیچ Authority، Effect، Data، Cost، Risk یا Autonomy Ceiling تازه‌ای از Parent ایجاد نمی‌کند. Effective Bound برابر سخت‌گیرانه‌ترین Intersection معتبر است.

P04-CON-031 — State Revision باید Monotonic و Concurrency-protected باشد. Transition باید Expected Prior Revision و Resulting Revision را ثبت کند.

P04-CON-032 — Run Context Snapshot نباید Policy، Approval، Lease یا Target State را برای تمام عمر Run معتبر فرض کند. هر Step باید Freshness/Validity لازم را در زمان Attempt دوباره ارزیابی کند.

P04-CON-033 — Deadline باید End-to-end باشد؛ Queue Time، Human Wait، Retry، Reconciliation و Child Work از آن خارج نمی‌شوند مگر Contract دقیق جداگانه داشته باشد.

P04-CON-034 — Warnings و Limitations Append-only History دارند. Resolution آن‌ها با Record تازه ثبت می‌شود و گذشته حذف نمی‌گردد.

P04-DEN-015 — Correlation ID، Session ID، Trace ID، Job ID، Ticket ID یا Human Task ID به‌تنهایی WorkflowRun Identity یا Definition Binding نیست.

P04-DEN-016 — Clone، Replay، Resume یا Fork یک Run نباید Approval، Lease، Nonce، Idempotency Result، Cost Reservation یا Risk Acceptance قبلی را به‌طور ضمنی به Run جدید منتقل کند.

P04-FAIL-007 — اگر Definition Digest، Tenant/Purpose، Root/Parent Link، State Revision، Deadline، Ceiling یا Policy Context نامعلوم/متعارض باشد، Run باید `BLOCKED_INDETERMINATE` شود و Step اثرگذار آغاز نشود.

P04-FAIL-008 — اگر Run Record یا State Store از Sourceهای متعارض Projection شود، هیچ Last-write-wins یا Majority Vote مجاز نیست؛ Transition متوقف و Reconciliation/Conflict Disposition لازم است.

## 7. Canonical Workflow State Machine و Transition Legality

P04-REQ-006 — State Projection پایه برای Definition و Run باید Semantics زیر را حفظ کند:

~~~text
Definition lifecycle:
DRAFT → VALIDATED → APPROVED_FOR_SCOPE → DEPRECATED|REVOKED|RETIRED

Run lifecycle:
DRAFT → VALIDATED → APPROVED_FOR_SCOPE → READY → RUNNING
RUNNING → WAITING_DEPENDENCY|WAITING_HUMAN|PAUSED|DEGRADED
RUNNING|WAITING_*|PAUSED|DEGRADED → SUCCEEDED|FAILED|PARTIAL|CANCELLED|UNKNOWN
PARTIAL|UNKNOWN|FAILED|CANCELLED → RECONCILED|COMPENSATED|RECOVERED|CLOSED_WITH_LIMITATIONS
SUCCEEDED|RECONCILED|COMPENSATED|RECOVERED → CLOSED_WITH_LIMITATIONS when unresolved limitations remain
~~~

P04-CON-035 — جدول بالا State Vocabulary و مسیرهای کلی Source-bound است؛ هر Definition باید Transitionهای دقیق، Guardها، Triggerها و Illegal Edgeها را صریح کند. Projection عملیاتی P03 شامل `ACCEPTED`، `QUEUED` و `WAITING_APPROVAL` نمای Invocation/OperationResource است، درحالی‌که Stateهای این بخش نمای Workflow Orchestration هستند؛ نگاشت بین دو Projection باید Explicit، Versioned و Lossless باشد. `ACCEPTED/QUEUED` به‌طور ضمنی `READY/RUNNING` و `WAITING_APPROVAL` به‌طور ضمنی Approval معتبر نیست.

P04-CON-036 — `DRAFT` یعنی Definition/Run هنوز برای Validation آماده یا معتبر اعلام نشده است؛ هیچ Work اثرگذار از آن مجاز نیست.

P04-CON-037 — `VALIDATED` یعنی Conformance تعریف‌شده ارزیابی شده است؛ نه Approval، نه Authority، نه Ready و نه Runtime Qualification.

P04-CON-038 — `APPROVED_FOR_SCOPE` فقط به Scope، Digest، Actor/Tenant/Purpose، Environment، Conditions و Window دقیق مقید است؛ Step اثرگذار هنوز Approval/Lease Applicable خود را می‌خواهد.

P04-CON-039 — `READY` یعنی Admission Preconditions شناخته‌شده برای شروع برقرار است. Ready به معنی Success یا Safe-for-all-transitions نیست.

P04-CON-040 — `RUNNING` یعنی حداقل یک Step/Attempt معتبر فعال یا Advance کنترل‌شده در جریان است؛ Worker Heartbeat یا Queue Claim به‌تنهایی کافی نیست.

P04-CON-041 — `WAITING_DEPENDENCY` و `WAITING_HUMAN` باید Dependency/Checkpoint دقیق، Owner، Since، Deadline/Expiry، Wake Condition و Escalation Rule داشته باشند.

P04-CON-042 — `WAITING_HUMAN` هیچ Automatic Timeout-to-Approval، Default Approval، Silence-is-consent یا AI-substitution ندارد.

P04-CON-043 — `PAUSED` فقط Advance تازه را متوقف می‌کند؛ Effectهای قبلی، External Work و Leaseهای موجود باید جداگانه Inspect/Revoke/Expire/Reconcile شوند.

P04-CON-044 — `DEGRADED` فقط مطابق Capability Matrix صریح و با Scope کاهش‌یافته مجاز است؛ Degraded State نمی‌تواند Requirementهای Authority، Security، Evidence، Risk، Cost یا Scientific Truth را حذف کند.

P04-CON-045 — `SUCCEEDED` فقط پس از برآورده‌شدن OutcomePredicateها، Receipt و Validation/Verification Applicable مجاز است؛ Step Completion، 100% Progress، Exit Code صفر یا Absence of Error کافی نیست.

P04-CON-046 — `FAILED`، `PARTIAL`، `CANCELLED` و `UNKNOWN` Stateهای متمایزند:

- `FAILED`: Failure تعیین‌شده با Effect State و Evidence شناخته‌شده؛
- `PARTIAL`: بخشی از Effect/Outcome تحقق یافته و Atomicity کامل نیست؛
- `CANCELLED`: درخواست توقف پذیرفته/اعمال شده، بدون اثبات Reversal؛
- `UNKNOWN`: Effect، State یا Outcome هنوز قابل‌اثبات نیست.

P04-CON-047 — `RECONCILED` یعنی State/Effect با روش و Evidence مشخص تعیین شده است؛ نتیجه می‌تواند Success، Failure، Partial یا Limitation باشد و الزاماً مثبت نیست.

P04-CON-048 — `COMPENSATED` یعنی Compensation Attempt معتبر و Outcome آن ثبت شده است؛ Compensation ممکن است کامل، جزئی یا دارای Residual Risk باشد.

P04-CON-049 — `RECOVERED` یعنی Service/Process به State قابل‌قبول تعریف‌شده رسیده است؛ Historical Failure یا Data Loss پنهان نمی‌شود.

P04-CON-050 — `CLOSED_WITH_LIMITATIONS` باید تمام Limitationها، Residual Effect/Risk، Unverified Claim، Missing Evidence، Owner و Follow-up Obligation را ثبت کند.

P04-DEN-017 — Transition بر اساس UI Status، Log Text، Progress Percentage، Model Confidence، Vote، Queue Empty، Worker Exit یا Absence of Alarm ممنوع است مگر Contract آن را Evidence کافی تعریف و Verify کرده باشد.

P04-DEN-018 — State نباید Skip، Rewrite، Backdate یا Rename شود تا Failure/Partial/Unknown پنهان گردد. Correction فقط با Event/Record تازه انجام می‌شود.

P04-DEN-019 — Terminal State یک Child یا Step نباید به‌طور خودکار Parent Run را `SUCCEEDED` کند؛ Parent OutcomePredicate مستقل لازم است.

P04-DEN-020 — `CANCELLED`، `COMPENSATED`، `RECOVERED` یا `RECONCILED` نباید به‌طور ضمنی `NO_EFFECT`، `ROLLED_BACK` یا `SAFE` معنا شود.

P04-FAIL-009 — Transition فاقد Prior State، Expected Revision، Trigger، Guard Result، Actor/Service، Causation، Timestamp یا Evidence باید `ILLEGAL_TRANSITION — DO_NOT_APPLY` شود.

P04-FAIL-010 — Unknown/Unsupported State یا State Version نباید به نزدیک‌ترین State Map شود؛ Run باید Quarantine و Compatibility/Reconciliation انجام شود.

P04-FAIL-011 — اگر OutcomePredicateها ناقص، متعارض یا غیرقابل‌ارزیابی‌اند، `SUCCEEDED` ممنوع و Result باید `UNKNOWN`، `PARTIAL` یا `CLOSED_WITH_LIMITATIONS` متناسب باقی بماند.

## 8. Step Contract، Attempt و Guarded Transition

P04-REQ-007 — هر Step Definition باید حداقل Contract زیر را داشته باشد:

~~~yaml
step_id:
step_version:
step_type: QUERY|COMPUTE|VALIDATE|HUMAN_REVIEW|DECISION|APPROVAL|EXECUTE|RECONCILE|NOTIFY
operation_reference:
input_contract:
output_contract:
preconditions: []
postconditions: []
guard_definitions: []
dependency_references: []
effect_class_reference:
effect_ceiling_reference:
required_permission_references: []
required_approval_references: []
required_competence_references: []
autonomy_ceiling_reference:
data_boundary_reference:
cost_bound_reference:
risk_bound_reference:
timeout:
deadline_share:
retry_profile_reference:
idempotency_profile_reference:
concurrency_profile_reference:
compensation_or_recovery_reference:
evidence_requirements: []
outcome_predicates: []
success_transitions: []
failure_transitions: []
unknown_transition:
~~~

P04-CON-051 — Step Type فقط Semantic Category است؛ Operation Reference، Actual/Transitive Effect و Boundهای Server-side تعیین‌کنندۀ Admission هستند.

P04-CON-052 — هر Step Attempt باید `step_attempt_id`، Run/Step Identity، Input Digest، Policy/Approval/Lease References، Executor Identity، Started/Finished TemporalStamp، Receipt، Effect State، Evidence و Resulting Transition را ثبت کند.

P04-CON-053 — Preconditions و Guards باید در زمان Attempt و نسبت به Authoritative State/Freshness لازم ارزیابی شوند. Evaluation قدیمی یا Definition-time جای Attempt-time Check را نمی‌گیرد.

P04-CON-054 — Postcondition باید Observed State را با Expected State مقایسه کند؛ SDK Return، HTTP 2xx، Queue Ack یا Tool Text به‌تنهایی Postcondition نیست.

P04-CON-055 — `QUERY` باید P03 Side-effect-free Contract را حفظ کند. Query دارای Hidden Mutation، Material Lock، External Trigger یا Variable Cost اثرگذار باید Reclassify شود.

P04-CON-056 — `COMPUTE` نتیجه علمی را جعل نمی‌کند؛ Scientific Compute باید Context و Status P06 را مصرف کند و Computation Completion را با Scientific Validity ادغام نکند.

P04-CON-057 — `VALIDATE` و `HUMAN_REVIEW` Evidence/Decision تولید می‌کنند؛ خودشان Approval یا Execution نیستند مگر Record مستقل Applicable طبق P03/P05 صادر شود.

P04-CON-058 — `DECISION` و `APPROVAL` باید Recordهای مستقل، Human-bound و Digest-bound تولید کنند. Step Label به‌تنهایی Decision/Approval معتبر نیست.

P04-CON-059 — `EXECUTE` فقط Application Command زمینی، Typed و محدود P03 را می‌پذیرد و به Approval/Lease دقیق نیاز دارد؛ هیچ Generic Execution مجاز نیست.

P04-CON-060 — `RECONCILE` State را از Evidence و Authoritative References تعیین می‌کند؛ با Retry، Compensation یا Success Assumption یکسان نیست.

P04-CON-061 — `NOTIFY` فقط انتقال اطلاع است. Delivery Receipt، Read Receipt یا Human Acknowledgement مجوز Transition اثرگذار تازه نیست.

P04-CON-062 — Step Output باید Canonicalized، Classified و Validated شود پیش از آن‌که Input Step بعدی گردد. Untrusted Output Authority تازه ایجاد نمی‌کند.

P04-DEN-021 — Step نباید هم‌زمان Input Validator، Effect Executor، Sole Approver و Independent Verifier خود باشد.

P04-DEN-022 — Generic Payload، Free-form Instruction، Prompt Text، User-provided URL، SQL، Shell، Code، Plugin Name یا Tool Name نباید به Operation اجرایی بدون Typed Mapping تبدیل شود.

P04-DEN-023 — Failure Transition نباید با Catch-all به `SUCCEEDED`، `APPROVED_FOR_SCOPE` یا Effectful Fallback برود.

P04-FAIL-012 — Missing/False/Unknown Guard، Stale Precondition، Unsupported Output، Scope Expansion یا Ceiling Breach باید Attempt/Transition را Block کند.

P04-FAIL-013 — Attempt Timeout پس از احتمال Effect باید `UNKNOWN` تولید کند؛ Blind Retry یا Success Assumption ممنوع و Reconciliation لازم است.

P04-FAIL-014 — Step Output ناقص، Untrusted، Non-converged، Disputed یا Indeterminate نباید به Validated Input یا Positive Decision ارتقا یابد.

## 9. Trigger، Admission، Authority Binding و Scope Propagation

P04-PROC-001 — Admission هر WorkflowRun و هر Step اثرگذار باید به‌ترتیب حداقل Predicateهای زیر را بررسی کند:

1. Definition Identity، Version، Digest و Status معتبر؛
2. Trigger Type، Origin، Freshness، Replay و Causation معتبر؛
3. Actor/Workload Authentication و Delegation Chain معتبر؛
4. Tenant، Purpose، Environment، Target و Data Scope معتبر؛
5. Input Schema، Classification و Provenance معتبر؛
6. Actual/Transitive Effect و Irreversibility قابل‌تعیین؛
7. Risk، Cost، Rate، Quota و Deadline در Envelope مجاز؛
8. Policy Snapshot و AuthorizationDecision Applicable معتبر؛
9. Approval Recordهای لازم Exact-scope و Exact-digest؛
10. ExecutionLease معتبر، کوتاه‌عمر، Target-bound و مصرف‌نشده؛
11. Preconditions، Expected Revision، Concurrency/Fencing و Dependencyها معتبر؛
12. Evidence، Receipt، Reconciliation، Recovery و Outcome Plan قابل‌اجرا.

P04-CON-063 — Trigger، Admission، Approval، Lease، Attempt، Receipt، Transition و Outcome محورهای مستقل‌اند. Pass شدن یک محور به محور دیگر منتقل نمی‌شود.

P04-CON-064 — Taxonomy دقیق `E0..E9`، `APR-*`، `PERM-*` و `AUT-*` فقط متعلق به P05 است. P04 فقط Workflow/Step را به Recordهای P05 Bind می‌کند و از تعریف رقیب خودداری می‌نماید.

P04-CON-065 — Effective Scope هر Child/Step برابر Intersection این Boundهاست:

`definition ∩ run ∩ parent ∩ actor ∩ tenant ∩ purpose ∩ environment ∩ policy ∩ approval ∩ lease ∩ risk ∩ cost ∩ data ∩ time`

Unknown یا Contradictory Intersection برابر Empty/Denied است، نه Broadest Scope.

P04-CON-066 — Approval و Lease باید Exact Workflow Definition/Run/Step، Operation، Target، Request Digest، Effect، Environment، Conditions و Validity Window را Bind کنند.

P04-CON-067 — Scope Reduction در Runtime مجاز است اگر Semantic Validity و Evidence حفظ شود. Scope Expansion، Target Addition، Higher Effect، New Destination یا Extended Deadline نیازمند Request/Review/Approval/Lease تازه است.

P04-CON-068 — Run Admission یک Snapshot قابل‌ردیابی می‌سازد؛ Revocation، Expiry، Policy Change، Risk Threshold Breach یا Target Revision Change می‌تواند Step بعدی را Block کند.

P04-CON-069 — Batch/Multi-target Workflow باید Cardinality Bound، Homogeneous Typed Semantics، Per-target State/Receipt/Evidence، Blast-radius Limit و Partial-failure Contract داشته باشد.

P04-DEN-024 — Schedule، Event Subscription، Human Trigger، Admin Role، Service Account، Generic Permission یا Prior Run Success جای Approval/Lease Step فعلی را نمی‌گیرد.

P04-DEN-025 — Parent Approval یا Workflow-level Approval نباید برای Child/Step دارای Digest، Target، Effect، Environment یا Time متفاوت Reuse شود.

P04-DEN-026 — Cardinality نامعلوم، Dynamic Target Discovery بدون Bound، Cross-tenant Fan-out یا Unbounded Recursion مساوی Scope نامعلوم و Admission Denied است.

P04-FAIL-015 — Missing/Stale/Expired/Revoked/Unknown Policy، Approval، Permission، Lease، Risk، Cost یا Scope Mapping نتیجه `DENY / DO_NOT_ADVANCE` دارد.

P04-FAIL-016 — Trigger تکراری با Digest متفاوت، Reused Nonce، Invalid Causation یا Replay Context نامعتبر باید Run/Step Effect را Block و Evidence ایجاد کند.

P04-FAIL-017 — هر Attempt برای ایجاد Workflow Route به `E9` یا کاهش `APR-X` یک Contract Violation بحرانی و مسیر Incident است، نه Change Request عادی.

## 10. Human-control Checkpoint و Informed Decision Contract

P04-REQ-008 — هر HumanCheckpoint Definition و Instance باید حداقل Contract زیر را داشته باشد:

~~~yaml
checkpoint_id:
checkpoint_type: REVIEW|DECISION|APPROVAL|RISK_ACCEPTANCE|BUDGET_AUTHORIZATION|SCIENTIFIC_VERIFICATION
workflow_definition_id:
workflow_definition_version:
workflow_run_id:
step_id:
checkpoint_request_digest:
presentation_manifest_reference:
required_role_reference:
required_competence_reference:
separation_of_duties_rule_reference:
conflict_of_interest_check_reference:
decision_options: []
allowed_conditions_schema:
scope_reference:
effect_reference:
risk_reference:
cost_reference:
data_reference:
valid_from: TemporalStamp
expires_at: TemporalStamp
replay_and_reuse_rule:
escalation_rule_reference:
status: PENDING|PRESENTED|DECIDED|EXPIRED|REVOKED|INVALIDATED|CONFLICTED
decision_record_reference:
evidence_references: []
~~~

P04-REQ-009 — Checkpoint Presentation باید حداقل موارد زیر را به‌صورت واضح، قابل‌مقایسه و غیرگمراه‌کننده ارائه کند:

1. Intent، Purpose، Target و Environment دقیق؛
2. Material Diff از State/Artifact/Plan قبلی؛
3. Actual و Transitive Effect و Blast Radius؛
4. Data Classification، Egress، Residency، Privacy و Security Impact؛
5. Scientific Assumption، Time/Frame/Unit/Covariance، Uncertainty و Verification Status Applicable؛
6. Risk Exposure، Appetite/Tolerance/Capacity Context و Residual Risk؛
7. Cost Exposure، Reservation، Variable-cost Range و Budget Owner؛
8. Evidence، Provenance، Tests، Dissent، Warnings و Limitations؛
9. Preconditions، Outcome Predicates و Failure/Unknown Consequences؛
10. Rollback، Compensation، Recovery و Irreversibility Limits؛
11. Approval Scope، Conditions، Expiry، Revocation و Replay Consequences؛
12. Alternatives شامل No-action/Defer در صورت Applicability.

P04-CON-070 — Human Decision باید به Exact Presentation/Request Digest Bind شود. هر تغییر مادی در Input، Target، Diff، Effect، Risk، Cost، Data، Evidence، Deadline، Capability یا Outcome Predicate Approval/Decision قبلی را Invalid می‌کند.

P04-CON-071 — Reviewer/Approver Identity باید Human بودن، Role، Competence، Scope، Tenant/Organization Context، Conflict-of-interest Status و Delegation معتبر را نشان دهد.

P04-CON-072 — Decision Options باید Semantically distinct و Machine-readable باشند؛ حداقل `APPROVE_EXACT_SCOPE`، `REJECT`، `REQUEST_CHANGE` و `DEFER` طبق Applicability از هم جدا بمانند. P04 Taxonomy Approval را تعریف نمی‌کند.

P04-CON-073 — Approval شرطی فقط با Conditionهای Typed، قابل‌ارزیابی، Time-bound و Digest-bound معتبر است. Free-text Condition نباید Escape Hatch یا Scope Expansion ایجاد کند.

P04-CON-074 — Checkpoint UI/Report باید Dissent، Unknown، Missing Evidence، Limitation و Negative Result را با برجستگی متناسب نمایش دهد و از Dark Pattern، Default Approval یا Approval Fatigue Design پرهیز کند.

P04-CON-075 — AI می‌تواند Draft، Summary یا Presentation Candidate بسازد؛ Server/Human Process باید Completeness، Fidelity و Suppressed Limitation را مستقل بررسی کند.

P04-CON-076 — AI، Agent، Orchestrator یا Tool نمی‌تواند Approver را انتخاب نهایی، Competence را خوداظهاری، Conflict را نادیده، Approval را صادر/تمدید/Reuse یا Decision را از لحن انسان استنتاج کند.

P04-CON-077 — `WAITING_HUMAN` باید بدون تغییر State اثرگذار باقی بماند تا Decision Record معتبر برسد. Timeout فقط Expiry/Escalation می‌سازد، نه Approval.

P04-CON-078 — Approver Unavailability مسیر Escalation مستند را فعال می‌کند. Escalation باید Role/Competence/Independence معادل یا سخت‌گیرانه‌تر را حفظ کند.

P04-CON-079 — Reject، Request-change، Defer، Expire، Revoke و Invalidate Outcomeهای معتبر Checkpoint هستند و نباید به Failure فنی یا Approval ضمنی تبدیل شوند.

P04-CON-080 — Decision Receipt باید Presentation Digest، Decision Option، Conditions، Rationale، Identity، Competence Evidence، Timestamp، Expiry و Signature/Integrity Reference Applicable را ثبت کند.

P04-DEN-027 — Silence، Delay، Lack of Objection، Meeting Attendance، Email Open، Chat Reaction، Checkbox پیش‌فرض یا Login Session Approval نیست.

P04-DEN-028 — Approval Bulk، Blanket، Future-unknown، Cross-environment، Cross-tenant، Cross-target یا بدون Digest برای Step اثرگذار معتبر نیست.

P04-DEN-029 — Approver نباید Material Diff، Risk/Cost/Data Impact، Unknown Outcome، Dissent یا Rollback Limitation را از Presentation حذف یا پنهان کند.

P04-DEN-030 — Edit پس از Approval، UI-side Patch، Hidden Field، Translated Summary با Loss یا Re-render بدون Digest Rebinding Approval را معتبر نگه نمی‌دارد.

P04-DEN-031 — Human Checkpoint نباید به Captcha، Rubber Stamp، Token Issuer خودکار یا Formality بدون زمان/اطلاعات/صلاحیت کافی تقلیل یابد.

P04-DEN-032 — Model Confidence، Majority Agent Vote، Tool Recommendation یا Prior Human Pattern نمی‌تواند Human Decision لازم را جایگزین کند.

P04-DEN-033 — هیچ Checkpoint یا Human Approvalی برای Spacecraft Command/Uplink قابل‌ساخت نیست؛ مسیر مربوط همیشه `E9 / APR-X / HARD_DENY` باقی می‌ماند.

P04-FAIL-018 — Missing/Expired/Revoked/Conflicted Approver Identity، Competence، Scope، Digest، Presentation یا Decision Record نتیجه `HUMAN_CHECKPOINT_INVALID — DO_NOT_ADVANCE` دارد.

P04-FAIL-019 — اگر Presentation ناقص یا گمراه‌کننده باشد، Checkpoint باید Invalidated و با Digest تازه بازسازی شود؛ Approval قبلی قابل‌ترمیم درجا نیست.

P04-FAIL-020 — اگر Conflict of Interest یا Separation-of-duties Violation حل نشده باشد، Decision اثرگذار پذیرفته نمی‌شود و Escalation/Independent Review لازم است.

P04-FAIL-021 — Approval Fatigue، Coercion، Ambiguous Choice، Insufficient Review Time یا Accessibility Failure باید به Human-factor Risk و Stop/Redesign متناسب منجر شود، نه Default Approval.

P04-FAIL-022 — اگر Human Decision به Request دیگری Bind شده یا پس از تغییر مادی Reuse شود، نتیجه `APPROVAL_DIGEST_MISMATCH` و Effect Blocked است.

## 11. Separation of Duties، Competence و Escalation

P04-REQ-010 — هر Workflow مادی باید Actor Assignment و Separation Contract حداقلی زیر را داشته باشد:

~~~yaml
role_assignment_id:
workflow_definition_id:
workflow_run_id:
role_type: PROPOSER|REVIEWER|DECIDER|APPROVER|EXECUTOR|INDEPENDENT_VERIFIER|RISK_OWNER|RISK_CHALLENGER|BUDGET_REQUESTER|BUDGET_APPROVER|RECORD_CUSTODIAN
actor_identity_reference:
human_or_workload_type:
competence_domain_references: []
scope_reference:
permission_reference:
delegation_reference:
independence_requirements: []
conflict_of_interest_status:
valid_from: TemporalStamp
expires_at: TemporalStamp
evidence_references: []
~~~

P04-CON-081 — برای Workflowهای مادی، Proposer و Approver باید متمایز باشند؛ Self-approval یا Approval توسط Actor تحت کنترل مستقیم همان Proposal بدون Independent Control مجاز نیست.

P04-CON-082 — برای Effectهای High/Critical یا معادل `E7/E8` طبق P05، Executor و Independent Verifier باید متمایز و به‌اندازۀ اثر موردنظر مستقل باشند.

P04-CON-083 — Scientific Producer و Independent Scientific Verifier باید از نظر Method، Evidence، Toolchain/Engine یا Organizational Influence به‌قدر تعریف‌شده مستقل باشند؛ جزئیات Scientific Independence متعلق به P06/P13 است.

P04-CON-084 — Budget Requester و Budget Approver برای Expenditure مادی باید جدا باشند. Technical Approval به معنی Budget Authorization نیست و Budget Authorization به معنی Risk Acceptance نیست.

P04-CON-085 — Risk Owner و Independent Challenger در Riskهای High/Critical یا موارد مقرر باید جدا باشند. Risk Acceptance فقط توسط Authority صلاحیت‌دار و در Envelope تعریف‌شده ممکن است.

P04-CON-086 — Record Custodian باید Integrity، Retention و Access Control را حفظ کند و نباید Outcome یا Evidence Producer منفرد برای Work تحت Custody خود تلقی شود.

P04-CON-087 — یک Actor می‌تواند چند Role کم‌ریسک داشته باشد فقط اگر Conflict Matrix، Effect/Risk Profile، Competence و Policy صریحاً اجازه دهند؛ Default برای تغییر مادی جداسازی است.

P04-CON-088 — Competence باید Domain-specific، Scope-specific، Current و Evidence-backed باشد. Generic Seniority، Job Title، Admin Role، Model Claim یا Past Approval کافی نیست.

P04-CON-089 — Delegation باید Delegator، Delegate، Scope، Purpose، Competence، Restrictions، Validity، Revocation و Non-delegable Duties را صریح Bind کند.

P04-CON-090 — Role Unavailability باید Wait، Reassign یا Escalate طبق Path ثبت‌شده ایجاد کند؛ Unavailability هیچ Approval یا Competence ضمنی ایجاد نمی‌کند.

P04-CON-091 — Escalation باید Reason، Prior Attempts، Urgency، Residual Risk، New Actor، Authority Basis و Decision Record را حفظ کند؛ Emergency Label Requirements را حذف نمی‌کند.

P04-CON-092 — Break-glass، در صورت تعریف در Parts مالک، فقط Scope/Time محدود و Evidence-heavy است و نمی‌تواند E9/APR-X، Scientific Truth، Evidence Integrity یا Separation بنیادی را دور بزند.

P04-CON-093 — Agent، Model، Workflow، Service یا Tool هیچ‌گاه Human Approver، Risk Acceptor، Budget Owner یا Independent Verifier انسانی محسوب نمی‌شود.

P04-DEN-034 — هیچ Actor نباید برای تغییر حساس هم‌زمان Proposer، Executor، Sole Verifier و Final Approver باشد.

P04-DEN-035 — Identity اشتراکی، Generic Team Account، Anonymous Review، Unverifiable Signature یا Borrowed Session برای Role حساس ممنوع است.

P04-DEN-036 — Orchestrator نباید با Auto-assignment، Round-robin یا Availability Optimization Actor فاقد Competence/Independence را انتخاب کند.

P04-DEN-037 — Conflict-of-interest نامعلوم برابر No Conflict نیست. Self-declaration بدون Policy/Evidence کافی برای موارد حساس معتبر نیست.

P04-DEN-038 — Delegation Chain نباید Scope یا Authority را در هر Hop گسترش دهد و Non-delegable Approval را قابل‌انتقال سازد.

P04-DEN-039 — Human Mediation، Pairing با AI یا Review پس از اجرا جای Approval و Separation لازم قبل از Effect را نمی‌گیرد.

P04-FAIL-023 — Role، Identity، Competence، Delegation، Independence یا Conflict Status نامعلوم/منقضی/متعارض باید Step حساس را Block کند.

P04-FAIL-024 — اگر Independent Actor در دسترس نیست، نتیجه `WAITING_HUMAN` یا `BLOCKED_BY_SEPARATION_OF_DUTIES` است؛ Downgrade خودکار ممنوع است.

P04-FAIL-025 — کشف Self-approval، Collusion Indicator یا Identity Misbinding باید Transition را متوقف، Evidence را حفظ و Security/Governance Incident مسیر مناسب را فعال کند.

## 12. Dependency، Parent/Child Orchestration و Long-running Process

P04-REQ-011 — هر Dependency Edge باید حداقل Contract زیر را داشته باشد:

~~~yaml
dependency_id:
consumer_run_id:
consumer_step_id:
provider_type: WORKFLOW_RUN|STEP|DATASET|SERVICE|HUMAN_CHECKPOINT|POLICY|APPROVAL|EXTERNAL_RESOURCE
provider_reference:
required_state_or_predicate:
version_or_revision_constraint:
freshness_requirement:
deadline:
failure_semantics:
partial_semantics:
unknown_semantics:
fallback_reference:
evidence_requirements: []
~~~

P04-CON-094 — Dependency Satisfaction باید Predicate، Version/Revision، Freshness، Integrity و Evidence صریح داشته باشد. Availability یا Non-empty Response کافی نیست.

P04-CON-095 — `WAITING_DEPENDENCY` باید Provider Identity، Required Predicate، Last Observation، Retry/Poll Bound، Deadline و Escalation را ثبت کند.

P04-CON-096 — Parent Run مسئول Aggregate OutcomePredicate خود است. Child Success فقط یک Fact ورودی است و Outcome Parent را خودکار تعیین نمی‌کند.

P04-CON-097 — Child Failure/Partial/Unknown باید طبق Dependency Contract به Parent Propagate شود؛ Parent نباید آن را با Successful Sibling، Majority یا Cached Output پنهان کند.

P04-CON-098 — Fan-out/Fan-in باید Cardinality، Ordering، Completion Rule، Quorum Semantics، Missing Target، Partial Failure و Per-target Evidence را از پیش تعریف کند.

P04-CON-099 — Quorum فقط برای Predicateهایی مجاز است که Semantically قابلیت Quorum دارند. Scientific Truth، Approval، Required Evidence یا Prohibited-path Denial با Majority قابل‌جایگزینی نیست.

P04-CON-100 — Long-running Process باید Durable State، Operation Identity، Progress Evidence، Heartbeat Semantics، Lease/Fencing، Pause/Resume، Cancellation، Reconciliation و Closure Rule داشته باشد.

P04-CON-101 — Progress باید بر مبنای Units/Steps/Predicates تعریف‌شده و Denominator قابل‌بازسازی باشد. درصد بدون Denominator، Exclusion و State Semantics Claim معتبر نیست.

P04-CON-102 — Callback، Polling و Event Consumption فقط Projectionهای متفاوت یک Dependency/Run Identity هستند و Authority تازه نمی‌سازند.

P04-CON-103 — External Dependency باید Provider، Region، Data/Egress، SLA Assumption، Receipt/Status Lookup، Idempotency و Unknown-outcome Behavior صریح داشته باشد.

P04-CON-104 — Workflow Timer باید TemporalStamp، Time Scale/Zone Applicable، Clock Source، Deadline Semantics و Late-fire Behavior را حفظ کند؛ Business Time و Scientific Time نباید مبهم ادغام شوند.

P04-CON-105 — Scheduled Run تازه باید Admission تازه داشته باشد. Approval، Lease، Policy یا Input Snapshot Run قبلی قابل‌انتقال نیست.

P04-CON-106 — Pause/Resume Childها باید Causation و State واقعی هر Child را حفظ کند؛ Parent Pause به‌تنهایی اثبات توقف External Effect نیست.

P04-DEN-040 — Dependency Cycle نامحدود، Recursive Spawn بدون Bound، Orphan Child یا Detached Effectful Work ممنوع است.

P04-DEN-041 — Health Check، Heartbeat، HTTP Success، File Existence یا Queue Delivery نباید به‌طور عمومی Dependency Outcome تلقی شود.

P04-DEN-042 — Fallback Dependency نباید Data Residency، Model/Engine Quality، Security، Risk، Cost، Evidence یا Authority Profile را Silent تغییر دهد.

P04-DEN-043 — Workflow نباید برای دورزدن Scope/Approval، Effect واحد را به Childهای ظاهراً کم‌خطر خرد کند؛ Aggregate و Transitive Effect ملاک است.

P04-FAIL-026 — Dependency Missing/Stale/Conflicted/Unsupported/Unknown باید Consumer را Block یا Degrade فقط طبق Matrix معتبر کند؛ Default Success ممنوع است.

P04-FAIL-027 — Orphaned Child یا Lost Parent Link باید Quarantine، Causation Reconstruction و Reconciliation ایجاد کند؛ Child Effect نباید حذف یا Blind Retry شود.

P04-FAIL-028 — اگر Fan-in Completion Rule یا Per-target State قابل‌اثبات نیست، Aggregate Result باید `PARTIAL_OR_INDETERMINATE` باقی بماند.

P04-FAIL-029 — Late Callback/Event پس از Closure باید با Run/Revision/Deadline Guard بررسی و به‌عنوان Late Fact ثبت شود؛ Silent Reopen یا Effect تازه ممنوع است.

## 13. Deadline، Timeout، Retry، Pause و Cancellation

P04-REQ-012 — هر Retry/Timeout Profile باید حداقل Contract زیر را داشته باشد:

~~~yaml
retry_profile_id:
applicable_step_types: []
retryable_error_codes: []
non_retryable_error_codes: []
max_attempts:
end_to_end_deadline:
per_attempt_timeout:
backoff_policy:
jitter_policy:
idempotency_requirement:
effect_unknown_behavior:
cost_bound_reference:
risk_bound_reference:
rate_quota_reference:
approval_and_lease_refresh_rule:
evidence_requirements: []
~~~

P04-CON-107 — Retry فقط برای Failure صریحاً Retryable، در Deadline، Attempt Bound، Cost/Risk/Rate Bound و Idempotency Semantics معتبر مجاز است.

P04-CON-108 — Retry Authority جدید ایجاد نمی‌کند. Policy، Approval، Permission، Lease، Target Revision و Preconditions باید برای Attempt جدید همچنان معتبر باشند.

P04-CON-109 — Same Idempotency Key + Same Normalized Digest باید Prior Attempt/Receipt/Outcome را بازیابی یا Reconciliation را ادامه دهد؛ Effect متمایز تازه نسازد.

P04-CON-110 — Same Idempotency Key + Different Digest باید `IDEMPOTENCY_CONFLICT` و Fail Closed باشد.

P04-CON-111 — Timeout قبل از Evidence قطعی عدم Attempt می‌تواند `NONE` باشد؛ Timeout پس از احتمال Effect باید `UNKNOWN` شود و Reconciliation پیش از Retry لازم است.

P04-CON-112 — Deadline Expiry باید Pending Work را متوقف یا Mark کند، اما Historical Effect، Receipt یا External State را حذف نمی‌کند.

P04-CON-113 — Pause باید Owner/Reason، Scope، Requested/Effective Time، In-flight Attempt Handling، Lease Handling، External Work Status و Resume Preconditions را ثبت کند.

P04-CON-114 — Resume یک Transition Guarded است و باید Definition/Policy/Approval/Lease/Dependency/Freshness/Revision را دوباره بررسی کند.

P04-CON-115 — Cancellation فقط درخواست توقف Run/Step جاری یا آینده است. Acceptance Cancellation به معنی Commit نشدن، Rollback، Compensation یا No Effect نیست.

P04-CON-116 — Cancellation Propagation به Childها باید Per-child Request/Receipt/State داشته باشد. Parent State از Aggregate Evidence تعیین می‌شود.

P04-CON-117 — Human Wait Time، External Dependency Time و Reconciliation Time باید در Deadline و SLO Accounting طبق Contract ثبت شوند؛ نباید برای بهبود Metric حذف شوند.

P04-CON-118 — Retry Budget باید Attempt Count، Variable Cost، External Calls، Rate و Blast Radius را Bound کند؛ Infinite Retry ممنوع است.

P04-CON-119 — Circuit Breaker، Bulkhead یا Backpressure در صورت استفاده فقط Control Flow را محدود می‌کند؛ Outcome/Effect Semantics را تعیین نمی‌کند.

P04-CON-120 — Error Classification و Retryability باید P03 Error Contract را مصرف کند؛ Workflow نباید Retryability رقیب یا خوش‌بینانه بسازد.

P04-CON-121 — Manual Retry نیز همان Idempotency، Reconciliation، Authority، Risk، Cost و Deadline Controlهای Automated Retry را می‌خواهد.

P04-DEN-044 — Blind Retry پس از Lost Receipt، Client Disconnect، Worker Crash، Callback Failure یا Unknown External State ممنوع است.

P04-DEN-045 — Retry نباید به‌عنوان Recovery، Compensation، Rollback یا Verification نام‌گذاری شود تا Effect جدید پنهان گردد.

P04-DEN-046 — Timeout نباید Failure را به Success، Cancelled-with-no-effect یا Safe-to-retry تبدیل کند.

P04-DEN-047 — Resume از Archived/Deprecated/Revoked Definition یا Stale Approval/Lease بدون Compatibility و Fresh Admission ممنوع است.

P04-DEN-048 — Operator Click روی «Retry» یا «Resume» Approval/Lease تازه و Effect Safety را اثبات نمی‌کند.

P04-FAIL-030 — اگر Retryability، Effect State، Idempotency یا Current Revision نامعلوم است، Retry ممنوع و State `UNKNOWN / AFTER_RECONCILIATION` باقی می‌ماند.

P04-FAIL-031 — Exhausted Attempts باید Failure/Partial/Unknown واقعی را ثبت کند؛ Attempt Counter Reset، New Worker یا Restart نباید Bound را دور بزند.

P04-FAIL-032 — Cancellation با In-flight Effect نامعلوم باید `CANCELLED` همراه `effect_state: UNKNOWN` یا State مناسب ثبت کند و Reconciliation را الزام نماید.

P04-FAIL-033 — Deadline Breach در Checkpoint یا Dependency نباید Approval/Dependency را فرض کند؛ Expire/Escalate/Fail طبق Contract لازم است.

P04-FAIL-034 — اگر Cost/Risk/Rate Bound در Retry قابل‌ارزیابی نیست، Retry Block می‌شود؛ Unknown Cost برابر Zero و Unknown Risk برابر Low نیست.

## 14. Compensation، Rollback، Recovery و Reconciliation

P04-REQ-013 — هر Step/Workflow اثرگذار باید Compensation-or-Recovery Profile متناسب با Contract زیر داشته باشد:

~~~yaml
recovery_profile_id:
applicable_operation_reference:
failure_and_effect_states: []
rollback_preconditions: []
rollback_operation_reference:
compensation_operation_reference:
recovery_operation_references: []
reconciliation_method_reference:
authoritative_state_references: []
irreversibility_and_residual_effects: []
required_approvals: []
required_leases: []
risk_and_cost_bounds: []
validation_predicates: []
evidence_requirements: []
closure_rules: []
~~~

P04-CON-122 — Rollback فقط وقتی معتبر است که State قبلی هنوز موجود، Compatible، Safe، Authorized و قابل‌اثبات باشد. Restore Attempt یا Version Label به‌تنهایی Rollback نیست.

P04-CON-123 — Compensation یک Application Command و Effect جدید است؛ Policy، Approval، Lease، Risk، Cost، Receipt و Outcome مستقل می‌خواهد.

P04-CON-124 — Recovery می‌تواند Roll-forward، State Repair، Isolation، Exposure Reduction، Rebuild، Reprocess یا Controlled Manual Procedure باشد؛ Success آن با Recovery Predicate تعیین می‌شود.

P04-CON-125 — Reconciliation باید Internal/External Authoritative State، Idempotency Record، Target Revision، External Receipt، Audit/Evidence، Attempt History و Dependency/Child State را بررسی کند.

P04-CON-126 — Saga Pattern Atomicity سراسری تضمین نمی‌کند. هر Local Commit، Failed Compensation، Partial State و Residual Effect باید قابل‌مشاهده بماند.

P04-CON-127 — Compensation Failure یک Failure تازه با Receipt/Evidence مستقل است و نمی‌تواند Effect اصلی را پاک یا Success فرض کند.

P04-CON-128 — Irreversible Change باید از ابتدا Recovery، Roll-forward، Exposure Reduction، Reconciliation و Acceptance Authority داشته باشد؛ Rollback خیالی ممنوع است.

P04-CON-129 — Data Deletion/Export/External Egress Recovery باید Retention، Legal Hold، Replica، Recipient/Destination، Revocation Limits و Evidence Parts مالک را رعایت کند.

P04-CON-130 — Reconciliation Result باید Effect Classification، Observed State، Confidence/Evidence Limitations، Residual Risk، Required Action و Outcome Link را ثبت کند.

P04-CON-131 — `RECONCILED`، `COMPENSATED` و `RECOVERED` باید با Result Qualifier همراه باشند؛ Label تنها Positive Success Claim نیست.

P04-CON-132 — Correction، Supersession یا Reclassification با Record/Event تازه انجام می‌شود. Prior Attempt/Receipt/Outcome Silent Rewrite نمی‌شود.

P04-CON-133 — Recovery Run باید Definition/Run Identity تازه یا Link دقیق به Run اصلی، Causation، Scope و Independent Admission داشته باشد.

P04-CON-134 — Dependent Effectful Work در State `PARTIAL` یا `UNKNOWN` تا Reconciliation، Competent Decision و Recovery کنترل‌شده Block می‌شود.

P04-CON-135 — Closure پس از Recovery باید Historical Failure، Downtime/Data Loss، Residual Limitation و Unresolved Obligation را حفظ کند.

P04-PROC-002 — مسیر اجباری Outcome/Effect نامعلوم:

`STOP → PRESERVE EVIDENCE → ISOLATE DEPENDENT EFFECTS → INSPECT AUTHORITATIVE STATE → CHECK IDEMPOTENCY/REVISION → RECONCILE → CLASSIFY EFFECT → COMPETENT HUMAN DECISION → CONTROLLED RECOVERY/COMPENSATION → VALIDATE → RECORD OUTCOME`

P04-DEN-049 — Compensation Success نباید بدون Validation Effect اصلی را Fully Reversed معرفی کند.

P04-DEN-050 — Rollback Script، Database Transaction، Saga Library، Snapshot یا Infrastructure Feature به‌تنهایی End-to-end Reversibility را اثبات نمی‌کند.

P04-DEN-051 — Recovery نباید Evidence، Failure State، Audit History، Dissent یا Unknown Interval را حذف یا Backfill ساختگی کند.

P04-DEN-052 — Reconciliation نباید بر Last Log Line، Model Guess، Majority Replica یا Client Assertion بدون Authority/Evidence تکیه کند.

P04-DEN-053 — `force_complete`، `mark_success`، `ignore_failure` یا Manual DB Edit برای بستن Run بدون Contract و Evidence ممنوع است.

P04-DEN-054 — Incident/Emergency Mode مجوز عبور از Reconciliation یا ایجاد Spacecraft-command Path نیست.

P04-FAIL-035 — اگر Rollback Preconditions برقرار نیست، Rollback Attempt ممنوع و Recovery/Compensation Plan متناسب لازم است.

P04-FAIL-036 — اگر Authoritative Stateها متعارض یا غیرقابل‌دسترس‌اند، Reconciliation باید `INDETERMINATE` بماند و Success Claim ممنوع است.

P04-FAIL-037 — Failed/Partial Compensation باید Residual Effect/Risk را ثبت و Dependent Work را تا Decision صلاحیت‌دار Block کند.

P04-FAIL-038 — اگر Irreversibility یا Residual Effect پیش از Execution نامعلوم است، Effectful Step باید Fail Closed شود.

P04-FAIL-039 — Lost Recovery Receipt یا Timeout Recovery نیز Outcome `UNKNOWN` ایجاد می‌کند؛ Recovery را Blind Retry نکن.

P04-FAIL-040 — اگر Reconciliation نتیجه No Effect را با Evidence کافی اثبات نکند، Safe-to-retry Claim مجاز نیست.

## 15. Concurrency، Fencing، Ordering و Causality

P04-REQ-014 — هر Aggregate/Resource و Workflow باید Concurrency Profile حداقلی زیر را تعریف کند:

~~~yaml
concurrency_profile_id:
aggregate_or_target_scope:
control_mode: OPTIMISTIC_REVISION|FENCED_LEASE|SINGLE_WRITER|SERIALIZED_QUEUE|COMMUTATIVE_MERGE
expected_revision_rule:
fencing_token_rule:
ordering_key:
ordering_scope:
partition_boundary:
duplicate_signal_rule:
out_of_order_rule:
conflict_rule:
lease_expiry_rule:
reconciliation_rule:
evidence_requirements: []
~~~

P04-CON-136 — هر State Transition باید Expected Prior Revision/Digest و Resulting Revision را Bind کند. Conflict نباید با Silent Last-write-wins حل شود.

P04-CON-137 — Fencing Token باید Monotonic/Unforgeable در Scope خود و به Actor/Lease/Target/Validity Bind باشد؛ Worker قدیمی پس از Token جدید حق Commit ندارد.

P04-CON-138 — Single-writer Lease فقط در Scope و Window خود معتبر است؛ Lease Expiry یا Network Partition Outcome Attempt قبلی را تعیین نمی‌کند.

P04-CON-139 — Ordering باید Key، Scope، Partition و Out-of-order Behavior مشخص داشته باشد. Global Ordering بدون End-to-end Evidence ادعا نمی‌شود.

P04-CON-140 — Duplicate Trigger/Signal نباید Effect تکراری بسازد. Deduplication باید Same Identity/Same Digest و Conflict Rule را رعایت کند.

P04-CON-141 — Causation ID علت مستقیم Transition را ثبت می‌کند؛ Correlation یا Trace فقط Grouping/Observation است و جای Causation را نمی‌گیرد.

P04-CON-142 — Out-of-order Event فقط وقتی قابل‌اعمال است که State Guard، Version Compatibility و Causal Preconditions معتبر باشند؛ در غیر این صورت Buffer/Reject/Reconcile لازم است.

P04-CON-143 — Concurrent Runs روی Target مشترک باید Scope Overlap، Effect Interaction، Revision Conflict، Priority و Serialization/Commutativity را صریح کنند.

P04-CON-144 — Commutative Merge فقط با Algebra/Semantics و Tests معتبر قابل‌ادعاست. Merge Metadata به معنی Merge-safe Business/Scientific State نیست.

P04-CON-145 — Approval، Policy Snapshot، Lease و Target Revision Stale باید Transition را Fail Closed کنند؛ Refresh یک Record تازه می‌خواهد.

P04-CON-146 — Clock Skew یا Delayed Delivery نباید با Timestamp Sorting تنها Causality را تعیین کند. Sequence/Fencing/Causation Evidence لازم است.

P04-CON-147 — Parent/Child Cancellation، Compensation و Recovery باید Raceهای Late Completion را با State Revision و Causation Guard کنترل کنند.

P04-CON-148 — Exactly-once Label در Broker/SDK/Workflow Engine، Exactly-once Outcome نیست. Claim پایه `AT_LEAST_ONCE` باقی می‌ماند مگر End-to-end Evidence قوی‌تر وجود داشته باشد.

P04-DEN-055 — Stale Worker، Expired Lease Holder یا Old Workflow Version نباید State/Effect Commit کند حتی اگر Work محاسباتی کامل شده باشد.

P04-DEN-056 — Conflict نباید با حذف Expected Revision، Force Update، Retry Loop یا Manual Override پنهان شود.

P04-DEN-057 — Deduplication نباید Correction، Compensation، Reconciliation، Supersession یا Evidence Event متمایز را حذف کند.

P04-DEN-058 — UI Ordering، File Timestamp، Arrival Order یا Log Order به‌تنهایی Canonical Causality نیست.

P04-FAIL-041 — Revision Conflict، Fencing Violation، Duplicate Different Digest، Invalid Ordering یا Reused Lease باید Effect را Block و Evidence ایجاد کند.

P04-FAIL-042 — اگر Concurrent Effects Interaction نامعلوم است، Runs باید Serialize/Block شوند؛ Optimistic Parallelism بدون Contract ممنوع است.

P04-FAIL-043 — Network Partition یا Split-brain با احتمال Commit باید State را `UNKNOWN/PARTIAL` نگه دارد و Reconciliation انجام شود.

P04-FAIL-044 — Late Result از Attempt/Version/Revision قدیمی نباید Current State را Overwrite کند؛ به‌عنوان Stale Fact ثبت یا Reject شود.

P04-FAIL-045 — اگر Ordering/Deduplication/Causality Semantics End-to-end نامعلوم است، Workflow نباید Outcome یکتا یا Deterministic Advance را فرض کند.

## 16. Scientific Workflow Delegation و حفاظت از حقیقت علمی

P04-REQ-015 — هر Scientific Step/Workflow باید علاوه بر Schemaهای عمومی، Scientific Context Reference حداقلی زیر را حمل کند:

~~~yaml
scientific_context_reference:
computation_contract_reference:
engine_and_version_reference:
force_model_or_method_profile_reference:
time_contract_reference:
frame_contract_reference:
unit_contract_reference:
covariance_and_uncertainty_reference:
auxiliary_data_version_references: []
initial_condition_reference:
numerical_tolerance_reference:
convergence_status_reference:
independent_verification_requirement_reference:
scientific_evidence_references: []
~~~

P04-CON-149 — P06 مالک Numerical Computation، Scientific Truth، Time/Frame/Unit، Covariance، Convergence، Equivalence و Independent Scientific Verification است. P04 فقط آن Contractها را در Workflow حفظ و ارکستره می‌کند.

P04-CON-150 — Scientific Workflow باید `NOT_COMPUTABLE`، `NOT_CONVERGED`، `DISPUTED`، `INVALID` و `INDETERMINATE` را First-class State/Result نگه دارد.

P04-CON-151 — Step Completion یا Engine Exit Success به معنی Scientific Validity نیست. OutcomePredicate علمی باید P06/P13 Evidence و Oracle Applicable را مصرف کند.

P04-CON-152 — Time، Frame، Unit، Covariance، Uncertainty، Engine/Method Profile، Auxiliary Data و Initial Conditions باید در تمام Step/Child/Retry/Translation Boundaries Losslessly حفظ شوند.

P04-CON-153 — Translation یا Conversion علمی فقط با Profile Versioned، Loss Characterization و Verification Applicable مجاز است؛ Unknown Mapping برابر Incompatible/Indeterminate است.

P04-CON-154 — Defined High-impact Output باید Independent Verification را پیش از Promotion، Recommendation Materialization یا Downstream High-impact Use طی کند.

P04-CON-155 — Primary Engine و Independent Verifier نباید Failure مشترک پنهان داشته باشند؛ Independence Semantics دقیق متعلق به P06/P13 است.

P04-CON-156 — Disagreement بین Engineها/Verifierها باید به `DISPUTED`، Investigation و Evidence preservation منجر شود، نه Average/Majority خودکار.

P04-CON-157 — AI Narrative، Summary یا Explanation نباید Scientific Status، Uncertainty، Covariance، Limitation یا Verification Result را Overwrite کند.

P04-CON-158 — Scenario/Maneuver Analysis فقط Analysis/Recommendation زمینی است و هیچ Transition آن نباید Operational Promotion یا Maneuver Execution خودکار ایجاد کند.

P04-CON-159 — Scientific Dataset/Model Auxiliary Source Freshness و Provenance باید در Admission و Retry بررسی شود؛ Cached Result بدون Applicability Claim معتبر نیست.

P04-CON-160 — `CSIP-EO-RS-STAGE-20` تا Domain Review مستقل، صلاحیت‌دار و Approval تازه Digest-bound در وضعیت `DOMAIN_REVIEW_REQUIRED` باقی می‌ماند؛ P04 آن را Approved فرض نمی‌کند.

P04-DEN-059 — Orchestrator نباید Missing Scientific Field را Default، Infer، Unit-convert حدسی یا از متن AI استخراج و قطعی کند.

P04-DEN-060 — Non-convergence، Missing Covariance، Unknown Frame/Tim