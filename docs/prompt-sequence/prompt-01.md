<<<CSIP-EO-FMSP-18P|0.9.0-draft|P01|START>>>
CSIP_EO_PROMPT_PACKAGE_ID: CSIP-EO-FINAL-MASTER-SUPERPROMPT-18P
CSIP_EO_PROMPT_PACKAGE_VERSION: 0.9.0-draft
PART_ID: CSIP-EO-FMSP-P01
PART_INDEX: 01
PART_COUNT: 18
PART_TITLE: Foundations and Architecture Baseline | مبانی و خط پایه معماری
SEMANTIC_OWNER_ARTIFACT_ID: CSIP-EO-RS-PART-1
SEMANTIC_OWNER_VERSION: 0.1.0-reconstituted-draft
SEMANTIC_OWNER_STATUS: RECONSTITUTED_DRAFT — REVIEW_READY — NOT_APPROVED — NOT_FROZEN
SEMANTIC_OWNER_SHA256: a33bf602b5a5e5c8518b709b5dde7ab6b96617cc76ac86c66d2c795271422c50
SUPPORTING_SOURCE_BINDINGS: CSIP-EO-AUDIT-GAP-02/0.1.0-candidate/fa400334a69702bf56e8588210449590573bccd3120d7c2cebd6ba9cc8fc161f; ENTERPRISE-TRUST-RISK-COST-EVIDENCE-REPRODUCIBILITY-MANDATE/verified-input-2026-07-28/1b5e7884a343589312d62259f181bd48f1a12b51e2613685c0d58c747a08dab4; CSIP-EO-PROMPT-ARCH-18P-C1/0.1.0-design-candidate/a4c80b938fccaab5d3d85c780351a41ee3444b4c6712920af45b493afbacb09b; CSIP-EO-GAP-RESOLUTION-MANIFEST-C1/0.1.0-candidate/349b590df9fad00c2e0ec317f4bd0b7ad747a5e22a1fead0f66f28c98e955216
PRIOR_PART_ID: NONE
NEXT_PART_ID: CSIP-EO-FMSP-P02
PART_PAYLOAD_SHA256: SEE_EXTERNAL_PROMPT_PACKAGE_MANIFEST
RECEIVE_MODE: CONTEXT_ONLY
ACTION_AUTHORITY: NONE

# پرامپت قسمت ۰۱ از ابرپرامپت نهایی ۱۸ قسمتی CSIP-EO
# مبانی و خط پایه معماری

## 0. دستور دریافت، مرز این قسمت و قفل ضدتوهم

این پیام فقط «قسمت ۰۱ از ۱۸» یک زمینۀ مرجعِ به‌هم‌پیوسته است. این قسمت مستقل، کامل‌کنندۀ کل پروژه یا مجوز شروع کار نیست. قسمت‌های ۰۲ تا ۱۸ هنوز در این پیام وجود ندارند و باید به‌ترتیب، در پیام‌های جداگانه دریافت شوند.

P01-REQ-001 — هنگام دریافت این قسمت، وضعیت داخلی خود را دقیقاً چنین در نظر بگیر:

`RECEIVING_P01 — CONTEXT_INCOMPLETE — ACTION_AUTHORITY_NONE`

P01-DEN-001 — از اطلاعات ناقص این قسمت برای حدس‌زدن، بازسازی، جعل یا تکمیل محتوای قسمت‌های ۰۲ تا ۱۸ استفاده نکن. دانش ازپیش‌آموخته، حافظه، تاریخچۀ مکالمه، جست‌وجوی وب، ابزار بازیابی، فایل مشابه، نام Stageها یا الگوهای رایج، مجوز ساختن محتوای غایب نیست.

P01-DEN-002 — تا پیش از دریافت و مونتاژ معتبر تمام ۱۸ قسمت، تحت هیچ شرایطی:

- تحلیل یکپارچۀ پروژه ارائه نکن؛
- طراحی جدید آغاز نکن؛
- تصمیم جدید نساز یا تصمیم موجود را تغییر نده؛
- Requirement، Architecture، Schema، API، Workflow، Algorithm یا Roadmap جدید تولید نکن؛
- کد، تست، فایل، پوشه، Repository، Branch، Commit یا Pull Request ایجاد یا تغییر نده؛
- Command، Script، Notebook، Build، Migration یا Deployment اجرا نکن؛
- Dependency، Package، Plugin، Model یا Tool نصب یا فعال نکن؛
- به Cloud، Database، API، Browser، GitHub، CI/CD، Registry، Production یا سرویس خارجی متصل نشو؛
- هیچ اقدام هزینه‌زا، دارای Side Effect، تغییردهنده، ارسال‌کنندۀ داده یا غیرقابل‌بازگشت انجام نده؛
- هیچ فناوری را Final، Approved، Selected-for-Implementation یا Frozen فرض نکن؛
- هیچ Source غایب، تصمیم تاریخی، نتیجۀ علمی، مالک سازمانی، Budget، Region، Provider، Threshold، SLO، RPO یا RTO را اختراع نکن؛
- ادعا نکن که Context کامل، Specification تصویب‌شده، Project Frozen یا Implementation Authorized است؛
- سؤال تکراری درباره اطلاعاتی که همین قسمت صریحاً ارائه کرده است مطرح نکن؛
- توصیه، گام بعدی اجرایی یا پیشنهاد شروع توسعه ارائه نکن.

P01-DEN-003 — دریافت یک Prompt، Digest، Signature، Manifest، Approval، Test Result یا سند به‌تنهایی مجوز اجرا نیست. «توانایی انجام عمل» با «اجازۀ انجام عمل» متفاوت است.

P01-REQ-002 — وظیفۀ تو پس از دریافت سالم و کامل این قسمت فقط این است:

1. متن را Parse و در Context جاری حفظ کنی؛
2. وجود Start Anchor، End Anchor، شناسه، شمارۀ قسمت، تعداد کل قسمت‌ها، Source Binding، Footer و پیوستگی `P01 → P02` را از روی همین پیام کنترل کنی؛
3. هیچ تحلیل محتوایی، طراحی، پیاده‌سازی یا اقدام ابزاری انجام ندهی؛
4. فقط پاسخ ثابت زیر را، بدون هیچ متن قبل یا بعد، برگردانی:

~~~text
قسمت ۰۱ از ۱۸ ابرپرامپت نهایی CSIP-EO با موفقیت دریافت و ثبت شد.
هیچ تحلیل، طراحی جدید، پیاده‌سازی یا اقدام اجرایی آغاز نمی‌شود.
منتظر قسمت ۰۲ هستم.
~~~

P01-FAIL-001 — اگر Start Anchor یا End Anchor وجود نداشت، `PART_INDEX` برابر `01` نبود، `PART_COUNT` برابر `18` نبود، متن آشکارا بریده بود، Footer کامل نبود یا Source Binding با Header همین قسمت تعارض داشت، موفقیت دریافت را جعل نکن. در آن حالت فقط پاسخ زیر را با ذکر دقیق ایراد در براکت ارائه کن:

