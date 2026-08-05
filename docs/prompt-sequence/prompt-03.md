
<<<CSIP-EO-FMSP-18P|0.9.0-draft|P03|START>>>
CSIP_EO_PROMPT_PACKAGE_ID: CSIP-EO-FINAL-MASTER-SUPERPROMPT-18P
CSIP_EO_PROMPT_PACKAGE_VERSION: 0.9.0-draft
PART_ID: CSIP-EO-FMSP-P03
PART_INDEX: 03
PART_COUNT: 18
PART_TITLE: API, Application Command and Query Contract | قرارداد API، Application Command و Query
SEMANTIC_OWNER_ARTIFACT_ID: CSIP-EO-RS-STAGE-17
SEMANTIC_OWNER_VERSION: 0.1.0-reconstituted-draft
SEMANTIC_OWNER_STATUS: RECONSTITUTED_DRAFT — REVIEW_READY — NOT_APPROVED — NOT_FROZEN
SEMANTIC_OWNER_SHA256: 3f16593a323f3024550a4515a1c48118872e53bfdbb60d3d7ae47385ab4ff249
SUPPORTING_SOURCE_BINDINGS: CSIP-EO-AUDIT-GAP-02/0.1.0-candidate/fa400334a69702bf56e8588210449590573bccd3120d7c2cebd6ba9cc8fc161f; ENTERPRISE-TRUST-RISK-COST-EVIDENCE-REPRODUCIBILITY-MANDATE/verified-input-2026-07-28/1b5e7884a343589312d62259f181bd48f1a12b51e2613685c0d58c747a08dab4; CSIP-EO-PROMPT-ARCH-18P-C1/0.1.0-design-candidate/a4c80b938fccaab5d3d85c780351a41ee3444b4c6712920af45b493afbacb09b; CSIP-EO-GAP-RESOLUTION-MANIFEST-C1/0.1.0-candidate/349b590df9fad00c2e0ec317f4bd0b7ad747a5e22a1fead0f66f28c98e955216
PRIOR_PART_ID: CSIP-EO-FMSP-P02
NEXT_PART_ID: CSIP-EO-FMSP-P04
PART_PAYLOAD_SHA256: SEE_EXTERNAL_PROMPT_PACKAGE_MANIFEST
RECEIVE_MODE: CONTEXT_ONLY
ACTION_AUTHORITY: NONE
# پرامپت قسمت ۰۳ از ابرپرامپت نهایی ۱۸ قسمتی CSIP-EO
# قرارداد API، Application Command و Query
## 0. دستور دریافت، مرز این قسمت و قفل ضدتوهم
این پیام فقط «قسمت ۰۳ از ۱۸» یک زمینۀ مرجعِ به‌هم‌پیوسته است. قسمت‌های ۰۱ و ۰۲ باید پیش از این قسمت و به‌ترتیب دریافت شده باشند. قسمت‌های ۰۴ تا ۱۸ هنوز در این پیام وجود ندارند. دریافت این قسمت فقط Context مربوط به Semantics فراخوانی API را گسترش می‌دهد و هیچ اختیار علمی، حقوقی، امنیتی، مالی، اجرایی یا عملیاتی ایجاد نمی‌کند.
P03-REQ-001 — هنگام دریافت این قسمت، وضعیت داخلی خود را دقیقاً چنین در نظر بگیر:
`RECEIVING_P03 — P01_P02_REQUIRED — CONTEXT_INCOMPLETE — ACTION_AUTHORITY_NONE`
P03-DEN-001 — اگر قسمت ۰۱ یا ۰۲ دریافت نشده، ترتیب `P01 → P02 → P03` قابل‌اثبات نیست، یا Header، Anchor، Source Binding، Footer یا Pointerهای این قسمت ناقص یا متعارض‌اند، این قسمت را فعال نکن و موفقیت دریافت را جعل نکن.
P03-DEN-002 — از این Part برای حدس‌زدن، بازسازی، تکمیل یا جعل محتوای قسمت‌های ۰۴ تا ۱۸ استفاده نکن. دانستن عنوان، Semantic Owner، Version، Status یا Digest یک Part بعدی مجوز ساخت محتوای غایب آن نیست.
P03-DEN-003 — تا پیش از دریافت و مونتاژ معتبر هر ۱۸ قسمت، تحت هیچ شرایطی:
- تحلیل یکپارچۀ CSIP-EO ارائه نکن؛
- API، Endpoint، Route، Schema اجرایی، SDK، Workflow، Capability، Plugin، Adapter یا Policy جدید طراحی یا پیاده‌سازی نکن؛
- هیچ Decision را تصویب، هیچ Source را Normative و هیچ Stage را Approved یا Frozen اعلام نکن؛
- کد، تست، فایل پروژه، Repository، Branch، Commit، Pull Request، Database، Infrastructure یا Configuration ایجاد یا تغییر نده؛
- Command، Query واقعی، Tool Call، Browse، Search، External Retrieval، Build، Migration، Release، Deployment، Pilot، Production یا Project Freeze اجرا نکن؛
- Dependency، Model، Runtime، Framework، Broker، Provider، Plugin یا Tool نصب، فعال یا متصل نکن؛
- هیچ Approval، Authorization، Execution Lease، Credential، Budget، Risk Acceptance یا External Effect ایجاد نکن؛
- هیچ داده‌ای را به External System ارسال، Export، Delete، Mutate یا منتشر نکن؛
- Application Command را Spacecraft Command، Telecommand، Uplink، Flight Control یا Autonomous Maneuver Execution تفسیر نکن؛
- توصیه یا گام بعدی اجرایی برای شروع توسعه ارائه نکن.
P03-REQ-002 — پس از دریافت سالم این قسمت فقط این چهار کار مجاز است:
1. متن را Parse و در Context جاری حفظ کن؛
2. پیوستگی `P01 → P02 → P03 → P04`، Header، Start Anchor، End Anchor، Source Binding و Footer را از روی Parts دریافت‌شده کنترل کن؛
3. هیچ تحلیل محتوایی پروژه، طراحی جدید، پیاده‌سازی یا اقدام ابزاری انجام نده؛
4. فقط پاسخ ثابت زیر را بدون هیچ متن قبل یا بعد برگردان:
~~~text
قسمت ۰۳ از ۱۸ ابرپرامپت نهایی CSIP-EO با موفقیت دریافت و ثبت شد.
هیچ تحلیل، طراحی جدید، پیاده‌سازی یا اقدام اجرایی آغاز نمی‌شود.
منتظر قسمت ۰۴ هستم.
~~~
P03-FAIL-001 — اگر دریافت ناقص، بریده، خارج از ترتیب یا متعارض بود، موفقیت را جعل نکن و فقط پاسخ زیر را با ایراد دقیق در براکت ارائه کن:
~~~text
دریافت قسمت ۰۳ از ۱۸ ابرپرامپت نهایی CSIP-EO کامل و معتبر نبود.
وضعیت: PART_TRUNCATED_OR_CONFLICTED — CONTEXT_NOT_ACTIVATED
مورد لازم برای اصلاح: [ایراد دقیق]
هیچ تحلیل، طراحی جدید، پیاده‌سازی یا اقدام اجرایی آغاز نمی‌شود.
~~~
P03-REQ-003 — سکوت، تأخیر کاربر، دریافت‌نشدن قسمت ۰۴ یا آگاهی از عنوان آن مجوز ادامۀ خودکار نیست. تا ارسال واقعی Part بعدی در وضعیت انتظار باقی بمان.
### 0.1 نقش این قسمت در بستۀ ۱۸ قسمتی
این قسمت مالک معنایی موارد زیر است:
- Semantics مستقل از Protocol برای Request و Result؛
- جداسازی Query، Application Command، Event، Recommendation، Decision، Approval، AuthorizationDecision، ExecutionLease، ExecutionReceipt و Outcome؛
- Canonical Request Envelope؛
- Contract خواندن Side-effect-free؛
- Contract تغییر محدود، Typed و زمینیِ Application State؛
- Receipt، Reconciliation و Validated Outcome Semantics؛
- Idempotency، Ordering، Concurrency، Retry و Replay Protection؛
- Long-running Operation Resource؛
- Error، Compatibility و Deprecation Contract؛
- ممنوعیت Generic/Untyped Execution Endpoint و هر مسیر Spacecraft Command.
P03-CON-001 — مالکیت این قسمت فقط Semantics فراخوانی و مرزبندی Recordهاست. Base Canonical Event Envelope متعلق به P01، Workflow و Human Checkpoint متعلق به P04، Taxonomyهای Effect/Approval/Permission/Autonomy متعلق به P05، Scientific Truth متعلق به P06، Capability Extension متعلق به P08، Security Controls متعلق به P11 و Verification Method متعلق به P13 باقی می‌مانند.
### 0.2 رابطۀ این قسمت با Parts قبلی و بعدی
P03-CON-002 — این قسمت هویت پروژه، Scope، TemporalStamp، Canonical Entity و Base Event Envelope را از P01 و پروتکل Stage، Decision، Action، Evidence و Gate Separation را از P02 مصرف می‌کند و حق تعریف رقیب برای آن‌ها ندارد.
P03-CON-003 — این قسمت Invocation Semantics را به P04 و P08 تحویل می‌دهد:
- P04 باید Workflow State Machine، Checkpoint و Human Control را روی همین Recordهای جدا بنا کند؛
- P08 باید هر Capability را از طریق Application Command تایپ‌شده و محدود قابل‌فراخوانی کند؛
- هیچ‌یک حق تبدیل Callback، Event، Tool Output، Approval یا Queue Acknowledgement به Outcome ضمنی را ندارند.
## 1. هویت منبع، وضعیت و محدودیت تاریخی
P03-DEF-001 — مالک معنایی این قسمت:
- Artifact ID: `CSIP-EO-RS-STAGE-17`
- Version: `0.1.0-reconstituted-draft`
- SHA-256: `3f16593a323f3024550a4515a1c48118872e53bfdbb60d3d7ae47385ab4ff249`
- Status: `RECONSTITUTED_DRAFT — REVIEW_READY — NOT_APPROVED — NOT_FROZEN`
- Successor candidate of: `CSIP-EO-STAGE-17`
- Historical source state: `MISSING_NORMATIVE_ARTIFACT`
- Title status: `RECONSTITUTED_SUCCESSOR_TITLE`
- Domain scope: `EARTH_ORBIT_ONLY`
- Deployment baseline: `TERRESTRIAL_BASELINE — ON_ORBIT_RUNTIME_DEFERRED`
P03-DEN-004 — این Artifact یک Successor Candidate تازه‌تألیف‌شده است؛ Bytes، عنوان قطعی، Decision IDs، Version یا Approval تاریخی Stage 17 بازیابی نشده‌اند. این متن هرگز نباید «اصل تاریخی بازیابی‌شده» یا «Stage 17 تصویب‌شده» معرفی شود.
P03-CON-004 — هویت هر Source با ترکیب زیر تعیین می‌شود:
`Artifact ID + Exact Version + Exact SHA-256 + Status`
Filename، Directory، تاریخ جدیدتر، متن طولانی‌تر، ترجمه، Summary، Retrieval Result، Memory یا Model Output به‌تنهایی Source Identity، Supersession یا Approval ایجاد نمی‌کند.
P03-CON-005 — Sourceهای پشتیبان این Part فقط Overlay، Mandate، Assembly Contract و Manifest هستند. آن‌ها Semantic Owner را جایگزین نمی‌کنند، Approval تازه نمی‌سازند و فقط در Scope و Status ثبت‌شدۀ خود قابل‌استفاده‌اند.
P03-CON-006 — پذیرش این Part برای Assembly فقط `PART_ACCEPTED_FOR_ASSEMBLY` ایجاد می‌کند. این پذیرش وضعیت `RECONSTITUTED_DRAFT` منبع، Decisionهای `PROPOSED` یا Gateهای Implementation/Verification/Release/Deployment/Freeze را ارتقا نمی‌دهد.
P03-FAIL-002 — اگر Version، Digest، Status یا Owner Binding منبع با Header، Canonical Map یا Manifest تعارض داشت، Binding برابر `SOURCE_BINDING_CONFLICTED` است و Context این Part نباید فعال شود. «فایل جدیدتر/طولانی‌تر برنده است» ممنوع است.
## 2. هدف، Scope و Exclusionهای صریح
P03-REQ-004 — هدف این قسمت ایجاد یک Contract دقیق و Protocol-neutral است تا هیچ Client، Agent، Model، Workflow، Plugin، Adapter، Tool یا Transport نتواند Read، Intent، Approval، Attempt و Outcome را با یکدیگر مخلوط کند یا از یک Record اختیار Record بعدی را استنتاج نماید.
P03-REQ-005 — این Contract باید حداقل موارد زیر را پوشش دهد:
1. Canonical Request و Result Envelope؛
2. Query واقعاً Side-effect-free نسبت به Authoritative و External State؛
3. Application Command زمینی، Typed، Bounded و Preconditions-bound؛
4. Receipt، Reconciliation و Validated Outcome؛
5. Idempotency، Ordering، Concurrency و Replay Protection؛
6. Long-running Operation؛
7. Safe Error و Retryability؛
8. Schema Versioning، Compatibility و Deprecation؛
9. Security، Tenant، Purpose، Classification، Risk، Cost و Evidence Context؛
10. Hard Denial برای Generic Execution و Spacecraft-command-enabling Path.
P03-DEN-005 — این Part هیچ HTTP Framework، RPC Framework، Message Broker، API Gateway، SDK، Serialization Format، Database، Cloud، Vendor، Runtime، Deployment Product، Port، URL یا Endpoint واقعی را انتخاب نمی‌کند.
P03-DEN-006 — `Application Command` در سراسر این Part فقط درخواست محدود برای تغییر State یک Application زمینی است. این اصطلاح هرگز Spacecraft Command، Telecommand، Uplink، Flight Control، Flight Dynamics Commanding یا Autonomous Maneuver Execution نیست.
P03-DEN-007 — هیچ Generic Endpoint یا Capability مانند `executeAnything`، Arbitrary Shell، Arbitrary SQL، Unrestricted URL Fetch، Arbitrary Plugin Invocation، Untyped `action`، Dynamic Eval یا Catch-all Executor مجاز نیست.
P03-CON-007 — هر Application Command باید به یک Capability تایپ‌شده، Versioned و محدود به Target/Scope زمینی Bind شود. هر مسیر مستقیم، غیرمستقیم یا توسعه‌پذیری که بتواند مرز فوق را دور بزند، `COMMAND_PATH_PROHIBITED` است.
P03-CON-008 — Schema یا Route فقط شکل Request را بیان می‌کند؛ وجود آن Permission، Approval، Authorization، Execution Lease، Execution، Receipt، Outcome یا Intended-use Validity ایجاد نمی‌کند.
P03-INV-001 — زنجیرۀ معنایی تغییرناپذیر این قسمت چنین است:
`intent → request → policy decision → approval when required → execution lease → attempt → receipt → validation/reconciliation → outcome event`
هیچ Link در این زنجیره ضمنی، قابل‌پرش یا قابل‌استنتاج نیست.
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
P03-CON-009 — تکرار این کپسول Safety Checksum است؛ مالکیت مبانی را از P01 منتقل نمی‌کند و Approval جدیدی ایجاد نمی‌نماید.
## 4. واژگان Canonical و جداسازی Semantics
P03-DEF-002 — `Query` درخواست Read-only است که نسبت به Authoritative State و External State هیچ Mutation، Lock مادی، Trigger اجرایی یا Effect پنهان ایجاد نمی‌کند.
P03-DEF-003 — `ApplicationCommand` درخواست یک State Transition محدود، Typed و زمینی است؛ Command نه Permission است، نه Execution و نه Evidence موفقیت.
P03-DEF-004 — `Event` طبق مالکیت P01 یک Fact Immutable درباره رخدادی است که اتفاق افتاده است. این Part فقط رابطۀ Event با API Lifecycle را تعریف می‌کند و Base Event Envelope را بازتعریف نمی‌نماید.
P03-DEF-005 — `Recommendation` یک Option مشورتی همراه Evidence، Uncertainty و Limitation است؛ نه Decision، Approval یا Authorization.
P03-DEF-006 — `Decision` انتخاب پاسخ‌گویانه میان Optionهاست؛ Decision به‌تنهایی هیچ Effect را اجرا نمی‌کند.
P03-DEF-007 — `Approval` موافقت Scope-bound، Version-bound، Digest-bound و Time-bound یک Authority صلاحیت‌دار است؛ Approval Permission دائمی یا Execution نیست.
P03-DEF-008 — `AuthorizationDecision` نتیجۀ Policy برای Actor، Action، Resource و Context دقیق است؛ این Record Human Approval نیست مگر Link صریح و معتبر داشته باشد.
P03-DEF-009 — `ExecutionLease` حق کوتاه‌عمر، Scope-bound و Digest-bound برای Attempt یک Action دقیق است؛ Credential عمومی یا قابل‌استفادۀ مجدد نیست.
P03-DEF-010 — `ExecutionReceipt` Evidence یک Attempt و Effect State مشاهده‌شده است؛ Receipt بدون Validation و Reconciliation ادعای Success نیست.
P03-DEF-011 — `Outcome` وضعیت Result پس از Validation یا Reconciliation نسبت به Intended Transition، Preconditions و Acceptance Rule تعریف‌شده است؛ Outcome از پذیرش Request یا متن Tool استنتاج نمی‌شود.
P03-DEF-012 — `RequestDigest` Digest حاصل از Envelope نرمال‌شده و Protected Payload Reference دقیق تحت Canonicalization Profile مشخص است. تا زمانی که Profile و Algorithm دقیق تعیین و Verify نشده‌اند، هیچ Cross-implementation Byte-equivalence Claim مجاز نیست.
P03-DEF-013 — `OperationResource` هویت پایدار یک کار Long-running است که Status، Eventها، Receiptها، Cancellation Request و Outcomeهای مربوط به همان Invocation را پیوند می‌دهد.
P03-DEF-014 — `Reconciliation` فرایند Evidence-led برای تعیین Effect واقعی پس از Timeout، Partial Result، Lost Receipt، Duplicate Attempt یا Outcome نامعلوم است؛ Blind Retry جایگزین آن نیست.
P03-DEF-015 — `Projection` نمایش Read-optimized، Cache، Index، Search View، Vector View یا Materialized View از Source مشخص است؛ Projection به‌خودی‌خود Canonical Truth نیست.
| Record | معنای محدود | تفسیر ممنوع |
|---|---|---|
| `Query` | خواندن بدون Authoritative Mutation | Hidden Write، External Effect یا Command |
| `ApplicationCommand` | درخواست State Transition زمینی محدود | Permission، Attempt یا Outcome |
| `Event` | Fact ثبت‌شده | Intent، Command، Approval یا Future Promise |
| `Recommendation` | پیشنهاد مشورتی | Decision یا Authorization |
| `Decision` | انتخاب ثبت‌شده | Automatic Execution |
| `Approval` | Consent دقیق و محدود | Blanket Permission |
| `AuthorizationDecision` | Policy Result دقیق | Human Approval ضمنی |
| `ExecutionLease` | حق کوتاه‌عمر برای Attempt دقیق | Reusable Credential |
| `ExecutionReceipt` | Evidence Attempt | Success بدون Verification |
| `Outcome` | Result اعتبارسنجی‌شده | نتیجه استنتاج‌شده از Acceptance |
P03-DEN-008 — Client Claim، Model Output، UI Label، Route Name، HTTP Verb، RPC Method، Queue Topic، Tool Description، Plugin Manifest یا Schema Enum به‌تنهایی Authority یا Effect Truth ایجاد نمی‌کند.
P03-DEN-009 — Recordهای جدول فوق نباید Merge، Alias یا از یکدیگر استنتاج شوند. Agreement میان Agentها، Model Confidence، Queue Acknowledgement یا Successful Parse هیچ Transition معنایی ایجاد نمی‌کند.
## 5. معماری منطقی Protocol-neutral و جریان Invocation
P03-CON-010 — Contract این قسمت در HTTP، RPC، Event-driven، Batch، SDK یا Transportهای آینده باید Semantics یکسان داشته باشد. Mapping یک Transport نمی‌تواند Requirement، Authority، Effect، Error، Evidence یا Outcome State را کاهش دهد.
P03-CON-011 — جریان منطقی Admission و Execution برای Request دارای Effect باید حداقل مراحل زیر را جدا نگه دارد:
1. دریافت و Parse Envelope؛
2. Authentication Actor و Workload؛
3. Canonicalization Tenant، Purpose، Target، Operation و Classification؛
4. Schema، Deadline، Payload، Quota و Integrity Validation؛
5. محاسبۀ Server-side Effect و Transitive Exposure؛
6. Policy Evaluation و AuthorizationDecision؛
7. Resolution Approvalهای لازم؛
8. صدور ExecutionLease دقیق و کوتاه‌عمر؛
9. Attempt توسط Executor مجاز؛
10. ثبت ExecutionReceipt؛
11. Validation یا Reconciliation؛
12. ثبت Outcome و انتشار Eventهای مربوط از طریق Contract P01.
P03-PROC-001 — هر مرحلۀ بالا باید ورودی، خروجی، Error State، Timestamp، Actor/Service Identity، Digest و Evidence Reference مستقل داشته باشد. گذر از یک مرحله فقط با Predicate صریح و Record معتبر مجاز است.
P03-DEN-010 — این جریان Base Event Envelope، Workflow State Machine، Authority Taxonomy یا Capability Descriptor را بازتعریف نمی‌کند؛ فقط نقاط اتصال آن‌ها را مشخص می‌سازد.
P03-CON-012 — عملیات Read-only از مسیر Query و تغییر State از مسیر Application Command انجام می‌شود. یک Endpoint یا Method واحد نباید با Payload مبهم بین Query و Command سوییچ کند.
P03-FAIL-003 — اگر Request Type، Target، Operation، Declared Intent، Effect، Identity، Tenant، Purpose، Policy Snapshot یا Deadline برای یک Request اثرگذار Missing، Unknown یا Contradictory باشد، نتیجه `DO_NOT_EXECUTE / REQUEST_INDETERMINATE` است.
## 6. Canonical Request Envelope
P03-REQ-006 — هر Query یا Application Command باید Envelope زیر را با Applicability و Cardinality معتبر حمل کند:
~~~yaml
request_id:
request_type: QUERY|APPLICATION_COMMAND
request_schema_id:
request_schema_version:
created_at: TemporalStamp
deadline_at: TemporalStamp
actor_chain: []
tenant_context:
purpose_context:
declared_intent:
target_reference:
operation:
declared_effect:
server_effect_classification:
data_classification:
environment:
risk_context:
cost_budget_context:
policy_snapshot_reference:
approval_reference:
execution_lease_reference:
idempotency_key:
correlation_id:
causation_id:
trace_id:
workflow_id:
payload_schema:
payload_digest:
payload_or_protected_reference:
client_capabilities:
~~~
P03-CON-013 — Actor، Tenant، Purpose، Target، Effect و Classification باید Server-side Canonicalize شوند. مقدار Client فقط Claim است و در صورت تعارض نمی‌تواند مقدار معتبرتر یا سخت‌گیرانه‌تر Server/Policy را کاهش دهد.
P03-CON-014 — RequestDigest باید Envelope نرمال‌شدۀ دقیق، Payload Schema، Payload Digest یا Protected Reference، Canonicalization Profile و Critical Context را Bind کند. Approval، AuthorizationDecision و ExecutionLease باید به همان Digest دقیق اشاره کنند.
P03-CON-015 — `created_at` و `deadline_at` باید `TemporalStamp` مطابق P01 و دارای Time Scale صریح باشند. Deadline منقضی یا Time Context نامعتبر پیش از Attempt باید Fail Closed شود.
P03-CON-016 — `request_schema_id`، `request_schema_version` و `payload_schema` باید Explicit و Registry-resolved باشند. Mutable Alias مانند `latest` در Qualified Path مجاز نیست.
P03-CON-017 — `actor_chain` باید Actor اصلی، Delegateها، Agentها، Serviceها و Executorهای مادی را بدون ایجاد Authority تازه Trace کند. Delegation فقط Scope موجود را منتقل می‌کند و نمی‌تواند آن را توسعه دهد.
P03-CON-018 — `correlation_id`، `causation_id`، `trace_id` و `workflow_id` برای Traceability هستند؛ هیچ‌کدام Identity، Tenant، Purpose، Permission یا Approval ایجاد نمی‌کنند.
P03-DEN-011 — Secret، Credential، Token، Password، Private Key یا Raw Sensitive Content نباید در Envelope غیرمحافظت‌شده، Log، Error، Event یا Evidence قرار گیرد. فقط Protected Reference و Digest مجاز است.
P03-FAIL-004 — Unsupported Critical Schema Version، Unknown Critical Field، Invalid TemporalStamp، Digest Mismatch، Expired Deadline، Missing Target یا Unresolvable Protected Reference باید Request را پیش از Effect رد کند.
## 7. Query Contract و Result Semantics
P03-REQ-007 — Query معتبر باید:
- نسبت به Authoritative و External State Side-effect-free باشد؛
- Source Authority یا Projection Authority صریح داشته باشد؛
- Snapshot، Watermark، Valid Time و Transaction Time را در صورت Applicability مشخص کند؛
- Freshness، Staleness، Completeness، Provenance و Uncertainty را برگرداند؛
- Pagination، Payload Size، Time و Resource Bound داشته باشد؛
- Classification، Masking، Tenant و Purpose را اعمال کند؛
- Cache، Index، Vector Store، Search Result یا AI-derived Record را به Canonical Truth ارتقا ندهد.
P03-CON-019 — Telemetry، Security Audit یا Read Accounting داخلی فقط زمانی با Query Semantics سازگار است که Authoritative Business State را تغییر ندهد، External Effect ایجاد نکند، Durable Business Lock نگیرد، Workflow Transition نسازد و Result را به وقوع آن Write وابسته نکند.
P03-DEN-012 — Query نباید Hidden Write، Command Dispatch، Notification، External Callback، Job پایدار/غیرهمزمان، تعهد هزینه خارج از Cost Envelope همان Query، Lock مادی، Durable Mutation، Approval Creation یا State Promotion ایجاد یا فعال کند.
P03-CON-020 — هر Query باید Source Authority و Projection Class را مشخص کند. اگر Projection Stale، Partial، Rebuilding، Lagging یا Disputed است، همان وضعیت باید در Result حفظ شود.
P03-CON-021 — Pagination Cursor باید به Query Identity، Filter/Sort، Snapshot یا Watermark و Tenant/Classification Context مناسب Bind شود. Cursor نباید Cross-tenant Data، Unstable Duplicate یا Silent Snapshot Drift ایجاد کند.
P03-REQ-008 — Canonical Query Result:
~~~yaml
query_result_id:
request_digest:
source_authority:
projection_class:
schema_id:
schema_version:
snapshot_or_watermark:
valid_time_context:
transaction_time_context:
freshness_status:
data_or_artifact_reference:
page_cursor:
classification_and_masking:
provenance_reference:
uncertainty_context:
warnings: []
limitations: []
result_state: COMPLETE|PARTIAL|EMPTY|ABSTAINED|INDETERMINATE
result_digest:
~~~
P03-CON-022 — `EMPTY`، `PARTIAL`، `STALE`، `ABSTAINED`، `UNKNOWN` و `INDETERMINATE` مفاهیم جدا هستند. هیچ‌یک نباید به Complete، Fresh یا Success تبدیل شوند.
P03-CON-023 — Retry یک Query فقط در صورتی مجاز است که Bound، Deadline، Rate/Cost Policy و Snapshot Semantics آن حفظ شوند. Retry نباید Read را به Job، External Effect یا Authoritative Mutation تبدیل کند.
P03-FAIL-005 — اگر Source Authority، Snapshot/Watermark، Freshness، Classification، Provenance یا Uncertainty لازم نامعلوم باشد، Result باید `PARTIAL`، `ABSTAINED` یا `INDETERMINATE` متناسب باقی بماند؛ پاسخ خوش‌بینانۀ Complete ممنوع است.
P03-FAIL-006 — اگر یک Query در عمل Authoritative Mutation یا External Effect ایجاد کند، Contract Violation مادی است؛ Request باید Stop/Block شود، Evidence حفظ گردد و Capability به‌عنوان Query معتبر معرفی نشود.
## 8. Application Command Contract
P03-REQ-009 — هر Application Command باید:
- دقیقاً یک Command Type و Capability Type معتبر داشته باشد؛
- Target Set محدود و قابل‌شمارش یا Bound داشته باشد؛
- Preconditions و Expected Revision/Digest را اعلام کند؛
- Desired Transition را Typed و قابل‌اعتبارسنجی کند؛
- حداکثر Effect مستقیم، غیرمستقیم، Transitive و Aggregated را Server-side دریافت کند؛
- Irreversibility، Blast Radius و Environment را مشخص کند؛
- Approval، Policy، Risk، Budget و ExecutionLease معتبر را Bind کند؛
- Rollback، Compensation یا Recovery Semantics را روشن سازد؛
- Idempotency و Unknown-outcome Reconciliation را تعریف کند؛
- Intent، Attempt، Receipt و Outcome Evidence جدا تولید نماید.
P03-REQ-010 — Canonical Command Body:
~~~yaml
command_id:
command_type:
target_set:
preconditions: []
expected_revision_or_digest:
desired_transition:
effect_class:
irreversibility:
blast_radius:
approval_class:
execution_constraints:
rollback_or_recovery_plan_reference:
reconciliation_profile:
~~~
P03-CON-024 — Command Type، Target Type، Desired Transition، Preconditions و Capability Reference باید Schema-bound و Versioned باشند. Free-form متن می‌تواند توضیح یا Proposal باشد، اما Executor Contract نیست.
P03-CON-025 — Expected Revision/Digest و Preconditions باید در نزدیک‌ترین نقطۀ معتبر پیش از Commit دوباره بررسی شوند. Check زمان Admission جایگزین Check زمان Execution نیست.
P03-CON-026 — Effect Class را Server از Maximum Actual/Transitive Effect محاسبه می‌کند. Client، Agent، Model، Plugin یا Tool نمی‌تواند Effect را کاهش دهد یا Unknown Exposure را Low Risk/Zero Cost اعلام کند.
P03-CON-027 — Rollback فقط در صورت اثبات Reversibility مجاز است. برای Effect غیرقابل Rollback باید Compensation، Recovery، Roll-forward یا Fencing Contract و Limitation صریح وجود داشته باشد.
P03-CON-028 — پذیرش Command فقط یعنی Request برای Processing پذیرفته شده است. Acceptance نه Approval، نه Lease، نه Attempt، نه Commit و نه Outcome است.
P03-CON-029 — Batch یا Multi-target Command فقط با Cardinality Bound، Homogeneous Typed Semantics، Blast-radius Limit، Partial-failure Contract و Per-target Evidence مجاز است. Cardinality نامعلوم مساوی Scope نامعلوم است.
P03-DEN-013 — Command نباید Generic، Untyped، Arbitrary، Catch-all یا دارای Escape Hatch به Shell، SQL، URL، Plugin، Tool، Network، Credential یا Dynamic Code باشد.
P03-DEN-014 — عبارت‌هایی مانند `dry_run`، `safe`، `internal`، `AI-approved`، `admin` یا `human-triggered` Effect، Risk، Approval یا Prohibition واقعی را کاهش نمی‌دهند.
P03-DEN-015 — هیچ Command Schema، Route، Enum، Mock، Example، Adapter، Callback، Plugin Hook، Workflow Step یا Hidden Field نباید Spacecraft Command، Telecommand، Uplink، Flight Control یا Autonomous Maneuver Execution را مدل یا فعال کند.
P03-FAIL-007 — اگر Target Set، Preconditions، Expected Revision، Effect، Blast Radius، Irreversibility، Approval Class، Lease یا Recovery Plan Missing/Contradictory باشد، Command برابر `COMMAND_INDETERMINATE — DO_NOT_EXECUTE` است.
P03-FAIL-008 — اگر Preconditions یا Expected Revision در زمان Attempt برقرار نباشد، Effect نباید Commit شود؛ Result باید Conflict دقیق، Current State Reference و Evidence مناسب برگرداند.
## 9. Admission، Authority Binding و Effect Routing
P03-PROC-002 — Admission یک Application Command باید به‌ترتیب حداقل این Predicateها را بررسی کند:
1. Request Identity و Schema معتبر؛
2. Actor/Workload Authentication معتبر؛
3. Tenant، Purpose، Target و Environment معتبر؛
4. Deadline، Nonce، Idempotency و Replay Context معتبر؛
5. Data Classification و Egress Boundary معتبر؛
6. Actual/Transitive Effect و Irreversibility قابل‌تعیین؛
7. Risk و Cost Exposure در Envelope مجاز؛
8. Policy Snapshot و AuthorizationDecision معتبر؛
9. Approval Recordهای لازم Exact-scope و Exact-digest؛
10. ExecutionLease معتبر، کوتاه‌عمر و مصرف‌نشده؛
11. Preconditions و Expected Revision معتبر؛
12. Evidence، Receipt و Reconciliation Plan قابل‌اجرا.
P03-CON-030 — Authentication، Authorization، Approval، ExecutionLease، Execution، Receipt و Outcome محورهای مستقل‌اند. Pass شدن یک محور به محور دیگر منتقل نمی‌شود.
P03-CON-031 — Taxonomy دقیق `E0..E9`، `APR-*`، `PERM-*` و `AUT-*` فقط متعلق به P05 است. این Part فقط باید Request را به Recordهای P05 Bind کند و از تعریف رقیب خودداری نماید.
P03-CON-032 — Effect Routing Baseline بازتاب‌یافته از Source این Part، بدون انتقال مالکیت Taxonomy:
| API Activity | Minimum Effect Routing | محدودیت |
|---|---:|---|
| Public/static read | `E0` | همچنان Policy-bound |
| Authenticated low-risk read | `E1` | Data Policy لازم |
| Sensitive/internal read یا Proposal Creation | `E2` | Promotion خودکار ممنوع |
| Bounded reversible Application Mutation | `E3/E4` | Exact Policy/Approval لازم |
| Material State/Configuration Mutation | `E5` | Domain Review لازم |
| External Egress، Code Execution یا Pilot Enablement | `E6+` | Multi-domain Approval لازم |
| Production، Bulk یا Cross-tenant Effect | `E7+` | Independent Approval لازم |
| Destructive یا Irreversible Effect | `E8` | Exceptional Dual Control لازم |
| Spacecraft Command/Uplink | `E9` | `APR-X / PROHIBITED` |
این جدول Routing Baseline است؛ Definition و Default Mapping دقیق فقط در P05 معتبر خواهد بود.
P03-CON-033 — Approval و ExecutionLease باید حداقل Actor/Workload، Tenant، Purpose، Target، Operation، RequestDigest، Effect، Environment، Conditions، Validity Window و Revocation/Consumption State دقیق را Bind کنند.
P03-CON-034 — Approval منقضی، Revoke‌شده، Scope-mismatched، Digest-mismatched، Environment-mismatched یا صادرشده برای Artifact دیگر معتبر نیست. Lease نیز قابل‌انتقال، قابل‌گسترش یا قابل‌استفادۀ مجدد نیست.
P03-DEN-016 — API Key، Session، Login، Admin Role، Generic Permission، Human Mediation، Browser Access، Shell Access، Plugin Install یا Tool Availability جای Approval و ExecutionLease دقیق را نمی‌گیرد.
P03-FAIL-009 — Missing، Stale، Expired، Revoked، Unknown یا Contradictory Policy/Approval/Permission/Autonomy/Risk/Cost Mapping نتیجه `DENY / DO_NOT_EXECUTE` دارد.
P03-FAIL-010 — هر Attempt برای ایجاد Approval Route به `E9` یا کاهش `APR-X` یک Contract Violation بحرانی و مسیر Incident است، نه Change Request عادی.
## 10. Execution Receipt، Validation، Reconciliation و Outcome
P03-REQ-011 — هر Attempt باید Execution Receipt مستقل با Contract زیر تولید کند:
~~~yaml
receipt_id:
request_digest:
lease_digest:
executor_identity:
attempt_id:
started_at: TemporalStamp
finished_at: TemporalStamp
effect_state: NONE|PENDING|COMMITTED|PARTIAL|ROLLED_BACK|COMPENSATED|UNKNOWN
observed_target_revision:
external_receipt_references: []
validation_status:
reconciliation_status:
warnings: []
failure_codes: []
evidence_references: []
receipt_digest:
~~~
P03-CON-035 — Receipt باید Attempt واقعی، Executor Identity، زمان، Lease Digest، Effect State مشاهده‌شده، Target Revision، Evidence و Limitation را ثبت کند. Queue Ack، HTTP Success، SDK Return، Tool Text یا Agent Statement Receipt کافی نیست مگر Contract فوق را واقعاً برآورده کند.
P03-DEN-017 — `COMMITTED` در یک Receipt به‌تنهایی Intended-use Success، Scientific Validity، Business Acceptance، Release Readiness یا Operational Outcome را اثبات نمی‌کند.
P03-CON-036 — Outcome باید حداقل به RequestDigest، Command/Query Identity، Receiptها، Target State/Revision، Validation Method/Oracle، Validator Identity، Evidence، Warnings، Limitations و Completion TemporalStamp متصل باشد و Result State را صریح ثبت کند.
P03-CON-037 — Outcome فقط پس از مقایسۀ Observed State با Desired Transition، Preconditions، Acceptance Rule و Evidence تعریف‌شده قابل‌ثبت است. Validation Status نامعلوم باید Outcome را `UNKNOWN` یا `INDETERMINATE` نگه دارد.
P03-CON-038 — Reconciliation باید State خارجی و داخلی، Idempotency Record، Target Revision، External Receipt، Audit/Evidence و Attempt History را بررسی کند و نتیجه را با Record جدید ثبت نماید؛ History قبلی Silent Rewrite نمی‌شود.
P03-CON-039 — Cancellation فقط درخواست توقف Attemptهای آینده یا جاری است. Cancellation نه Commit قبلی را برمی‌گرداند، نه Rollback را اثبات می‌کند و نه Outcome را خودکار `CANCELLED_WITH_NO_EFFECT` می‌سازد.
P03-FAIL-011 — Timeout پیش از اثبات عدم Attempt می‌تواند `NONE` باشد؛ Timeout پس از احتمال Commit باید `UNKNOWN` شود. در حالت دوم Retry خودکار ممنوع و Reconciliation اجباری است.
P03-FAIL-012 — `PARTIAL` یا `UNKNOWN` باید Dependent Effectful Work را تا Reconciliation، Competent Decision و Recovery کنترل‌شده Block کند.
P03-PROC-003 — مسیر اجباری Outcome نامعلوم:
`STOP → PRESERVE EVIDENCE → INSPECT STATE → CHECK IDEMPOTENCY → RECONCILE → CLASSIFY EFFECT → COMPETENT DECISION → CONTROLLED RECOVERY → OUTCOME RECORD`
P03-DEN-018 — Lost Receipt، Timeout، Client Disconnect، Callback Failure یا Unknown Tool State مجوز Blind Retry، Success Assumption یا Duplicate Effect نیست.
## 11. Idempotency، Ordering، Concurrency و Replay Protection
P03-REQ-012 — هر Command اثرگذار و هر Query نیازمند Retry-safe Semantics باید Idempotency Scope، Key، RequestDigest، Retention Window، Outcome/Reconciliation Behavior و Conflict Rule صریح داشته باشد.
P03-CON-040 — Same Idempotency Key + Same Normalized RequestDigest باید Prior Status/Receipt/Outcome را برگرداند یا Safe Reconciliation را ادامه دهد؛ نباید Effect متمایز جدیدی ایجاد کند.
P03-CON-041 — Same Idempotency Key + Different RequestDigest برابر `IDEMPOTENCY_CONFLICT` است و باید Fail Closed شود.
P03-CON-042 — Optimistic Concurrency باید از Expected Revision/Digest استفاده کند. Conflict نباید با Last-write-wins پنهان، Silent Overwrite یا حذف Preconditions حل شود.
P03-CON-043 — عملیاتی که Serialization لازم دارند باید Ordering Key، Ordering Scope، Partition/Target Boundary و Out-of-order Behavior تعریف کنند. Global Ordering بدون Evidence نباید ادعا شود.
P03-CON-044 — At-least-once Delivery خط پایۀ Claim است مگر Semantics قوی‌تر End-to-End با Evidence اثبات شود. Exactly-once Label در یک Broker یا SDK اثبات Exactly-once Outcome نیست.
P03-CON-045 — Deduplication نباید Correction، Compensation، Reconciliation، Supersession یا Evidence Event متمایز را حذف کند.
P03-CON-046 — Replay Protection باید Actor/Workload، Tenant، Purpose، Target، Operation، RequestDigest، Nonce، Validity Window، Idempotency Context و Lease Consumption را Bind کند.
P03-CON-047 — Retry فقط برای Failure صریحاً Retryable، در Deadline و Attempt Bound، با Backoff/Jitter Policy و Cost/Rate/Risk Limits معتبر مجاز است. Retry Authority جدید ایجاد نمی‌کند.
P03-FAIL-013 — Ordering Violation، Revision Conflict، Duplicate with Different Digest، Reused Nonce، Expired Lease یا Replay Context نامعتبر باید Effect را Block و Evidence مناسب ایجاد کند.
P03-FAIL-014 — اگر Semantics تحویل، Deduplication، Ordering یا Retry در End-to-End Path نامعلوم است، Claim باید `AT_LEAST_ONCE_OR_INDETERMINATE` باقی بماند و طراحی نباید Outcome یکتا را فرض کند.
## 12. Long-running Operation Contract
P03-REQ-013 — کار Long-running باید یک OperationResource پایدار با Identity، Version، RequestDigest، Owner/Tenant، State، Timestamps، Progress Evidence، Dependencies، Approval Wait، Receiptها، Cancellation State و Outcome Reference داشته باشد.
State Projection پایه:
`ACCEPTED → QUEUED → RUNNING → WAITING_APPROVAL|WAITING_DEPENDENCY → SUCCEEDED|FAILED|PARTIAL|CANCELLED|UNKNOWN`
P03-CON-048 — هر State Transition باید Event جدا مطابق P01 تولید کند و به Operation Identity، Prior State، Trigger، Actor/Service، Causation و Evidence Bind شود.
P03-CON-049 — Polling، Callback و Event Consumption فقط Projectionهای متفاوت روی همان Operation Identity هستند. Callback Delivery، Subscription، Poll Token یا Webhook Signature Authority تازه ایجاد نمی‌کند.
P03-CON-050 — `SUCCEEDED` فقط زمانی مجاز است که Receipt و Validation متناسب با Acceptance Rule همان Operation موجود باشد. Queue Completion، Worker Exit Code یا 100% Progress به‌تنهایی Success نیست.
P03-CON-051 — Transition Legality، Human Checkpoint، Pause/Resume و Workflow Compensation در P04 تعریف می‌شود؛ این Part فقط State Semantics و Invocation Link را حفظ می‌کند.
P03-DEN-019 — Operation State نباید از درصد پیشرفت، آخرین Log Line، Model Confidence، Majority Vote یا Absence of Error استنتاج شود.
P03-FAIL-015 — `WAITING_APPROVAL` یا `WAITING_DEPENDENCY` بدون Approval/Dependency معتبر نباید به Running منتقل شود. Expiry یا Revocation باید State را Block/Fail متناسب کند.
P03-FAIL-016 — `CANCELLED` به معنی Rollback یا No Effect نیست. اگر Attempt ممکن است Commit شده باشد، Effect State تا Reconciliation `UNKNOWN` باقی می‌ماند.
## 13. Error Contract و Retryability
P03-REQ-014 — هر Failure Response باید Contract زیر را داشته باشد:
~~~yaml
error_id:
error_code:
category: VALIDATION|AUTHENTICATION|AUTHORIZATION|APPROVAL|POLICY|SCIENTIFIC|CONFLICT|RATE|COST|RISK|DEPENDENCY|INTEGRITY|INTERNAL|PROHIBITED
message_safe:
retryability: NEVER|AFTER_BACKOFF|AFTER_CHANGE|AFTER_APPROVAL|AFTER_RECONCILIATION|UNKNOWN
field_violations: []
current_state_reference:
evidence_reference:
correlation_id:
~~~
P03-CON-052 — Retryability Semantics:
| Value | معنای محدود |
|---|---|
| `NEVER` | همان Request نباید Retry شود |
| `AFTER_BACKOFF` | فقط همان Digest، در Bound و Deadline معتبر، پس از Delay کنترل‌شده |
| `AFTER_CHANGE` | Input/Precondition باید اصلاح و Request/Digest جدید ساخته شود |
| `AFTER_APPROVAL` | فقط پس از Approval/Lease دقیق و تازه؛ Approval خودکار ساخته نمی‌شود |
| `AFTER_RECONCILIATION` | ابتدا Outcome/Effect نامعلوم تعیین شود |
| `UNKNOWN` | Retry ممنوع تا Classification صلاحیت‌دار |
P03-CON-053 — Error Message باید Safe، Machine-readable و Traceable باشد و Secret، Credential، Internal Topology، Security Control Detail غیرضروری یا Cross-tenant Existence را افشا نکند.
P03-CON-054 — Error Code، Category و Retryability باید با Effect State و Reconciliation Status سازگار باشند. Internal Error نباید Failure مادی را به Client Fault تبدیل یا Receipt احتمالی را حذف کند.
P03-REQ-015 — Hard Failureهای حداقلی:
- `EFFECT_UNKNOWN`
- `APPROVAL_MISSING_OR_MISMATCHED`
- `POLICY_INDETERMINATE`
- `TARGET_SCOPE_EXCEEDED`
- `SCIENTIFIC_CONTEXT_INCOMPLETE`
- `IDEMPOTENCY_CONFLICT`
- `OUTCOME_RECONCILIATION_REQUIRED`
- `COMMAND_PATH_PROHIBITED`
P03-DEN-020 — خطا نباید با Empty Success، Default Value، Stale Cache، Silent Downgrade، Automatic Approval یا Generic `200/OK` پنهان شود.
P03-FAIL-017 — اگر Retryability، Effect State یا Current State نامعلوم است، Error باید `UNKNOWN` یا `AFTER_RECONCILIATION` باقی بماند؛ Retry خوش‌بینانه ممنوع است.
## 14. Versioning، Compatibility و Deprecation
P03-REQ-016 — هر Contract باید Schema ID، Schema Version، Semantic Version Rule، Critical Field Set، Compatibility Matrix، Translation Profile، Deprecation Record و Consumer Evidence صریح داشته باشد.
P03-CON-055 — Backward/Forward Compatibility باید Field-by-field و Semantics-by-semantics تعریف شود؛ Parser Success، Optional Field یا Transport Compatibility اثبات Contract Compatibility نیست.
P03-CON-056 — Unknown Critical Field یا Unsupported Critical Enum باید Reject شود. Ignore کردن Fieldهای Effect، Identity، Tenant، Purpose، Time، Frame، Unit، Covariance، Approval، Policy، Provenance، Classification یا Digest ممنوع است.
P03-CON-057 — Scientific Identity، Time، Frame، Unit، Covariance، Effect، Approval و Provenance فقط با Translation Lossless و Independently Verified قابل‌نگاشت‌اند. Translation نامعلوم برابر `INCOMPATIBLE_OR_INDETERMINATE` است.
P03-CON-058 — Deprecation باید Owner، Reason، Replacement، Announcement/Observation Window، Deadline، Consumer Inventory، Migration Evidence، Rollback/Coexistence Rule و Removal Gate داشته باشد.
P03-CON-059 — Breaking Change یک Major Contract جدید، Compatibility/Coexistence Plan، Migration، Consumer Qualification و Approval تازه می‌خواهد. Silent In-place Rewrite ممنوع است.
P03-CON-060 — Capability Negotiation باید Exact Version منتخب و Lost/Unsupported Semantics را ثبت کند. Client Capability نمی‌تواند Security، Authority، Evidence یا Scientific Requirement را کاهش دهد.
P03-DEN-021 — `latest`، Mutable Alias، Implicit Default Version، Silent Fallback، Silent Downgrade یا «Best Effort» برای Critical Qualified Path ممنوع است.
P03-FAIL-018 — اگر Mapping دو Version Critical Semantics را Lossless حفظ نمی‌کند یا Evidence Compatibility ناقص است، Request باید Reject یا به Explicit Non-qualified Path محدود شود؛ Qualified Success ممنوع است.
P03-PROC-004 — Removal یک Version فقط پس از Inventory Consumerها، Evidence مهاجرت، پایان Window، Review Impact، Approval دقیق و Immutable Deprecation Record مجاز است. این Part هیچ Removalی را اجرا نمی‌کند.
## 15. Security، Tenant، Purpose، Risk، Cost و Evidence Implications
P03-CON-061 — Admission باید پیش از Work پرهزینه یا حساس، Authentication، Tenant، Purpose، Classification، Environment، Rate، Quota، Deadline، Payload Bound، Egress، Risk، Cost Reservation و Policy را ارزیابی کند.
P03-CON-062 — Cross-tenant Access به‌طور پیش‌فرض Deny است. Tenant Claim Client کافی نیست و Existence، Cursor، Error، Cache، Trace یا Timing نباید Data Tenant دیگر را افشا کند.
P03-CON-063 — Export و External Egress باید Capability تایپ‌شده، Destination/Recipient دقیق، Data Manifest، Classification، Purpose، Residency/Transfer Rule، Approval، Cost/Risk Bound و Receipt مستقل داشته باشند.
P03-CON-064 — AI/Model Output فقط می‌تواند Proposal، Draft، Recommendation یا Candidate Payload ایجاد کند. Server باید آن را Canonicalize، Validate، Reclassify و تحت Policy قرار دهد؛ Model حق Approval، Lease Issuance یا Direct Execution ندارد.
P03-CON-065 — Request، Error، Receipt، Event، Log و Evidence باید Data Minimization و Protected Reference را رعایت کنند. Raw Secret یا Credential هرگز Evidence لازم محسوب نمی‌شود.
P03-CON-066 — Cost Unknown برابر Zero Cost نیست و Risk Unknown برابر Low Risk نیست. نبود Budget، Reservation، Cost Owner، Appetite/Tolerance/Capacity یا Acceptance Authority باید Effect مربوط را Block کند.
P03-CON-067 — Evidence باید Request، Policy Decision، Approval، Lease، Attempt، Receipt، Reconciliation و Outcome را به‌صورت Recordهای جدا و Link‌شده حفظ کند. Audit Log به‌تنهایی Truth یا Outcome نیست.
P03-DEN-022 — هیچ API نباید امکان Disable/Suppress کردن Audit، Evidence، Security، Risk، Cost یا Command-denial Control را از مسیر Generic، Self-service یا Self-approved فراهم کند.
P03-DEN-023 — AI، Agent، Workflow، Plugin، SDK یا Client نمی‌تواند Actor Identity، Competence، Tenant، Purpose، Effect، Risk Acceptance، Budget Authority یا Approval را خوداظهاری و قطعی کند.
P03-FAIL-019 — Policy Result نامعلوم، Cross-tenant Ambiguity، Classification Conflict، Unbounded Cost، Unaccepted Risk، Missing Evidence Plan یا Security Control Failure نتیجه `DENY / BLOCK / INDETERMINATE` دارد.
## 16. Event Integration بدون بازتعریف Base Envelope
P03-CON-068 — تمام Eventهای API Lifecycle باید Base Canonical Event Envelope متعلق به P01 و Extension Profileهای Applicable آن را مصرف کنند. این Part هیچ Field پایه را Rename، Replace یا Duplicate نمی‌کند.
P03-CON-069 — حداقل Factهای متمایز موردنیاز، در صورت وقوع و Applicability:
- Request received/rejected؛
- Policy decision recorded؛
- Approval linked/rejected/expired؛
- Execution lease issued/revoked/consumed؛
- Attempt started/finished؛
- Receipt recorded؛
- Reconciliation started/completed؛
- Outcome validated؛
- Correction، Compensation یا Supersession recorded.
هر Fact باید Event Type و Payload Schema تایپ‌شده داشته باشد و Record دیگر را جایگزین نکند.
P03-CON-070 — `command_id`، `approval_reference`، `correlation_id`، `causation_id`، `trace_id`، `workflow_id`، `ordering_key` و `idempotency_key` طبق Applicability Contract P01 استفاده می‌شوند.
P03-CON-071 — Event Delivery خط پایۀ At-least-once دارد. Consumer باید Duplicate، Out-of-order، Unsupported Version و Invalid Event را مدیریت و State Transition را Validate کند.
P03-CON-072 — Event Consumer مجاز نیست صرف دریافت Event، Action را اجرا کند. هر Effect جدید نیازمند Application Command تازه، Server-side Classification، Policy، Approval و Lease مستقل است.
P03-DEN-024 — Event، Callback، Webhook، Queue Message یا Subscription نباید Command، Approval، Lease یا Outcome تلقی شود؛ Topic/Route Name نیز این مرز را تغییر نمی‌دهد.
P03-FAIL-020 — اگر Publication Event پس از Commit ناموفق شود، Outcome گذشته حذف یا Retry Blind نمی‌شود. Canonical State/Outbox/Evidence باید حفظ و Delivery طبق Recovery Contract P01 Reconcile شود.
## 17. اتصال به Workflow و Capability بدون Escape Hatch
P03-CON-073 — P04 مالک Workflow State Machine، Human Checkpoint، Pause/Resume، Escalation، Compensation و Illegal Transition است. P03 فقط Record و Invocation Semantics لازم برای آن را فراهم می‌کند.
P03-CON-074 — P08 مالک Capability Descriptor، Registration، Broker، Adapter، Tool و Plugin Lifecycle است. هر Capability اثرگذار باید یک یا چند Application Command تایپ‌شده، Target-bound، Policy-bound و Evidence-bound ارائه کند.
P03-CON-075 — یک Capability Reference باید Identity، Version، Digest/Descriptor Reference، Supported Operation، Input/Output Schema، Effect Ceiling، Environment/Data Boundary، Timeout، Idempotency، Evidence و Revocation State قابل‌حل داشته باشد؛ جزئیات Canonical Descriptor در P08 تعریف می‌شود.
P03-CON-076 — Sync Response، Async Operation، Batch، Callback و Event-driven Invocation باید به همان RequestDigest، Operation Identity، Receipt و Outcome Chain نگاشت شوند. تغییر Transport مجوز تغییر Semantics نیست.
P03-DEN-025 — Workflow، Plugin، Adapter یا Tool حق ندارد با Nested Call، Generic Parameter، Dynamic Route، Hidden Callback، Archived Version یا Human Mediation ممنوعیت Arbitrary Execution یا `E9` را دور بزند.
P03-FAIL-021 — اگر Capability Identity/Version، Effect Ceiling، Target Scope، Input/Output Schema، Adapter Behavior یا Transitive Tool Chain نامعلوم باشد، Invocation باید `CAPABILITY_INDETERMINATE — DO_NOT_EXECUTE` شود.
## 18. رفتار Failure، Unknown، Degraded و Recovery
P03-FAIL-022 — تمام حالت‌های `UNKNOWN`، `MISSING`، `STALE`، `CONFLICTED`، `INVALID`، `PARTIAL`، `NON_CONVERGED` یا `INDETERMINATE` باید حفظ شوند و هرگز به Complete، Success، Ready، Approved یا Safe تبدیل نشوند.
P03-CON-077 — Degraded Read-only Mode فقط برای Queryهایی مجاز است که Source Authority، Freshness، Tenant، Classification، Security و Resource Bounds معتبر باقی مانده‌اند. Stale/Partial Result باید صریح برچسب بخورد.
P03-DEN-026 — Degraded Mode، Emergency، Break-glass یا Incident Mode نمی‌تواند Command را به Query تبدیل، Approval را حذف، Effect را کاهش یا مسیر `E9` را فعال کند.
P03-CON-078 — Recovery باید Request، Attempt، Receipt، Failure، Evidence، External Reference، Correction و Outcome History را حفظ کند. Rollback یا Compensation مجوز Silent Rewrite گذشته نیست.
P03-FAIL-023 — اگر Executor پس از Lease Issuance Unavailable شود و Evidence عدم Attempt قطعی نباشد، State نباید Success یا Safe-to-retry فرض شود؛ Reconciliation لازم است.
P03-FAIL-024 — اگر Schema Registry، Policy Service، Identity، Approval Record، Lease Validation، Evidence Store یا Target State قابل‌اعتماد در دسترس نباشد، Effectful Request Fail Closed می‌شود. Availability Pressure مجوز Fail Open نیست.
P03-FAIL-025 — اگر Command-path Prohibition نقض یا مسیر قابل‌استفاده‌ای به Spacecraft Command/Uplink کشف شود:
`HARD_STOP → DISABLE/ISOLATE PATH → PRESERVE EVIDENCE → INC-0 → INDEPENDENT REVIEW → REMOVE PATH`
هیچ Approval، Waiver یا Recovery برای فعال نگه‌داشتن آن در CSIP-EO وجود ندارد.
## 19. Verification Requirements و Part-level Acceptance
P03-REQ-017 — Verification آینده برای این Contract باید حداقل شامل موارد زیر باشد:
1. Schema و Semantic Conformance؛
2. Property-based و Boundary Tests؛
3. Idempotency، Duplicate، Replay، Ordering و Concurrency Tests؛
4. Timeout، Cancellation، Lost Receipt و Out-of-order Tests؛
5. Authentication، Authorization، Approval و Confused-deputy Tests؛
6. Cross-tenant، Purpose و Classification Tests؛
7. Contract Downgrade، Unknown Critical Field و Version Translation Tests؛
8. Partial/Unknown-effect Reconciliation Tests؛
9. Scientific-field Losslessness Tests؛
10. Exhaustive Negative Tests برای Generic Execution و Spacecraft-command Path.
P03-CON-079 — P13 مالک Test Design، Oracle، Dataset، Threshold، Equivalence، Qualification و Assurance است. این Part فقط Claim/Contractهای قابل‌Verification را تحویل می‌دهد.
P03-DEN-027 — هیچ Test، Benchmark، Simulation، Integration، Penetration Test، Qualification یا Independent Verification توسط این Prompt Part اجرا نشده است؛ بنابراین هیچ Pass، Coverage، Performance، Security یا Production-readiness Claim مجاز نیست.
P03-REQ-018 — Acceptance این Part برای Assembly فقط وقتی قابل‌پیشنهاد است که:
1. Header، Anchor، Footer و Pointerها کامل باشند؛
2. Semantic Owner ID/Version/Status/Digest دقیق باشد؛
3. تمام ۱۰ مؤلفۀ اجباری Part 03 در Architecture Contract پوشش داده شوند؛
4. Global Invariant Capsule بدون Drift حاضر باشد؛
5. Query/ApplicationCommand/Event/Approval/Receipt/Outcome جدا بمانند؛
6. P01 Event Envelope و P05 Authority Taxonomy بازتعریف نشوند؛
7. Generic Execution و Spacecraft-command Path صریحاً Deny شوند؛
8. Decisionهای RS17 فقط `PROPOSED` گزارش شوند؛
9. Open Issueها و Historical Limitation پنهان نشوند؛
10. هیچ Implementation، Test، Spend، Deployment یا Freeze مجاز یا ادعا نشود.
P03-PROC-005 — Part-level Audit باید Source Binding، Clause ID Uniqueness، Fence Closure، Anchor Uniqueness، Required Section Coverage، Decision Projection، Open Issue Preservation و Prohibited-path Negative Scan را بررسی کند.
P03-FAIL-026 — Missing Evidence، Unclosed Fence، Duplicate Clause ID، Truncation، Status Drift، Owner Redefinition یا Prohibited Authority Expansion نتیجه `REWORK_REQUIRED / PART_NOT_ACCEPTED` دارد.
## 20. Traceability، Decision Projection و Open Issueها
### 20.1 مالکیت و مصرف Requirementهای بحرانی
P03-CON-080 — این قسمت مالک اصلی Requirementهای زیر است:
- `CGR-REQ-007` — جداسازی Query، Application Command، Event، Recommendation، Decision، Approval، Authorization، ExecutionLease، Receipt و Outcome؛ Consumerهای اصلی: P04، P08 و P15.
- `CGR-REQ-008` — Application Command تایپ‌شده و محدود و ممنوعیت Arbitrary/Untyped Action؛ Consumerهای اصلی: P08 و P11، با Negative Verification در P13.
P03-CON-081 — این قسمت Requirementهای زیر را مصرف می‌کند و حق تعریف رقیب ندارد:
- `CGR-REQ-002` از P01 — ممنوعیت دائمی Spacecraft Command/Uplink؛
- `CGR-REQ-011` از P05 — Actual/Transitive Effect Truth؛
- `CGR-REQ-012` از P05 — Approval Class و Exact Binding؛
- `CGR-REQ-015` از P05 — Fail-closed Intersection محورهای Authority؛
- `CGR-REQ-016` از P01 — Base Canonical Event Envelope؛
- `CGR-REQ-018` از P01 — Timestamp تایپ‌شده و Time-scale Explicit؛
- `CGR-REQ-022` از P13 — Traceability و Orphan Detection؛
- `CGR-REQ-034` از P02 — استقلال Lifecycle Gateها.
P03-CON-082 — Clauseهای مادی این Part از الگوی زیر استفاده می‌کنند:
`P03-{INV|REQ|DEF|CON|PROC|DEN|FAIL|DEC|OI}-nnn`
هر Trace Record باید Source Artifact، Version، Section، Digest، Status، Supporting Source، Consumer Part، Conflict Status و Compression Operation را حفظ کند.
### 20.2 Decision Projectionهای Source
Decisionهای زیر Projection مستقیم `CSIP-EO-RS-STAGE-17` هستند؛ Historical Decision نیستند و همگی `PROPOSED` باقی می‌مانند:
P03-DEC-001 — `RS17-DEC-001`: Protocol Neutrality؛ Canonical Semantics مستقل از HTTP/RPC/Event Protocol — Status: `PROPOSED`.
P03-DEC-002 — `RS17-DEC-002`: Semantic Separation؛ Query، Command، Event، Approval، Execution و Outcome جدا هستند — Status: `PROPOSED`.
P03-DEC-003 — `RS17-DEC-003`: Server-side Effect Truth؛ Client/Model نمی‌تواند Effect یا Classification را کاهش دهد — Status: `PROPOSED`.
P03-DEC-004 — `RS17-DEC-004`: Digest-bound Requests؛ Policy، Approval و Lease به Request نرمال‌شدۀ دقیق Bind می‌شوند — Status: `PROPOSED`.
P03-DEC-005 — `RS17-DEC-005`: Idempotency Model؛ Same Key/Same Digest و Conflict Fail-closed — Status: `PROPOSED`.
P03-DEC-006 — `RS17-DEC-006`: Unknown Outcome؛ Reconciliation پیش از Retry یا Dependent Effect — Status: `PROPOSED`.
P03-DEC-007 — `RS17-DEC-007`: Compatibility؛ Critical Semantics نیازمند Lossless Verified Mapping است — Status: `PROPOSED`.
P03-DEC-008 — `RS17-DEC-008`: Generic Actions؛ Arbitrary/Untyped Execution Endpoint ممنوع است — Status: `PROPOSED`.
P03-DEC-009 — `RS17-DEC-009`: Error Model؛ Failureها Machine-readable، Safe و Retry-explicit هستند — Status: `PROPOSED`.
P03-DEC-010 — `RS17-DEC-010`: Command Boundary؛ هیچ Spacecraft-command Schema، Route یا Adapter وجود ندارد — Status: `PROPOSED`.
P03-DEN-028 — وجود `P03-DEC-*` یا `RS17-DEC-*` در این Prompt Part به معنی Approval جدید، Historical Recovery، Normative Activation یا Implementation Decision نیست.
### 20.3 Open Issueهای اجباری
- `P03-OI-001` — Bytes، Title قطعی، Version، Decisionها و Approval تاریخی `CSIP-EO-STAGE-17` بازیابی نشده‌اند.
- `P03-OI-002` — `CSIP-EO-RS-STAGE-17` هنوز Successor Normative تصویب‌شده نیست و نمی‌تواند `OI-32-003` را ببندد تا Exact Digest آن مستقلاً بررسی، به‌عنوان Successor تازه تصویب و در Successor Manifest ثبت شود.
- `P03-OI-003` — Exact Protocol Mapping، Framework، Transport، Serialization و SDK انتخاب نشده‌اند.
- `P03-OI-004` — Canonicalization/Serialization Profile و Algorithm دقیق برای Cross-implementation RequestDigest هنوز انتخاب و Qualified نشده است.
- `P03-OI-005` — P04 Workflow/Human-control Contract و P05 Authority Taxonomy در Parts بعدی دریافت می‌شوند و این Part حق پیش‌تصویب آن‌ها را ندارد.
- `P03-OI-006` — P08 Capability، P11 Security و P13 Verification باید این Contract را مصرف و Validate کنند؛ Implementation Evidence وجود ندارد.
- `P03-OI-007` — Full machine-readable Trace Graph برای تمام Clauseها و Consumer Edgeها هنوز تکمیل و Validate نشده است.
- `P03-OI-008` — Ownerهای واقعی سازمانی، Provider، Region، Workload، Budget، Threshold، Rate، Quota، SLO، RPO، RTO و Risk Acceptance Authority تا Evidence معتبر `UNKNOWN` هستند.
- `P03-OI-009` — `CSIP-EO-RS-STAGE-20` همچنان `DOMAIN_REVIEW_REQUIRED` است.
- `P03-OI-010` — Stage 32 همچنان `PROPOSED` است و Project Specification Freeze اجرا نشده است.
P03-CON-083 — هیچ Part، Summary، Model، Agent، Review یا Assembly Acceptance حق ندارد Open Issueهای فوق را فقط به دلیل کامل‌بودن متن ببندد.
## 21. Anti-claimها و تفسیرهای ممنوع
این Part و دریافت، Review یا پذیرش آن برای Assembly هیچ‌یک از ادعاها یا مجوزهای زیر را ایجاد نمی‌کند:
- بازیابی Historical Stage 17؛
- تصویب یا Normative Activation منبع `CSIP-EO-RS-STAGE-17`؛
- Approval تصمیم‌های `RS17-DEC-001..010`؛
- انتخاب HTTP، REST، GraphQL، gRPC، Protobuf، OpenAPI، Broker، SDK یا Vendor؛
- ایجاد API، Endpoint، Route، Schema Registry، Service، Queue، Topic، Database یا Infrastructure؛
- اجرای Query یا Application Command واقعی؛
- صدور Policy Decision، Approval، Authorization یا ExecutionLease؛
- اجرای Test، Benchmark، Build، Migration، Release، Deployment، Pilot، Production یا Operation؛
- اثبات Idempotency، Exactly-once، Compatibility، Security، Performance یا Availability؛
- Spend، Procurement، External Egress، Data Transfer یا Risk Acceptance؛
- Legal Compliance، Certification، Qualification یا Production Readiness؛
- تصویب علمی Stage 20؛
- تصویب Stage 32 یا اجرای Project Specification Freeze؛
- ایجاد هر مسیر Spacecraft Command، Telecommand، Uplink، Flight Control یا Autonomous Maneuver Execution.
P03-DEN-029 — واژۀ `Command` بدون قید در این Part نباید خارج از تعریف `Application Command زمینی` تفسیر شود. هر تفسیر فرمان فضایی با مرز پروژه تعارض دارد.
P03-DEN-030 — واژۀ `Canonical` در نام Envelope یا Contract به معنی Implemented، Verified، Approved، Normative یا Frozen نیست؛ فقط هویت طراحی پیشنهادی Source-bound را نشان می‌دهد.
P03-DEN-031 — `REVIEW_READY` مساوی Reviewed، Accepted یا Approved نیست. `PART_ACCEPTED_FOR_ASSEMBLY` نیز Approval منبع یا مجوز Implementation نیست.
P03-DEN-032 — هیچ Consumer Part، Adapter، Fork، Archive، Successor، Plugin، Human-mediated Process یا External Service حق ندارد با تعریف Alias یا مسیر جایگزین، Hard Denialهای این Part را دور بزند.
## 22. تحویل به قسمت بعدی و وابستگی‌ها
P03-CON-084 — Parts پایین‌دست باید این Contract را چنین مصرف کنند:
- P04 — Workflow Stateها و Human Checkpointها را روی Recordهای جدا و Digest-bound بنا کند؛
- P05 — Effect/Approval/Permission/Autonomy Taxonomy دقیق را تعریف کند، بدون ادغام محورهای P03؛
- P08 — Capabilityها، Pluginها و Adapterها را فقط از طریق Invocation تایپ‌شده و محدود ارائه کند؛
- P09 — Query Projection و Persistence را بدون ارتقای Projection به Truth پیاده‌سازی‌پذیر سازد؛
- P11 — Authentication، Authorization، Tenant، Purpose، Data و Egress Control را اعمال کند؛
- P12 — Telemetry و SLIها را بدون تبدیل Receipt به Outcome اندازه‌گیری کند؛
- P13 — Contract، Negative-path، Reconciliation و Command-denial Verification را تعریف کند؛
- P15 — Change/Release Automation را به همین Approval/Lease/Receipt/Outcome Separation Bind کند؛
- P18 — Trace، Conflict و Open Issueها را Compile کند و Definition این Part را بازنویسی نکند.
P03-CON-085 — Part بعدی مورد انتظار:
- Part ID: `CSIP-EO-FMSP-P04`
- Part Index: `04 of 18`
- Title: `Workflow, Process and Human-Control Contract | قرارداد Workflow، Process و کنترل انسانی`
- Semantic Owner: `CSIP-EO-RS-STAGE-18`
- Semantic Owner Version: `0.1.0-reconstituted-draft`
- Semantic Owner Status: `RECONSTITUTED_DRAFT — REVIEW_READY — NOT_APPROVED — NOT_FROZEN`
- Semantic Owner SHA-256: `98c58b2fc8fe56e0d84f39c901421642d8b8b525c18979b9a1b2aaee25c5d75b`
- Receive Mode: `CONTEXT_ONLY`
- Action Authority during reception: `NONE`
P03-REQ-019 — Part 04 باید در پیام جداگانه و فقط پس از تصمیم صریح کاربر ارسال شود. تا آن زمان محتوای آن را حدس نزن، Stage 18 را آغاز نکن و در وضعیت انتظار باقی بمان.
P03-REQ-020 — پس از دریافت سالم این قسمت، تنها پاسخ مجاز متن ثابت زیر است و هیچ عبارت دیگری نباید قبل یا بعد از آن قرار گیرد:
~~~text
قسمت ۰۳ از ۱۸ ابرپرامپت نهایی CSIP-EO با موفقیت دریافت و ثبت شد.
هیچ تحلیل، طراحی جدید، پیاده‌سازی یا اقدام اجرایی آغاز نمی‌شود.
منتظر قسمت ۰۴ هستم.
~~~
RECEIVER_MUST_WAIT_FOR_NEXT_PART: TRUE
PART_DECLARED_COMPLETE: TRUE
NEXT_EXPECTED_PART: P04
RECEPTION_ACTION: ACK_ONLY
<<<CSIP-EO-FMSP-18P|0.9.0-draft|P03|END>>>