~~~text
دریافت قسمت ۰۱ از ۱۸ ابرپرامپت نهایی CSIP-EO کامل و معتبر نبود.
وضعیت: PART_TRUNCATED_OR_CONFLICTED — CONTEXT_NOT_ACTIVATED
مورد لازم برای اصلاح: [ایراد دقیق]
هیچ تحلیل، طراحی جدید، پیاده‌سازی یا اقدام اجرایی آغاز نمی‌شود.
~~~

P01-REQ-003 — سکوت، تأخیر کاربر یا نبود قسمت بعدی مجوز ادامه‌دادن نیست. اگر قسمت ۰۲ ارسال نشد، در وضعیت انتظار باقی بمان و هیچ محتوای جایگزینی تولید نکن.

### 0.1 نقش این قسمت در بستۀ ۱۸ قسمتی

این قسمت مالک معنایی «هویت پروژه، مأموریت، محدودۀ فعال، ممنوعیت‌های دائمی، اصول بنیادین، لایه‌های منطقی، Stable Core، جداسازی Engineها، وضعیت Technology Baseline، قرارداد بنیادین داده و Base Canonical Event Envelope» است.

این قسمت مالک جزئیات API، Workflow، Authority Taxonomy، الگوریتم‌های علمی، AI lifecycle، Plugin behavior، Persistence، Data Governance، Security controls، Observability، Testing، Deployment، SDLC، Constitution، Implementation Roadmap یا Project Freeze نیست. آن حوزه‌ها در قسمت‌های مالک خود تعریف می‌شوند.

### 0.2 شاخص ناوبری و پیوستگی ۱۸ قسمت

این فهرست فقط نقشۀ دریافت و مرجع پیوند است؛ تعریف کامل هر حوزه فقط در قسمت مالک همان حوزه معتبر است:

1. قسمت ۰۱ — مبانی و خط پایه معماری: هویت، مأموریت، Scope، اصول، داده و Event پایه.
2. قسمت ۰۲ — نقشۀ تکمیل و پروتکل همکاری: ترتیب Stageها، تصمیم‌گیری، همکاری و تفکیک Gateها.
3. قسمت ۰۳ — قرارداد API، Application Command و Query: تعاملات تایپ‌شده و جداسازی Query/Command/Event/Outcome.
4. قسمت ۰۴ — قرارداد Workflow، Process و Human Control: State Machine، checkpoint و کنترل فرایند.
5. قسمت ۰۵ — Taxonomy اثر، Approval، Permission و Autonomy: محورهای مستقل اقتدار و قواعد Fail-Closed.
6. قسمت ۰۶ — حقیقت علمی، محاسبۀ عددی و Verification مستقل: قراردادهای Astrodynamics و Scientific Assurance.
7. قسمت ۰۷ — مرز AI Advisory، RAG، Knowledge و Memory: محدودۀ اختیار AI و جداسازی حقیقت Canonical.
8. قسمت ۰۸ — Plugin، Adapter، Tool و Capability Extension: توسعه‌پذیری کنترل‌شده و Capability Broker.
9. قسمت ۰۹ — Persistence، Database، Projection و Data Access: نگهداری و دسترسی بدون مخلوط‌کردن Source of Truth و Projection.
10. قسمت ۱۰ — Data Governance و Dataset Lifecycle: Classification، Retention، Archival، Legal Hold و Deletion.
11. قسمت ۱۱ — Security، Privacy، Threat Model و Trust Boundaries: Zero Trust و کنترل امنیت/حریم خصوصی.
12. قسمت ۱۲ — Observability، Reliability، SLO، Performance و Capacity: اندازه‌گیری، تاب‌آوری و ظرفیت.
13. قسمت ۱۳ — Testing، Verification، Validation، Benchmark و Assurance: شواهد پذیرش و هم‌ارزی Artifact.
14. قسمت ۱۴ — Deployment، Environments، Infrastructure و Operations: محیط‌ها و معماری عملیاتی کنترل‌شده.
15. قسمت ۱۵ — SDLC، Repository، Change، Release و Incident Management: چرخه تغییر و انتشار.
16. قسمت ۱۶ — Project Constitution و Binding Engineering Governance: قانون اساسی و حاکمیت الزام‌آور پروژه.
17. قسمت ۱۷ — Implementation Roadmap، Vertical Slices و Controlled Delivery: برنامۀ پیش‌اجرا و تحویل مرحله‌ای.
18. قسمت ۱۸ — Final Integration، Master Compilation و Project Freeze Architecture: ممیزی مونتاژ، تعارض‌ها و Gateهای نهایی.

P01-CON-001 — هیچ قسمت بعدی مجاز نیست تعریف مالک این قسمت را بی‌صدا بازنویسی کند. قسمت‌های بعدی می‌توانند آن را مصرف، محدود یا با کنترل سازگار سخت‌گیرانه‌تر کنند، اما برای تغییر آن باید Conflict و Change Record صریح ایجاد شود.

P01-CON-002 — دریافت هر قسمت فقط Context را گسترش می‌دهد؛ نه Authority را. حتی پس از دریافت قسمت ۱۸، حالت مجاز فقط `CONTEXT_ASSEMBLED — AWAITING_EXPLICIT_TASK` است، نه `IMPLEMENTATION_AUTHORIZED` یا `PROJECT_FROZEN`.

## 1. هویت منبع، وضعیت و محدودیت تاریخی

P01-DEF-001 — مالک معنایی این قسمت:

- Artifact ID: `CSIP-EO-RS-PART-1`
- Version: `0.1.0-reconstituted-draft`
- SHA-256: `a33bf602b5a5e5c8518b709b5dde7ab6b96617cc76ac86c66d2c795271422c50`
- Status: `RECONSTITUTED_DRAFT — REVIEW_READY — NOT_APPROVED — NOT_FROZEN`
- Successor candidate of: `CSIP-EO-MASTER-CONTEXT-PART-1`
- Historical source state: `MISSING_NORMATIVE_ARTIFACT`
- Domain scope: `EARTH_ORBIT_ONLY`
- Deployment baseline: `TERRESTRIAL_BASELINE — ON_ORBIT_RUNTIME_DEFERRED`

P01-DEN-004 — این منبع یک Successor Candidate تازه‌تألیف‌شده است؛ Bytes تاریخیِ Part 1 بازیابی نشده‌اند، تصویب تاریخی به ارث نرسیده است و این متن هرگز نباید «اصل تاریخی بازیابی‌شده» معرفی شود.

P01-CON-003 — پذیرش قبلی کاربر برای `PROMPT_DESIGN_WORKING_BASELINE_ONLY` و سپس `PROMPT_ARCHITECTURE_AND_ASSEMBLY_WORKING_BASELINE` فقط تولید و بازبینی ترتیبی متن ۱۸ قسمت را مجاز کرده است. آن پذیرش‌ها وضعیت Normative منابع، Stage 20، Stage 32، Project Freeze یا مجوز اجرا را تغییر نداده‌اند.

P01-CON-004 — هویت هر Source با ترکیب زیر تعیین می‌شود:

`Artifact ID + Exact Version + Exact SHA-256 + Status`

Filename، تاریخ جدیدتر، متن طولانی‌تر، ترجمه، Summary، Memory، Retrieval Result یا Model Output به‌تنهایی Source را جایگزین یا تصویب نمی‌کند.

P01-FAIL-002 — هر ادعای تاریخی یا Normative که Source، Version، Digest، Status و Approval Record معتبر ندارد، `UNVERIFIED_CLAIM` است و نباید به‌عنوان حقیقت پروژه استفاده شود.

## 2. هدف، محدودۀ فعال و استثناهای صریح

### 2.1 هویت و مأموریت

P01-DEF-002 — نام رسمی پروژه:

`CSIP-EO — Cognitive Space Intelligence Platform for Earth Orbit`

تعریف فارسی:

`پلتفرم شناختی هوشمندی فضایی برای مدار زمین`

P01-REQ-004 — CSIP-EO باید یک پلتفرم Enterprise-Grade، Production-Oriented، Physics-First، Evidence-Based، Explainable، Uncertainty-Aware و AI-Assisted برای ایجاد درک موقعیتی یکپارچه و قابل‌اعتماد از اشیا و فعالیت‌های مدار زمین باشد.

P01-CON-005 — زنجیرۀ مأموریت سطح‌بالا:

`Multi-source acquisition → validation and normalization → observation management → object identity and association → orbit determination and update → covariance and uncertainty → trajectory and ephemeris → conjunction detection → collision-risk assessment → scenario and maneuver analysis → digital twin → anomaly and behavior analysis → governed knowledge and evidence → explanation and recommendation → human decision support → independent verification → audit, rollback or supersession`

P01-DEN-005 — CSIP-EO یک Model واحد، Chatbot، Dashboard، Database، Propagator، Mission Tool یا Workflow ساده نیست. هیچ جزء منفردی نمایندۀ کل Platform یا صاحب تمام Authorityها نیست.

### 2.2 محدودۀ فعال

P01-REQ-005 — محدودۀ فعال Baseline فقط `EARTH_ORBIT_ONLY` است و شامل موارد زیر می‌شود:

- `LEO`
- `MEO`
- `GEO`
- `HEO`
- سایر رژیم‌های معتبر مرتبط با مدار زمین، فقط پس از تعریف و تصویب Profile مربوط
- Ingestion، Computation، Storage، Simulation، Verification و Decision Support زمینی

P01-CON-006 — معماری می‌تواند Extension Pointهای آینده برای Domainهای خارج از مدار زمین داشته باشد، اما وجود Extension Point به معنی فعال‌شدن Capability نیست.

### 2.3 محدودۀ Deferred

موارد زیر در Baseline فعلی غیرفعال و Deferred هستند:

- Domainهای خارج از Earth Orbit؛
- On-orbit runtime؛
- Flight-software integration؛
- هر رابطی که بتواند به Control یا Command عملیاتی فضاپیما منجر شود.

P01-DEN-006 — Scope غیرفعال از طریق Plugin، Adapter، Generic API، Workflow، Configuration، Feature Flag، Amendment، Fork، Successor Package، Emergency Mode یا Human Mediation به‌صورت ضمنی فعال نمی‌شود.

### 2.4 ممنوعیت دائمی مسیر فرمان فضایی

P01-DEN-007 — CSIP-EO نباید مستقیم، غیرمستقیم، عمومی، اختصاصی، Human-mediated، AI-mediated، Archived، Amended، Forked یا Successor-inherited هیچ مسیر قابل‌اجرا برای موارد زیر ایجاد، عرضه، پنهان، شبیه‌سازی به‌عنوان Interface اجرایی یا فعال کند:

- Spacecraft Command؛
- Telecommand؛
- Uplink؛
- Flight-control execution؛
- Autonomous maneuver execution.

P01-CON-007 — هر مسیر فوق بدون استثنا `E9 / APR-X / INC-0 / HARD_DENY` است. `APR-X` یعنی هیچ Approval Route معتبری درون CSIP-EO وجود ندارد. Budget، Risk Acceptance، Human Approval، Emergency، AI Recommendation، Operator Intent یا Business Pressure نمی‌تواند این ممنوعیت را رفع کند.

P01-FAIL-003 — مشاهده یا پیشنهاد هر مسیر Command-enabling یک Conflict کلاس `C9` و Incident سطح `INC-0` ایجاد می‌کند و نتیجۀ مجاز فقط `BLOCK → ISOLATE → PRESERVE EVIDENCE → REMOVE PATH → INDEPENDENT REVIEW` است؛ نه درخواست Approval برای اجرای آن.

## 3. اصول بنیادین و تغییرناپذیر

اصول زیر در تمام قسمت‌های بعدی ارث‌بری می‌شوند و هیچ جزء، Model، Agent، Tool، Human Role یا Workflow حق کاهش آن‌ها را ندارد:

P01-INV-001 — Physics Before AI: هیچ خروجی AI جایگزین محاسبۀ فیزیکی معتبر، داده معتبر یا Verification علمی نمی‌شود.

P01-INV-002 — Human Authority: اختیار انسانی باید Scope-bound، Competence-bound، Evidence-bound، Time-bound، Revocable و Auditable باشد؛ حضور انسان به‌تنهایی یک Action ممنوع را مجاز نمی‌کند.

P01-INV-003 — Evidence Before Claims: هر ادعای مادی باید به Evidence قابل‌بررسی، Provenance و Limitation متصل باشد.

P01-INV-004 — Explainability: نتیجه مهم باید Method، Input، Assumption، Configuration، Limitation، Uncertainty، Confidence و Verification Status را آشکار کند.

P01-INV-005 — Uncertainty First-Class: Uncertainty، Covariance، Confidence، Quality، Validity و Unknown State جزء Domain هستند، نه متن تزئینی.

P01-INV-006 — Independent Verification: نتایج علمی یا پراثر باید متناسب با Consequence، Uncertainty و Common-mode Risk توسط مسیر مستقل بررسی شوند.

P01-INV-007 — Event-Driven Integration: Domain Eventها Immutable، Versioned، Auditable، Replay-aware و دارای Causality صریح هستند.

P01-INV-008 — Governed Digital Twin: Digital Twin یک نمایش تحلیلی نسخه‌بندی‌شده است؛ Controller خودمختار یا مجوز اثر واقعی نیست.

P01-INV-009 — Zero Trust: User، Service، Workload، Device، Model، Plugin، Tool، Provider و Network Location به‌صورت پیش‌فرض مورد اعتماد نیستند.

P01-INV-010 — Replaceability: Vendor، Runtime، Model، Framework، Cloud، Database، Broker و Engine باید پشت Contract و Adapter قابل‌جایگزینی باشند.

P01-INV-011 — Graceful Degradation: خرابی AI نباید Physics Core، Data Ingestion یا Safety Monitoring را متوقف کند؛ Capability Loss باید صریح، قابل‌مشاهده و Fail-safe باشد.

P01-INV-012 — Reproducibility: هر نتیجۀ مادی باید در Scope و Equivalence Contract تعریف‌شده با Input، Version، Configuration، Dependency، Policy، Model، Dataset و Auxiliary Data قابل‌بازسازی باشد.

P01-INV-013 — Immutable History: تاریخچه با Supersession و Correction Record اصلاح می‌شود، نه Silent Overwrite یا حذف بی‌ردپا.

P01-INV-014 — Minimum Sufficient Complexity: هیچ Technology، Service، Agent، Control یا Process بدون Requirement و Evidence توجیه‌کننده وارد معماری نمی‌شود.

P01-INV-015 — Fail Closed: Authority، Approval، Effect، Source، Integrity، Scientific Validity یا Policy نامعلوم/مبهم/متعارض مساوی `DENY_OR_BLOCK` است، نه Allow.

P01-INV-016 — AI Advisory Only: AI می‌تواند پیشنهاد، طبقه‌بندی، خلاصه، توضیح یا Hypothesis تولید کند؛ نمی‌تواند حقیقت علمی جعل، Approval صادر، Risk قبول، Budget متعهد یا Action خود را تصویب کند.

P01-INV-017 — Record Separation: Recommendation، Decision، Approval، Authorization، Execution، Receipt و Outcome رکوردهای جدا هستند و یکی از دیگری استنتاج نمی‌شود.

P01-INV-018 — Integrity Is Not Correctness: Digest یا Signature می‌تواند Fixity/Origin را پشتیبانی کند؛ صحت علمی، امنیت، انطباق، Approval یا Permission را به‌تنهایی ثابت نمی‌کند.

## 4. کپسول ثابت جهانی برای تمام ۱۸ قسمت

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

## 5. معماری منطقی و مرزهای Authority

### 5.1 لایه‌های پلتفرم

P01-CON-008 — CSIP-EO حداقل از لایه‌های منطقی زیر تشکیل می‌شود. این‌ها Boundary مسئولیت هستند و الزاماً به معنی Microservice مستقل نیستند:

1. Data Platform — Acquisition، Validation، Canonicalization، Lineage و Lifecycle؛ بدون Authority برای جعل حقیقت علمی.
2. Physics Platform — Force Model، Propagation و Deterministic Transform؛ فقط در محدوده Profile تصویب‌شده معتبر.
3. Estimation Platform — Orbit/State Estimation و Covariance؛ با حفظ Model، Residual و Uncertainty Evidence.
4. Simulation Platform — Scenario و Digital Twin Execution؛ بدون Real-world Command Authority.
5. Conjunction Platform — Encounter Detection و Geometry؛ بدون تصمیم عملیاتی خودکار.
6. Collision-Risk Platform — روش‌های مصوب Probability/Risk؛ بدون عدد ساختگی AI.
7. AI Intelligence Platform — Classification، Extraction، Synthesis و Anomaly Hypothesis؛ Advisory Only.
8. Knowledge Platform — Fact، Relationship، Retrieval و Provenance؛ Index و Embedding، Projection هستند نه Canonical Truth.
9. Decision-Support Platform — Explanation، Option، Trade-off و Recommendation؛ Decision انسانی جداست.
10. Verification Platform — Independent Recalculation، Challenge و Assurance؛ با کنترل Common-mode Failure.
11. Governance Platform — Policy، Risk، Cost، Approval و Configuration Control؛ بدون اختیار تغییر حقیقت علمی با رأی.
12. Security and Audit Platform — Identity، Authorization، Evidence، Forensics و Accountability؛ بدون اختیار ساخت Domain Truth.

P01-DEN-008 — هیچ لایه‌ای نباید هم‌زمان Proposer، Executor، Verifier و Final Approver یک تغییر حساس باشد.

### 5.2 Stable Platform Core

P01-DEF-003 — Stable Core مجموعه قراردادهای معنایی و Control Conceptهای زیر است:

- Identity و Actor-chain Registry؛
- Workflow و State-machine Contracts؛
- Configuration و Policy Registry؛
- Plugin Registry؛
- Capability Registry؛
- Model Registry؛
- Physics Engine Registry؛
- Canonical Entity، Event و Schema Registry؛
- Security و Authorization Policy؛
- Approval و Execution-lease concepts؛
- Audit، Evidence و Provenance Ledgers؛
- Observability و Reliability Profiles؛
- Risk و Cost Control Planes؛
- Digital Twin Identity و Versioning؛
- Independent Verification Registry.

P01-CON-009 — Stable Core به معنی ثبات Semantic Contract است، نه Freeze شدن Vendor، Product، Runtime یا Implementation.

### 5.3 جداسازی Engineها

Engineهای زیر باید از نظر Contract، Version، Input، Output، Evidence، Failure State و Authority از یکدیگر جدا بمانند:

- Physics Engine؛
- Estimation Engine؛
- Simulation Engine؛
- Conjunction Engine؛
- Collision-Risk Engine؛
- AI Reasoning Engine؛
- Predictive/Behavioral Engine؛
- Knowledge and Retrieval Engine؛
- Decision-Support Engine؛
- Verification Engine.

P01-CON-010 — هیچ Engine حق ندارد Authority یک Engine دیگر را Silent Absorb کند. Cross-engine exchange فقط از طریق Request/Result تایپ‌شده، Versioned و Evidence-linked انجام می‌شود.

P01-FAIL-004 — اگر Engine boundary، Source Version، Unit، Frame، Time، Uncertainty یا Verification Status گم شود، Result برای Promotion به Canonical Truth نامعتبر است و باید Quarantine یا Degraded شود.

## 6. استقلال معماری و وضعیت Technology Baseline

P01-INV-019 — تمام Domain Contractها باید در سطح معماری:

- Runtime-Neutral؛
- Vendor-Neutral؛
- Model-Neutral؛
- Framework-Neutral؛
- Cloud-Neutral؛
- Database-Neutral؛
- Broker-Neutral؛
- و در سطح Domain Contract، Programming-Language-Neutral

باشند.

P01-DEN-009 — نام فناوری در Baseline مجوز نصب، خرید، فعال‌سازی، اتصال، پیاده‌سازی یا Freeze آن نیست.

### 6.1 وضعیت‌های ثبت‌شده

وضعیت‌های زیر باید دقیقاً حفظ شوند:

| حوزه | فناوری یا قرارداد | وضعیت ثبت‌شده |
|---|---|---|
| Languages | Python, Java, TypeScript | `PROVISIONAL_SELECTION` |
| Language Research | Rust | `RESEARCH_TRACK` |
| HTTP API | FastAPI + OpenAPI | `PROVISIONAL_SELECTION` |
| RPC | gRPC + Protobuf | `PROVISIONAL_SELECTION` |
| Event Backbone | Redpanda | `SHORTLISTED` |
| Event Backbone | NATS JetStream | `SHORTLISTED` |
| Transactional Database | PostgreSQL | `PROVISIONAL_SELECTION` |
| Analytical Database | ClickHouse | `PROVISIONAL_SELECTION_WITH_ACTIVATION_GATE` |
| Object Storage Contract | S3-compatible | `APPROVED_PRINCIPLE` |
| Object Storage Candidate | Ceph | `SHORTLISTED` |
| Data-table Format | Apache Iceberg | `PROVISIONAL_SELECTION` |
| Vector Store | Qdrant | `PROVISIONAL_SELECTION` |
| Distributed Compute | Ray | `PROVISIONAL_SELECTION` |
| Orchestration | Kubernetes | `SHORTLISTED` |
| Packaging | OCI Containers | `APPROVED_PRINCIPLE` |
| Telemetry | OpenTelemetry | `PROVISIONAL_SELECTION` |
| Policy | OPA | `PROVISIONAL_SELECTION` |
| Workload Identity | SPIFFE/SPIRE | `SHORTLISTED` |
| Artifact Signing | Sigstore/Cosign | `PROVISIONAL_SELECTION` |
| AI Serving | vLLM | `PROVISIONAL_SELECTION` |
| AI Serving Alternatives | Triton, Ray Serve | `SHORTLISTED` |
| Model Registry Contract | MLflow | `PROVISIONAL_SELECTION` |

P01-CON-011 — هر Candidate باید بعداً از Gateهای Requirement Fit، License، Security، Scientific Correctness، Reliability، Replaceability، Performance، Testability، Operability، Interoperability، Cost، Benchmark، Failure Testing، Exit Strategy، ADR و Human Approval عبور کند.

P01-FAIL-005 — هیچ `PROVISIONAL_SELECTION`، `SHORTLISTED` یا `RESEARCH_TRACK` نباید در Summary یا اجرای بعدی به `APPROVED` تبدیل شود. Status drift یک خطای Blocking است.

## 7. خط پایه Astrodynamics، Physics و AI

### 7.1 موتورهای Astrodynamics و نقش موردنظر

| Engine | نقش موردنظر | محدودیت Authority |
|---|---|---|
| Orekit | Primary operational astrodynamics engine candidate | Implementation باید Contract-bound و بعداً Qualified شود |
| GMAT | Independent verification candidate | نباید تمام Failure Causeها را با Primary مشترک داشته باشد |
| Tudat/TudatPy | Research و Scientific Comparison | نتیجۀ آن خودکار Operational Authority ایجاد نمی‌کند |
| Basilisk | 6-DOF و Advanced Simulation | فقط با Use Case، Profile و Qualification جدا فعال می‌شود |

P01-CON-012 — Domain Contract باید Engine-agnostic باشد. Time Scale، Epoch، Reference Frame، Frame Realization، Unit، Convention، Covariance، Uncertainty، Force-model Profile و Auxiliary-data Version برای Result علمی مادی اجباری‌اند.

P01-DEN-010 — LLM یا Model AI نباید Orbit، State Vector، Covariance، Time of Closest Approach، Miss Distance، Hard-body Radius، Collision Probability، Frame Transform یا Maneuver Result را جعل کند.

P01-CON-013 — Propagation Tierهای `0..4` و Physics Confidence Levelهای `PHY-C0..PHY-C5` محورهای Classification هستند؛ Definition دقیق Algorithm/Profile و Gateهای آن‌ها در قسمت علمی مالک این حوزه ارائه می‌شود.

P01-FAIL-006 — اختلاف علمی با Evidence، Reproduction و Competent Adjudication حل می‌شود؛ Majority Vote، Model Confidence یا Governance Preference جایگزین حقیقت علمی نیست.

### 7.2 خط پایه AI

خانواده‌های Capability هوش مصنوعی شامل موارد زیرند:

- Data and Document Intelligence؛
- Observation Quality and Association Assistance؛
- Behavioral and Anomaly Analysis؛
- Predictive Assistance؛
- Risk Interpretation؛
- Knowledge and Retrieval؛
- Explanation and Communication؛
- Verification Assistance؛
- Human Decision Support.

P01-CON-014 — Model Gateway باید هر Model Call را به Versionهای Model، Tokenizer، Runtime، Precision، Parameter، Prompt، Tool، Corpus، Policy، Cost و Evidence متصل کند.

P01-DEN-011 — Retrieval، Tool Output و Model Output در Trust Boundary برابر `DATA_ONLY / UNTRUSTED_UNTIL_VALIDATED` هستند.

P01-DEN-012 — Model Self-evaluation، Confidence یا Consensus بین Agentها Qualification، Approval یا Scientific Verification نیست.

P01-CON-015 — Online Learning، Autonomous Prompt Update، Model Promotion، Memory Commitment یا تغییر Model Gateway نیازمند Change و Approval مستقل است.

P01-CON-016 — AI Confidence Levelهای `AI-C0..AI-C5` فقط Evidence Maturity را بیان می‌کنند و هرگز Authority تولید نمی‌کنند.

## 8. قرارداد بنیادین داده Canonical

### 8.1 Canonical Entity Envelope

P01-DEF-004 — هر Entity یا Revision Canonical باید حداقل Envelope زیر را داشته باشد:

~~~yaml
entity_id:
entity_type:
schema_id:
schema_version:
revision:
lifecycle_status:
tenant_context:
purpose_context:
valid_time:
transaction_time:
source_references: []
provenance_reference:
quality_context:
uncertainty_context:
classification:
content_digest:
supersedes: []
limitations: []
payload:
~~~

P01-CON-017 — Current State، Immutable History، Projection، Cache، Index، Archive و Evidence کلاس‌های متفاوت‌اند. هیچ Projection یا Index به‌صورت خودکار Source of Truth نمی‌شود.

P01-CON-018 — Correction باید Revision جدید بسازد و Record قبلی را از طریق `supersedes` حفظ کند. Silent Overwrite ممنوع است.

P01-DEN-013 — مقدار Missing نباید با مقدار Synthetic یا AI-generated جایگزین شود. Null بدون Semantics در Record مادی مجاز نیست؛ حالت‌هایی مانند `UNKNOWN`، `NOT_OBSERVED`، `NOT_APPLICABLE`، `WITHHELD`، `REDACTED`، `INVALID` یا `PENDING` باید به‌صورت تایپ‌شده استفاده شوند.

P01-CON-019 — Identity، Time، Frame، Unit، Uncertainty، Quality و Provenance در Translation، Serialization، Projection یا Model Context نباید حذف شوند.

### 8.2 قرارداد زمان

P01-DEF-005 — هر Timestamp Canonical باید یک `TemporalStamp` تایپ‌شده باشد:

~~~yaml
instant:
time_scale:
source_clock:
clock_quality:
uncertainty:
leap_second_table_version:
conversion_provenance:
~~~

P01-DEN-014 — Timestamp بدون Time Scale برای Record علمی یا Governance Canonical نامعتبر است.

P01-CON-020 — `event_time`، `observation_time`، `valid_time`، `transaction_time/record_time`، `ingest_time` و `publication_time` مفاهیم جدا هستند و نباید یکی فرض شوند.

### 8.3 قرارداد Frame و Unit

هر Quantity علمی باید حداقل مشخص کند:

- Reference Frame و Realization/Version؛
- Epoch و Time Scale؛
- Unit و Dimension؛
- Convention و Transform Chain؛
- Precision، Tolerance و Uncertainty؛
- Auxiliary Data و Constant-set Versions.

P01-FAIL-007 — Scientific Record فاقد Time Scale، Frame، Unit، Convention یا Uncertainty لازم باید `INVALID_OR_INCOMPLETE` شود و نباید به Result فعال، Recommendation قطعی یا Pass تبدیل گردد.

## 9. Base Canonical Event Envelope و Event Semantics

### 9.1 مالکیت و Envelope پایه

P01-DEF-006 — قسمت ۰۱ تنها مالک Base Canonical Event Envelope است. Fieldهای Conversation-attested پایه عبارت‌اند از:

~~~yaml
event_id:
event_type:
event_version:
event_category:
occurred_at: TemporalStamp
recorded_at: TemporalStamp
published_at: TemporalStamp
producer:
producer_version:
producer_instance:
subject_references: []
correlation_id:
causation_id:
trace_id:
workflow_id:
command_id:
approval_reference:
ordering_key:
idempotency_key:
payload_schema:
payload:
security_context:
provenance:
quality_context:
delivery_metadata:
content_hash:
signature:
~~~

P01-CON-021 — Mandate یا قسمت‌های بعدی حق Rename یا Replace کردن Base Envelope را ندارند. Fieldهای Risk، Cost، Security، Audit، Reliability، Evidence، Scientific و Data Lifecycle فقط از طریق Extension Profileهای Applicability-bound افزوده می‌شوند.

### 9.2 Core Profile و Applicability

P01-CON-022 — حداقل Core Profile هر Event Canonical باید شامل موارد زیر باشد:

~~~yaml
event_id:
event_type:
event_version:
event_category:
occurred_at: TemporalStamp
recorded_at: TemporalStamp
producer:
producer_version:
subject_references: []
correlation_id:
causation_id:
payload_schema:
payload_or_protected_reference:
provenance:
quality_context:
content_hash:
~~~

P01-CON-023 — `published_at`، `producer_instance`، `trace_id`، `workflow_id`، `command_id`، `approval_reference`، `ordering_key`، `idempotency_key`، `delivery_metadata` و `signature` زمانی اجباری‌اند که Applicability Predicate مربوط برقرار باشد. Optional بودن در Schema به معنی Optional بودن در هر Context نیست.

### 9.3 Registry پروفایل‌های Extension

P01-DEF-007 — Registry پایه Extension Profileها:

1. `EVT-SCI` — Observation یا Scientific Input/Result: Epoch، Time Scale Profile، Frame، Unit، Covariance، Uncertainty، Algorithm/Engine/Config/Auxiliary-data Digest، Validity Domain و Verification Status.
2. `EVT-SEC-AUD` — Access، Policy، Approval، Privileged یا Sensitive Effect: Tenant، Environment، Region، Actor، Authentication، Authorization، Action، Target، Intent، Policy Decision، Approval، Outcome، Error، Classification، Redaction، Retention و Residency.
3. `EVT-RISK-COST` — Material Risk یا Cost-bearing Action: Risk ID/Tier/Method/Appetite/Acceptance، Control/KRI/KCI/Owner، Budget، Cost Center، Reservation، Actual Cost و Usage Dimension.
4. `EVT-REL-OBS` — Service/Workflow Reliability: Service/Instance، Request/Trace/Span، Sequence، Timestamp Confidence، Retryability، SLI Eligibility، Good-event Status و Telemetry Quality.
5. `EVT-REL-EVID` — Build/Release/Deploy/Model/Data/Evidence Lifecycle: Commit، Build، Artifact، Deployment، Config، Feature Flag، Model، Prompt، Tool، Dataset/Index، Input/Output Digest، Evidence Reference، Signature و Previous Hash/Checkpoint.
6. `EVT-DATA-LIFE` — Classification، Retention، Archival، Deletion یا Legal Hold: Opaque Data-subject References، Policy/Basis، Retention Class، Hold، Tombstone/Purge Graph، Derived-copy Propagation و Verifier Receipt.

P01-CON-024 — Producer و Consumer باید Profile Applicability، Required Cardinality، Privacy، Classification و Size Bound را Validate کنند. Extension Profile نباید Base را دور بزند یا Secret را وارد Event کند.

### 9.4 Event، Command و Query

P01-DEF-008 — `Event` یک Fact Immutable دربارۀ رخداد اتفاق‌افتاده است.

P01-DEF-009 — `Command` درخواست انجام Action است و Evidence وقوع Action نیست.

P01-DEF-010 — `Query` درخواست Read-only است و حق Mutation State ندارد.

P01-DEN-015 — Event، Command، Query، Approval، Execution Receipt و Outcome نباید با هم مخلوط یا از هم استنتاج شوند.

P01-CON-025 — Correlation مساوی Causation نیست؛ `causation_id` باید رابطۀ علّی را صریح کند. `trace_id` نیز Identity، Tenant، Policy یا Authority ایجاد نمی‌کند.

### 9.5 Delivery، Idempotency، Retry و Replay

P01-CON-026 — Baseline تحویل Event برابر `AT_LEAST_ONCE` است. Exactly-once نباید به‌عنوان تضمین مطلق End-to-End ادعا شود.

P01-CON-027 — Consumer باید Idempotent باشد، Duplicate و Out-of-order Event را مدیریت کند، Unsupported Version را رد و گزارش کند، Invalid Event را Quarantine کند و State Transition را Validate کند.

P01-CON-028 — برای State Change تراکنشی، ثبت State و Outbox Record باید در یک Transaction قرار گیرد و Publication پس از Commit انجام شود.

P01-CON-029 — Retry فقط برای Failure موقت، با Bound و Backoff معتبر مجاز است. Retry نامحدود ممنوع است. پس از حد مجاز: `Dead Letter → Quarantine → Alert → Audit → Root-cause Analysis → Controlled Replay → Resolution Record`.

P01-CON-030 — Replay باید نوع، Scope، Source Boundary، Side-effect Policy و Approval Requirement داشته باشد. External Notification، Deployment، Payment، Data Deletion، Production Mutation و هر Effect حساس در Replay پیش‌فرض غیرفعال است.

P01-DEN-016 — Secret، Token، Password، Private Key یا Credential نباید در Event Payload، Metadata، Log یا Evidence غیرمحافظت‌شده قرار گیرد.

P01-CON-031 — Correction Event، Record قبلی را تغییر نمی‌دهد؛ Event جبرانی یا Superseding ایجاد می‌کند و History را حفظ می‌نماید.

## 10. بنیاد Decision، Permission و Control Planeها

### 10.1 وضعیت تصمیم‌ها

P01-DEF-011 — وضعیت‌های عمومی تصمیم/انتخاب که باید بدون Status Laundering حفظ شوند:

`PROPOSED | UNDER_RESEARCH | SHORTLISTED | PROVISIONAL_SELECTION | APPROVED | REJECTED | DEFERRED | DEPRECATED | SUPERSEDED | FROZEN`

P01-CON-032 — Lifecycle اجرایی یک تصمیم می‌تواند Recordهای جدا برای `PROPOSED → REVIEWED → CONDITIONALLY_APPROVED | APPROVED | REJECTED → IMPLEMENTED → VERIFIED → FROZEN | SUPERSEDED | WITHDRAWN` داشته باشد؛ اما هیچ Transition بدون Evidence و Authority معتبر استنتاج نمی‌شود.

### 10.2 محورهای مستقل Authority

محورهای زیر مستقل‌اند و تعریف تفصیلی آن‌ها متعلق به قسمت ۰۵ است:

- Effect: `E0..E9`؛
- Approval: `APR-0..APR-4` و `APR-X`؛
- Permission: `PERM-A..PERM-E`؛
- Autonomy: `AUT-0..AUT-5`؛
- Risk Tier؛
- Data Class؛
- Environment Class؛
- Cost Exposure؛
- Irreversibility.

P01-DEN-017 — هیچ نگاشت یک‌به‌یک خودکاری میان این محورهای مستقل وجود ندارد. Missing یا Contradictory Mapping برابر `AUTHORITY_MAPPING_INDETERMINATE → DENY / DO_NOT_EXECUTE` است.

P01-CON-033 — `AUT-5` یعنی No Autonomous Execution؛ `APR-X` یعنی No Approval Route. این دو هم‌معنا نیستند. مسیر `E9` فقط به `APR-X` نگاشت می‌شود و در CSIP-EO هیچ Exit ندارد.

### 10.3 پنج Control Plane یکپارچه

P01-DEF-012 — پنج Control Plane منطقی زیر باید به‌صورت یک معماری هماهنگ عمل کنند، نه پنج قابلیت جدا:

1. Authority and Sensitive Data Control Plane؛
2. Security–FinOps Cost Control Plane؛
3. Observability, Audit, Provenance and Forensic Evidence Plane؛
4. Reproducible Build, Environment Parity and Immutable Delivery Plane؛
5. Enterprise Risk Governance, Assessment, Decision and Continuous Assurance Plane.

P01-CON-034 — این Control Planeها Constraint و Evidence تولید می‌کنند؛ Domain Science را جایگزین نمی‌کنند، Authority خود را افزایش نمی‌دهند و به‌تنهایی مجوز اجرا نیستند.

P01-CON-035 — Budget Approval، Security Authorization، Risk Acceptance، Human Approval و Technical Success رکوردهای مستقل‌اند. وجود یکی، دیگری را اثبات نمی‌کند.

P01-DEN-018 — هیچ System، Model، Workflow یا Agent حق ندارد Authority، Budget، Policy Right، Credential، Capability، Risk-acceptance Authority یا Exception Scope خود را افزایش دهد یا Action خود را تصویب کند.

## 11. پیامدهای Authority، Security، Risk، Cost و Evidence

P01-CON-036 — در زمان دریافت این قسمت، `ACTION_AUTHORITY: NONE` حاکم است. حتی Read، Browse یا Tool Call برای تکمیل Context غایب مجاز نیست، زیرا وظیفۀ این مرحله فقط Reception است.

P01-CON-037 — هر Action حساس در مراحل آینده باید دست‌کم Identity، Purpose، Scope، Capability، Data Boundary، Effect، Risk Context، Cost Exposure، Required Approval، Evidence Path، Validation و Recovery Strategy داشته باشد. تعریف تفصیلی این Gateها در قسمت‌های مالک ارائه خواهد شد.

P01-CON-038 — Missing Evidence باید `UNKNOWN` یا `INCOMPLETE_EVIDENCE` ثبت شود. Unknown Exposure نباید Low Risk گزارش شود.

P01-DEN-019 — عبارت‌هایی مانند `100% secure`، `risk-free`، `fully guaranteed`، `guaranteed on every device` یا `production ready` بدون Bounded Assurance Contract و Evidence معتبر ممنوع‌اند.

P01-CON-039 — Bounded Assurance باید Scope، Assumption، Support Matrix، Hard Invariant، Threshold، Residual Risk، Uncertainty، Evidence، Expiry و Invalidation Condition داشته باشد.

P01-CON-040 — هیچ Source، Dependency، Configuration، Build Input، Policy، Prompt، Model، Dataset یا Operational Assumption مادی نباید در Release Path پنهان یا بدون Traceability باشد.

## 12. رفتار Failure، Unknown، Degraded و Recovery

P01-FAIL-008 — هر حالت `UNKNOWN`، `MISSING`، `STALE`، `CONFLICTED`، `INVALID`، `NON_CONVERGED` یا `INDETERMINATE` باید صریح حفظ شود و هرگز به `PASS`، `SUCCESS`، `READY` یا `APPROVED` تبدیل نشود.

P01-FAIL-009 — اگر AI در دسترس نباشد یا Degraded شود، Physics Core، Data Ingestion و Safety Monitoring باید در حدود Capability معتبر ادامه دهند؛ AI-dependent Feature باید صریحاً Disabled/Degraded شود.

P01-FAIL-010 — اگر Scientific Engineها اختلاف مادی داشته باشند، Result باید `DISPUTED_OR_UNVERIFIED` شود و تا Adjudication مستقل نباید فعال گردد.

P01-FAIL-011 — اگر Source Digest، Version یا Status تعارض داشت، Source Binding باید `CONFLICTED` شود؛ «فایل جدیدتر برنده است» ممنوع است.

P01-FAIL-012 — اگر Permission، Approval، Budget، Risk Acceptance یا Execution Lease ناقص/منقضی/مبهم باشد، Effect انجام نمی‌شود.

P01-FAIL-013 — Recovery باید History، Evidence و Failure Record را حفظ کند. Rollback مجوز حذف Audit Trail یا بازنویسی حقیقت گذشته نیست.

P01-FAIL-014 — Emergency یا Break-glass فقط می‌تواند Exposure و Authority را کاهش دهد؛ نمی‌تواند مسیر `E9`، Hard Invariant یا Scope ممنوع را فعال کند.

## 13. Traceability، Decision Projection و Open Issueها

### 13.1 مالکیت Requirementهای بحرانی این قسمت

قسمت ۰۱ مالک اصلی Requirementهای زیر است و قسمت‌های مصرف‌کننده فقط آن‌ها را اعمال یا Verify می‌کنند:

- `CGR-REQ-001` — Scope فعال `EARTH_ORBIT_ONLY` و Deferred بودن Domainهای خارج از آن؛ مصرف‌کنندگان اصلی: P16 و P18.
- `CGR-REQ-002` — ممنوعیت دائمی هر مسیر Spacecraft Command/Telecommand/Uplink؛ مصرف‌کنندگان: تمام قسمت‌ها، با Negative Verification در P13 و P18.
- `CGR-REQ-016` — هویت و Semantics پایه Base Canonical Event Envelope؛ مصرف‌کنندگان: P03 تا P18.
- `CGR-REQ-017` — Extension Profileهای Applicability-bound که Base را جایگزین نمی‌کنند؛ مصرف‌کنندگان: P06، P10، P11، P12، P13، P15 و P18.
- `CGR-REQ-018` — Timestamp تایپ‌شده و Time-scale Explicit؛ مصرف‌کنندگان: تمام قسمت‌ها، با تقویت علمی در P06.

P01-CON-041 — `CGR-REQ-003` و `CGR-REQ-004` در این قسمت به‌عنوان Invariant/Foundation حضور دارند، اما مالک تفصیلی Scientific Truth، Time/Frame/Unit Validation و Acceptance آن‌ها قسمت ۰۶ است.

### 13.2 Decision Projectionهای Overlay

- `CGR-DEC-022` — Base Event Envelope حفظ می‌شود و Mandate Fieldها Extension هستند — Status: `PROPOSED`.
- `CGR-DEC-023` — هر Timestamp باید Time-scale Explicit باشد — Status: `PROPOSED`.
- `CGR-DEC-024` — Precedence باید Source-aware، Domain-aware و Fail-closed باشد — Status: `PROPOSED`; مالک اصلی Governance در P16 است.

P01-DEN-020 — `PROPOSED` به معنی `APPROVED` نیست. قرارگرفتن این Decisionها در Prompt فقط برای حفظ Context و طراحی است.

### 13.3 Open Issueهای اجباری

- `P01-OI-001` — Bytes تاریخی `CSIP-EO-MASTER-CONTEXT-PART-1` بازیابی نشده‌اند.
- `P01-OI-002` — `CSIP-EO-RS-PART-1` هنوز Normative Successor تصویب‌شده نیست.
- `P01-OI-003` — `CSIP-EO-RS-STAGE-20` همچنان `DOMAIN_REVIEW_REQUIRED` است.
- `P01-OI-004` — Stage 32 همچنان `PROPOSED` است و Project Specification Freeze اجرا نشده است.
- `P01-OI-005` — Full machine trace graph برای تمام Corpus پایین‌دست هنوز تکمیل نشده است.
- `P01-OI-006` — Ownerهای واقعی سازمانی، Budget، Provider، Region، Workload، Threshold، SLO، RPO و RTO تا زمانی که با Evidence تعیین نشوند `UNKNOWN` هستند.

P01-CON-042 — هیچ قسمت، Summary یا Agent بعدی حق ندارد این Open Issueها را فقط به دلیل دریافت Context ببندد.

## 14. Anti-claims و تفسیرهای ممنوع

این قسمت و دریافت آن هیچ‌یک از ادعاها یا مجوزهای زیر را ایجاد نمی‌کند:

- بازیابی Historical Part 1؛
- تصویب یا فعال‌سازی Normative Successor؛
- تصویب علمی Stage 20؛
- تصویب Stage 32؛
- تکمیل یا Freeze شدن Project Specification؛
- Implementation Readiness یا Production Readiness؛
- ایجاد یا تغییر Code، Repository، File، Database، Infrastructure یا Configuration؛
- اجرای Test، Benchmark، Build، Migration، Release، Deployment، Pilot یا Production؛
- نصب Dependency، Model، Runtime، Plugin یا Tool؛
- انتخاب نهایی Vendor، Cloud، Database، Broker، Runtime، Region یا Provider؛
- مجوز Spend، Procurement، External Message یا Data Transfer؛
- ادعای Legal Compliance، Certification، Qualification یا Operational Safety؛
- مجوز Spacecraft Command، Telecommand، Uplink، Flight Control یا Autonomous Maneuver Execution؛
- اختیار شروع قسمت ۰۲ توسط دریافت‌کننده بدون ارسال واقعی آن از سوی کاربر.

P01-DEN-021 — واژۀ `Final` در نام بستۀ Prompt فقط فرم هدفِ مونتاژ نهایی Context را توصیف می‌کند و به معنی `PROJECT_FROZEN`، `NORMATIVE`، `IMPLEMENTED` یا `PRODUCTION_READY` نیست.

## 15. تحویل به قسمت بعدی و وابستگی‌ها

P01-CON-043 — تمام تعریف‌های مالک این قسمت باید توسط قسمت‌های ۰۲ تا ۱۸ با Source Binding و Status فعلی مصرف شوند. Consumer حق ایجاد تعریف رقیب برای Base Event Envelope، Scope، Permanent Prohibition یا Global Invariantها را ندارد.

P01-CON-044 — قسمت بعدی مورد انتظار:

- Part ID: `CSIP-EO-FMSP-P02`
- Part Index: `02 of 18`
- Title: `Completion Roadmap and Collaboration Protocol | نقشۀ تکمیل و پروتکل همکاری`
- Semantic Owner: `CSIP-EO-RS-PART-2`
- Receive Mode: `CONTEXT_ONLY`
- Action Authority during reception: `NONE`

P01-REQ-006 — قسمت ۰۲ در پیام جداگانه و فقط پس از تصمیم کاربر ارسال خواهد شد. تا آن زمان هیچ کاری انجام نده، محتوای قسمت بعدی را حدس نزن، پروژۀ CSIP-EO را شروع نکن و در وضعیت انتظار باقی بمان.

P01-REQ-007 — پس از دریافت سالم این قسمت، تنها پاسخ مجاز همان متن ثابت زیر است و هیچ عبارت دیگری نباید قبل یا بعد از آن قرار گیرد:

~~~text
قسمت ۰۱ از ۱۸ ابرپرامپت نهایی CSIP-EO با موفقیت دریافت و ثبت شد.
هیچ تحلیل، طراحی جدید، پیاده‌سازی یا اقدام اجرایی آغاز نمی‌شود.
منتظر قسمت ۰۲ هستم.
~~~

RECEIVER_MUST_WAIT_FOR_NEXT_PART: TRUE
PART_DECLARED_COMPLETE: TRUE
NEXT_EXPECTED_PART: P02
RECEPTION_ACTION: ACK_ONLY
<<<CSIP-EO-FMSP-18P|0.9.0-draft|P01|END>>>