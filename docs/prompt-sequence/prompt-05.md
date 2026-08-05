<<<CSIP-EO-FMSP-18P|0.9.0-draft|P05|START>>>
CSIP_EO_PROMPT_PACKAGE_ID: CSIP-EO-FINAL-MASTER-SUPERPROMPT-18P
CSIP_EO_PROMPT_PACKAGE_VERSION: 0.9.0-draft
PART_ID: CSIP-EO-FMSP-P05
PART_INDEX: 05
PART_COUNT: 18
PART_TITLE: Effect, Approval, Permission and Autonomy Taxonomy | طبقه‌بندی Effect، Approval، Permission و Autonomy
SEMANTIC_OWNER_ARTIFACT_ID: CSIP-EO-RS-STAGE-19
SEMANTIC_OWNER_VERSION: 0.1.0-reconstituted-draft
SEMANTIC_OWNER_STATUS: RECONSTITUTED_DRAFT — REVIEW_READY — NOT_APPROVED — NOT_FROZEN
SEMANTIC_OWNER_SHA256: 30525213394593910a4bb0406ba3eb2ee784ddae05170933cea1a033654d8731
SUPPORTING_SOURCE_BINDINGS: CSIP-EO-AUDIT-GAP-02/0.1.0-candidate/fa400334a69702bf56e8588210449590573bccd3120d7c2cebd6ba9cc8fc161f; ENTERPRISE-TRUST-RISK-COST-EVIDENCE-REPRODUCIBILITY-MANDATE/verified-input-2026-07-28/1b5e7884a343589312d62259f181bd48f1a12b51e2613685c0d58c747a08dab4; CSIP-EO-PROMPT-ARCH-18P-C1/0.1.0-design-candidate/a4c80b938fccaab5d3d85c780351a41ee3444b4c6712920af45b493afbacb09b; CSIP-EO-GAP-RESOLUTION-MANIFEST-C1/0.1.0-candidate/349b590df9fad00c2e0ec317f4bd0b7ad747a5e22a1fead0f66f28c98e955216
PRIOR_PART_ID: CSIP-EO-FMSP-P04
NEXT_PART_ID: CSIP-EO-FMSP-P06
PART_PAYLOAD_SHA256: SEE_EXTERNAL_PROMPT_PACKAGE_MANIFEST
RECEIVE_MODE: CONTEXT_ONLY
ACTION_AUTHORITY: NONE

# پرامپت قسمت ۰۵ از ابرپرامپت نهایی ۱۸ قسمتی CSIP-EO
# طبقه‌بندی Effect، Approval، Permission و Autonomy

## 0. دستور دریافت، مرز این قسمت و قفل ضدتوهم

این پیام فقط «قسمت ۰۵ از ۱۸» یک زمینۀ مرجع به‌هم‌پیوسته است. قسمت‌های ۰۱، ۰۲، ۰۳ و ۰۴ باید پیش از این قسمت و به‌ترتیب دریافت شده باشند. قسمت‌های ۰۶ تا ۱۸ هنوز در این پیام وجود ندارند. دریافت این قسمت فقط Context مربوط به طبقه‌بندی Effect، Approval، Permission، Autonomy و Report Profile را گسترش می‌دهد و هیچ اختیار علمی، حقوقی، امنیتی، مالی، اجرایی یا عملیاتی ایجاد نمی‌کند.

P05-REQ-001 — هنگام دریافت این قسمت، وضعیت داخلی خود را دقیقاً چنین در نظر بگیر:

`RECEIVING_P05 — P01_P02_P03_P04_REQUIRED — CONTEXT_INCOMPLETE — ACTION_AUTHORITY_NONE`

P05-DEN-001 — اگر قسمت ۰۱، ۰۲، ۰۳ یا ۰۴ دریافت نشده، ترتیب `P01 → P02 → P03 → P04 → P05` قابل‌اثبات نیست، یا Header، Anchor، Source Binding، Footer یا Pointerهای این قسمت ناقص یا متعارض‌اند، این قسمت را فعال نکن و موفقیت دریافت را جعل نکن.

P05-DEN-002 — از این Part برای حدس‌زدن، بازسازی، تکمیل یا جعل محتوای قسمت‌های ۰۶ تا ۱۸ استفاده نکن. دانستن عنوان، Semantic Owner، Version، Status یا Digest یک Part بعدی مجوز ساخت محتوای غایب آن نیست.

P05-DEN-003 — تا پیش از دریافت و مونتاژ معتبر هر ۱۸ قسمت، تحت هیچ شرایطی:

- تحلیل یکپارچۀ کل CSIP-EO ارائه نکن؛
- P06 یا هیچ Part بعدی را آغاز یا تولید نکن؛
- Taxonomy، Policy، Approval Service، Authorization Engine، Capability، Workflow، Schema اجرایی یا Architecture اجرایی جدید خارج از مالکیت همین Part طراحی یا پیاده‌سازی نکن؛
- هیچ Decision را تصویب، هیچ Source را Normative و هیچ Stage را Approved یا Frozen اعلام نکن؛
- کد، تست، فایل پروژه، Repository، Branch، Commit، Pull Request، Database، Infrastructure یا Configuration ایجاد یا تغییر نده؛
- Command، Query واقعی، Workflow Run، Tool Call، Browse، Search، External Retrieval، Build، Migration، Release، Deployment، Pilot، Production یا Project Freeze اجرا نکن؛
- Dependency، Model، Runtime، Framework، Broker، Provider، Plugin یا Tool نصب، فعال یا متصل نکن؛
- هیچ Approval، AuthorizationDecision، ExecutionLease، Credential، Budget Authorization، Risk Acceptance یا External Effect ایجاد نکن؛
- هیچ داده‌ای را به External System ارسال، Export، Delete، Mutate یا منتشر نکن؛
- `LITE`، `STANDARD` یا `FULL` را به مجوز اجرا تبدیل نکن؛
- `DENY` یا `APR-X` را با Escalation، Human Mediation، Emergency، Waiver یا Successor دور نزن؛
- هیچ مسیر Spacecraft Command، Telecommand، Uplink، Flight Control یا Autonomous Maneuver Execution ایجاد، مدل یا فعال نکن؛
- توصیه یا گام بعدی اجرایی برای شروع توسعه ارائه نکن.

P05-REQ-002 — پس از دریافت سالم این قسمت فقط این چهار کار مجاز است:

1. متن را Parse و در Context جاری حفظ کن؛
2. پیوستگی `P01 → P02 → P03 → P04 → P05 → P06`، Header، Start Anchor، End Anchor، Source Binding و Footer را از روی Parts دریافت‌شده کنترل کن؛
3. هیچ تحلیل یکپارچه، طراحی جدید خارج از مالکیت، پیاده‌سازی یا اقدام ابزاری انجام نده؛
4. فقط پاسخ ثابت انتهای همین Part را بدون هیچ متن قبل یا بعد برگردان.

P05-FAIL-001 — اگر دریافت ناقص، بریده، خارج از ترتیب یا متعارض بود، موفقیت را جعل نکن و فقط پاسخ زیر را با ایراد دقیق در براکت ارائه کن:

~~~text
دریافت قسمت ۰۵ از ۱۸ ابرپرامپت نهایی CSIP-EO کامل و معتبر نبود.
وضعیت: PART_TRUNCATED_OR_CONFLICTED — CONTEXT_NOT_ACTIVATED
مورد لازم برای اصلاح: [ایراد دقیق]
هیچ تحلیل، طراحی جدید، پیاده‌سازی یا اقدام اجرایی آغاز نمی‌شود.
~~~

P05-REQ-003 — سکوت، تأخیر کاربر، دریافت‌نشدن قسمت ۰۶ یا آگاهی از عنوان آن مجوز ادامۀ خودکار نیست. تا ارسال واقعی Part بعدی در وضعیت انتظار باقی بمان.

### 0.1 نقش این قسمت در بستۀ ۱۸ قسمتی

این قسمت مالک معنایی موارد زیر است:

- Taxonomy قطعی طراحی برای Effectهای `E0..E9`؛
- Truth Contract برای Actual، Direct، Indirect، Transitive و Aggregated Effect؛
- Taxonomy قطعی طراحی برای `APR-0..APR-4` و `APR-X`؛
- Exact Approval Binding، Scope، Digest، Validity، Consumption و Revocation؛
- Taxonomy قطعی طراحی برای `PERM-A..PERM-E`؛
- Taxonomy قطعی طراحی برای `AUT-0..AUT-5` و Migration کنترل‌شدۀ `A0..A5`؛
- استقلال Effect، Approval، Permission، Autonomy، AuthorizationDecision و ExecutionLease؛
- Fail-closed Intersection تمام محورهای Authority؛
- Cost/Risk Admission در مرز Authority، بدون ادغام Budget Authorization و Risk Acceptance؛
- Routing و Tailoring قطعی طراحی برای `LITE`، `STANDARD`، `FULL` و `DENY`؛
- Aggregation، Reclassification، Escalation و Profile-downgrade Prevention؛
- Authority Classification Recordها و Event Implicationهای این حوزه، بدون بازتعریف Base Canonical Event Envelope.

P05-CON-001 — مالکیت این قسمت فقط Taxonomyها و Admission/Report-routing بالا است. Project Identity، Scope، Base Canonical Event Envelope و Global Invariantها متعلق به P01؛ Stage/Decision/Gate Protocol متعلق به P02؛ Query/ApplicationCommand/Approval/AuthorizationDecision/ExecutionLease/Receipt/Outcome Record Semantics متعلق به P03؛ Workflow/Human Checkpoint/State/Recovery Semantics متعلق به P04؛ Scientific Truth متعلق به P06؛ AI/RAG/Memory Boundary متعلق به P07؛ Capability/Tool Qualification متعلق به P08؛ Data Lifecycle و Canonical Data Classification متعلق به P10؛ Security/Privacy Controls متعلق به P11؛ Cost Telemetry و Evidence/Observability متعلق به P12؛ Verification Method متعلق به P13؛ Environment/Deployment Contract متعلق به P14؛ Governance/Risk Authority متعلق به P16؛ و Compilation/Conflict Disposition متعلق به P18 باقی می‌مانند.

P05-DEN-004 — این Part نباید Recordهای P03، Stateهای P04، Algorithmهای علمی P06، AI Authority، Capability Qualification، Data-classification Policy، Security Mechanism، FinOps Ledger، Test Oracle، Environment Promotion Gate یا Risk-governance Constitution رقیب تعریف کند.

### 0.2 رابطۀ این قسمت با Parts قبلی و بعدی

P05-CON-002 — این قسمت هویت پروژه، Scope، Permanent Prohibition، TemporalStamp، Canonical Entity و Base Event Envelope را از P01؛ Stage/Decision/Action/Gate Protocol را از P02؛ Invocation و Record Separation را از P03؛ و Workflow/Human-control/Report-routing Context را از P04 مصرف می‌کند و حق تعریف رقیب برای آن‌ها ندارد.

P05-CON-003 — این قسمت Authority Contract را به Parts پایین‌دست تحویل می‌دهد:

- P06 باید هر Scientific Computation، Promotion و Verification Path را به Effect/Approval/Permission/Autonomy و Report Profile این Part Bind کند، بدون انتقال Scientific Truth به P05؛
- P07 باید AI را Advisory نگه دارد و هیچ Approval، Permission، Risk Acceptance، Budget Authority یا Execution Right از Model Output استنتاج نکند؛
- P08 باید Capability و Transitive Dependency Graph را برای Server-side Effect Classification قابل‌حل کند؛
- P09 تا P17 باید هر Effectful Concept را به Intersection این Part Bind کنند؛
- P18 باید Trace و Conflict را Compile کند و Taxonomy این Part را بازنویسی نکند.

## 1. هویت منبع، وضعیت و محدودیت تاریخی

P05-DEF-001 — مالک معنایی این قسمت:

- Artifact ID: `CSIP-EO-RS-STAGE-19`
- Version: `0.1.0-reconstituted-draft`
- SHA-256: `30525213394593910a4bb0406ba3eb2ee784ddae05170933cea1a033654d8731`
- Status: `RECONSTITUTED_DRAFT — REVIEW_READY — NOT_APPROVED — NOT_FROZEN`
- Successor candidate of: `CSIP-EO-STAGE-19`
- Historical source state: `MISSING_NORMATIVE_ARTIFACT`
- Title status: `RECONSTITUTED_SUCCESSOR_TITLE`
- Domain scope: `EARTH_ORBIT_ONLY`
- Deployment baseline: `TERRESTRIAL_BASELINE — ON_ORBIT_RUNTIME_DEFERRED`

START>>>
CSIP_EO_PROMPT_PACKAGE_ID: CSIP-EO-FINAL-MASTER-SUPERPROMPT-18P
CSIP_EO_PROMPT_PACKAGE_VERSION: 0.9.0-draft
PART_ID: CSIP-EO-FMSP-P05
PART_INDEX: 05
PART_COUNT: 18
PART_TITLE: Effect, Approval, Permission and Autonomy Taxonomy | طبقه‌بندی Effect، Approval، Permission و Autonomy
SEMANTIC_OWNER_ARTIFACT_ID: CSIP-EO-RS-STAGE-19
SEMANTIC_OWNER_VERSION: 0.1.0-reconstituted-draft
SEMANTIC_OWNER_STATUS: RECONSTITUTED_DRAFT — REVIEW_READY — NOT_APPROVED — NOT_FROZEN
SEMANTIC_OWNER_SHA256: 30525213394593910a4bb0406ba3eb2ee784ddae05170933cea1a033654d8731
SUPPORTING_SOURCE_BINDINGS: CSIP-EO-AUDIT-GAP-02/0.1.0-candidate/fa400334a69702bf56e8588210449590573bccd3120d7c2cebd6ba9cc8fc161f; ENTERPRISE-TRUST-RISK-COST-EVIDENCE-REPRODUCIBILITY-MANDATE/verified-input-2026-07-28/1b5e7884a343589312d62259f181bd48f1a12b51e2613685c0d58c747a08dab4; CSIP-EO-PROMPT-ARCH-18P-C1/0.1.0-design-candidate/a4c80b938fccaab5d3d85c780351a41ee3444b4c6712920af45b493afbacb09b; CSIP-EO-GAP-RESOLUTION-MANIFEST-C1/0.1.0-candidate/349b590df9fad00c2e0ec317f4bd0b7ad747a5e22a1fead0f66f28c98e955216
PRIOR_PART_ID: CSIP-EO-FMSP-P04
NEXT_PART_ID: CSIP-EO-FMSP-P06
PART_PAYLOAD_SHA256: SEE_EXTERNAL_PROMPT_PACKAGE_MANIFEST
RECEIVE_MODE: CONTEXT_ONLY
ACTION_AUTHORITY: NONE

# پرامپت قسمت ۰۵ از ابرپرامپت نهایی ۱۸ قسمتی CSIP-EO
# طبقه‌بندی Effect، Approval، Permission و Autonomy

## 0. دستور دریافت، مرز این قسمت و قفل ضدتوهم

این پیام فقط «قسمت ۰۵ از ۱۸» یک زمینۀ مرجع به‌هم‌پیوسته است. قسمت‌های ۰۱، ۰۲، ۰۳ و ۰۴ باید پیش از این قسمت و به‌ترتیب دریافت شده باشند. قسمت‌های ۰۶ تا ۱۸ هنوز در این پیام وجود ندارند. دریافت این قسمت فقط Context مربوط به طبقه‌بندی Effect، Approval، Permission، Autonomy و Report Profile را گسترش می‌دهد و هیچ اختیار علمی، حقوقی، امنیتی، مالی، اجرایی یا عملیاتی ایجاد نمی‌کند.

P05-REQ-001 — هنگام دریافت این قسمت، وضعیت داخلی خود را دقیقاً چنین در نظر بگیر:

`RECEIVING_P05 — P01_P02_P03_P04_REQUIRED — CONTEXT_INCOMPLETE — ACTION_AUTHORITY_NONE`

P05-DEN-001 — اگر قسمت ۰۱، ۰۲، ۰۳ یا ۰۴ دریافت نشده، ترتیب `P01 → P02 → P03 → P04 → P05` قابل‌اثبات نیست، یا Header، Anchor، Source Binding، Footer یا Pointerهای این قسمت ناقص یا متعارض‌اند، این قسمت را فعال نکن و موفقیت دریافت را جعل نکن.

P05-DEN-002 — از این Part برای حدس‌زدن، بازسازی، تکمیل یا جعل محتوای قسمت‌های ۰۶ تا ۱۸ استفاده نکن. دانستن عنوان، Semantic Owner، Version، Status یا Digest یک Part بعدی مجوز ساخت محتوای غایب آن نیست.

P05-DEN-003 — تا پیش از دریافت و مونتاژ معتبر هر ۱۸ قسمت، تحت هیچ شرایطی:

- تحلیل یکپارچۀ کل CSIP-EO ارائه نکن؛
- P06 یا هیچ Part بعدی را آغاز یا تولید نکن؛
- Taxonomy، Policy، Approval Service، Authorization Engine، Capability، Workflow، Schema اجرایی یا Architecture اجرایی جدید خارج از مالکیت همین Part طراحی یا پیاده‌سازی نکن؛
- هیچ Decision را تصویب، هیچ Source را Normative و هیچ Stage را Approved یا Frozen اعلام نکن؛
- کد، تست، فایل پروژه، Repository، Branch، Commit، Pull Request، Database، Infrastructure یا Configuration ایجاد یا تغییر نده؛
- Command، Query واقعی، Workflow Run، Tool Call، Browse، Search، External Retrieval، Build، Migration، Release، Deployment، Pilot، Production یا Project Freeze اجرا نکن؛
- Dependency، Model، Runtime، Framework، Broker، Provider، Plugin یا Tool نصب، فعال یا متصل نکن؛
- هیچ Approval، AuthorizationDecision، ExecutionLease، Credential، Budget Authorization، Risk Acceptance یا External Effect ایجاد نکن؛
- هیچ داده‌ای را به External System ارسال، Export، Delete، Mutate یا منتشر نکن؛
- `LITE`، `STANDARD` یا `FULL` را به مجوز اجرا تبدیل نکن؛
- `DENY` یا `APR-X` را با Escalation، Human Mediation، Emergency، Waiver یا Successor دور نزن؛
- هیچ مسیر Spacecraft Command، Telecommand، Uplink، Flight Control یا Autonomous Maneuver Execution ایجاد، مدل یا فعال نکن؛
- توصیه یا گام بعدی اجرایی برای شروع توسعه ارائه نکن.

P05-REQ-002 — پس از دریافت سالم این قسمت فقط این چهار کار مجاز است:

1. متن را Parse و در Context جاری حفظ کن؛
2. پیوستگی `P01 → P02 → P03 → P04 → P05 → P06`، Header، Start Anchor، End Anchor، Source Binding و Footer را از روی Parts دریافت‌شده کنترل کن؛
3. هیچ تحلیل یکپارچه، طراحی جدید خارج از مالکیت، پیاده‌سازی یا اقدام ابزاری انجام نده؛
4. فقط پاسخ ثابت انتهای همین Part را بدون هیچ متن قبل یا بعد برگردان.

P05-FAIL-001 — اگر دریافت ناقص، بریده، خارج از ترتیب یا متعارض بود، موفقیت را جعل نکن و فقط پاسخ زیر را با ایراد دقیق در براکت ارائه کن:

~~~text
دریافت قسمت ۰۵ از ۱۸ ابرپرامپت نهایی CSIP-EO کامل و معتبر نبود.
وضعیت: PART_TRUNCATED_OR_CONFLICTED — CONTEXT_NOT_ACTIVATED
مورد لازم برای اصلاح: [ایراد دقیق]
هیچ تحلیل، طراحی جدید، پیاده‌سازی یا اقدام اجرایی آغاز نمی‌شود.
~~~

P05-REQ-003 — سکوت، تأخیر کاربر، دریافت‌نشدن قسمت ۰۶ یا آگاهی از عنوان آن مجوز ادامۀ خودکار نیست. تا ارسال واقعی Part بعدی در وضعیت انتظار باقی بمان.

### 0.1 نقش این قسمت در بستۀ ۱۸ قسمتی

این قسمت مالک معنایی موارد زیر است:

- Taxonomy قطعی طراحی برای Effectهای `E0..E9`؛
- Truth Contract برای Actual، Direct، Indirect، Transitive و Aggregated Effect؛
- Taxonomy قطعی طراحی برای `APR-0..APR-4` و `APR-X`؛
- Exact Approval Binding، Scope، Digest، Validity، Consumption و Revocation؛
- Taxonomy قطعی طراحی برای `PERM-A..PERM-E`؛
- Taxonomy قطعی طراحی برای `AUT-0..AUT-5` و Migration کنترل‌شدۀ `A0..A5`؛
- استقلال Effect، Approval، Permission، Autonomy، AuthorizationDecision و ExecutionLease؛
- Fail-closed Intersection تمام محورهای Authority؛
- Cost/Risk Admission در مرز Authority، بدون ادغام Budget Authorization و Risk Acceptance؛
- Routing و Tailoring قطعی طراحی برای `LITE`، `STANDARD`، `FULL` و `DENY`؛
- Aggregation، Reclassification، Escalation و Profile-downgrade Prevention؛
- Authority Classification Recordها و Event Implicationهای این حوزه، بدون بازتعریف Base Canonical Event Envelope.

P05-CON-001 — مالکیت این قسمت فقط Taxonomyها و Admission/Report-routing بالا است. Project Identity، Scope، Base Canonical Event Envelope و Global Invariantها متعلق به P01؛ Stage/Decision/Gate Protocol متعلق به P02؛ Query/ApplicationCommand/Approval/AuthorizationDecision/ExecutionLease/Receipt/Outcome Record Semantics متعلق به P03؛ Workflow/Human Checkpoint/State/Recovery Semantics متعلق به P04؛ Scientific Truth متعلق به P06؛ AI/RAG/Memory Boundary متعلق به P07؛ Capability/Tool Qualification متعلق به P08؛ Data Lifecycle و Canonical Data Classification متعلق به P10؛ Security/Privacy Controls متعلق به P11؛ Cost Telemetry و Evidence/Observability متعلق به P12؛ Verification Method متعلق به P13؛ Environment/Deployment Contract متعلق به P14؛ Governance/Risk Authority متعلق به P16؛ و Compilation/Conflict Disposition متعلق به P18 باقی می‌مانند.

P05-DEN-004 — این Part نباید Recordهای P03، Stateهای P04، Algorithmهای علمی P06، AI Authority، Capability Qualification، Data-classification Policy، Security Mechanism، FinOps Ledger، Test Oracle، Environment Promotion Gate یا Risk-governance Constitution رقیب تعریف کند.

### 0.2 رابطۀ این قسمت با Parts قبلی و بعدی

P05-CON-002 — این قسمت هویت پروژه، Scope، Permanent Prohibition، TemporalStamp، Canonical Entity و Base Event Envelope را از P01؛ Stage/Decision/Action/Gate Protocol را از P02؛ Invocation و Record Separation را از P03؛ و Workflow/Human-control/Report-routing Context را از P04 مصرف می‌کند و حق تعریف رقیب برای آن‌ها ندارد.

P05-CON-003 — این قسمت Authority Contract را به Parts پایین‌دست تحویل می‌دهد:

- P06 باید هر Scientific Computation، Promotion و Verification Path را به Effect/Approval/Permission/Autonomy و Report Profile این Part Bind کند، بدون انتقال Scientific Truth به P05؛
- P07 باید AI را Advisory نگه دارد و هیچ Approval، Permission، Risk Acceptance، Budget Authority یا Execution Right از Model Output استنتاج نکند؛
- P08 باید Capability و Transitive Dependency Graph را برای Server-side Effect Classification قابل‌حل کند؛
- P09 تا P17 باید هر Effectful Concept را به Intersection این Part Bind کنند؛
- P18 باید Trace و Conflict را Compile کند و Taxonomy این Part را بازنویسی نکند.

## 1. هویت منبع، وضعیت و محدودیت تاریخی

P05-DEF-001 — مالک معنایی این قسمت:

- Artifact ID: `CSIP-EO-RS-STAGE-19`
- Version: `0.1.0-reconstituted-draft`
- SHA-256: `30525213394593910a4bb0406ba3eb2ee784ddae05170933cea1a033654d8731`
- Status: `RECONSTITUTED_DRAFT — REVIEW_READY — NOT_APPROVED — NOT_FROZEN`
- Successor candidate of: `CSIP-EO-STAGE-19`
- Historical source state: `MISSING_NORMATIVE_ARTIFACT`
- Title status: `RECONSTITUTED_SUCCESSOR_TITLE`
- Domain scope: `EARTH_ORBIT_ONLY`
- Deployment baseline: `TERRESTRIAL_BASELINE — ON_ORBIT_RUNTIME_DEFERRED`

P05-DEN-005 — Stage 19 تاریخی فقط به‌صورت Downstream-attested مالک `E0..E9` و `APR-0..APR-X` شناخته شده بود؛ Bytes و تعریف‌های دقیق تاریخی آن در دسترس نیست. این Artifact یک Successor Candidate تازه‌تألیف‌شده است و هرگز نباید «Stage 19 تاریخی بازیابی‌شده» یا «Stage 19 تصویب‌شده» معرفی شود.

P05-CON-004 — هویت هر Source با ترکیب زیر تعیین می‌شود:

`Artifact ID + Exact Version + Exact SHA-256 + Status`

Filename، Directory، تاریخ جدیدتر، متن طولانی‌تر، Duplicate متفاوت، ترجمه، Summary، Retrieval Result، Memory یا Model Output به‌تنهایی Source Identity، Supersession یا Approval ایجاد نمی‌کند.

P05-CON-005 — Sourceهای پشتیبان این Part فقط Overlay، Mandate، Assembly Contract، Manifest و Contracts بالادست P01 تا P04 هستند. آن‌ها Semantic Owner را جایگزین نمی‌کنند، Approval تازه نمی‌سازند و فقط در Scope و Status ثبت‌شدۀ خود قابل‌استفاده‌اند.

P05-CON-006 — Statusهای Source پشتیبان باید دقیقاً حفظ شوند:

- `CSIP-EO-AUDIT-GAP-02 / 0.1.0-candidate`: `CANDIDATE — REVIEW_READY — NON_NORMATIVE_UNTIL_DIGEST_BOUND_APPROVAL`؛
- `ENTERPRISE-TRUST-RISK-COST-EVIDENCE-REPRODUCIBILITY-MANDATE / verified-input-2026-07-28`: `PRESENT_VERIFIED_BYTES / SUPPLEMENTAL_CROSS_CUTTING_INPUT`؛
- `CSIP-EO-PROMPT-ARCH-18P-C1 / 0.1.0-design-candidate`: `DESIGN_CANDIDATE — REVIEW_READY — NOT_APPROVED — NOT_FROZEN`؛
- `CSIP-EO-GAP-RESOLUTION-MANIFEST-C1 / 0.1.0-candidate`: `REVIEW_READY_NOT_APPROVED`.

P05-CON-007 — پذیرش این Part برای Assembly فقط `PART_ACCEPTED_FOR_ASSEMBLY` ایجاد می‌کند. این پذیرش Status منبع `RECONSTITUTED_DRAFT`، Decisionهای `PROPOSED` یا Gateهای Implementation، Verification، Validation، Qualification، Release، Deployment، Operation و Freeze را ارتقا نمی‌دهد.

P05-FAIL-002 — اگر Version، Digest، Status یا Owner Binding منبع با Header، Canonical Map یا Manifest متعارض باشد، نتیجه `SOURCE_BINDING_CONFLICT — PART_NOT_ACCEPTED` است تا تعارض در Part مالک حل شود. قاعدۀ «نسخۀ جدیدتر یا طولانی‌تر برنده است» ممنوع است.

## 2. Objective، Scope، Exclusion و اصول تغییرناپذیر Authority

P05-REQ-004 — Objective این قسمت تعریف یک Contract دقیق، Server-computed، Source-bound و Fail-closed است تا هیچ Client، Model، Agent، Workflow، Plugin، Tool، Human Label یا Transport نتواند Effect واقعی را کاهش دهد، Approval را جعل یا تعمیم دهد، Permission را با Approval ادغام کند، Autonomy را Authority بداند یا از Report Profile برای ایجاد مجوز استفاده کند.

P05-REQ-005 — Scope این Part حداقل شامل موارد زیر است:

1. `E0..E9` و Actual/Transitive/Aggregated Effect Truth؛
2. `APR-0..APR-4/APR-X` و Exact Approval Binding؛
3. `PERM-A..PERM-E` و Actor-domain/Competence Boundary؛
4. `AUT-0..AUT-5` و رد برچسب مبهم `A*`؛
5. استقلال کامل شش محور Effect، Approval، Permission، Autonomy، AuthorizationDecision و ExecutionLease؛
6. Intersection با Risk Tier، Data Class، Environment Class، Cost Exposure و Irreversibility؛
7. Cost/Risk Admission و استقلال Budget Authorization، Security Authorization و Risk Acceptance؛
8. `LITE/STANDARD/FULL/DENY` همراه Trigger، Exact Sections، Aggregation و Escalation؛
9. Record، Lifecycle، Event، Failure، Unknown، Degraded و Verification Implicationهای Authority.

P05-REQ-006 — Exclusionهای صریح این Part:

- تعریف Scientific Validity، Numerical Algorithm، Covariance، Threshold یا Scientific Approval؛
- تعریف AI Model Lifecycle، RAG/Memory Truth یا Model Qualification؛
- تعریف Capability Descriptor، Plugin Runtime یا Tool Sandbox؛
- تعریف Canonical Data-class Vocabulary نهایی یا Retention/Deletion Policy؛
- تعریف Security Protocol، Authentication Mechanism، Cryptographic Scheme یا Secret Handling Implementation؛
- تعریف Cost Price، Currency، Budget Amount، Provider Rate یا Organizational Budget Hierarchy نهایی؛
- تعریف Risk Appetite، Tolerance، Capacity، Risk Methodology یا Risk Owner واقعی سازمانی؛
- تعریف Environment Promotion، Deployment Technology یا Production Topology؛
- اجرای Approval، Authorization، Lease، Effect، Test، Spend، Deployment یا Production.

P05-INV-001 — اصل مرکزی این Part:

`classification constrains authority; classification never manufactures authority`

P05-INV-002 — تصمیم مؤثر همیشه از سخت‌گیرانه‌ترین Intersection تمام کنترل‌های Applicable به‌دست می‌آید:

`effective_decision = most_restrictive(applicable controls)`

P05-INV-003 — هیچ محور permissive نمی‌تواند محور restrictive را Override کند. Effect پایین، Permission بالا، Approval موجود، Budget کافی، Risk Acceptance، Human Presence، Admin Role، Green Test یا `FULL` Report هیچ‌کدام به‌تنهایی Execution را مجاز نمی‌کنند.

P05-CON-008 — Missing، Stale، Expired، Revoked، Unverified، Unsupported یا Conflicting Classification باید صریح حفظ شود و برای Effectful Work نتیجه `DENY / DO_NOT_EXECUTE` ایجاد کند.

P05-DEN-006 — Client، Model، Agent، Tool، Plugin، Workflow Author، Executor یا Approver حق تعیین قطعی Effect، Permission، Autonomy Ceiling یا Report Profile خود را ندارد.

P05-DEN-007 — Self-approval، Self-authorization، Self-issued Lease، Self-assigned Competence، Self-accepted Risk، Self-raised Budget یا Self-lowered Classification ممنوع است.

P05-DEN-008 — هیچ Approval، Permission، AuthorizationDecision، Lease، Profile یا Emergency Mode نمی‌تواند `E9/APR-X` را کاهش دهد یا برای آن Exit بسازد.

P05-DEN-009 — عبارت‌هایی مانند `read-only`، `dry-run`، `simulation`، `safe`، `internal`، `admin`، `human-approved`، `AI-guarded`، `temporary`، `reversible` یا `no-cost` بدون Evidence و Classification Server-side اثر واقعی را کاهش نمی‌دهند.

P05-DEN-010 — Benefit، Deadline، Availability Pressure، Commercial Priority، Scientific Interest، User Request یا Executive Preference نمی‌تواند Hard Legal/Safety/Privacy/Security/Command Prohibition را Trade-off کند.

P05-DEN-011 — Completeness متن این Part یا عبور از کنترل داخلی فایل به معنی Approval، Normative Activation، Implementation، Verification، Qualification، Production Readiness یا Freeze نیست.

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

P05-CON-009 — تکرار این کپسول Safety Checksum است؛ مالکیت مبانی را از P01 منتقل نمی‌کند و Approval جدیدی ایجاد نمی‌نماید.

## 4. واژگان Canonical، محورهای مستقل و جداسازی Recordها

P05-DEF-002 — `Effect` بیشینۀ پیامد واقعی، ممکن و Commit‌شدنی یک Action در Scope دقیق است، شامل پیامد مستقیم، غیرمستقیم، Transitive، Aggregated، Retry، Child، External، Cost، Data، Governance و Recovery.

P05-DEF-003 — `Actual Effect` اثری است که از رفتار واقعی Operation، Target، Dependency و Environment به‌دست می‌آید؛ نه از نام Endpoint، HTTP Verb، UI Label، Client Claim، Model Output یا Desired Outcome.

P05-DEF-004 — `Transitive Effect` بیشینۀ اثر تمام Nodeها و Edgeهای Dependency/Invocation Graph است که Action می‌تواند مستقیم یا غیرمستقیم فعال کند، از جمله Nested Tool، Adapter، Callback، Retry، Child Workflow، Provider، Egress، Credential، Compensation و Recovery.

P05-DEF-005 — `Aggregated Effect` اثر ترکیبی روی تمام Targetها، Tenantها، Batchها، Childها، Attemptها، زمان‌ها و Shared Dependencyهاست؛ مجموعۀ Effectهای ظاهراً کوچک ممکن است Class بالاتری ایجاد کند.

P05-DEF-006 — `Approval Class` حداقل سطح Consent، Competence، Independence و Governance لازم برای Request دقیق است؛ Approval Class نه Permission دائمی است و نه Execution.

P05-DEF-007 — `Permission Class` حوزۀ عملی است که Actor در Role/Domain/Scope مشخص حق انجام یا بررسی آن را دارد؛ Permission شدت Effect، Approval موردنیاز یا Autonomy را تعیین نمی‌کند.

P05-DEF-008 — `Autonomy Profile` سقف فنی و حاکمیتی برای میزان Attempt خودکار در Envelope تصویب‌شده است؛ Autonomy نه Permission، نه Approval و نه AuthorizationDecision است.

P05-DEF-009 — `AuthorizationDecision` نتیجۀ Policy-bound برای Actor، Action، Resource، Tenant، Purpose، Environment و Context دقیق است؛ Semantics Record متعلق به P03 است و این Part فقط ورودی‌های Taxonomy آن را تعیین می‌کند.

P05-DEF-010 — `ExecutionLease` حق کوتاه‌عمر، کمینه، Scope-bound، Digest-bound، Nonce-bound و Revocable برای Attempt دقیق است؛ Semantics Record متعلق به P03 است و این Part هیچ Lease صادر نمی‌کند.

P05-DEF-011 — `Execution` Attempt واقعی Operation است و باید از Approval، AuthorizationDecision و Lease جدا بماند.

P05-DEF-012 — `ExecutionReceipt` Evidence یک Attempt و Effect State مشاهده‌شده است؛ Receipt به‌تنهایی Success یا Outcome نیست.

P05-DEF-013 — `Outcome` نتیجه‌ای است که پس از Validation یا Reconciliation نسبت به Intended Transition و Acceptance Rule تعیین می‌شود؛ Outcome از Approval، Lease یا Receipt استنتاج نمی‌شود.

P05-DEF-014 — `BudgetAuthorization` موافقت Finance/Budget Authority با Cost Scope، Ceiling، Reservation و Conditions دقیق است؛ BudgetAuthorization نه Risk Acceptance است و نه Security/Execution Authorization.

P05-DEF-015 — `RiskAcceptance` تصمیم صلاحیت‌دار، Scope-bound، Evidence-linked، Time-bound و Revocable برای Residual Risk مشخص در Limits معتبر است؛ RiskAcceptance نه BudgetAuthorization است و نه Execution Permission.

P05-DEF-016 — `ReportProfile` میزان حداقلی محتوای Report پیش از Change/Effect است؛ Profile یک Documentation/Admission Obligation است و هیچ Authority، Approval یا Lease ایجاد نمی‌کند.

P05-INV-004 — محورهای زیر مستقل و غیرقابل‌ادغام‌اند:

| محور | پرسش محدود |
|---|---|
| `E0..E9` | چه Effect واقعی و Transitive ممکن است رخ دهد؟ |
| `APR-0..APR-4/APR-X` | حداقل چه Approvalی لازم است یا آیا هیچ Approval Route وجود ندارد؟ |
| `PERM-A..PERM-E` | Actor در کدام Domain و Scope مجاز است؟ |
| `AUT-0..AUT-5` | سقف Attempt خودکار چیست؟ |
| AuthorizationDecision | آیا Policy برای Request دقیق Allow/Constrain/Deny می‌کند؟ |
| ExecutionLease | آیا حق کوتاه‌عمر برای همین Attempt دقیق صادر شده است؟ |
| Risk Tier/Status | Exposure و Acceptance Requirement چیست؟ |
| Data Class | چه Sensitivity، Rights، Purpose و Residency Constraints وجود دارد؟ |
| Environment Class | Effect در کدام Environment مجاز است؟ |
| Cost Exposure | چه Commitment ثابت، محدود، متغیر یا مادی ممکن است رخ دهد؟ |
| Irreversibility | State چگونه Revert، Compensate، Recover یا Destroy می‌شود؟ |

P05-CON-010 — یک Request فقط وقتی Candidate اجراست که تمام محورهای Applicable به‌طور مستقل Resolve و سپس Intersect شوند. عدم Applicability باید با Predicate و Source اثبات شود؛ Field خالی مساوی `NOT_APPLICABLE` نیست.

P05-CON-011 — Approval می‌تواند شرط لازم باشد اما کافی نیست. Permission می‌تواند موجود باشد اما بدون Approval/Authorization/Lease کافی نیست. Lease می‌تواند معتبر باشد اما با Revocation، Effect Escalation، Target Revision Change یا Risk/Cost Breach باید Block شود.

P05-CON-012 — Decision، Approval، AuthorizationDecision، RiskAcceptance، BudgetAuthorization، ExecutionLease، Execution، Receipt و Outcome باید Recordهای مستقل، Immutable-history و Link‌شده باقی بمانند.

P05-CON-013 — یک Record می‌تواند Reference Record دیگر را حمل کند؛ نمی‌تواند Semantics، Authority یا Lifecycle آن را جذب کند. UI Merge، Database Join، Workflow Grouping یا Single Form جداسازی معنایی را حذف نمی‌کند.

P05-CON-014 — `approved` بدون Subject Type مبهم است. هر نمایش باید روشن کند Approval متعلق به Request، Design، Risk، Budget، Data Use، Release، Deployment یا مورد دیگری است.

P05-CON-015 — `authorized` بدون Actor، Action، Target، Scope، Environment، Purpose، Policy Version، Time Window و Conditions معتبر نیست.

P05-CON-016 — `permitted` بدون Domain، Role، Competence، Tenant، Resource و Operation Scope معتبر نیست.

P05-CON-017 — `autonomous` بدون Profile، Capability، Data/Environment Boundary، Effect Ceiling، Cost/Risk Bound و Kill/Revocation Behavior معتبر نیست.

P05-CON-018 — `human-in-the-loop` فقط Description است. Human Authority معتبر به Identity، Competence، Independence، Exact Presentation Digest، Scope، Decision، Conditions، Timestamp و Expiry نیاز دارد.

P05-CON-019 — `admin`، `owner`، `service account`، `system`، `operator` یا `governing authority` Label به‌تنهایی Approval، Competence، Permission یا Lease نیست.

P05-CON-020 — Integrity Evidence مانند Digest یا Signature می‌تواند Fixity/Origin را پشتیبانی کند؛ Correctness، Competence، Approval Validity، Policy Allow، Scientific Truth یا Outcome را به‌تنهایی ثابت نمی‌کند.

P05-DEN-012 — هیچ Mapping مستقیم و کلی مانند `E3 = APR-1`، `PERM-D = AUT-4` یا `FULL = ALLOW` خارج از Matrix Floor و Context دقیق مجاز نیست.

P05-DEN-013 — Recommendation، Plan، Draft، Model Output، Agent Consensus، Risk Score، Budget Remaining، Policy Cache، Prior Success یا Workflow State نباید Approval/Authorization/Lease ضمنی ایجاد کند.

P05-DEN-014 — Absence of Denial، Silence، Timeout، Unavailability، Missing Reviewer، Lack of Objection یا Approval Fatigue مساوی Consent نیست.

P05-DEN-015 — Event، Queue Ack، Callback، HTTP Success، Tool Return، Commit، Deployment Receipt یا Log Entry به‌تنهایی Outcome یا Authority نیست.

P05-DEN-016 — هیچ Record Aggregator، Dashboard، Report یا Agent Memory حق ندارد Missing Record را با Summary یا Inference جایگزین کند.

P05-FAIL-003 — اگر نوع Record، Authority Owner، Scope، Link Identity یا Lifecycle State نامعلوم یا متعارض باشد، نتیجه `SEMANTIC_AUTHORITY_BOUNDARY_INDETERMINATE — DO_NOT_EXECUTE` است.

## 5. Effect Taxonomy — `E0` تا `E9`

P05-REQ-007 — Effect باید Server-side از بیشینۀ پیامد واقعی و Transitive محاسبه شود و حداقل Taxonomy زیر را بدون کاهش معنایی حفظ کند:

| Effect | معنای Canonical | مثال‌های محدود | حداقل Handling |
|---:|---|---|---|
| `E0` | Passive public/static read یا Ephemeral Analysis؛ بدون Authenticated Sensitive Access، Durable Authoritative Write، Egress Side Effect یا Cost فراتر از Preapproved Negligible Envelope | خواندن Baseline عمومی؛ محاسبۀ محلی روی متن غیرحساس ارائه‌شده | Policy Check؛ Audit متناسب با Scope |
| `E1` | Scoped authenticated low-risk read یا Reversible Local Workspace Record بدون Authoritative Promotion | خواندن Posture کم‌ریسک خود؛ ذخیرۀ Draft محلی | Identity/Purpose Binding؛ Reversible Record |
| `E2` | Controlled internal/sensitive read یا ایجاد Proposal، Finding، Metadata یا Memory Proposal غیرAuthoritative | Internal Read؛ Invocation Proposal؛ Threat Draft | Data Policy؛ ممنوعیت Automatic Promotion |
| `E3` | Bounded، Idempotent و Reversible Operational Effect با Blast Radius پایین و بدون Material Production/Scientific/Governance Promotion | Session Issue/Revoke عادی؛ Isolated Projection Rebuild؛ Advisory Publication کنترل‌شده | Explicit Predicate؛ Receipt؛ Rollback/Compensation |
| `E4` | Authoritative Ordinary State، Role، Policy-record، Governance-record یا Controlled Promotion Effect | Entitlement Change عادی؛ Canonical Revision Activation؛ Roadmap Approval | Scoped Human/Policy Approval و Evidence |
| `E5` | Material Configuration، Schema، Workflow، Provider، Baseline، Data یا Cost Change با Cross-component Consequence معنادار | Index/Schema Change؛ Descriptor Registration؛ Material Risk Acceptance؛ Procurement Proposal/Commitment | Multi-domain Review متناسب |
| `E6` | Sensitive، Privileged، Externally Connected، Variable-cost، Egress، Code-execution، Deployment-enablement یا External-pilot Effect | Privileged Grant؛ Plugin Enablement؛ Live-web Egress؛ External Pilot | Independent Approval؛ Short Lease؛ Security/Data/Risk/Cost Gates |
| `E7` | Production، Bulk، Public-release، Cross-tenant، Legal-hold، Logical-deletion یا High-blast-radius Effect | Production Release؛ Bulk Export؛ Public Dataset؛ Logical Deletion | Executive/Domain Approval؛ Qualification؛ Independent Verification |
| `E8` | Destructive، Irreversible-in-practice، Recovery-affecting یا Cryptographic/Physical Destruction Effect | Physical Purge؛ Backup Expiry؛ Key Destruction؛ Media Sanitization؛ Irreversible Migration | Exceptional Digest-bound Multi-role Approval؛ Dual Control؛ Fencing؛ Recovery Evidence |
| `E9` | هر مسیر مستقیم، غیرمستقیم، Generic، Human-mediated یا Enabling برای Spacecraft Command، Telecommand، Uplink یا Flight Control | Route، Schema، Credential، Adapter، Workflow یا Successor Hook | `APR-X / PROHIBITED / HARD_DENY / INC-0` |

P05-CON-021 — Effect Class یک Ordinal ساده برای Average یا جمع جبری نیست؛ `maximum applicable effect` و Amplifierهای مستقل تعیین‌کننده‌اند.

P05-CON-022 — `E0` فقط وقتی معتبر است که نبود Authenticated Sensitive Access، Durable Write، External Effect، Variable Cost، Privileged Path و Hidden Dependency قابل‌اثبات باشد.

P05-CON-023 — Local Draft در `E1` باید واقعاً Reversible، Non-authoritative، Tenant/Purpose-bound و فاقد Promotion ضمنی باشد. Sync، Share، Auto-index، External Backup یا Memory Commit می‌تواند Effect را بالا ببرد.

P05-CON-024 — Sensitive Read در `E2` همچنان Data Policy، Purpose، Minimization، Access Logging و Non-promotion Guard می‌خواهد. Read-only بودن Effect را صفر نمی‌کند.

P05-CON-025 — `E3` فقط وقتی معتبر است که Operation Typed، Idempotent، Bounded، Low-blast-radius و Reversible باشد و Unknown Outcome با Reconciliation مدیریت شود.

P05-CON-026 — `E4` شامل Promotion یا Authoritative Change عادی است؛ عادی‌بودن به معنی بدون Approval یا بدون Evidence نیست.

P05-CON-027 — `E5` با Materiality، Cross-component Consequence یا تغییر Baseline/Schema/Workflow/Provider/Data/Cost فعال می‌شود؛ Non-production Label آن را خودکار به `E3` کاهش نمی‌دهد.

P05-CON-028 — `E6` با هر Sensitive/Privileged/External/Variable-cost/Egress/Code-execution/Deployment-enablement/External-pilot Trigger قابل‌فعال‌شدن است، حتی اگر Direct Write کوچک باشد.

P05-CON-029 — `E7` با Production، Bulk، Public Release، Cross-tenant، Legal Hold، Logical Deletion یا High Blast Radius فعال می‌شود. Cardinality و Audience بخشی از Effect Truth هستند.

P05-CON-030 — `E8` برای Physical/Logical Destruction، Key Loss، Backup Expiry، Irreversible Migration یا Recovery-affecting Change است. ادعای Rollback بدون اثبات Preconditions Class را کاهش نمی‌دهد.

P05-CON-031 — `E9` Global Prohibition است؛ نه «بالاترین سطح مجاز». هیچ Approval Class، Human Role، Risk Acceptance، Budget، Emergency یا External System نمی‌تواند آن را مجاز کند.

P05-CON-032 — یک Event به‌خودی‌خود Execution Effect نیست، اما Consumer آن اگر Action تازه‌ای Trigger کند باید Request، Classification، Policy، Approval و Lease مستقل داشته باشد.

P05-CON-033 — Query فقط وقتی Query می‌ماند که نسبت به Authoritative State و External State هیچ Mutation، Lock مادی، Trigger اجرایی، Cost-bearing Hidden Call یا Egress Effect نداشته باشد.

P05-CON-034 — Compensation، Rollback Attempt، Recovery، Reconciliation Write، Cleanup، Revocation و Containment هرکدام Effect مستقل دارند و باید جداگانه Classify شوند.

P05-CON-035 — Safety Containment که فقط Authority/Exposure را کاهش می‌دهد می‌تواند تحت Preapproved Deny-only Profile اجراپذیر باشد؛ Restoration، Re-enable یا Scope Expansion Effect مستقل و عادی می‌خواهد.

P05-CON-036 — Permission Grant، Policy Change، Budget-ceiling Change، Risk-appetite Change، Evidence Deletion و Audit Disable صرف‌نظر از UI یا Actor Label باید طبق Effect واقعی و حداقل `AUT-5` برای Automation بررسی شوند.

P05-CON-037 — Source Data Read که Provider Training، Retention، External Processing یا Egress ایجاد می‌کند فقط Read نیست؛ Transitive Provider Behavior در Effect لحاظ می‌شود.

P05-CON-038 — Scientific Analysis می‌تواند Effect پایین داشته باشد، اما Scientific-baseline Promotion یا Operational Use Effect و Approval بالاتر می‌خواهد. P05 Scientific Validity را تعیین نمی‌کند.

P05-CON-039 — AI Generation می‌تواند Draft غیرAuthoritative `E0..E2` باشد؛ Model/Prompt/Corpus/Tool Promotion، External Tool Use یا Downstream Effect طبق رفتار واقعی Classify می‌شود.

P05-CON-040 — Default Effect Matrix فقط Floor است. Law، Policy، Data، Risk، Cost، Environment، Target Cardinality، External Exposure یا Irreversibility می‌تواند Handling را سخت‌گیرانه‌تر کند.

P05-DEN-017 — Client-supplied `effect_class`، Capability Description، Model Annotation، Prompt Instruction یا Tool Metadata Source of Truth Effect نیست.

P05-DEN-018 — `dry_run` فقط وقتی Class را پایین نگه می‌دارد که Server اثبات کند هیچ External/Durable/Costly/Privileged Effect یا Hidden Write ممکن نیست.

P05-DEN-019 — خردکردن Bulk، Cross-tenant، Costly یا High-blast-radius Work به Requestهای کوچک برای کاهش Effect ممنوع است.

P05-DEN-020 — Retry، Loop، Recursion، Fan-out، Schedule یا Queue نباید Cardinality/Cost/Blast Radius را از Effect Classification حذف کند.

P05-DEN-021 — Wrapper، Adapter، Plugin، Child Workflow، Human Task، Alternate Account، Archived Version یا External Provider نباید Effect واقعی را پنهان کند.

P05-DEN-022 — Reversible Label بدون State Snapshot، Preconditions، Tested Method، Authority، Deadline و Evidence معتبر نیست.

P05-DEN-023 — Compensation Possibility به معنی Reversibility نیست و Effect اصلی را کاهش نمی‌دهد.

P05-DEN-024 — `E9` نباید به `E8`، `AUT-5`، `APR-4`، Human-only یا External-system-owned Reclassify شود.

P05-DEN-025 — Effect Unknown، Dependency Unknown، Target Cardinality Unknown یا External Behavior Unknown نباید با Lowest Plausible Class جایگزین شود.

P05-FAIL-004 — Unknown Transitive Behavior نتیجه `EFFECT_INDETERMINATE — DENY / DO_NOT_EXECUTE` دارد.

P05-FAIL-005 — کشف Runtime Effect بالاتر از Classified Effect باید Attempt را Stop/Fence، Evidence را Preserve، State را Reconcile و Reclassification/Incident متناسب را فعال کند.

P05-FAIL-006 — اگر Effect پایین‌تر از Ceiling باشد ولی Approval/Permission/Autonomy/Risk/Cost/Data/Environment نامعتبر باشد، Execution همچنان Denied است.

P05-FAIL-007 — کشف Command-enabling Path نتیجه `E9 / APR-X / INC-0` و مسیر `HARD_STOP → ISOLATE → PRESERVE EVIDENCE → REMOVE PATH → INDEPENDENT REVIEW` دارد.

P05-FAIL-008 — اگر Aggregate/Transitive Effect از Per-item Effect بالاتر باشد، Profile و Approval باید به Class بالاتر Reclassify شوند؛ Work قبلی نباید مبنای Grandfathering شود.

## 6. Actual Effect و Transitive Effect Truth

P05-PROC-001 — الگوریتم Classification باید منطقی معادل مسیر زیر باشد:

~~~text
1. Resolve exact request, normalized digest, purpose, tenant, environment and target set.
2. Resolve capability identity, operation, version, manifest and effect ceiling.
3. Expand the complete direct and transitive dependency/invocation graph.
4. Include child workflows, tools, adapters, providers, callbacks, retries, loops,
   scheduled continuations, compensation, recovery, cleanup and external egress.
5. Determine per-node direct effect and all effect amplifiers.
6. Aggregate target cardinality, tenant scope, concurrency, duration, retries,
   shared dependencies, cost exposure, data movement and blast radius.
7. Apply hard triggers for production, privileged access, external exposure,
   public release, destructive behavior and E9 paths.
8. Select the maximum applicable E-class; retain all contributing reasons.
9. Resolve uncertainty; if a material node or edge is unknown, mark
   EFFECT_INDETERMINATE and deny effectful execution.
10. Reclassify whenever request, graph, target, policy, data, environment,
    risk, cost, irreversibility or runtime observation materially changes.
~~~

P05-REQ-008 — هر `EffectClassificationRecord` باید حداقل Contract زیر را داشته باشد:

~~~yaml
effect_classification_id:
request_reference:
normalized_request_digest:
classification_version:
classifier_identity_and_version:
classified_at: TemporalStamp
tenant_and_purpose_scope:
environment_reference:
target_manifest_reference:
target_cardinality_bound:
capability_and_operation_references: []
dependency_graph_reference:
direct_effects: []
indirect_effects: []
transitive_effects: []
aggregated_effect_factors: []
effect_amplifiers: []
selected_effect_class:
selection_reasons: []
effect_ceiling_reference:
data_class_reference:
risk_context_reference:
cost_exposure_reference:
irreversibility_class:
external_egress_or_publication:
production_or_privileged_scope:
unknowns: []
conflicts: []
evidence_references: []
validity_window:
reclassification_triggers: []
status: RESOLVED|INDETERMINATE|CONFLICTED|STALE|SUPERSEDED
supersedes_reference:
provenance_reference:
~~~

P05-CON-041 — Classification باید Server-controlled و Policy-bound باشد؛ Client Input فقط Evidence Candidate است.

P05-CON-042 — Dependency Graph باید Versioned و Digest-bound باشد و Dynamic Discovery فقط در Allowlisted/Bounded Scope معتبر است.

P05-CON-043 — هر Node باید Operation Type، Target، Data Movement، External Destination، Credential Use، Cost Model، Retry/Loop Bound، Recovery Behavior و Effect Ceiling قابل‌حل داشته باشد.

P05-CON-044 — Graph Closure باید Edgeهای Sync، Async، Event-driven، Scheduled، Human-mediated و Out-of-band Provider Behavior را در حد Applicability پوشش دهد.

P05-CON-045 — Target Cardinality باید Upper Bound قابل‌اثبات داشته باشد. Dynamic Target Discovery بدون Bound مساوی Aggregate Effect نامعلوم است.

P05-CON-046 — Effect Amplifierها حداقل شامل Production، Privilege، External Egress، Public Audience، Cross-tenant، Bulk، Legal Hold، Destruction، Variable Cost، Code Execution، Long Duration، High Concurrency و Shared Critical Dependency هستند.

P05-CON-047 — Maximum Plausible Committed Effect ملاک است؛ Average، Most-likely یا Intended Happy Path ملاک کاهش نیست.

P05-CON-048 — Preconditionهایی که Effect را محدود می‌کنند فقط وقتی قابل‌اتکا هستند که Server-enforced، Versioned، Testable، Current و Fail-closed باشند.

P05-CON-049 — Capability Manifest Ceiling Upper Bound است، نه Grant. اگر Actual Operation بالاتر از Ceiling باشد Invocation Invalid است؛ اگر پایین‌تر باشد سایر Gateها همچنان لازم‌اند.

P05-CON-050 — Static Classification باید در Execution Boundary دوباره Validate شود. Cache فقط با Version، Freshness، Scope و Invalidation Contract معتبر است.

P05-CON-051 — Reclassification باید Prior Class، New Class، Trigger، Diff، Impacted Approval/Permission/Autonomy/Profile/Lease و Evidence را ثبت کند.

P05-CON-052 — Reclassification به Class پایین‌تر فقط پس از اثبات حذف واقعی Trigger، Graph/Target Closure تازه، Independent Review متناسب و Record جدید ممکن است؛ Silent Downgrade ممنوع است.

P05-CON-053 — Reclassification به Class بالاتر باید Work را قبل از Effect بیشتر Pause/Block کند، Approval/Profile تازه بخواهد و Lease قبلی را Invalid کند.

P05-CON-054 — Effect Classification Expiry باید با Request، Dependency، Policy، Price، Provider، Environment، Risk، Data و Target Change هماهنگ باشد.

P05-CON-055 — Classification Evidence باید Assumption، Unknown، Counterevidence، Limitation و Unverified Edge را حفظ کند.

P05-CON-056 — Observed Outcome نمی‌تواند Classification پیشین را Retroactively Correct نشان دهد؛ Underclassification Defect باقی می‌ماند حتی اگر Harm رخ نداده باشد.

P05-CON-057 — Higher-class Effect که به دلیل Guard مسدود شده همچنان برای Threat/Abuse/Bypass Analysis ثبت می‌شود؛ Blocked Attempt اثر قابل‌بررسی است.

P05-DEN-026 — Model-generated Dependency Graph بدون Registry/Manifest/Evidence کافی Source of Truth نیست.

P05-DEN-027 — Missing Edge نباید به No Edge، Missing Cost به Zero Cost یا Missing Target به Single Target تبدیل شود.

P05-DEN-028 — UI Preview، Test Mode، Sandbox Label یا Non-production Environment نمی‌تواند External/Privileged/Destructive Trigger واقعی را حذف کند.

P05-DEN-029 — Scope Reduction Client-side بدون Server-enforced Target/Capability Bound معتبر نیست.

P05-DEN-030 — Cached Prior Classification برای Request Digest، Target Revision، Provider، Environment یا Dependency Graph متفاوت قابل‌استفاده نیست.

P05-DEN-031 — Outcome موفق قبلی، Lack of Incident یا Low Observed Cost Evidence کاهش Maximum Plausible Effect Request جدید نیست.

P05-DEN-032 — Effect Classification نباید با Approval Availability، Team Size، Deadline یا مطلوبیت Business تنظیم شود.

P05-FAIL-009 — Missing Capability/Operation Identity، Version، Manifest یا Ceiling نتیجه `CAPABILITY_EFFECT_UNRESOLVED` و Deny دارد.

P05-FAIL-010 — Missing/Unbounded Target Cardinality نتیجه `AGGREGATE_EFFECT_INDETERMINATE` و Deny دارد.

P05-FAIL-011 — Unsupported/Conflicted Dependency Version یا Provider Behavior نتیجه `TRANSITIVE_GRAPH_CONFLICTED` و Deny دارد.

P05-FAIL-012 — Stale Classification در Execution Boundary باید Recompute شود؛ Expiry نباید Fail Open کند.

P05-FAIL-013 — اگر Reclassification Requirements قابل‌تکمیل نیست، Work در `BLOCKED_BY_EFFECT_RECLASSIFICATION` باقی می‌ماند.

P05-FAIL-014 — Lost Classification Record یا Integrity Failure باید Effectful Work را Stop و Evidence/State Reconciliation را فعال کند.

P05-FAIL-015 — Classification Bypass Attempt باید Security/Governance Finding ثبت کند؛ اگر E9-related باشد `INC-0` اجباری است.

## 7. Approval Taxonomy — `APR-0` تا `APR-4` و `APR-X`

P05-REQ-009 — Approval Class باید حداقل Taxonomy زیر را حفظ کند:

| Class | معنای Canonical | ویژگی‌های لازم |
|---|---|---|
| `APR-0` | بدون Per-action Human Approval درون Manifest/Policy Envelope از قبل تصویب‌شده | Deterministic Policy، Bounded Scope، Current Identity، Logging، Revocation و Evidence |
| `APR-1` | یک Approval انسانی پاسخ‌گو برای Action محدود، Reversible و Low-materiality | Exact Request Digest، Preview، Expiry و Outcome Receipt |
| `APR-2` | Approval مالک Domain پاسخ‌گو همراه Specialist Concurrenceهای Applicable | Data/Science/Security/Privacy/Operations/Publication Review متناسب |
| `APR-3` | Independent Multi-role Approval برای Effect مادی یا حساس | Separation of Duties، Risk/Cost Review، Short-lived Lease، Canary/Rollback/Recovery |
| `APR-4` | Exceptional Governing/Executive Authorization برای `E7/E8` High-blast-radius، Production-critical یا Destructive | Dual Control، Independent Challenge، Exact Manifest، Bounded Window، Abort/Fencing، Post-effect Verification |
| `APR-X` | هیچ Approval معتبر درون CSIP-EO وجود ندارد | Hard Prohibition؛ Approval Attempt خود Incident است |

P05-CON-058 — Approval Class حداقل Floor است. Law، Policy، Risk، Data، Science، Environment، Cost، Irreversibility یا Separation Rule می‌تواند Class سخت‌گیرانه‌تر یا Deny ایجاد کند.

P05-CON-059 — `APR-0` به معنی «بدون کنترل» نیست؛ Action باید در Envelope دقیق از قبل تصویب‌شده، Deterministic Policy، Current Identity، Bounded Scope، Evidence و Revocation قرار داشته باشد.

P05-CON-060 — `APR-1` فقط برای Request دقیق، Low-materiality، Bounded و Reversible معتبر است و Approval عمومی Owner کافی نیست.

P05-CON-061 — `APR-2` نیازمند Domain Owner و تمام Specialist Concurrenceهای Applicable است؛ یک Reviewer نمی‌تواند Domainهای خارج از Competence را پوشش دهد.

P05-CON-062 — `APR-3` نیازمند استقلال واقعی Multi-role، Review Risk/Cost و Lease کوتاه‌عمر است؛ Serial Click توسط یک Actor Multi-role استقلال نیست.

P05-CON-063 — `APR-4` Exceptional است و باید Governing/Executive Authority، Independent Challenge، Dual Control، Exact Manifest، Fencing، Recovery Evidence و Verification پس از Effect را Bind کند.

P05-CON-064 — `APR-X` Class Approval نیست؛ علامت No-route و Hard Denial است.

P05-CON-065 — Default Effect-to-Approval Floor فقط نقطۀ آغاز است:

| Effect | Default Approval Floor |
|---:|---|
| `E0` | `APR-0` داخل Policy |
| `E1` | `APR-0` داخل Policy |
| `E2` | `APR-0/APR-1` برحسب Data/Write Context |
| `E3` | `APR-1` یا Policy از پیش تصویب‌شدۀ `APR-0` |
| `E4` | `APR-1/APR-2` |
| `E5` | `APR-2/APR-3` |
| `E6` | `APR-3` |
| `E7` | `APR-3/APR-4` |
| `E8` | `APR-4` |
| `E9` | فقط `APR-X` |

P05-CON-066 — Range در Matrix بالا به معنی انتخاب دلخواه Lower Bound نیست. Exact Request باید با تمام Triggerها Classify و Class بالاتر Applicable انتخاب شود.

P05-CON-067 — Approval باید Informed باشد: Presentation باید Intent، Exact Scope، Material Diff، Actual/Transitive Effect، Data، Risk، Cost، Irreversibility، Alternatives، Evidence، Unknown، Dissent، Recovery و Conditions را نشان دهد.

P05-CON-068 — Approval برای Change پس از Material Diff، Scope Expansion، Target Addition، Environment Change، Provider Change، Effect Escalation، Cost/Risk Breach یا Expiry باید تازه صادر شود.

P05-DEN-033 — Blanket، Future-unknown، Cross-tenant، Cross-environment، Cross-provider، Cross-model، Cross-artifact، Cross-target یا Digest-free Approval ممنوع است.

P05-DEN-034 — Approval Request نباید Missing Evidence، Counterevidence، Unknown Outcome، Dissent، Cost Tail، Risk Concentration یا Recovery Limitation را پنهان کند.

P05-DEN-035 — AI، Agent، Workflow، Service، Tool یا Model Human Approver، Risk Acceptor، Budget Owner یا Governing Authority نیست.

P05-DEN-036 — Self-approval یا Approval توسط Actor تحت کنترل مستقیم Proposer برای Material/High/Critical Work بدون Independent Control ممنوع است.

P05-DEN-037 — Silence، Delay، Meeting Attendance، Email Open، Chat Reaction، Checkbox Default، Prior Pattern یا Absence of Objection Approval نیست.

P05-DEN-038 — Approval Availability یا Reviewer Unavailability نباید Class را کاهش دهد؛ Outcome باید Wait/Block/Escalate با Competence معادل یا سخت‌گیرانه‌تر باشد.

P05-DEN-039 — `APR-4` نمی‌تواند `APR-X` را Override کند و Human-only Route برای `E9` وجود ندارد.

P05-DEN-040 — Approval پس از Execution جای Approval لازم قبل از Effect را نمی‌گیرد؛ فقط می‌تواند Review/Incident/Disposition Record باشد.

P05-FAIL-016 — Missing/Expired/Revoked/Conflicted Approval نتیجه `APPROVAL_INVALID — DO_NOT_EXECUTE` دارد.

P05-FAIL-017 — Approval Class پایین‌تر از Floor Applicable باید `APPROVAL_CLASS_INSUFFICIENT` و Block ایجاد کند.

P05-FAIL-018 — Incomplete/Misleading Presentation Approval را Invalid می‌کند و Request با Digest تازه باید بازسازی شود.

P05-FAIL-019 — Self-approval، Competence Gap یا Separation Violation باید Effect را Block و Finding/Incident متناسب ثبت کند.

P05-FAIL-020 — Approval Attempt برای `E9/APR-X` باید `PROHIBITED_APPROVAL_ATTEMPT` و `INC-0` ایجاد کند.

## 8. Exact Approval Binding، Scope، Digest، Validity و Revocation

P05-DEF-017 — `Approval State` یکی از Stateهای صریح زیر است:

`PENDING | ISSUED | REJECTED | DEFERRED | EXPIRED | REVOKED | CONSUMED | INVALIDATED | SUPERSEDED`

P05-REQ-010 — هر Approval Record باید حداقل Contract زیر را داشته باشد:

~~~yaml
approval_id:
approval_class:
approval_state:
approval_subject_type:
approver_identity:
approver_role_and_domain:
competence_reference:
independence_and_conflict_status:
request_reference:
request_digest:
presentation_digest:
target_manifest_digest:
effect_class:
effect_classification_reference:
tenant_and_environment_scope:
purpose_scope:
operation_and_capability_scope:
target_scope_and_cardinality:
data_scope:
external_destination_scope:
cost_ceiling:
budget_authorization_reference:
risk_decision_reference:
security_and_privacy_references: []
scientific_or_domain_review_references: []
conditions: []
prohibited_conditions: []
issued_at: TemporalStamp
valid_from: TemporalStamp
expires_at: TemporalStamp
nonce:
single_use: true
consumption_status:
revocation_status:
revoked_at: TemporalStamp|null
revocation_reason:
revocation_authority_reference:
independent_review_references: []
dissent_and_limitations: []
signature_or_attestation:
provenance_reference:
supersedes_reference:
~~~

P05-CON-069 — `request_digest` باید Request نرمال‌شده، Critical Payload References و Canonicalization Profile مشخص را Bind کند؛ Algorithm/Profile دقیق تا تعیین و Qualification نباید Cross-implementation Equivalence ادعا شود.

P05-CON-070 — `presentation_digest` باید دقیقاً محتوایی را Bind کند که Approver دیده است؛ Hidden Field، Omitted Diff یا Lossy Translation Approval را معتبر نمی‌گذارد.

P05-CON-071 — `target_manifest_digest` باید Target Set، Cardinality، Version/Revision، Provider/Destination و Environment Applicable را Bind کند.

P05-CON-072 — Approval Scope باید Tenant، Purpose، Operation، Capability، Target، Data، Destination، Environment، Effect، Cost، Risk، Time و Conditions را صریح کند.

P05-CON-073 — Validity فقط در Intersection `valid_from ≤ now < expires_at`، Nonce معتبر، Not Revoked، Not Consumed، Same Digest، Same Scope و Current Policy برقرار است.

P05-CON-074 — Single-use Approval پس از Consumption قابل Replay نیست. Multi-use فقط اگر Source Policy صریحاً اجازه دهد و Count/Scope/Window Bound و هر Attempt Link مستقل داشته باشد؛ Default `single_use: true` است.

P05-CON-075 — Approval Issuance و Lease Issuance Recordهای جدا هستند. Approval حق Attempt مستقیم ایجاد نمی‌کند.

P05-CON-076 — Approval Rejection، Defer، Expiry، Revocation، Consumption و Invalidation Outcomeهای معتبرند و نباید به Failure فنی یا Approval ضمنی تبدیل شوند.

P05-CON-077 — Revocation از زمان مؤثر، Attempt تازه را منع می‌کند؛ History، Prior Attempt، Receipt یا Outcome را حذف نمی‌کند.

P05-CON-078 — Revocation حین Attempt باید Executor را در حد توان Stop/Fence، Lease را Revoke، State را Inspect و Outcome را Reconcile کند؛ Revocation به‌تنهایی اثبات توقف Effect نیست.

P05-CON-079 — Renewal یا Extension Approval Record تازه با Review، Digest، Scope، Validity و Nonce تازه می‌خواهد؛ Mutation درجا ممنوع است.

P05-CON-080 — Material Change پس از Approval باید Approval را `INVALIDATED` یا `SUPERSEDED` کند و Approval تازه بخواهد.

P05-CON-081 — Approver Competence باید Domain-specific، Scope-specific، Current و Evidence-backed باشد. Seniority، Title یا Admin Role کافی نیست.

P05-CON-082 — Delegated Approval باید Delegator، Delegate، Delegable Scope، Competence، Constraints، Validity، Revocation و Non-delegable Duties را Bind کند و Authority را گسترش ندهد.

P05-CON-083 — Independent Review Reference باید Reviewer Identity، Competence، Independence، Evidence، Findings، Dissent و Disposition را حفظ کند.

P05-CON-084 — Conditions باید Machine-checkable در حد امکان، Non-ambiguous، Non-expansive و Time-bound باشند. Free-text Condition Escape Hatch نیست.

P05-CON-085 — Approval Signature/Attestation Integrity را پشتیبانی می‌کند؛ Informedness، Competence، Correctness یا Continued Validity را به‌تنهایی ثابت نمی‌کند.

P05-CON-086 — Approval Record باید Immutable-history باشد؛ Correction با Superseding/Correction Record انجام می‌شود، نه Silent Edit.

P05-CON-087 — Revocation، Expiry و Consumption باید برای Policy/Lease/Workflow Consumerها قابل‌مشاهده و Reconciliation-aware باشد؛ Eventual Propagation نباید Window بدون Bound بسازد.

P05-DEN-041 — Approval بدون Exact Request Digest، Scope، Approver Identity، Competence، Validity و Revocation State برای Effectful Work معتبر نیست.

P05-DEN-042 — Reuse Approval برای Request مشابه، Later Phase، Different Environment، Tenant، Provider، Model، Artifact، Dataset، Risk Acceptance یا Larger Scope ممنوع است.

P05-DEN-043 — Approver Session، Login، Credential یا Team Membership Approval Record نیست.

P05-DEN-044 — Edit پس از Approval، UI-side Patch، Hidden Default، Auto-filled Field یا Re-render متفاوت Approval را حفظ نمی‌کند.

P05-DEN-045 — Coerced، Uninformed، Accessibility-defective، Approval-fatigued یا بدون Alternative/Review Time کافی Approval معتبر نیست.

P05-DEN-046 — Backdated Approval، Reconstructed Approval بدون Provenance یا Approval تولیدشده از Log/Chat ممنوع است.

P05-DEN-047 — Approval Token نباید Bearer Credential عمومی، Cross-service Permission یا Reusable Secret شود.

P05-DEN-048 — Revoked/Expired Approval نباید با Cache، Offline Mode، Retry، Resume، Failover یا Human Override استفاده شود.

P05-DEN-049 — Approval Revocation نباید Evidence، Rationale، Dissent یا Prior State را حذف کند.

P05-DEN-050 — `APR-X` Approval Record `ISSUED` ندارد؛ تنها Denial/Incident Record می‌تواند ساخته شود.

P05-FAIL-021 — Request/Presentation/Target Digest Mismatch نتیجه `APPROVAL_DIGEST_MISMATCH` و Block دارد.

P05-FAIL-022 — Invalid Nonce، Replay یا Duplicate Consumption نتیجه `APPROVAL_REPLAY_DETECTED` و Block/Incident متناسب دارد.

P05-FAIL-023 — Expired/Revoked/Consumed Approval نتیجه `APPROVAL_NOT_CURRENT` و Block دارد.

P05-FAIL-024 — Missing Competence/Independence Evidence نتیجه `APPROVER_AUTHORITY_INDETERMINATE` و Block دارد.

P05-FAIL-025 — Revocation Propagation Failure باید Lease/Effectful Path را Fail Closed، State را Reconcile و Incident متناسب ایجاد کند.

P05-FAIL-026 — Canonicalization/Profile Conflict باید Approval Binding را `INDETERMINATE` کند؛ Byte Similarity یا Human Claim جای آن را نمی‌گیرد.

## 9. Permission Taxonomy — `PERM-A` تا `PERM-E`

P05-REQ-011 — Permission Class باید Actor-domain Authority را طبق Taxonomy زیر تعریف کند:

| Class | Actor Domain | مجاز در Scope دقیق | نمی‌تواند |
|---|---|---|---|
| `PERM-A — OBSERVER` | مشاهدۀ Viewهای مجاز | Read permitted views و Ephemeral Analysis | Authoritative Write، Approval، Execution |
| `PERM-B — CONTRIBUTOR` | مشارکت غیرAuthoritative | Proposal، Draft، Finding و Bounded Non-authoritative Record | Promote، Approve own work، Privileged Execution |
| `PERM-C — OPERATOR` | عملیات زمینی محدود | اجرای Capabilityهای Terrestrial صریحاً فهرست‌شده تحت Policy/Lease | Expand Capability، Self-approve، Change Ceiling |
| `PERM-D — DOMAIN_AUTHORITY` | Authority در Domain نام‌برده | Approve/Operate در Scientific، Data، Security، Finance، Risk یا Operations Domain مشخص | خارج از Competence/Scope عمل کند یا High-impact Work خود را به‌تنهایی Verify کند |
| `PERM-E — GOVERNING_AUTHORITY` | حاکمیت Baseline/Constitution | Ratify Constitutional/Baseline Decision و Appoint/Revoke Authority محدود | Law، Scientific Evidence یا Entrenched Prohibition را Override کند |

P05-CON-088 — Permission پاسخ می‌دهد «Actor در کدام Domain و Scope حق دارد؟» و هیچ Severity، Approval Floor یا Autonomy را خودکار تعیین نمی‌کند.

P05-CON-089 — یک Actor می‌تواند Permissionهای متفاوت در Domainهای متفاوت داشته باشد؛ هر Permission باید Domain، Tenant، Resource، Operation، Environment، Purpose، Effect Ceiling، Validity و Revocation را Bind کند.

P05-CON-090 — `PERM-A` فقط Read Viewهای Policy-permitted را پوشش می‌دهد؛ Sensitive Read، Cross-tenant View، Export، Trigger یا Hidden Write خارج از آن است.

P05-CON-091 — `PERM-B` حق ایجاد Proposal/Draft دارد، اما Promotion، Approval، Execution یا تبدیل Draft به Canonical Record را ندارد.

P05-CON-092 — `PERM-C` فقط Capability و Operationهای Terrestrial Allowlisted، Typed، Versioned و Lease-bound را اجرا می‌کند و حق تغییر Manifest/Ceiling/Policy ندارد.

P05-CON-093 — `PERM-D` Domain-specific است؛ Science Authority Budget، Security یا Risk Authority نیست و برعکس.

P05-CON-094 — `PERM-E` Governing Authority نیز در Scope، Law، Constitution، Evidence، Separation و Prohibition محدود است و Superuser مطلق نیست.

P05-CON-095 — Permission Assignment باید Identity، Role، Domain، Competence، Scope، Conditions، Issuer Authority، Validity، Review/Recertification و Revocation داشته باشد.

P05-CON-096 — Permission Delegation نمی‌تواند Class، Domain، Scope، Effect Ceiling، Tenant، Environment یا Validity را گسترش دهد.

P05-CON-097 — Permission برای Approval فقط وقتی معتبر است که Actor علاوه بر Class، Competence و Independence لازم برای همان Approval Subject را داشته باشد.

P05-CON-098 — Permission برای Operation بدون AuthorizationDecision و ExecutionLease کافی نیست.

P05-CON-099 — Permission Revocation یا Expiry Attempt تازه را Block می‌کند و Leaseهای وابسته باید Re-evaluate/Revoke شوند؛ History حذف نمی‌شود.

P05-CON-100 — Separation of Duties Transaction-specific است؛ داشتن چند Permission Class تعارض را حذف نمی‌کند.

P05-CON-101 — Least Privilege باید سخت‌گیرانه‌ترین Permission لازم برای Request را انتخاب کند؛ Broad Role نباید به Token/Lease منتقل شود.

P05-DEN-051 — Job Title، Team، Group، Email Domain، Network Location، Past Access یا Admin UI Permission قطعی نیست.

P05-DEN-052 — Permission Generic مانند `all`، `execute`، `admin`، `custom` یا `tool-use` بدون Typed Operation/Target/Scope ممنوع است.

P05-DEN-053 — `PERM-D` یا `PERM-E` Self-approval، Sole Verification یا Risk/Budget Authority خارج از Domain ایجاد نمی‌کند.

P05-DEN-054 — Shared Identity، Generic Team Account، Borrowed Session یا Unverifiable Actor برای Permission حساس ممنوع است.

P05-DEN-055 — Permission Inheritance، Group Nesting یا Delegation Chain نباید Authority Creep یا Scope Expansion پنهان ایجاد کند.

P05-DEN-056 — Permission Cached پس از Revocation، Role Change، Tenant Change، Environment Change یا Competence Expiry معتبر نیست.

P05-DEN-057 — Permission برای یک Tenant/Environment/Target به دیگری منتقل نمی‌شود.

P05-DEN-058 — `PERM-E` هیچ Route برای `E9/APR-X` ایجاد نمی‌کند.

P05-DEN-059 — Agent/Model نمی‌تواند Permission خود یا Human Permission را از Prompt، Tool Availability یا Conversation استنتاج کند.

P05-FAIL-027 — Missing/Expired/Revoked Permission نتیجه `PERMISSION_INVALID — DO_NOT_EXECUTE` دارد.

P05-FAIL-028 — Domain/Competence Mismatch نتیجه `PERMISSION_DOMAIN_MISMATCH` و Block دارد.

P05-FAIL-029 — Delegation Scope Conflict نتیجه `DELEGATED_AUTHORITY_CONFLICTED` و Block دارد.

P05-FAIL-030 — Separation/Conflict-of-interest نامعلوم برای Approval حساس نتیجه `PERMISSION_INDEPENDENCE_INDETERMINATE` و Block دارد.

P05-FAIL-031 — Permission Store/Identity/Recertification Failure باید Effectful Work را Fail Closed کند.

## 10. Autonomy Taxonomy — `AUT-0` تا `AUT-5` و رد `A*` مبهم

P05-REQ-012 — Autonomy Profile باید Taxonomy زیر را حفظ کند:

| Profile | Autonomous Capability |
|---:|---|
| `AUT-0` | فقط Synthetic Data؛ بدون External Connection |
| `AUT-1` | Read Public Data در Allowlisted Sourceها |
| `AUT-2` | Restricted Read داده Internal/Sensitive تحت Policy |
| `AUT-3` | Restricted، Idempotent و Reversible Write داخل Preapproved Envelope |
| `AUT-4` | Sensitive/Privileged Attempt فقط پس از Preview، Independent Human Approval و Short-lived Permit؛ Automation Approval صادر نمی‌کند |
| `AUT-5` | Autonomous Execution ممنوع؛ Human/Governance Path فقط برای Action غیر`E9` و تحت `APR-4` و Authority Applicable ممکن است |

P05-CON-102 — Labelهای Mandate `A0..A5` فقط Compatibility Alias هستند و در Canonical Contract به `AUT-0..AUT-5` Rename می‌شوند تا با Permission Classها تداخل نکنند.

P05-CON-103 — Mapping Compatibility:

| Legacy | Canonical | Effect Relationship | Approval Relationship |
|---|---|---|---|
| `A0` | `AUT-0` | معمولاً `E0/E1` | `APR-0` داخل Policy |
| `A1` | `AUT-1` | معمولاً `E0/E1` | `APR-0` داخل Policy |
| `A2` | `AUT-2` | معمولاً Read-only `E1/E2` | Data Policy؛ `APR-0/1` |
| `A3` | `AUT-3` | معمولاً `E3/E4`؛ هرگز فرضی نیست | `APR-0..2` برحسب Action دقیق |
| `A4` | `AUT-4` | معمولاً `E5/E6` و ممکن است `E7` | `APR-2..4` |
| `A5` | `AUT-5` | Effect جداگانه `E0..E8` Classify می‌شود؛ Autonomous Deny | Human/Governance Route فقط اگر مجاز |

P05-CON-104 — هیچ Mappingی از Legacy Authority Label به `E9` وجود ندارد؛ `E9` همیشه `APR-X` است.

P05-CON-105 — `AUT-0` نیازمند اثبات Synthetic Data، Local-only Processing، No External Connection و No Hidden Provider/Telemetry Egress است.

P05-CON-106 — `AUT-1` فقط Public Data، Allowlisted Source، Read-only Behavior و Bounded Cost/Rate را پوشش می‌دهد.

P05-CON-107 — `AUT-2` Sensitive/Internal Read را فقط با Purpose، Data Policy، Minimization، Tenant/Scope، Egress Denial و Evidence معتبر اجازه می‌دهد.

P05-CON-108 — `AUT-3` فقط Write تایپ‌شده، Idempotent، Reversible، Bounded، Preapproved و Low-blast-radius را پوشش می‌دهد؛ Promotion یا Privileged Change خارج از آن است.

P05-CON-109 — `AUT-4` Automation را فقط پس از Preview، Independent Human Approval، Valid AuthorizationDecision و Short-lived Permit به Attempt محدود می‌کند؛ Automation هرگز Approver نیست.

P05-CON-110 — `AUT-5` Profile «بیشترین Autonomy» نیست؛ No-autonomous-execution است.

P05-CON-111 — `AUT-5` با `APR-X` متفاوت است: Action `AUT-5` ممکن است برای `E0..E8` Human/Governance Route معتبر داشته باشد؛ `E9/APR-X` هیچ Route ندارد.

P05-CON-112 — Actionهای زیر همیشه حداقل `AUT-5` هستند و هیچ Autonomous Execution Path ندارند:

- تغییر Security Policy؛
- اعطای Privileged Permission؛
- مدیریت Root Credential یا Primary Key؛
- تغییر Budget Ceiling؛
- تغییر Risk Appetite، Tolerance، Capacity، Limit، Methodology یا Acceptance Authority؛
- Accept کردن Residual Risk متعلق به خود؛
- کاهش Risk Classification خود؛
- Disable کردن Audit، Risk، KRI/KCI، Safety یا Mandatory Assurance؛
- Bulk Sensitive Export؛
- Bulk Deletion؛
- حذف Evidence یا Backup؛
- تغییر Retention Lock؛
- Primary-key Destruction؛
- Approve کردن Action متعلق به همان System.

P05-CON-113 — `AUT-5` Action غیر`E9` فقط پس از Human/Governance Route، Class/Authority Applicable و Execution Mode غیرAutonomous می‌تواند Candidate شود؛ این Part هیچ Candidate را Approved نمی‌کند.

P05-CON-114 — Autonomous Ceiling باید Capability، Operation، Data، Environment، Target، Effect، Cost، Risk، Concurrency، Retry، Duration و External Destination را Bind کند.

P05-CON-115 — Parent/Child، Agent/Tool و Model/Workflow Autonomy باید Intersect شود؛ Child نمی‌تواند Ceiling Parent یا Capability Manifest را افزایش دهد.

P05-CON-116 — Human Click وسط Automation، Execution را Human-operated نمی‌کند اگر System تصمیم، Scope، Target یا Timing مادی را خودکار انتخاب کند.

P05-CON-117 — Preapproved Envelope باید Exact، Versioned، Bounded، Revocable، Evidence-backed و فاقد Generic Action باشد.

P05-CON-118 — Autonomy Promotion از Profile پایین‌تر به بالاتر Governance Change مستقل با Effect/Risk/Data/Cost/Threat/Testing/Approval/Expiry می‌خواهد.

P05-CON-119 — Default Effect-to-Autonomy Matrix فقط Floor و Routing Baseline است:

| Effect | Default Autonomous-execution Profile |
|---:|---|
| `E0` | `AUT-0` برای Synthetic/Local-only؛ `AUT-1` برای Public Read |
| `E1` | `AUT-2` برای Read؛ `AUT-3` فقط برای Reversible Local-draft Write داخل Approved Envelope |
| `E2` | `AUT-2` برای Read؛ `AUT-3` برای Non-authoritative Proposal/Metadata/Memory-proposal Write |
| `E3` | `AUT-3` |
| `E4` | `AUT-3` |
| `E5` | `AUT-4` |
| `E6` | `AUT-4` |
| `E7` | `AUT-5` به‌صورت Default؛ Automated Attempt بسیار محدود، اگر هیچ Prohibition دیگری برقرار نباشد، باید پیش از Approval/Execution صریحاً `AUT-4` Classify شود |
| `E8` | `AUT-5` |
| `E9` | هیچ Profile؛ `PROHIBITED` |

Autonomy Demotion یا Kill/Disable می‌تواند Exposure را کاهش دهد؛ Restoration یا Promotion Change مستقل است. هیچ Row این Matrix Approval، Permission، AuthorizationDecision یا Lease ایجاد نمی‌کند.

P05-DEN-060 — برچسب بدون Namespace مانند `A0`، `A1`، `A2`، `A3`، `A4`، `A5` یا `A*` در Contract جدید ممنوع است؛ باید به `AUT-*` با Source/Mapping صریح Normalize شود.

P05-DEN-061 — اگر `A*` بتواند Permission، Approval، Effect یا Autonomy معنی دهد، Mapping `AMBIGUOUS_AUTHORITY_LABEL` است و Deny می‌شود.

P05-DEN-062 — Autonomy Profile نباید از Tool Availability، Model Capability، Agent Plan، Prior Run یا User Expectation استنتاج شود.

P05-DEN-063 — `AUT-3` یا `AUT-4` Self-approval، Self-lease، Self-expansion یا Dynamic Capability Discovery بدون Bound را مجاز نمی‌کند.

P05-DEN-064 — `AUT-4` به معنی «اجرا پس از هر Human Click» نیست؛ Approval/Policy/Lease/Scope دقیق لازم است.

P05-DEN-065 — `AUT-5` نباید به Human-mediated Autonomous Path، Background Job، Scheduled Task، External Agent یا Delegated Service تبدیل شود.

P05-DEN-066 — Human Override، Break-glass یا Emergency نمی‌تواند `AUT-5` Action را Autonomous کند یا `E9` را فعال سازد.

P05-DEN-067 — Online Learning، Self-modification، Auto-promotion یا Policy/Prompt/Tool Mutation نباید Autonomy Ceiling را Silent تغییر دهد.

P05-DEN-068 — Autonomy Label نباید Effect Class، Approval Floor یا Permission Need را کاهش دهد.

P05-DEN-069 — Legacy Compatibility نباید Approval/Status تاریخی یا Normative Authority به ارث دهد.

P05-FAIL-032 — Missing/Conflicted Autonomy Profile نتیجه `AUTONOMY_PROFILE_INDETERMINATE — DO_NOT_EXECUTE` دارد.

P05-FAIL-033 — Ambiguous `A*` نتیجه `AMBIGUOUS_AUTHORITY_LABEL — DENY` دارد.

P05-FAIL-034 — Attempt بالاتر از Autonomy Ceiling باید Hard Stop، Lease Revocation، Evidence Preservation و Incident/Review متناسب ایجاد کند.

P05-FAIL-035 — اگر Human/Automation Boundary قابل‌اثبات نیست، Execution Mode باید Autonomous فرض و به Ceiling سخت‌گیرانه‌تر Bind شود.

P05-FAIL-036 — Autonomy Promotion بدون Governance Change/Approval/Evidence معتبر Block می‌شود.

## 11. Fail-closed Intersection و استقلال Authorization/Execution Lease

P05-DEF-018 — `AuthorityIntersection` ارزیابی اتمیک و قابل‌ردیابی تمام Axisها، Gateها و Hard Constraintهای Applicable برای یک Request دقیق در یک لحظۀ مشخص است.

P05-REQ-013 — الگوریتم تصمیم باید منطقی معادل مسیر زیر باشد:

~~~text
1. Authenticate actor and workload.
2. Resolve tenant, purpose, environment, operation, target and target revision.
3. Resolve capability manifest and full transitive dependency graph.
4. Compute maximum actual/transitive/aggregated Effect E0..E9.
5. Resolve Data Class, Risk Tier/Status, Cost Exposure and Irreversibility.
6. Verify PERM domain, competence, delegation and separation of duties.
7. Verify AUT ceiling and actual execution mode.
8. Derive minimum APR and all specialist/governance concurrence.
9. Validate policy snapshot, approval digest, nonce, scope, validity and revocation.
10. Validate Security Authorization, Budget Authorization/Reservation
    and Risk Acceptance independently where applicable.
11. Select required Report Profile and verify exact section/evidence closure.
12. Record an AuthorizationDecision using deny-first precedence.
13. If and only if every gate is valid, a separate short-lived
    least-privilege ExecutionLease may be issued by the P03-owned path.
14. Revalidate every mutable predicate at the execution boundary.
15. Attempt, receipt, verification/reconciliation and outcome remain separate.
~~~

P05-REQ-014 — هر `AuthorityIntersectionRecord` باید حداقل Contract زیر را داشته باشد:

~~~yaml
authority_intersection_id:
request_reference:
request_digest:
evaluated_at: TemporalStamp
evaluation_policy_version:
actor_and_workload_identity:
tenant_and_purpose:
environment_and_region_reference:
capability_manifest_reference:
operation_and_target_scope:
effect_classification_reference:
effect_class:
required_approval_class:
approval_references: []
permission_references: []
permission_evaluation:
autonomy_profile_reference:
actual_execution_mode:
data_class_and_policy_reference:
risk_assessment_and_status_reference:
risk_acceptance_reference:
cost_exposure_and_estimate_reference:
budget_authorization_and_reservation_reference:
irreversibility_and_recovery_reference:
security_privacy_legal_science_domain_decisions: []
report_profile_reference:
report_completion_reference:
hard_constraint_results: []
unknowns: []
conflicts: []
constraints: []
decision: DENY|REQUIRE_HUMAN_APPROVAL|ALLOW_WITH_CONSTRAINTS|ALLOW
decision_reasons: []
valid_until: TemporalStamp
revalidation_triggers: []
provenance_reference:
~~~

P05-INV-005 — Decision Precedence دقیقاً Deny-first است:

`DENY > REQUIRE_HUMAN_APPROVAL > ALLOW_WITH_CONSTRAINTS > ALLOW`

P05-CON-120 — اگر چند Policy/Authority Result Applicable باشند، Result سخت‌گیرانه‌تر حاکم است؛ Majority Vote، Average، Weighted Score یا Last-writer-wins مجاز نیست.

P05-CON-121 — `FALSE` یا `UNKNOWN` در هر Hard Predicate باید Effectful Execution را Block کند؛ Unknown به False برای Allow و به Explicit Unknown برای Evidence تبدیل می‌شود.

P05-CON-122 — `NOT_APPLICABLE` فقط با Applicability Predicate، Source Owner و Evidence قابل‌استفاده است؛ نبود Field یا Service Failure `NOT_APPLICABLE` نیست.

P05-CON-123 — Effect Resolver می‌تواند Effect را بالا ببرد یا Indeterminate اعلام کند؛ حق Approval/Permission Grant ندارد.

P05-CON-124 — Approval Resolver می‌تواند Floor را تعیین یا Approval را Validate کند؛ حق Effect Downgrade، Permission Grant یا Lease Issuance ندارد.

P05-CON-125 — Permission Resolver فقط Domain/Scope/Competence را Resolve می‌کند؛ حق Approval، Risk Acceptance، Budget Commitment یا Autonomy Promotion ندارد.

P05-CON-126 — Autonomy Resolver فقط Ceiling را اعمال می‌کند؛ حق افزایش Permission، تغییر Effect یا تبدیل Human Approval به Automation Authority ندارد.

P05-CON-127 — Policy Service می‌تواند Authority را کاهش یا Deny کند؛ نمی‌تواند فراتر از Manifest، Law، Hard Invariant، Effect Ceiling، Permission یا Approval Grant دهد.

P05-CON-128 — AuthorizationDecision باید Exact Request/Context و Policy Snapshot را Bind کند و از Human Approval Record جدا باشد.

P05-CON-129 — ExecutionLease فقط پس از AuthorizationDecision معتبر و تمام Approval/Permission/Risk/Cost/Data/Environment Gateهای Applicable Candidate است؛ P05 صدور Lease را مجاز یا انجام‌شده اعلام نمی‌کند.

P05-CON-130 — Lease باید Least-privilege، Short-lived، Single-purpose، Target-bound، Effect-bound، Nonce-bound، Revocable و Attempt-limited باشد.

P05-CON-131 — Lease Issuance هیچ Success، Receipt یا Outcome ایجاد نمی‌کند و Lease Expiry/Revocation Outcome گذشته را تغییر نمی‌دهد.

P05-CON-132 — Material Change در Request، Target Revision، Effect، Data، Environment، Cost، Risk، Permission، Approval، Policy یا Report Profile باید AuthorizationDecision و Lease قبلی را Invalid کند.

P05-CON-133 — Runtime Revalidation باید Identity، Permission، Approval، Lease، Target Revision، Policy، Cost Reservation، Risk Status، Data/Environment Bound و Prohibited-path Scan را پوشش دهد.

P05-CON-134 — Authorization Cache فقط در Exact Scope، Version، Digest، Validity و Invalidation Contract معتبر است؛ Cache Miss یا Outage نباید Allow ایجاد کند.

P05-CON-135 — Parent Authorization/Lease Child Authority تولید نمی‌کند. Child باید Boundهای Parent را به‌علاوۀ Boundهای خود Intersect کند.

P05-CON-136 — Batch Authorization باید Per-target Identity/State، Aggregate Cardinality و Homogeneous Typed Semantics داشته باشد؛ Mixed/Unknown Target باید Split برای Classification شود، نه برای Downgrade.

P05-CON-137 — Retry یا Resume Attempt تازه است و باید Current Approval، Permission، Authorization، Lease، Risk، Cost و Target State را دوباره بررسی کند.

P05-CON-138 — Compensation/Recovery Application Command جدید است و Intersection مستقل می‌خواهد.

P05-CON-139 — Manual Operation نیز همان Effect/Permission/Approval/Risk/Cost/Data/Environment Gateها را می‌خواهد؛ Manual بودن Bypass نیست.

P05-CON-140 — External Provider یا Human-mediated Service باید همان Intersection را رعایت کند؛ انتقال Execution به خارج، Accountability یا Prohibition را منتقل نمی‌کند.

P05-CON-141 — Valid Security Authorization بدون Budget Authorization یا Risk Decision کافی نیست؛ Valid Budget بدون Security/Data/Approval کافی نیست.

P05-CON-142 — Technical Success، Green Test، Qualification، Release Approval یا Deployment Gate هیچ‌کدام به‌تنهایی Runtime Authorization نیستند.

P05-CON-143 — `FULL` Report Completion فقط Evidence/Review Obligation را نشان می‌دهد و به `ALLOW` ترجمه نمی‌شود.

P05-CON-144 — Denial Reasonها باید Machine-readable، Human-readable، Source-linked و فاقد Sensitive Leakage باشند.

P05-CON-145 — Denial Record باید امکان Correction/Resubmission برای Condition قابل‌رفع را از Approval Escalation متمایز کند؛ `E9/APR-X` هیچ Approval Escalation ندارد.

P05-DEN-070 — هیچ Service، Agent یا Human Role نباید تمام Axisها را با یک Boolean عمومی `authorized=true` جایگزین کند.

P05-DEN-071 — Missing Axis نباید از Axis دیگر استنتاج شود؛ `APR-0` Permission، `PERM-E` Approval و `AUT-4` Lease نیست.

P05-DEN-072 — Allow Result از Policy قدیمی، Environment دیگر، Tenant دیگر، Target دیگر یا Digest دیگر قابل‌انتقال نیست.

P05-DEN-073 — Lease نباید Bearer Credential عمومی، Long-lived Secret، Cross-operation Token یا Delegable Blanket Authority باشد.

P05-DEN-074 — Retry/Resume/Failover نباید Lease، Approval یا Budget Reservation منقضی را زنده کند.

P05-DEN-075 — Feature Flag، Emergency Label، Operator Override یا Provider Console نباید Intersection را دور بزند.

P05-DEN-076 — Human Approval نباید AuthorizationDecision یا ExecutionLease را Embedded و غیرقابل‌ردیابی سازد.

P05-DEN-077 — AuthorizationDecision نباید Risk Acceptance، Budget Authorization یا Scientific Verification را جعل کند.

P05-DEN-078 — Safe Mode فقط در Envelope از قبل تصویب‌شده و Exposure-reducing معتبر است؛ Safe Mode ناشناخته Fail Closed است.

P05-DEN-079 — هیچ Intersectionی برای `E9` به نتیجۀ غیر`DENY` نمی‌رسد.

P05-FAIL-037 — Missing/Contradictory Axis نتیجه `AUTHORITY_MAPPING_INDETERMINATE → DENY / DO_NOT_EXECUTE` دارد.

P05-FAIL-038 — AuthorizationDecision Stale یا Digest-mismatched باید `AUTHORIZATION_INVALID` و Block ایجاد کند.

P05-FAIL-039 — Lease Missing/Expired/Revoked/Consumed نتیجه `EXECUTION_LEASE_INVALID` و Block دارد.

P05-FAIL-040 — Revalidation Failure باید Attempt را Stop/Fence و State را Reconcile کند؛ Prior Allow مجوز ادامه نیست.

P05-FAIL-041 — Split-brain یا Conflict میان Policy/Identity/Approval/Lease Store باید `AUTHORITY_STATE_CONFLICTED` و Block ایجاد کند.

P05-FAIL-042 — Unknown Attempt State پس از Lease/Timeout باید `UNKNOWN` باقی بماند و پیش از Retry Reconciliation شود.

P05-FAIL-043 — Any Deny-bypass Attempt باید Evidence/Finding ایجاد کند؛ E9-related Bypass `INC-0` است.

## 12. Risk Tier، Data Class، Environment Class، Cost Exposure و Irreversibility

### 12.1 Boundary قرارداد و مالکیت

P05-CON-146 — P05 مالک Taxonomy سازمانی نهایی Risk، Data، Environment یا FinOps نیست؛ مالک نحوۀ مصرف Fail-closed این محورهای مستقل در Authority Intersection و Report Profile است.

P05-CON-147 — Risk Governance/Authority در P16، Canonical Data Lifecycle/Classification در P10 با Security/Privacy Constraints در P11، Environment/Promotion در P14 و Cost Metering/Evidence در P12/P16 تکمیل می‌شوند. این Part فقط Source-bound Admission Projection لازم برای Axis Intersection را تعریف می‌کند.

P05-CON-148 — Exact Organizational Owner، Currency، Amount، Threshold، Region، Jurisdiction، Data-class Vocabulary، Risk Appetite، Tolerance، Capacity، RTO/RPO و Environment Promotion Rule که در منابع موجود صریح نیستند `NOT_FOUND / OPEN_ISSUE` باقی می‌مانند.

### 12.2 Risk Tier و Risk Status

P05-DEF-019 — `Risk Tier` برای Admission، Exposure را طبق Mandate در شش سطح زیر Project می‌کند؛ Method/Threshold نهایی باید توسط P16 Source-bound شود:

| Tier | معنای Source-bound |
|---:|---|
| `R0 — Negligible` | بدون Impact مادی بر Objective/Stakeholder؛ Ownership و Monitoring عادی |
| `R1 — Low` | Exposure محدود، Reversible، Localized و Within Appetite |
| `R2 — Moderate` | Exposure معنادار؛ Named Owner، Treatment Decision و Periodic Review لازم |
| `R3 — High` | Exposure مادی؛ Independent Challenge، Senior Approval، Time-bound Acceptance/Treatment و Enhanced Monitoring |
| `R4 — Critical` | Exposure نزدیک یا بالاتر از Tolerance/Capacity؛ Executive Risk Authority، Immediate Treatment، Restricted Operation یا Suspension |
| `R5 — Prohibited/Intolerable` | Unlawful، Safety/Policy-prohibited، Existential یا Unacceptable؛ Execution تا حذف Condition ممنوع |

P05-CON-149 — Risk Status مستقل از Tier باید یکی از Semanticsهای Source-bound زیر را حفظ کند:

`PROHIBITED | ABOVE_CAPACITY | ABOVE_TOLERANCE | WITHIN_TOLERANCE_BUT_REQUIRES_TREATMENT | WITHIN_APPETITE | UNKNOWN`

P05-CON-150 — Risk Tier و Status نباید فقط با Likelihood×Impact یا Heat-map Average تعیین شوند؛ Catastrophic Low-frequency، Fat-tail، Legal Prohibition، Uncertainty، Correlation، Concentration و Common-mode Failure باید حفظ شوند.

P05-CON-151 — `R3/R4` نیازمند Independent Challenge و Authority متناسب است؛ `R5` قابل‌قبول یا قابل‌Waive توسط Automation نیست.

P05-CON-152 — Unknown/Stale/Unsupported Risk Evidence باید `UNKNOWN` بماند و هرگز `R0/R1` یا `WITHIN_APPETITE` فرض نشود.

P05-CON-153 — Risk Acceptance فقط Residual Risk مشخص را در Scope/Time/Authority معتبر پوشش می‌دهد و Hard Legal/Safety/Privacy/Security/Command Prohibition را رفع نمی‌کند.

### 12.3 Data Class Consumption Contract

P05-DEF-020 — `DataClassAdmissionFacts` مجموعۀ Factهای Policy-resolved زیر است؛ این نام، Taxonomy Canonical P10/P11 را جایگزین نمی‌کند:

~~~yaml
data_class_reference:
classification_status: RESOLVED|UNKNOWN|CONFLICTED|STALE
synthetic_or_public_status:
internal_or_sensitive_status:
personal_or_rights_impact:
privileged_or_secret_bearing_status:
tenant_scope:
purpose_and_legal_basis_reference:
residency_and_jurisdiction_reference:
egress_export_publication_status:
recipient_destination_manifest_reference:
retention_and_secondary_use_reference:
minimization_and_redaction_reference:
owner_and_policy_references:
~~~

P05-CON-154 — Exact Canonical Data Class labels و Thresholdهای P10/P11 در منابع P01 تا P04 و Stage 19 `NOT_FOUND` هستند؛ P05 نباید آن‌ها را اختراع یا Final اعلام کند.

P05-CON-155 — Synthetic/Public Data ممکن است فقط در صورت No-sensitive Join، No Hidden Identifier، No External Side Effect و Policy معتبر برای LITE Eligible باشد.

P05-CON-156 — Internal/Sensitive Read می‌تواند `E2` باشد، اما Purpose، Scope، Minimization، Tenant، Residency، Retention، Evidence و No-auto-promotion لازم است.

P05-CON-157 — Sensitive Egress/Export، Public Release، Cross-tenant Access، Privileged/Secret-bearing Data یا Material Legal/Privacy Impact حداقل `FULL` Trigger است و ممکن است Deny باشد.

P05-CON-158 — Secret/Credential نباید در Approval، Report، Event، Log یا Evidence Raw قرار گیرد؛ Protected Reference لازم است.

P05-CON-159 — Data Class Unknown/Conflicted برای تحلیل، `FULL` و Limitation صریح؛ برای Effectful Execution، `DENY` است.

### 12.4 Environment Class Consumption Contract

P05-DEF-021 — `EnvironmentAdmissionClass` برای Routing حداقل Semantics زیر را مصرف می‌کند:

| Class | معنای محدود |
|---|---|
| `RESEARCH_OR_LOCAL` | Terrestrial Research/Local Scope؛ بدون Production Claim یا External Pilot |
| `NON_PRODUCTION` | Development/Test/Staging یا Equivalent کنترل‌شده |
| `EXTERNAL_PILOT` | اثر روی External Participant/Provider/Audience در Pilot محدود |
| `PRODUCTION` | Environment یا Path دارای Production Effect |
| `ON_ORBIT_RUNTIME` | Deferred و خارج از Deployment Baseline فعلی |
| `ENVIRONMENT_UNKNOWN_OR_CONFLICTED` | Environment قابل‌اثبات نیست |

P05-CON-160 — Classهای بالا P05-local Admission Semantics هستند؛ Promotion، Region، Release و Runtime Contract دقیق متعلق به P14 است.

P05-CON-161 — `RESEARCH_OR_LOCAL` یا `NON_PRODUCTION` فقط یک Axis است و External Egress، Privilege، Destruction، Sensitive Data، High Risk یا Material Cost را کاهش نمی‌دهد.

P05-CON-162 — `EXTERNAL_PILOT` و `PRODUCTION` حداقل `FULL` Profile Trigger هستند.

P05-CON-163 — `ON_ORBIT_RUNTIME` در Baseline فعلی `DEFERRED / NOT_AUTHORIZED` است و هیچ Environment Mappingی نمی‌تواند Spacecraft-command Path بسازد.

P05-CON-164 — Environment Unknown/Conflicted برای Effectful Work `DENY` است؛ تحلیل فقط با `FULL` و Limitation مجاز است.

### 12.5 Cost Exposure

P05-DEF-022 — `CostExposureBand` برای Authority Admission، Sourceهای `fixed/bounded/variable/material` را به Semantics زیر Normalize می‌کند:

| Band | معنای محدود |
|---|---|
| `PREAPPROVED_NEGLIGIBLE` | Cost ناچیز داخل Envelope از قبل تصویب‌شده و Hard-bounded |
| `FIXED_BOUNDED` | Commitment ثابت و سقف‌دار با Owner/Budget مشخص |
| `VARIABLE_BOUNDED` | Cost متغیر با Worst-case Estimate، Hard Bound و Atomic Reservation |
| `MATERIAL` | Spend/Commitment مادی یا Procurement/Long-term Commitment |
| `UNBOUNDED_OR_UNKNOWN` | Rate، Cardinality، Duration، Retry، Egress یا Commitment نامعلوم/نامحدود |

P05-CON-165 — Bandهای بالا Amount/Currency Threshold نهایی نیستند؛ Exact Thresholdها `NOT_FOUND` و متعلق به Finance/Risk Governance هستند.

P05-CON-166 — Worst-case Cost باید Input/Output، Tool Call، Compute Time، Storage، Egress، Retry، Concurrency، Non-interruptible Commitment و Safety Margin را در حد Applicability شامل شود.

P05-CON-167 — `PREAPPROVED_NEGLIGIBLE` فقط در Envelope دقیق، Current Budget/Policy و No-bypass Path معتبر است.

P05-CON-168 — `VARIABLE_BOUNDED` نیازمند Estimate محافظه‌کارانه، Atomic/Idempotent Reservation، Metering، Settlement و Reconciliation است.

P05-CON-169 — `MATERIAL` حداقل `FULL` Report و Budget Authority مستقل می‌خواهد.

P05-CON-170 — `UNBOUNDED_OR_UNKNOWN` برای Execution `DENY` و برای Analysis `FULL` با Unknown صریح است.

### 12.6 Irreversibility

P05-DEF-023 — `IrreversibilityClass` باید یکی از Semanticsهای زیر را حفظ کند:

| Class | معنای محدود |
|---|---|
| `REVERSIBLE` | State قبلی معتبر، Compatible، Safe و Authorized است و Restore قابل‌اثبات است |
| `COMPENSABLE` | State عیناً برنمی‌گردد؛ Effect تازه می‌تواند Consequence را کاهش/خنثی کند |
| `RECOVERABLE_ONLY` | Roll-forward/Repair/Rebuild/Restore/Containment لازم است؛ بازگشت دقیق تضمین نیست |
| `DESTRUCTIVE_OR_IRREVERSIBLE` | Destruction یا Loss در عمل برگشت‌ناپذیر/Recovery-affecting است |
| `IRREVERSIBILITY_UNKNOWN` | Reversal/Compensation/Recovery قابل‌اثبات نیست |

P05-CON-171 — `REVERSIBLE` فقط با Preconditions، State Preservation، Compatibility، Authority، Tested Method، Deadline و Evidence معتبر است.

P05-CON-172 — `COMPENSABLE` Effect اصلی را حذف نمی‌کند و Compensation خود Effect/Cost/Risk/Approval مستقل دارد.

P05-CON-173 — `RECOVERABLE_ONLY` حداقل `FULL` Trigger است اگر Material، Production، Sensitive یا Recovery-affecting باشد.

P05-CON-174 — `DESTRUCTIVE_OR_IRREVERSIBLE` حداقل `E8/FULL/APR-4/AUT-5` Floor دارد، مگر Hard Condition آن را `DENY` کند.

P05-CON-175 — `IRREVERSIBILITY_UNKNOWN` برای Effectful Work `DENY` است.

P05-DEN-080 — Risk Score نباید Catastrophic/Prohibited Dimension را با Average پایین پنهان کند.

P05-DEN-081 — Risk Transfer، Insurance یا Outsourcing Accountability و Hard Constraint را منتقل نمی‌کند.

P05-DEN-082 — Budget Availability Risk Acceptance یا Within-appetite Status نیست.

P05-DEN-083 — Data Class Client-supplied یا Model-inferred بدون Policy/Owner Resolution قطعی نیست.

P05-DEN-084 — Non-production Label، Synthetic Claim یا Redaction Label بدون Evidence نباید Data/Environment Trigger را کاهش دهد.

P05-DEN-085 — Cost Alert، Forecast یا Provider Invoice جای Pre-execution Hard Bound/Reservation نیست.

P05-DEN-086 — Split Request، Child Fan-out، Retry Reset، Alternate Provider یا External Billing نباید Cost Bound را دور بزند.

P05-DEN-087 — Rollback Button، Backup Existence یا Prior Restore بدون Current Evidence Reversibility را ثابت نمی‌کند.

P05-DEN-088 — `R5`، `PROHIBITED`، `ABOVE_CAPACITY` یا Hard Legal/Safety Condition با Budget، Approval، `FULL` Report یا Emergency قابل‌پذیرش نیست.

P05-DEN-089 — On-orbit Runtime Deferred نباید به Research/Non-production Alias تبدیل شود.

P05-FAIL-044 — Risk Tier/Status Unknown یا Acceptance Invalid نتیجه `RISK_ADMISSION_INDETERMINATE_OR_DENIED` دارد.

P05-FAIL-045 — Data Class/Purpose/Residency/Destination Conflict نتیجه `DATA_ADMISSION_CONFLICTED — DENY` دارد.

P05-FAIL-046 — Environment Unknown/Unsupported/Deferred نتیجه `ENVIRONMENT_NOT_AUTHORIZED` دارد.

P05-FAIL-047 — Cost Unbounded/Unknown یا Reservation Failure نتیجه `COST_ADMISSION_DENIED` دارد.

P05-FAIL-048 — Irreversibility Unknown یا Recovery Evidence Missing نتیجه `IRREVERSIBILITY_INDETERMINATE — DENY` دارد.

P05-FAIL-049 — Hard Constraint Conflict باید به Deny برسد؛ Trade-off یا Score Aggregation ممنوع است.

P05-FAIL-050 — اگر Owner/Threshold/Authority واقعی `NOT_FOUND` باشد، این Part آن را اختراع نمی‌کند و Effect وابسته Block می‌ماند.

## 13. Cost/Risk Admission و استقلال Budget Approval و Risk Acceptance

P05-REQ-015 — هر Cost-bearing یا Material-risk Request باید پیش از AuthorizationDecision حداقل Contract زیر را Resolve کند:

~~~yaml
cost_risk_admission_id:
request_and_effect_references:
tenant_environment_purpose:
cost_exposure_band:
worst_case_cost_estimate:
estimate_method_and_price_version:
cardinality_concurrency_retry_duration_bounds:
budget_id:
cost_center:
budget_owner:
budget_authorization_reference:
reservation_id_and_amount:
reservation_status:
risk_id:
risk_tier:
risk_status:
risk_assessment_version:
risk_appetite_tolerance_capacity_references:
risk_owner:
control_effectiveness_references: []
residual_risk:
risk_acceptance_reference:
independent_challenge_reference:
monitoring_kri_kci_references: []
expiry_and_revalidation_triggers:
admission_decision:
denial_reasons: []
evidence_references: []
~~~

P05-CON-176 — Cost Control باید قبل از ایجاد Cost انجام شود؛ Alert پس از مصرف Hard Control نیست.

P05-CON-177 — Worst-case Cost Estimate باید محافظه‌کارانه، Versioned، Scope-bound و Evidence-linked باشد؛ Price Drift Revalidation Trigger است.

P05-CON-178 — Budget Reservation باید Atomic و Idempotent باشد و قبل از Provider/Resource Commitment رخ دهد.

P05-CON-179 — Actual Cost باید علیه Reservation Settle و Difference Reconcile شود؛ Receipt مالی Outcome فنی یا Risk Result نیست.

P05-CON-180 — Budget Hierarchy و Owner باید قابل‌حل باشد؛ Budget Parent/Child نباید Double-spend یا Scope Expansion ایجاد کند.

P05-CON-181 — Risk Assessment باید Inherent، Current Residual، Target Residual و Realized Impact را جدا نگه دارد.

P05-CON-182 — Risk Status باید Appetite، Tolerance، Capacity، Hard Limit، Control Effectiveness، Uncertainty، Correlation و Concentration را لحاظ کند.

P05-CON-183 — Control بدون Design/Operating-effectiveness Evidence معتبر نباید Residual Risk را کاهش دهد.

P05-CON-184 — `R3/R4` Risk Acceptance نیازمند Independent Challenge، Authorized Acceptor، Scope، Rationale، Alternatives، Compensating Control، Monitoring، Expiry و Revocation است.

P05-CON-185 — Risk Acceptance Expiry، KRI/KCI Breach، Control Failure، Scope Change، Environment Change، Provider Change یا Material Incident Reassessment/Block Trigger است.

P05-CON-186 — BudgetAuthorization، RiskAcceptance، SecurityAuthorization، Human Approval و Technical Validation پنج Record مستقل‌اند؛ هیچ‌کدام دیگری را اثبات نمی‌کند.

P05-CON-187 — Within Budget و Technically Functional بودن به معنی Risk Acceptable نیست؛ Within Appetite بودن به معنی Budget Available نیست.

P05-CON-188 — Admission منطقی باید حداقل معادل این Intersection باشد:

~~~text
COST_RISK_ADMISSION_ALLOWED =
COST_EXPOSURE_BOUNDED
AND WORST_CASE_ESTIMATE_CURRENT
AND BUDGET_OWNER_AND_SCOPE_VALID
AND BUDGET_AUTHORIZATION_VALID
AND RESERVATION_VALID
AND RISK_ASSESSMENT_CURRENT
AND RISK_NOT_PROHIBITED
AND RISK_WITHIN_CAPACITY
AND RISK_WITHIN_TOLERANCE_OR_VALID_TREATMENT_DECISION
AND REQUIRED_RISK_ACCEPTANCE_VALID
AND CONTROL_EFFECTIVENESS_SUPPORTED
AND MONITORING_PATH_READY
~~~

P05-CON-189 — هر `FALSE` یا `UNKNOWN` در Predicate بالا Effect Cost-bearing/Material-risk را Block می‌کند.

P05-CON-190 — `R5/PROHIBITED` و `ABOVE_CAPACITY` Approval-to-execute ندارند؛ Design/Context باید Condition را حذف کند.

P05-CON-191 — `ABOVE_TOLERANCE` فقط طبق P16-owned Authority/Policy می‌تواند Treatment/Restricted Operation/Stop داشته باشد؛ P05 هیچ Acceptance Authority واقعی اختراع نمی‌کند.

P05-CON-192 — Approved Lower-cost Route یا Degraded Mode فقط اگر از قبل Policy-approved، Quality/Security/Data/Risk-compliant و Effect-reducing باشد قابل‌استفاده است.

P05-CON-193 — Cost Reduction نمی‌تواند Quality، Science، Security، Privacy، Safety، Residency، Contract یا Evidence Requirement را کاهش دهد.

P05-CON-194 — Risk Benefit یا Opportunity نمی‌تواند Hard Constraint را Override کند.

P05-CON-195 — Aggregate Cost/Risk باید Request، Workflow، Service، Tenant، Provider، Product و Shared Dependency را طبق Source-owned Rules لحاظ کند؛ Per-request Pass کافی نیست.

P05-CON-196 — Cost/Risk Admission Record باید به Approval، AuthorizationDecision، Lease، Receipt، Outcome، Incident و Reconciliation Link شود و با آن‌ها ادغام نشود.

P05-DEN-090 — Unknown Cost برابر Zero نیست و Unknown Risk برابر Low نیست.

P05-DEN-091 — Budget Approval نباید به Risk Acceptance، Procurement Approval، Security Authorization یا Execution Lease تفسیر شود.

P05-DEN-092 — Risk Acceptance نباید Budget Commitment، Legal Waiver، Security Exception یا Execution Authorization ایجاد کند.

P05-DEN-093 — Risk Owner، Control Owner یا Proposer نباید High/Critical Residual Risk خود را به‌تنهایی قبول کند.

P05-DEN-094 — Risk Acceptance نباید Incident، Issue، Vulnerability یا Control Deficiency فعال را پنهان یا Closed اعلام کند.

P05-DEN-095 — Cost Cap نباید با Unbounded Concurrency، Retry، Egress، Duration، Autoscaling یا Non-interruptible Commitment جعلی باشد.

P05-DEN-096 — Provider Billing Delay نباید Runtime Metering/Quota/Reservation را جایگزین کند.

P05-DEN-097 — Expired Acceptance، Budget، Reservation، Price Snapshot یا Control Evidence قابل‌Reuse نیست.

P05-DEN-098 — Emergency Reserve فقط در Scope از قبل تصویب‌شده و برای Exposure Reduction/Critical Continuity معتبر است؛ Authority یا Risk Capacity را افزایش نمی‌دهد.

P05-DEN-099 — Automation نمی‌تواند Risk Appetite/Tolerance/Capacity، Budget Ceiling، Acceptance Authority یا Risk Tier خود را تغییر دهد.

P05-FAIL-051 — Budget Authorization معتبر ولی Risk Denied نتیجه `DENY` دارد؛ هیچ Offset مالی مجاز نیست.

P05-FAIL-052 — Risk Acceptance معتبر ولی Budget Missing نتیجه `DENY` دارد؛ هیچ Unfunded Execution مجاز نیست.

P05-FAIL-053 — Reservation Race/Overcommit/Conflict باید Request را Block و Ledger را Reconcile کند.

P05-FAIL-054 — KRI/KCI Breach یا Control Failure باید Admission را Reassess و طبق Policy Pause/Contain/Escalate کند.

P05-FAIL-055 — Cost/Risk Store یا Evidence Path Failure باید Variable-cost/Material-risk Work را Fail Closed کند.

## 14. Report Profile Selection — `LITE`، `STANDARD`، `FULL` و `DENY`

P05-DEF-024 — Strictness Order برای Routing:

`LITE < STANDARD < FULL < DENY`

`DENY` Richer Report نیست؛ Terminal No-execute Disposition و Denial/Incident Record است.

P05-REQ-016 — Profile باید پیش از Material Work براساس سخت‌گیرانه‌ترین Trigger از محورهای زیر تعیین شود:

`Effect + Risk + Data + Environment + Cost + Irreversibility + Scientific/AI Materiality + External Exposure + Legal/Privacy/Security Constraint`

P05-PROC-002 — Selection Algorithm:

~~~text
1. Resolve every profile-trigger axis independently.
2. Apply hard DENY conditions first.
3. Determine the minimum profile triggered by each resolved axis.
4. Select the strictest applicable profile.
5. If any material classification is missing:
   - select FULL for analysis/report preparation;
   - select DENY for effectful execution.
6. Aggregate child, dependency, target, tenant, retry, external and cost/risk triggers.
7. Record all triggers, not only the winning trigger.
8. Reclassify upward immediately when a stricter trigger appears.
9. Reclassification downward requires proof that every stricter trigger
   has been removed and a fresh server-side decision.
10. Profile completion never substitutes for approval, authorization,
    lease, verification or outcome.
~~~

P05-CON-197 — Base Effect Mapping:

| Effect | Minimum Profile Floor |
|---:|---|
| `E0..E2` | `LITE` فقط اگر تمام Eligibilityها برقرار؛ در غیر این صورت بالاتر |
| `E3..E5` | `STANDARD` |
| `E6..E8` | `FULL` |
| `E9` | `DENY` |

P05-CON-198 — Risk Mapping طراحی P05:

| Risk | Minimum Profile Floor |
|---|---|
| `R0/R1` و `WITHIN_APPETITE` | `LITE` Eligible فقط اگر سایر Axisها اجازه دهند |
| `R2` یا Treatment/Review معنادار | `STANDARD` |
| `R3/R4`، High/Critical، Above-tolerance-but-not-hard-prohibited Analysis | `FULL` |
| `R5/PROHIBITED/ABOVE_CAPACITY` | `DENY` برای Execution |
| `UNKNOWN/STALE/CONFLICTED` | `FULL` برای Analysis؛ `DENY` برای Execution |

P05-CON-199 — Data Mapping:

| Data Trigger | Minimum Profile Floor |
|---|---|
| Synthetic/Public و No-sensitive Join/Egress | `LITE` Eligible |
| Bounded Internal/Sensitive Read بدون Egress و Low Risk | `LITE` یا `STANDARD` طبق Effect/Materiality |
| Material Data/Privacy/Security Change | `STANDARD` یا `FULL` طبق Trigger |
| Sensitive Egress/Export، Cross-tenant، Public Release، Privileged/Secret-bearing | `FULL` |
| Unknown/Conflicted Classification/Purpose/Destination | `FULL` Analysis؛ `DENY` Execution |

P05-CON-200 — Environment Mapping:

| Environment Trigger | Minimum Profile Floor |
|---|---|
| `RESEARCH_OR_LOCAL/NON_PRODUCTION` | `LITE` یا `STANDARD` طبق سایر Axisها |
| `EXTERNAL_PILOT/PRODUCTION` | `FULL` |
| `ON_ORBIT_RUNTIME` در Baseline فعلی | `DENY / DEFERRED` |
| Unknown/Unsupported | `FULL` Analysis؛ `DENY` Execution |

P05-CON-201 — Cost Mapping:

| Cost Trigger | Minimum Profile Floor |
|---|---|
| `PREAPPROVED_NEGLIGIBLE` | `LITE` Eligible |
| `FIXED_BOUNDED/VARIABLE_BOUNDED` غیرمادی | `STANDARD` اگر Effectful |
| `MATERIAL` یا Provider/Long-term Commitment | `FULL` |
| `UNBOUNDED_OR_UNKNOWN` | `FULL` Analysis؛ `DENY` Execution |

P05-CON-202 — Irreversibility Mapping:

| Irreversibility | Minimum Profile Floor |
|---|---|
| `REVERSIBLE` | `LITE` یا `STANDARD` طبق Effect |
| `COMPENSABLE` | حداقل `STANDARD` |
| `RECOVERABLE_ONLY` | `FULL` اگر Material/Production/Sensitive |
| `DESTRUCTIVE_OR_IRREVERSIBLE` | `FULL`؛ `DENY` اگر Unbounded/Prohibited |
| `IRREVERSIBILITY_UNKNOWN` | `FULL` Analysis؛ `DENY` Execution |

P05-CON-203 — Scientific-baseline Change، Model/Prompt/Corpus/Tool Promotion، Provider Onboarding، Privileged Access، External Pilot/Publication، Production، High/Critical Risk، Material Spend، Destructive Change یا Material Legal/Privacy Impact همیشه `FULL` Trigger هستند.

P05-CON-204 — `DENY` Triggerها حداقل شامل `E9`، Invalid/Prohibited Purpose، Nonexistent Authority، Missing Mandatory Approval، Missing Critical Classification برای Execution، `R5/PROHIBITED/ABOVE_CAPACITY`، Prohibited Legal Condition، Unbounded Cost و Unbounded Destructive Target هستند.

P05-CON-205 — Profile Selector باید Server-side، Versioned، Policy-bound و Evidence-linked باشد.

P05-CON-206 — Profile Trigger Matrix Floor است؛ Part مالک Domain می‌تواند سخت‌گیرانه‌تر کند، نه آسان‌تر.

P05-CON-207 — `FULL` برای Analysis در حالت Unknown به معنی Execution Candidate نیست؛ همان Request تا Closure Unknown `DENY` می‌ماند.

P05-CON-208 — Profile باید Request/WorkflowRun/Step/Change Record را Bind کند و Validity/Reclassification Trigger داشته باشد.

P05-CON-209 — Exact Section Titles و Order هر Profile در Sectionهای 15–18 همین Part، Canonical Draft هستند.

P05-CON-210 — هر Section اجباری باید حاضر باشد؛ اگر واقعاً Not Applicable است، `NOT_APPLICABLE` همراه Applicability Rationale، Owner و Evidence ثبت شود، نه حذف Section.

P05-CON-211 — `UNKNOWN`، `NOT_FOUND`، Dissent، Counterevidence و Limitation باید در Profile متناظر آشکار بمانند.

P05-CON-212 — Profile Completion Status باید مستقل از GO/NO-GO، Approval، AuthorizationDecision، Test Pass، Lease، Execution و Outcome ثبت شود.

P05-DEN-100 — Client/Model/Agent/Workflow Author/Executor Self-selection قطعی Profile ممنوع است.

P05-DEN-101 — Desired Speed، Available Approver، Team Size، UI Mode، Deadline، AI Confidence یا Cost of Documentation دلیل Downgrade نیست.

P05-DEN-102 — Lower-risk Axis نمی‌تواند Higher-risk Trigger را خنثی کند.

P05-DEN-103 — `LITE` یا `STANDARD` برای Trigger بالاتر، Unknown Critical Classification یا Transitive High-impact Effect ممنوع است.

P05-DEN-104 — Profile Sectionها نباید با Link مبهم، Summary ناقص یا «Same as prior» بدون Exact Version/Digest حذف شوند.

P05-DEN-105 — `DENY` نباید به `FULL + Approval` تبدیل شود وقتی علت `E9/APR-X` یا Hard Prohibition است.

P05-FAIL-056 — Missing/Stale/Conflicted Profile Mapping نتیجه `REPORT_PROFILE_INDETERMINATE` دارد؛ Analysis `FULL` و Execution `DENY` است.

P05-FAIL-057 — Profile پایین‌تر از Trigger باید Work را `BLOCKED_BY_PROFILE_DOWNGRADE` کند.

P05-FAIL-058 — Missing Mandatory Section/Evidence باید Profile را `INCOMPLETE` کند؛ Completion یا GO Claim ممنوع است.

P05-FAIL-059 — Selector/Policy Outage باید Effectful Work را Fail Closed کند.

P05-FAIL-060 — Profile Misclassification کشف‌شده پس از Work باید Evidence، Reclassification، Impact Review و Incident/Defect متناسب ایجاد کند.

## 15. `LITE` Profile — تعریف قطعی طراحی و Exact Sections

P05-REQ-017 — `LITE` فقط وقتی مجاز است که تمام شروط زیر هم‌زمان برقرار باشند:

- Effect در `E0..E2` باشد؛
- Production، Privileged، External-write، Sensitive-data Egress یا Destructive Effect وجود نداشته باشد؛
- Cost کم و Bounded در Approved Envelope باشد؛
- Work Reversible باشد؛
- Scientific Baseline Change یا AI/Model Promotion وجود نداشته باشد؛
- Material Risk، Legal/Privacy Issue یا Critical Unknown حل‌نشده وجود نداشته باشد؛
- تمام Axisها Resolved و Profile Server-side انتخاب شده باشد.

Exact Sections `LITE`:

1. Intent and Exact Scope
2. Current Evidence and Assumptions
3. Effect, Data, Risk and Cost Classification
4. Files and Resources Touched
5. Validation Method
6. Reversal and Cleanup
7. Evidence to Retain
8. Approval/Policy Basis and GO/NO-GO

P05-CON-213 — Section 1 باید Intent، Purpose، Tenant/Environment، Target، Bound، Exclusion و Non-goal را دقیق کند.

P05-CON-214 — Section 2 باید Evidence Current، Assumption، Unknown، Source/Version و Limitation را جدا کند.

P05-CON-215 — Section 3 باید Effect، Data، Risk، Cost، Irreversibility، Profile Trigger و Unknown Status را ثبت کند.

P05-CON-216 — Section 4 باید تمام File/Resource/Record/Provider/External Pathهای Applicable را با Identity دقیق فهرست کند.

P05-CON-217 — Section 5 باید Validation Method، Expected Predicate، Evidence و Failure Rule را پیش از Effect مشخص کند.

P05-CON-218 — Section 6 باید Reversal Preconditions، Cleanup، Residual Effect و Unknown Handling را بیان کند.

P05-CON-219 — Section 7 باید Evidence ID/Type، Retention Owner، Integrity و Chain-of-custody Need را مشخص کند.

P05-CON-220 — Section 8 باید Policy Basis، Approval Class/Status، GO/NO-GO Rationale و Stop Condition را جداگانه ثبت کند؛ GO هیچ Execution Lease ایجاد نمی‌کند.

P05-DEN-106 — `LITE` نباید برای تغییر Authoritative/Production، Sensitive Egress، External Pilot، Model Promotion، Material Cost/Risk یا Irreversible Work استفاده شود.

P05-FAIL-061 — نقض هر Eligibility شرط `LITE` باید Profile را حداقل به `STANDARD/FULL/DENY` طبق Trigger Escalate کند.

## 16. `STANDARD` Profile — تعریف قطعی طراحی و Exact Sections

P05-REQ-018 — `STANDARD` Default برای `E3..E5` یا Change محدود، Bounded، Non-production و Reversible در System/Data/Workflow/Configuration است، مگر Trigger بالاتر `FULL/DENY` را الزام کند.

Exact Sections `STANDARD`:

1. Executive Summary
2. Requirements and Scope
3. Current State and Evidence
4. Assumptions and Unknowns
5. Gap and Impact Analysis
6. Risk and Threat Summary
7. Cost and Resource Impact
8. Current/Target Architecture Delta
9. Data, Privacy, Security, Science and AI Impact as Applicable
10. Control and Authority Matrix
11. Event, Audit and Evidence Impact
12. Exact Change Plan
13. Migration and Compatibility Plan
14. Test and Acceptance Plan
15. Rollout and Canary
16. Rollback, Recovery and Reconciliation
17. Residual Risk and Monitoring
18. Approval Requirements and GO/NO-GO

P05-CON-221 — `STANDARD` باید تمام ۱۸ Section را با Detail متناسب اما غیرحذف‌شده حفظ کند.

P05-CON-222 — Architecture Delta باید Component/Contract/Dataflow/Trust Boundary/Dependency Diff را بدون انتخاب Technology اختیاری پنهان نشان دهد.

P05-CON-223 — Control and Authority Matrix باید Actor/Role، Effect، APR، PERM، AUT، Authorization، Lease، Risk، Budget و Separation را مستقل نشان دهد.

P05-CON-224 — Exact Change Plan باید Subject/Resource/Sequence/Precondition/Postcondition/Owner/Evidence را مشخص کند؛ این Plan مجوز اجرا نیست.

P05-CON-225 — Test/Acceptance باید Requirement، Method/Oracle Owner، Data/Environment، Threshold/Tolerance و Failure Rule را Bind کند؛ P13 مالک Verification Method است.

P05-CON-226 — Rollout/Canary فقط اگر Environment/Release Owner اجازه دهد و Trigger `FULL` ایجاد نکند در `STANDARD` می‌ماند.

P05-CON-227 — Residual Risk/Monitoring باید Owner، Evidence، KRI/KCI، Review/Expiry و Escalation را ثبت کند.

P05-CON-228 — Section 18 باید تمام Approvalهای مستقل و NO-GO Triggerها را نشان دهد؛ Availability یک Approver Class را کاهش نمی‌دهد.

P05-DEN-107 — `STANDARD` نباید برای `E6..E8`، Production، External Pilot/Public Release، Sensitive Egress، Material Spend، Provider Onboarding، Privileged Access، Scientific/AI Promotion، High/Critical Risk یا Destruction استفاده شود.

P05-FAIL-062 — هر `FULL` Trigger کشف‌شده در `STANDARD` باید Work را Pause/Block و Report را به `FULL` Reclassify کند.

## 17. `FULL` Profile — تعریف قطعی طراحی و ۳۴ Section

P05-REQ-019 — `FULL` برای هر `E6..E8`، Production، External Pilot/Public Release، Sensitive Egress، Material Spend، Provider Onboarding، Privileged Access، Scientific-baseline Change، Model/Prompt/Corpus/Tool Promotion، High/Critical Risk، Destructive/Irreversible Change یا Material Legal/Privacy Impact اجباری است.

تمام ۳۴ عنوان Mandate باید دقیقاً حفظ شوند:

1. Executive Summary
2. Precise Understanding of Requirements
3. Current State with Evidence
4. Assumptions and Unknowns
5. Gap Analysis
6. Risk Register
7. Threat Model
8. Cost Model
9. Current Architecture
10. Target Architecture
11. Control Matrix
12. Capability Levels
13. Event/Audit Schema
14. Retention Model
15. Platform Support Matrix
16. Environment and Release Contract
17. Exact Change Plan at File, Service, and Infrastructure Level
18. Migration Strategy
19. Test and Acceptance Plan
20. Rollout and Rollback
21. Cost and Resource Impact
22. Residual Risks
23. Decisions Requiring Approval
24. GO/NO-GO Recommendation
25. Risk Governance, RACI, and Acceptance Authority Matrix
26. Risk Taxonomy, Methodology, and Calibration
27. Risk Appetite, Tolerance, Capacity, and Limits
28. Enterprise Risk Profile and Aggregation/Concentration Analysis
29. Business Impact Analysis and Critical-Dependency Map
30. Risk Treatment Plan and Risk Debt
31. KRI/KCI and Continuous Risk Monitoring Plan
32. AI/Model and Third-Party Risk Analysis where applicable
33. Scenario, Stress, and Reverse-Stress Test Plan
34. Control-Effectiveness and Independent-Assurance Plan

P05-CON-229 — `FULL` باید ۳۴ Section را به همین عنوان و Order حفظ کند؛ Compression می‌تواند Detail را متناسب کند اما Title/Obligation را حذف نمی‌کند.

P05-CON-230 — هر Section باید Source، Scope، Owner، Evidence، Unknown، Limitation، Decision/Action Need و Cross-referenceهای Applicable را حفظ کند.

P05-CON-231 — Risk Register باید Scenario، Owner، Inherent/Residual/Target Risk، Control Evidence، Treatment، Acceptance، Expiry، Correlation/Concentration و History را در حد Applicability پوشش دهد.

P05-CON-232 — Cost Model باید Worst-case، Variable Exposure، Reservation، Unit Economics، Commitment، Owner، Reconciliation و Unknown را پوشش دهد.

P05-CON-233 — Control Matrix باید Design و Operating Effectiveness را جدا کند؛ Control Claim بدون Evidence Risk را کاهش نمی‌دهد.

P05-CON-234 — Capability Levels باید `PERM/AUT/Effect Ceiling` و Capability Manifest را بدون ادغام نشان دهد.

P05-CON-235 — Event/Audit Schema باید Base Envelope P01 و Extension Profileهای Applicable را Reference کند، نه Base جایگزین بسازد.

P05-CON-236 — Environment and Release Contract باید P14/P15-owned Gateها را Reference کند؛ `FULL` آن‌ها را Pass‌شده اعلام نمی‌کند.

P05-CON-237 — Decisions Requiring Approval باید Subject، APR Floor، Domain Authorities، Separation، Digest، Validity و Missing Approval را دقیق کند.

P05-CON-238 — GO/NO-GO Recommendation باید Evidence/Unknown/Residual Risk/Hard Constraint را آشکار کند و از Approval/Authorization/Lease جدا باشد.

P05-CON-239 — Section 32 فقط در صورت Applicability `NOT_APPLICABLE` می‌شود و باید دلیل و Owner تأییدکننده داشته باشد.

P05-CON-240 — `FULL` Report Completion به‌تنهایی Approval، Scientific Validity، Verification Pass، Qualification، Release، Deployment Readiness، Execution یا Outcome نیست.

P05-DEN-108 — هیچ‌یک از ۳۴ Section نباید با «not needed» بدون Applicability Rationale، Source و Owner حذف شود.

P05-DEN-109 — `FULL` نباید به Ceremonial Report بدون Exact Scope، Evidence، Decision Owner، Threshold، Control و Action تبدیل شود.

P05-FAIL-063 — Missing Title/Section، Hidden Unknown، Unsupported Claim یا Orphan Requirement نتیجه `FULL_PROFILE_INCOMPLETE — NO_GO` دارد.

## 18. `DENY` Profile — Terminal No-execute و Exact Denial Record

P05-REQ-020 — `DENY` برای `E9`، Prohibited/Invalid Purpose، Nonexistent Authority، Missing Mandatory Approval، Missing Critical Classification برای Execution، `R5/PROHIBITED/ABOVE_CAPACITY`، Hard Legal/Safety/Privacy/Security Condition، Unbounded Cost، Unbounded Destructive Target یا هر Hard Intersection Failure اعمال می‌شود.

تعریف تازه و P05-owned برای Exact Denial Record، تحت Status همین Part و همچنان `NOT_APPROVED`:

1. Denial Executive Statement
2. Exact Request, Intent, Purpose and Scope
3. Actor, Tenant, Environment, Capability and Target Binding
4. Actual/Transitive Effect and Trigger Classification
5. Violated Invariant, Policy, Law or Source-bound Constraint
6. Missing, Invalid, Expired, Revoked or Conflicted Authority Records
7. Risk, Data, Cost, Irreversibility and External-exposure Basis
8. No-execute, Containment, Isolation and Lease/Path Revocation Status
9. Evidence, Provenance and Chain-of-custody References
10. Incident, Escalation and Independent-review References where Applicable
11. Permissible Correction or Redesign Conditions, if Any
12. Final Denial Disposition and Next Non-effectful Authorized Step

P05-CON-241 — `DENY` Output Approval Request نیست و نباید Execution Plan تولید کند.

P05-CON-242 — Section 5 باید Exact Clause/Policy/Source و Conflict Class Applicable را ثبت کند.

P05-CON-243 — Section 6 باید Record Typeها را جدا نگه دارد و Missing Approval را با Missing Permission یا Lease ادغام نکند.

P05-CON-244 — Section 8 باید Effect بیشتر را متوقف کند، اما Prior Attempt/Unknown Outcome را Success یا No-effect فرض نکند؛ Reconciliation ممکن است لازم باشد.

P05-CON-245 — Section 10 برای `E9` باید `INC-0` و Independent Review را ثبت کند.

P05-CON-246 — Section 11 فقط برای Condition قابل‌رفع می‌تواند Correction/Redesign را بیان کند؛ `E9/APR-X` هیچ Approval/Waiver/Exception Route ندارد و فقط Removal of Path مجاز است.

P05-CON-247 — Denial Record باید Immutable-history، Time-stamped، Source-linked و Non-repudiable در حد Applicable باشد.

P05-CON-248 — Denial Response نباید Secret، Sensitive Policy Detail یا Cross-tenant Existence را Leak کند؛ Evidence کامل در Protected Reference باقی می‌ماند.

P05-CON-249 — Denial Re-evaluation فقط با Request/Context/Source/Authority تازه و Record جدید ممکن است؛ Prior Denial Silent Overwrite نمی‌شود.

P05-CON-250 — `DENY` می‌تواند به Pause/Contain/Quarantine/Reject/Incident Route Bind شود، اما هیچ‌کدام Effect ممنوع را فعال نمی‌کنند.

P05-DEN-110 — Denial نباید با Retry، Alternate Route، External Tool، Human Mediation، Provider Console یا Archived Workflow دور زده شود.

P05-DEN-111 — `E9` Denial هیچ Escalation-to-approval، Exception، Break-glass، Externalization یا Human-only Exit ندارد.

P05-DEN-112 — Missing Authority نباید با Requester/Owner Identity یا Schedule Pressure جایگزین شود.

P05-FAIL-064 — اگر Denial Record ناقص است، Effect همچنان Denied می‌ماند؛ Failure گزارش Deny به معنی Allow نیست.

## 19. Aggregation، Reclassification، Escalation و جلوگیری از Profile Downgrade

P05-REQ-021 — Aggregate Profile باید بیشینۀ Profile تمام Stepها، Childها، Targets، Tenantها، Dependencies، Data/External Paths، Retry/Loopها، Cost/Risk Exposureها، Irreversibility و Transitive Effects را رعایت کند.

P05-CON-251 — Aggregation Operator برای Profile `max_strictness` است؛ Average، Majority، Percentile یا Dominant Low-risk Volume مجاز نیست.

P05-CON-252 — یک Child `FULL` کل Parent Scope مرتبط را حداقل `FULL` می‌کند، مگر Parent Work به‌طور Semantically/Operationally مستقل Split و Shared Trigger حذف‌شده باشد؛ Split برای Downgrade ممنوع است.

P05-CON-253 — یک `DENY` Trigger مرتبط Effectful Aggregate را Deny می‌کند؛ Siblingهای Allowed آن Trigger را خنثی نمی‌کنند.

P05-CON-254 — Cross-tenant، Bulk، Public، Shared Provider، Common Control، Common Credential و Cascading Dependency باید Aggregate Trigger ایجاد کنند.

P05-CON-255 — Cost/Risk Aggregation باید Retry، Fan-out، Concurrency، Duration، Commitment، Concentration و Common-mode Failure را لحاظ کند.

P05-CON-256 — Profile Reclassification Triggerها حداقل شامل Effect Escalation، New Target/Tenant، Data-class Change، Egress/Destination، Environment Promotion، Provider/Tool Change، Cost Estimate/Price Change، Risk/KRI Breach، Control Failure، Irreversibility Discovery و Legal/Policy Change هستند.

P05-CON-257 — Upward Reclassification باید Immediate باشد، Work را Pause/Block کند، Missing Sections/Evidence را تعیین کند و Approval/Authorization/Lease تازه را الزام نماید.

P05-CON-258 — Downward Reclassification فقط با Evidence حذف تمام Higher Triggers، Fresh Complete Classification، Owner/Reviewer Competence، Source/Policy Current و New Record ممکن است.

P05-CON-259 — Profile Change Record باید حداقل شامل موارد زیر باشد:

~~~yaml
profile_change_id:
request_or_workflow_reference:
prior_profile:
new_profile:
change_direction:
trigger:
trigger_source_and_evidence:
effect_risk_data_environment_cost_irreversibility_diff:
impacted_steps_targets_children:
missing_or_new_sections:
approval_authorization_lease_impact:
work_pause_or_block_status:
reviewer_and_owner_references:
effective_at: TemporalStamp
supersedes_reference:
~~~

P05-CON-260 — Material Scope Expansion همیشه Fresh Classification می‌خواهد؛ Approval/Profile قبلی Grandfathering ایجاد نمی‌کند.

P05-CON-261 — Profile را می‌توان برای Presentation لایه‌بندی کرد، اما Canonical Report باید تمام Sections Profile سخت‌گیرانه‌تر را حفظ کند.

P05-CON-262 — Reference به Artifact دیگر فقط وقتی Section را Satisfy می‌کند که Exact ID/Version/Digest، Scope، Freshness، Access، Status و Required Semantics را پوشش دهد.

P05-CON-263 — Reused Section باید Material Diff را آشکار کند؛ `unchanged` بدون Comparison Evidence کافی نیست.

P05-CON-264 — Partial Report باید `INCOMPLETE` باشد و Effectful Work را Block کند؛ درصد Completion مجوز نیست.

P05-CON-265 — Profile Routing و Approval Routing مستقل‌اند؛ Profile Escalation ممکن است APR را بالا ببرد اما Mapping دقیق باید جدا ثبت شود.

P05-CON-266 — Profile Aggregation و Effect Aggregation مستقل‌اند اما Mutual Input دارند؛ هیچ‌کدام دیگری را جایگزین نمی‌کند.

P05-CON-267 — Reclassification پس از Attempt باید علاوه بر Report، Underclassification Impact، Affected Evidence، Prior Approval/Lease Validity و Incident Need را بررسی کند.

P05-CON-268 — Profile Selector Version Change باید Existing Open Work را برای Compatibility/Reclassification ارزیابی کند؛ Silent Retroactive Downgrade ممنوع است.

P05-CON-269 — Emergency/Incident Mode می‌تواند `DENY` یا Higher Profile ایجاد کند، نه Lower Profile.

P05-CON-270 — Closure یک Profile نیازمند Section Completeness، Evidence Link، Open Issue Visibility و Final Disposition است؛ Closure Success/Approval نیست.

P05-DEN-113 — Work نباید برای فرار از `FULL` به چند `LITE/STANDARD` تقسیم شود.

P05-DEN-114 — Low-risk Majority، Low Average Cost یا Successful History نباید Single High/Critical Trigger را پنهان کند.

P05-DEN-115 — Profile پایین‌تر نباید به‌دلیل Documentation Burden، Deadline، Token Limit، Context Limit یا Reviewer Availability انتخاب شود.

P05-DEN-116 — Section Summary نباید Risk Register، Threat Model، Cost Model، Control Matrix یا Recovery Detail اجباری را برای `FULL` حذف کند.

P05-DEN-117 — Profile Cache یا Template قدیمی پس از Policy/Trigger Matrix Change معتبر نیست.

P05-DEN-118 — Downward Reclassification توسط Proposer/Executor/Model به‌تنهایی ممنوع است.

P05-FAIL-065 — Aggregate Trigger Missing یا Cardinality Unknown نتیجه `PROFILE_AGGREGATION_INDETERMINATE` و Execution Deny دارد.

P05-FAIL-066 — Upward Trigger حین Work باید `PROFILE_ESCALATION_REQUIRED — PAUSE/BLOCK` ایجاد کند.

P05-FAIL-067 — Unjustified Downgrade نتیجه `PROFILE_DOWNGRADE_VIOLATION` و Finding/Incident متناسب دارد.

P05-FAIL-068 — Missing Referenced Section/Artifact یا Stale Digest نتیجه `REPORT_REFERENCE_UNRESOLVED` و Incomplete دارد.

P05-FAIL-069 — Profile Selector Conflict میان Serviceها باید سخت‌گیرانه‌ترین Result را موقتاً اعمال و Conflict را برای Owner Review ثبت کند؛ Silent Merge ممنوع است.

## 20. اتصال دقیق به P01، P02، P03 و P04 و قفل مرز مالکیت

P05-REQ-022 — هر مصرف این Part باید قراردادهای بالادست را با Source Identity و Owner اصلی آن‌ها حفظ کند؛ P05 فقط Taxonomy، Intersection و Report-routing تحت مالکیت خود را می‌افزاید و هیچ تعریف بالادست را Replace، Reinterpret یا Promote نمی‌کند.

P05-CON-271 — اتصال P05 به P01 شامل موارد زیر است:

1. Project Identity، `EARTH_ORBIT_ONLY`، `TERRESTRIAL_BASELINE` و `ON_ORBIT_RUNTIME_DEFERRED`؛
2. Global Invariant Capsule و Permanent `E9/APR-X/INC-0/HARD_DENY` Boundary؛
3. Canonical Entity Envelope، `TemporalStamp`، Base Canonical Event Envelope و Extension-profile Registry؛
4. Record Separation و اصل Fail Closed؛
5. استقلال Effect، Approval، Permission، Autonomy، Risk Tier، Data Class، Environment Class، Cost Exposure و Irreversibility؛
6. استقلال Budget Approval، Security Authorization، Risk Acceptance، Human Approval و Technical Success.

P05-CON-272 — P05 تعریف Base Canonical Event Envelope، Canonical Entity، TemporalStamp، Domain Scope یا Technology Statusهای P01 را تکرار یا تغییر نمی‌دهد؛ فقط Referenceهای لازم را در Recordها و Event Implicationهای خود الزام می‌کند.

P05-CON-273 — اتصال P05 به P02 شامل Stage Work Packet، Source Lock، Decision/Approval/Action Separation، Lifecycle Gate Independence، Entry/Exit Criteria، Evidence-bound Acceptance و Handoff Protocol است.

P05-CON-274 — `PART_DECLARED_COMPLETE`، `PART_ACCEPTED_FOR_ASSEMBLY`، Design Review، Source Digest Match یا Handoff هیچ‌یک جای Gateهای مستقل `IMPLEMENTATION / VERIFICATION / VALIDATION / QUALIFICATION / RELEASE / DEPLOYMENT / OPERATION / FREEZE` متعلق به P02 را نمی‌گیرد.

P05-CON-275 — اتصال P05 به P03 شامل جداسازی `Query / ApplicationCommand / Event / Approval / AuthorizationDecision / ExecutionLease / ExecutionReceipt / Outcome`، Invocation Envelope، Idempotency، Ordering، Replay Protection و Exact Record References است.

P05-CON-276 — P05 فقط Classification و Binding Requirementهای Approval/Authorization/Lease را تعیین می‌کند؛ Record Semantics، API Contract، Transport، Receipt و Outcome Semantics متعلق به P03 باقی می‌مانند.

P05-CON-277 — اتصال P05 به P04 شامل Workflow/Step Context، Digest-bound Human Checkpoint، Separation of Duties، Pause/Block/Reconciliation، Retry/Compensation/Recovery Distinction، Aggregate Workflow Scope و Profile-routing Consumer Contract است.

P05-CON-278 — P05 Workflow State، Transition، Checkpoint UI، Scheduler، Compensation Algorithm یا Recovery State رقیب تعریف نمی‌کند؛ P04 باید Profile و Authority Result این Part را مصرف کند و P05 باید Workflow Record Referenceهای P04 را حفظ نماید.

P05-CON-279 — Cross-Part Binding باید حداقل Tuple زیر را حمل کند:

~~~yaml
source_part_id:
source_owner_artifact_id:
source_owner_version:
source_owner_digest:
source_status:
source_clause_or_section:
consumed_semantic:
consumer_clause:
ownership_mode: REFERENCE_ONLY|P05_OWNED_EXTENSION
conflict_status:
~~~

P05-CON-280 — `REFERENCE_ONLY` یعنی P05 حق تغییر تعریف، Status، Approval یا Owner را ندارد. `P05_OWNED_EXTENSION` فقط برای Effect/Approval/Permission/Autonomy، Authority Intersection، Cost/Risk Admission و Report Profile مجاز است.

P05-CON-281 — اگر Clause بالادست و Requirement P05 در Scope متفاوت‌اند، هر دو باید با Scope صریح حفظ شوند؛ Model حق ندارد با Summary آن‌ها را یکسان یا یکی را Superseded اعلام کند.

P05-CON-282 — تعارض واقعی میان Ownerها باید `CONFLICTED — FAIL_CLOSED` ثبت و برای P18/P16 یا Domain Owner مربوط Route شود؛ P05 به‌تنهایی Conflict Taxonomy یا Disposition نهایی را تعیین نمی‌کند.

P05-CON-283 — P01 `CGR-REQ-002`، `CGR-REQ-016` و `CGR-REQ-018` را مالک است؛ P05 آن‌ها را برای Command Prohibition، Event Identity و Typed Time مصرف می‌کند.

P05-CON-284 — P02 `CGR-REQ-034` را مالک است؛ P05 استقلال Design/Implementation/Verification/Validation/Qualification/Release/Deploy/Operate/Freeze را مصرف می‌کند.

P05-CON-285 — P03 `CGR-REQ-007` و `CGR-REQ-008` را مالک است؛ P05 Record Separation و Typed Bounded ApplicationCommand را مصرف می‌کند.

P05-CON-286 — P04 `CGR-REQ-009` و `CGR-REQ-010` را مالک است؛ P05 Explicit Workflow State و Digest-bound Human Checkpoint/Separation of Duties را مصرف می‌کند.

P05-CON-287 — P05 مالک اصلی `CGR-REQ-011`، `CGR-REQ-012`، `CGR-REQ-013`، `CGR-REQ-014`، `CGR-REQ-015`، `CGR-REQ-023` و `CGR-REQ-027` است؛ Consumerها باید Definition همین Part را Reference کنند و حق ایجاد Taxonomy موازی ندارند.

P05-CON-288 — P13 مالک `CGR-REQ-022` و Verification Method است؛ P05 Traceability/Orphan Contract و Verifiable Claims را تحویل می‌دهد اما Test Oracle نهایی را تصاحب نمی‌کند.

P05-CON-289 — P10/P11 مالک Canonical Data Classification و Security/Privacy Enforcement؛ P12 مالک Evidence/Telemetry و Cost Accounting؛ P14/P15 مالک Environment/Release/Delivery؛ P16 مالک Risk Governance/Authority؛ و P18 مالک Compilation/Conflict Disposition است. P05 فقط Facts و Gate Resultهای این حوزه‌ها را در Intersection مصرف می‌کند.

P05-CON-290 — Consumer Part نمی‌تواند به دلیل داشتن تعریف تخصصی‌تر، `E9/APR-X`، Fail-closed Intersection، Exact Approval Binding یا Profile-downgrade Prevention را حذف کند؛ تخصص پایین‌دست فقط می‌تواند کنترل سازگار و سخت‌گیرانه‌تر اضافه کند.

P05-CON-291 — هر Downstream Override ادعایی باید Source-bound Change/Conflict Record داشته باشد؛ تا Disposition معتبر، تصمیم مؤثر سخت‌گیرانه‌ترین Constraint است.

P05-DEN-119 — P05 نباید Base Event Envelope P01، Stage/Gate Protocol P02، Invocation Record P03 یا Workflow State P04 را با Alias تازه بازتعریف کند.

P05-DEN-120 — Consumer نباید Approval Record P03 را با Approval Class P05، Workflow Checkpoint P04 یا Human Click یکی بداند.

P05-DEN-121 — Part Order یا Newer Part Index Precedence معنایی ایجاد نمی‌کند؛ Semantic Owner و Source Hierarchy حاکم‌اند.

P05-DEN-122 — Reference به P01–P04 بدون Exact Part/Owner/Version/Digest/Clause برای Claim مادی کافی نیست.

P05-DEN-123 — Status `APPROVED` در یک Source پایین‌دست نباید Status `NOT_APPROVED` Semantic Owner P05 را Launder کند.

P05-DEN-124 — Missing Downstream Vocabulary نباید در P05 با حدس پر شود؛ فقط Boundary، Expected Consumer و `NOT_FOUND/OPEN_ISSUE` ثبت می‌شود.

P05-FAIL-070 — Owner Collision یا Competing Definition نتیجه `SEMANTIC_OWNER_CONFLICT — FAIL_CLOSED` دارد.

P05-FAIL-071 — Unresolved Cross-part Reference یا Digest نتیجه `CROSS_PART_BINDING_UNRESOLVED` و Block برای Normative Promotion دارد.

P05-FAIL-072 — Status Drift یا Approval Inheritance نتیجه `STATUS_LAUNDERING_VIOLATION — REWORK_REQUIRED` دارد.

P05-FAIL-073 — اگر Consumer نتواند Contract بالادست را بدون Loss حفظ کند، باید `INCOMPATIBLE_CONSUMER_MAPPING` ثبت کند؛ Silent Compression ممنوع است.

## 21. Architecture Contract و Logical Authority Components

P05-REQ-023 — Architecture این حوزه باید به‌صورت Logical، Replaceable، Policy-bound و Fail-closed طراحی شود و حداقل Component Boundaryهای زیر را مستقل نگه دارد؛ این Contract هیچ Technology، Service Product، Deployment Topology یا Implementation را انتخاب نمی‌کند.

P05-DEF-025 — `AuthorityClassificationSnapshot` مجموعه‌ای Atomic و Time-bound از Effect، Approval Floor، Permission Resolution، Autonomy Ceiling، Risk/Data/Environment/Cost/Irreversibility Facts، Profile، Source Versions و Unknownها برای یک Request Digest دقیق است.

P05-CON-292 — Logical Componentهای P05-owned عبارت‌اند از:

1. Effect and Dependency Classifier؛
2. Approval-floor and Binding Validator؛
3. Permission-domain and Competence Resolver؛
4. Autonomy-ceiling Resolver؛
5. Cross-axis Authority Intersection Evaluator؛
6. Cost/Risk Admission Coordinator؛
7. Report Profile Selector and Reclassifier؛
8. Authority Classification/Decision-evidence Recorder.

P05-CON-293 — Componentهای بالا Logical Boundary هستند؛ می‌توانند در Deployment آینده ادغام یا جدا شوند، اما Semantic Separation، Independent Records، Traceability و Fail-closed Behavior نباید از بین برود.

P05-CON-294 — Effect Classifier باید Operation، Capability Manifest، Dependency Graph، Target Cardinality، Data Movement، Environment، External Destination، Credential Use، Retry/Fan-out، Cost و Recovery/Destruction را مصرف و Maximum Actual/Transitive Effect را تولید کند.

P05-CON-295 — Approval-floor Resolver فقط Minimum Class و Required Domain/Independence Set را محاسبه می‌کند؛ Approval صادر نمی‌کند.

P05-CON-296 — Approval Binding Validator باید Exact Record، Scope، Digest، Competence، Independence، Validity، Nonce، Consumption و Revocation را بررسی کند؛ Valid Result نیز AuthorizationDecision یا Lease نیست.

P05-CON-297 — Permission Resolver باید Identity/Role/Domain/Competence/Delegation/Tenant/Purpose/Environment/Operation Scope را از Authority Source معتبر Resolve کند و نتیجه Missing یا Conflicted را مجاز تلقی نکند.

P05-CON-298 — Autonomy Resolver باید Capability/Manifest Ceiling، Required Human Boundary، Data/External Access، Reversibility، Effect Class و Prohibited Autonomous Actions را Resolve کند؛ Model یا Client Ceiling قطعی تعیین نمی‌کند.

P05-CON-299 — Intersection Evaluator باید تمام Axis Resultها، Hard Prohibitionها و Gate Statusها را در یک Snapshot منسجم و Versioned ارزیابی کند؛ Join جزئی یا Time-inconsistent Result مجاز نیست.

P05-CON-300 — Cost/Risk Admission Coordinator فقط Reservation/Authorization/Risk Status Referenceهای Ownerهای اصلی را جمع و Consistency را ارزیابی می‌کند؛ Budget یا Risk Acceptance صادر نمی‌کند.

P05-CON-301 — Profile Selector باید Strictest Trigger و Exact Section Obligation را تولید کند؛ Report Generation یا Completion هیچ Authority ایجاد نمی‌کند.

P05-CON-302 — Recorder باید Source، Input Digest، Version، Classification، Unknown، Decision Basis، Counterevidence، Reclassification و Supersession Chain را حفظ کند و Silent Overwrite نداشته باشد.

P05-CON-303 — Minimum Input Contract برای Authority Classification:

~~~yaml
classification_request_id:
request_reference:
request_digest:
actor_and_workload_identity_reference:
tenant_and_purpose:
environment_reference:
operation_and_capability_reference:
capability_manifest_digest:
dependency_graph_digest:
targets_and_cardinality:
data_manifest_and_destinations:
risk_context_reference:
cost_estimate_and_budget_context_reference:
irreversibility_and_recovery_facts:
policy_snapshot_references: []
source_versions_and_digests: []
observed_at: TemporalStamp
~~~

P05-CON-304 — Minimum Output Contract برای Classification Snapshot:

~~~yaml
classification_snapshot_id:
request_digest:
effect_class:
effect_basis_and_graph_reference:
approval_floor:
required_domain_authorities: []
permission_result:
autonomy_ceiling:
risk_tier_and_status:
data_admission_facts:
environment_admission_class:
cost_exposure_band:
irreversibility_class:
report_profile:
hard_constraints: []
unknowns_and_conflicts: []
source_and_policy_versions: []
valid_from: TemporalStamp
expires_at: TemporalStamp
result: COMPLETE|INDETERMINATE|DENIED
supersedes_reference:
evidence_and_provenance_references: []
~~~

P05-CON-305 — Classification Snapshot فقط برای Request Digest، Context، Source/Policy Version و Validity Window خود معتبر است؛ Reuse میان Tenant، Environment، Target، Provider یا Revision ممنوع است.

P05-CON-306 — Logical Dataflow باید `request facts → effect graph → axis resolution → strictest profile → approval requirement → exact binding validation → intersection result` را حفظ کند؛ Shortcut مستقیم از Request به Execution ممنوع است.

P05-CON-307 — AuthorizationDecision و ExecutionLease پس از Intersection نیز فقط توسط P03/P11/P16-owned Controlها و طبق Workflow P04 قابل‌صدورند؛ P05 Output صرفاً ورودی Constraint است.

P05-CON-308 — Trust Boundary باید Client/Model/Tool/Plugin/External Provider Input را `UNTRUSTED_UNTIL_VALIDATED` در نظر بگیرد و Server-resolved Registry/Policy/Evidence را از Self-asserted Label جدا کند.

P05-CON-309 — Cache Boundary باید Key کامل Request/Target/Manifest/Policy/Source/Environment/Price/Risk Version، Freshness، Revocation و Invalidation داشته باشد؛ Partial Key ممنوع است.

P05-CON-310 — Time Boundary باید TemporalStamp و Clock/Time-source Confidence کافی برای Validity/Expiry/Ordering داشته باشد؛ Time Unknown مجوز استفاده از Approval یا Lease نمی‌دهد.

P05-CON-311 — Consistency Boundary باید اجازه ندهد Classification جدید با Approval قدیمی، Permission Revoked، Risk Stale یا Budget Reservation متفاوت ترکیب شود.

P05-CON-312 — Availability Design باید Deny-only Containment را از Effect-expanding Recovery جدا کند؛ Failover Component نمی‌تواند Authority Ceiling را افزایش دهد.

P05-CON-313 — Bypass Resistance باید Direct DB/API/Console/Tool/Provider/Queue/Batch/Retry/Human-mediated Path را در Effect Graph و Enforcement Boundary پوشش دهد.

P05-CON-314 — Architecture Evidence باید Component/Contract/Owner/Trust Boundary/Dataflow/Failure Mode/Control/Trace و Open Issue را نشان دهد؛ Diagram یا Name به‌تنهایی Evidence نیست.

P05-CON-315 — Replaceability باید Semantic Conformance را حفظ کند؛ تعویض Policy Engine، Registry، Workflow Engine یا Provider نیازمند Compatibility/Reclassification و Verification مستقل است.

P05-DEN-125 — هیچ Logical Component حق Self-classification نهایی Request متعلق به خود یا Self-approval/Permission/Autonomy Escalation ندارد.

P05-DEN-126 — Frontend، Prompt، SDK، Decorator، Annotation، HTTP Method یا Tool Description Enforcement Point قطعی نیست.

P05-DEN-127 — Architecture نباید Approval Validator را با Credential Validator یا Permission Resolver ادغام معنایی کند.

P05-DEN-128 — Central Component نباید بدون Bound به Single Point of Unreviewed Authority تبدیل شود.

P05-DEN-129 — Policy Service نمی‌تواند Beyond-manifest Grant بسازد؛ فقط در Bound معتبر Allow/Constrain/Deny می‌کند.

P05-DEN-130 — Availability/Failover Path نباید Stale Snapshot، Cached Approval یا Missing Revocation را Fail Open کند.

P05-DEN-131 — این Architecture Contract انتخاب Implementation، Provider، Database، Broker، Language، Framework یا Cloud نیست.

P05-FAIL-074 — Partial Join میان Axisها نتیجه `AUTHORITY_SNAPSHOT_NON_ATOMIC — DENY` دارد.

P05-FAIL-075 — Classification Snapshot Expired یا Source-version Mismatch نتیجه `AUTHORITY_SNAPSHOT_STALE — RECOMPUTE_OR_DENY` دارد.

P05-FAIL-076 — Resolver Disagreement نتیجه `AUTHORITY_CLASSIFICATION_CONFLICTED` و سخت‌گیرانه‌ترین Temporary Result تا Review دارد.

P05-FAIL-077 — Detected Bypass Path باید Path را Isolate و Finding/Incident متناسب ایجاد کند؛ E9-related Path همیشه `INC-0` است.

P05-FAIL-078 — Cache Invalidation یا Revocation-feed Failure باید Effectful Work را Block کند.

P05-FAIL-079 — Time-source/ordering Uncertainty که Validity را غیرقابل‌اثبات کند نتیجه `AUTHORITY_TIME_INDETERMINATE — DENY` دارد.

## 22. Lifecycle، Record Separation و Boundary Revalidation

P05-REQ-024 — Authority Lifecycle باید از Intent تا Reconciliation تمام Axisها را مستقل، Revalidatable و Traceable نگه دارد و هیچ Stage Completion را به مجوز Stage بعدی تبدیل نکند.

P05-CON-316 — Lifecycle منطقی P05 به‌ترتیب زیر است؛ این توالی Workflow State Machine P04 را جایگزین نمی‌کند:

1. Receive typed Request/Intent facts؛
2. Resolve Actor، Tenant، Purpose، Environment، Capability و Target؛
3. Close Dependency/Transitive-effect Graph؛
4. Compute Maximum Actual/Aggregated Effect؛
5. Resolve Risk/Data/Environment/Cost/Irreversibility Facts؛
6. Resolve Permission Domain و Autonomy Ceiling؛
7. Derive Approval Floor و Required Authorities؛
8. Select Strictest Report Profile؛
9. Complete Required Report/Evidence without treating it as Approval؛
10. Validate Exact Approval، Budget، Risk، Security/Privacy و Domain Records؛
11. Produce AuthorityIntersectionRecord؛
12. Allow P03-owned AuthorizationDecision/Lease processing only if all Gates pass؛
13. Revalidate at Execution Boundary؛
14. Observe Receipt/Outcome/Reconciliation references؛
15. Reclassify، Revoke، Supersede یا Close Classification history as facts change.

P05-CON-317 — Lifecycle Step 1 Request است، نه Approval یا Action. Intent باید Purpose/Scope/Non-goal و Requested Effect را از Actual Effect Truth جدا نگه دارد.

P05-CON-318 — Stepهای 2 تا 8 Classification و Admission Preparation هستند؛ هیچ‌کدام Execution Right ایجاد نمی‌کنند.

P05-CON-319 — Step 9 Documentation Obligation است؛ `LITE/STANDARD/FULL` Completion فقط Evidence/Decision Preparation است.

P05-CON-320 — Step 10 باید هر Authority Record را مستقل Validate کند و Absence یک Record را با Strength Record دیگر جبران نکند.

P05-CON-321 — Step 11 Result می‌تواند `ALLOW_CANDIDATE_WITH_CONSTRAINTS`، `REQUIRE_APPROVAL_OR_REMEDIATION` یا `DENY` باشد؛ نام دقیق Authorization Outcome متعلق به P03/P11 است و این Part Execution را Allow نمی‌کند.

P05-CON-322 — Step 12 مشروط به Separate AuthorizationDecision است؛ Approval موجود یا Intersection Complete به معنی Decision صادرشده نیست.

P05-CON-323 — Step 13 باید Identity، Request/Target Digest، Effect، Policy، Approval، Permission، AUT، Risk، Data، Environment، Cost، Irreversibility، Time، Revocation و Lease را دوباره بررسی کند.

P05-CON-324 — هر Material Diff بین Classification و Execution Boundary Snapshot قبلی را Invalid و Reclassification/Approval/Lease تازه را لازم می‌کند.

P05-CON-325 — Step 14 Receipt/Outcome را فقط Reference می‌کند؛ موفقیت Transport، HTTP، Queue Ack، Tool Return یا Provider Receipt به معنی Valid Outcome نیست.

P05-CON-326 — Step 15 History را با Supersession/Correction حفظ می‌کند؛ Closure Classification به معنی Risk Closure، Approval، Verification یا Project Freeze نیست.

P05-CON-327 — Record Separation Matrix:

| Record | سؤال اصلی | Owner معنایی | رابطۀ P05 |
|---|---|---|---|
| Request/Query/ApplicationCommand | چه چیزی درخواست شد؟ | P03 | Input Reference |
| WorkflowRun/Step/Checkpoint | فرایند در چه State است؟ | P04 | Context Reference |
| EffectClassificationRecord | بیشینۀ Effect چیست؟ | P05 | Owner |
| Approval Requirement/Binding | چه Approval لازم و معتبر است؟ | P05 taxonomy؛ P03 record semantics | Constraint/Validation |
| Permission Assignment/Competence Evidence | Actor در چه Domain مجاز است؟ | P11/P16 record authority؛ P05 taxonomy | Resolve/Validate |
| Autonomy Ceiling Assignment | چه Attempt خودکاری ممکن است؟ | P05 taxonomy؛ P08 manifest consumer | Resolve/Validate |
| ReportProfileRecord | چه Report Obligation لازم است؟ | P05 | Owner |
| Budget Authorization/Reservation | چه Cost Scope مجاز/رزرو شده؟ | Finance/Cost owners P12/P16 | Independent Reference |
| Risk Assessment/Acceptance | چه Residual Risk و Authority وجود دارد؟ | P16 | Independent Reference |
| AuthorizationDecision | آیا Request دقیق Policy-authorized است؟ | P03/P11 | Input from P05; separate record |
| ExecutionLease | آیا Attempt دقیق، کوتاه‌عمر و Revocable است؟ | P03/P11 | Separate downstream record |
| ExecutionReceipt | چه Attempt/Effect مشاهده شد؟ | P03/P12 | Independent evidence reference |
| Validated Outcome | Intended Transition واقعاً چه شد؟ | P03 + Domain owner | Independent outcome |

P05-CON-328 — One Record ID نباید هم‌زمان نقش Approval، AuthorizationDecision، Lease، Receipt یا Outcome را بازی کند؛ Correlation فقط با Referenceهای صریح است.

P05-CON-329 — Approval Consumption، Lease Consumption و Command Idempotency Stateهای متفاوت‌اند؛ یکی دیگری را مصرف‌شده یا موفق نمی‌کند.

P05-CON-330 — Permission Assignment معمولاً Longer-lived است اما Transaction Scope، Competence، Conflict و Revocation در هر Request دوباره بررسی می‌شود.

P05-CON-331 — Autonomy Ceiling می‌تواند Capability/Environment-specific باشد و باید Version/Manifest-bound باشد؛ Ceiling بالاتر Permission یا Approval بالاتر ایجاد نمی‌کند.

P05-CON-332 — Risk Acceptance و Budget Authorization باید Expiry/Revocation/Scope جدا داشته باشند و Revalidation مستقل شوند.

P05-CON-333 — Cancellation، Revocation، Denial، Expiry، Failure، Receipt Missing و Outcome Unknown State/Recordهای متمایزند؛ هیچ‌کدام خودکار Success/No-effect نیست.

P05-CON-334 — Retry یک Request/Attempt تازه یا Link‌شده است و باید Effect Aggregation، Cost/Risk، Approval Consumption، Lease و Idempotency را دوباره Evaluate کند.

P05-CON-335 — Compensation/Recovery/Restoration Effectهای مستقل‌اند و Class/Approval/Profile خود را می‌خواهند؛ «بازگردانی» به‌طور پیش‌فرض E0 نیست.

P05-CON-336 — Emergency Containment فقط اگر Exposure را کاهش دهد، Scope/TTL از قبل تصویب‌شده داشته باشد و Evidence/Review تولید کند قابل Route است؛ Restoration Lifecycle عادی را طی می‌کند.

P05-CON-337 — Revocation باید Future Attempt را Block کند، Active Lease را Fence/Revoke کند و Current State/Outcome را Reconcile نماید؛ Revocation به‌تنهایی Undo نیست.

P05-CON-338 — Long-running Work باید Periodic/Re-trigger Revalidation برای Policy، Effect Graph، Target، Risk، Cost، Data، Environment، Approval و Lease داشته باشد.

P05-CON-339 — Reconciliation باید Expected/Observed/Unknown Effect، Receipt، Provider State، Budget Settlement، Evidence Gap و Required Incident/Recovery را جدا ثبت کند.

P05-CON-340 — Lifecycle Evidence باید Causal Links و TemporalStampهای P01 را حفظ کند؛ Timestamp بدون Time Scale یا Uncertain Ordering برای Approval/Lease Validity کافی نیست.

P05-DEN-132 — Report Completion، Approval Issuance یا Lease Issuance نباید Workflow/Execution/Outcome را Implicitly Advance کند.

P05-DEN-133 — Resume پس از Pause/Failure/Revocation بدون Fresh Revalidation ممنوع است.

P05-DEN-134 — Retry نباید Approval Single-use، Cost Cap، Risk Limit، Target Bound یا Profile Trigger را Reset کند.

P05-DEN-135 — Compensation Label نباید Destructive/External/Costly Effect واقعی را کاهش دهد.

P05-DEN-136 — Outcome Unknown نباید برای Closure، Billing، Risk یا Evidence به Success/Failure قطعی تبدیل شود.

P05-DEN-137 — Record Correlation by Timestamp/Name/Actor بدون Exact ID/Causation Reference مجاز نیست.

P05-DEN-138 — Emergency/Break-glass هیچ Route برای E9، Scope Expansion، Budget Ceiling Increase، Risk Acceptance، Evidence Destruction یا Data-class Downgrade ایجاد نمی‌کند.

P05-FAIL-080 — Revalidation Failure نتیجه `BOUNDARY_REVALIDATION_FAILED — DO_NOT_EXECUTE_OR_CONTINUE` دارد.

P05-FAIL-081 — Receipt Missing یا Provider Outcome Ambiguous نتیجه `EFFECT_OUTCOME_UNKNOWN — RECONCILE` دارد.

P05-FAIL-082 — Record-role Collision نتیجه `AUTHORITY_RECORD_CONFLATION` و Invalidity دارد.

P05-FAIL-083 — Revocation during Attempt باید `REVOCATION_IN_FLIGHT`، Fence/Stop best effort، Preserve Evidence و Reconciliation ایجاد کند.

P05-FAIL-084 — Retry/Recovery که Class یا Profile بالاتر ایجاد کند باید Pause و Fresh Approval/Lease بخواهد.

P05-FAIL-085 — Lifecycle History Gap نتیجه `AUTHORITY_LIFECYCLE_INCOMPLETE` است؛ Absence Record Success نیست.

## 23. Event Implications بدون بازتعریف Base Canonical Event Envelope

P05-REQ-025 — هر Fact مادی Authority باید در صورت وقوع و Applicability به Eventی با Base Canonical Event Envelope P01 و Extension Profile مناسب متصل شود؛ Event Fact است و Command، Approval یا Outcome نیست.

P05-CON-341 — P05 فقط Event Type/Fact Implicationهای حوزۀ خود را تعیین می‌کند؛ Field Identity، Envelope Versioning، Delivery Semantics، TemporalStamp و Extension Registry متعلق به P01 باقی می‌مانند.

P05-CON-342 — Eventهای Authority باید `EVT-SEC-AUD` را برای Actor/Policy/Approval/Permission/Authorization Context و `EVT-RISK-COST` را برای Risk/Budget/Cost Context در حد Applicability Reference کنند.

P05-CON-343 — `EVT-REL-EVID` برای Digest/Manifest/Policy/Source/Evidence/Supersession و `EVT-REL-OBS` برای Availability/Latency/Retry/Quality Context قابل‌استفاده است؛ هیچ Extension Base را جایگزین نمی‌کند.

P05-CON-344 — Minimum Authority Fact Event Types عبارت‌اند از:

1. `AUTHORITY_CLASSIFICATION_REQUESTED`؛
2. `EFFECT_CLASSIFIED`؛
3. `EFFECT_CLASSIFICATION_INDETERMINATE`؛
4. `EFFECT_RECLASSIFIED`؛
5. `APPROVAL_REQUIREMENT_DERIVED`؛
6. `APPROVAL_VALIDATED`؛
7. `APPROVAL_REJECTED_OR_INVALID`؛
8. `APPROVAL_EXPIRED_REVOKED_CONSUMED`؛
9. `PERMISSION_RESOLVED_OR_DENIED`؛
10. `AUTONOMY_CEILING_RESOLVED_OR_DENIED`؛
11. `AUTHORITY_INTERSECTION_EVALUATED`؛
12. `REPORT_PROFILE_SELECTED`؛
13. `REPORT_PROFILE_ESCALATED_OR_DOWNGRADE_REJECTED`؛
14. `COST_RISK_ADMISSION_EVALUATED`؛
15. `AUTHORITY_BOUNDARY_REVALIDATION_FAILED`؛
16. `PROHIBITED_PATH_DETECTED`.

P05-CON-345 — Event Name فقط Human-readable Type است؛ Semantics باید Schema Version، Source Clause، Request/Classification/Record Reference و Outcome State صریح داشته باشد.

P05-CON-346 — Classification Event باید Request Digest، Prior/New Class، Trigger، Graph/Target Reference، Source/Policy Version، Validity، Unknown و Evidence References را حمل کند.

P05-CON-347 — Approval Event باید Approval ID/Class/State، Request/Presentation/Target Digest، Scope، Validity، Consumption/Revocation و Reason Reference را حمل کند؛ Sensitive Details Protected Reference می‌مانند.

P05-CON-348 — Permission/Autonomy Event باید Assignment/Manifest Version، Domain/Scope، Competence/Ceiling، Expiry/Revocation و Conflict Status را جدا نگه دارد.

P05-CON-349 — Intersection Event باید Axis Resultها را به‌صورت Referenceable و جدا ثبت کند؛ Flattened `allowed=true` بدون Basis ممنوع است.

P05-CON-350 — Profile Event باید Prior/New Profile، Strictest Trigger، Exact Required Sections، Missing Evidence، Work Pause/Block Status و Reclassification Reason را ثبت کند.

P05-CON-351 — Cost/Risk Admission Event باید Budget Authorization/Reservation و Risk Assessment/Acceptance را دو Reference مستقل نگه دارد.

P05-CON-352 — Prohibited Path Event برای E9 باید Unsampled، High-priority، Tamper-evident، `INC-0`-linked و Evidence-preserving باشد.

P05-CON-353 — Event Publication نباید Pre-commit Fact را به Committed Fact تبدیل کند؛ Proposed، Validated، Issued، Consumed، Attempted و Outcome Stateها جدا هستند.

P05-CON-354 — Event Consumer باید Idempotent و Duplicate-aware باشد و Event Arrival را Authority Grant تلقی نکند.

P05-CON-355 — Out-of-order Event باید با Entity Revision/Sequence/Causation و Current Source State Reconcile شود؛ Last-arrival-wins ممنوع است.

P05-CON-356 — Revocation/Expiry Event Delay Window باید Bounded باشد و Consumer تا اثبات Freshness Fail Closed بماند.

P05-CON-357 — Event Sampling برای Approval، Revocation، Denial، Effect Reclassification، Destruction، E9، Security/Privacy Incident و Critical Risk/Cost Gate مجاز نیست.

P05-CON-358 — Event Payload نباید Secret، Credential، Raw Sensitive Payload، Cross-tenant Identifier یا Unnecessary Personal Data افشا کند؛ Protected Reference و Data Minimization لازم است.

P05-CON-359 — Event Correction با New Correction/Superseding Event انجام می‌شود و Original History حفظ می‌گردد.

P05-CON-360 — Event Transport Ack، Delivery، Processing یا Projection Success به معنی Approval، Authorization، ExecutionReceipt یا Outcome نیست.

P05-CON-361 — Event Projection/Index/Cache Derivative است و نمی‌تواند Source Approval/Permission/Policy Record را Silent Replace کند.

P05-CON-362 — Cross-tenant Event Route، Topic، Partition، Cursor، Error و Timing باید Tenant Isolation و Purpose Bound را حفظ کند.

P05-CON-363 — Event Evidence باید Producer Identity/Version، Payload Schema، Source Timestamp/Scale، Ingest Quality، Integrity/Provenance و Retention Reference Applicable داشته باشد.

P05-CON-364 — Event Set آینده باید Schema Registry/Compatibility و Verification P13 را طی کند؛ فهرست این Part Implementation یا Event Deployment نیست.

P05-DEN-139 — Event نمی‌تواند ApplicationCommand، Approval، AuthorizationDecision، Lease یا Risk Acceptance را ضمنی ایجاد کند.

P05-DEN-140 — Event-driven Consumer نباید بدون Fresh Intersection و Lease Action اثرگذار را اجرا کند.

P05-DEN-141 — Missing Event نباید No Effect یا No Revocation تلقی شود؛ Source Record و Reconciliation لازم است.

P05-DEN-142 — Event Replay نباید External/Costly/Destructive Effect یا Approval Consumption را تکرار کند مگر مسیر جدا، Typed و مجاز وجود داشته باشد.

P05-DEN-143 — Metric Label یا Log Message جای Authority Event/Evidence نیست.

P05-DEN-144 — `PROHIBITED_PATH_DETECTED` هیچ Approval-request Consumer یا Auto-remediation Effect-expanding Path ندارد.

P05-FAIL-086 — Event Envelope/Profile Schema Invalid نتیجه `AUTHORITY_EVENT_INVALID` و عدم مصرف برای Authority دارد.

P05-FAIL-087 — Critical Authority Event Loss/GAP باید `EVENT_EVIDENCE_GAP`، Fail-closed Consumer و Reconciliation ایجاد کند.

P05-FAIL-088 — Duplicate/Replay Approval Event نباید Duplicate Consumption یا Execution ایجاد کند.

P05-FAIL-089 — Revocation Event Lag/Conflict باید Approval/Lease Path را Block و Source Record را Re-resolve کند.

P05-FAIL-090 — Cross-tenant Event Leak باید Isolation، Evidence Preservation و Security/Privacy Incident Process را فعال کند.

P05-FAIL-091 — Event Projection Corruption نباید Source Authority را تغییر دهد؛ Projection Rebuild/Reconciliation لازم است.

## 24. Denial Rules، Failure Modes، Unknown Handling و Degraded Behavior

P05-REQ-026 — Unknown، Missing، Stale، Expired، Revoked، Unsupported، Unverified، Conflicted، Non-atomic یا Unbounded Authority Fact باید صریح ثبت شود و برای Effectful Work Fail Closed باشد؛ هیچ Degraded Mode مجاز نیست Authority یا Exposure را افزایش دهد.

P05-DEF-026 — `Degraded Authority Mode` فقط یک وضعیت از پیش طراحی‌شده، Policy-bound، Time-bound و Evidence-producing برای کاهش Exposure است؛ Degraded Mode مجوز دورزدن Gate یا ادامۀ Effectful Work با Facts نامعلوم نیست.

P05-CON-365 — Unknown States حداقل شامل موارد زیرند:

`NOT_FOUND | NOT_APPLICABLE_WITH_RATIONALE | UNRESOLVED | INDETERMINATE | STALE | EXPIRED | REVOKED | CONFLICTED | UNVERIFIED | UNSUPPORTED | UNBOUNDED | OUTCOME_UNKNOWN`

P05-CON-366 — `NOT_APPLICABLE` فقط با Scope، Rationale، Source Rule و Owner معتبر است؛ در غیر این صورت Missing باقی می‌ماند.

P05-CON-367 — Unknown نباید به Default Low، Zero Cost، Public Data، Non-production، Reversible، No Egress، One Target یا APR-0 تبدیل شود.

P05-CON-368 — Analysis ممکن است برای تکمیل Facts تحت Profile `FULL` انجام شود فقط اگر خود Analysis Effectful Trigger بالاتر یا ممنوع نداشته باشد؛ Execution تا Resolution `DENY` است.

P05-CON-369 — Degraded Matrix:

| Failure/Unknown | Minimum Behavior | ممنوع |
|---|---|---|
| Effect/Dependency/Target unresolved | `DENY`; close graph or redesign | infer low effect |
| Approval service/record unavailable | `DENY/WAIT` | cached/implicit approval |
| Permission/competence unresolved | `DENY` | infer from title/admin |
| AUT ceiling/manifest stale | `DENY` | select higher autonomy |
| Policy/source version conflicted | strictest temporary result + review | newer/longer wins |
| Risk service/register unavailable | `DENY` material work; deny-only containment if preapproved | assume within appetite |
| Cost estimate/ledger/reservation unavailable | block variable/material cost | assume zero/charge later |
| Data class/destination/residency unknown | block access/egress | assume internal/public |
| Environment identity/promotion state unknown | block effectful work | assume non-production |
| Approval revocation freshness unknown | block/revoke lease | use cache |
| Time/expiry validation unknown | deny current validity | extend validity |
| Report profile selector unavailable | `FULL` for analysis; `DENY` for execution | choose LITE/STANDARD |
| Evidence integrity/store unavailable | block high/material effect; preserve local bounded evidence if preapproved | proceed without chain |
| Receipt/provider outcome unknown | stop further effect and reconcile | retry blindly/declare success |
| E9 path detected | hard stop/isolate/preserve/`INC-0`/remove/review | approve, waive or externalize |

P05-CON-370 — Degraded Mode باید Entry Trigger، Allowed deny-only Operations، Effect Ceiling، Tenant/Environment Scope، TTL، Evidence، Owner، Exit Criteria و Post-event Review داشته باشد.

P05-CON-371 — Allowed Degraded Operations فقط می‌توانند Stop، Deny، Isolate، Revoke، Rate-limit، Quarantine، Block Egress یا Reduce Exposure باشند و باید خودشان از قبل Bound و Classify شده باشند.

P05-CON-372 — Restoration، Replay، Resumption، Failover to External Provider، Privilege Grant، Budget Increase یا Risk Acceptance Degraded Operation نیست و Lifecycle عادی می‌خواهد.

P05-CON-373 — Policy/Resolver Outage نباید Last-known Allow را تمدید کند؛ فقط Last-known Deny یا Exposure-reducing Constraint در Bound معتبر قابل‌حفظ است.

P05-CON-374 — Conflicting Results باید سخت‌گیرانه‌ترین Result را موقتاً اعمال کنند، Conflict را Preserve و Owner Review را Trigger نمایند؛ Temporary Result Approval نهایی نیست.

P05-CON-375 — Partial Classification باید `INDETERMINATE` باشد حتی اگر تمام Axisهای موجود permissive باشند.

P05-CON-376 — Unbounded Retry/Fan-out/Target/Cost/Duration/External Destination یا Destruction Range Hard Denial برای Execution است تا Bound واقعی ایجاد شود؛ Bound Document-only کافی نیست.

P05-CON-377 — Stale Source/Policy/Manifest باید Freshness Rule و Version Owner خود را رعایت کند؛ Wall-clock جدید به‌تنهایی Validity نمی‌سازد.

P05-CON-378 — Revoked/Expired Authority قابل Repair با Retry نیست؛ Request/Approval/Authorization/Lease تازه لازم است.

P05-CON-379 — Denial Record Failure نباید Denial را معکوس کند؛ Minimal Protected Denial Evidence باید در اولین فرصت امن Reconcile شود.

P05-CON-380 — E9 Detection Failure Suspected یا Incomplete Scan باید Path را Isolate و تا Exhaustive Review Block کند.

P05-CON-381 — Emergency Authority فقط Exposure Reduction است و خودکار Expire می‌شود؛ استفاده، Non-use، Failure و Restoration Attempt باید Review شوند.

P05-CON-382 — Human Override در صورت وجود فقط می‌تواند در Authority و Scope معتبر Constraint سخت‌گیرانه‌تر اعمال کند؛ Override برای Missing Classification یا `APR-X` وجود ندارد.

P05-CON-383 — External Provider Degradation نباید Provider جدید، Region جدید، Data Egress یا Cost Model جدید را Silent فعال کند.

P05-CON-384 — Security Incident Mode نمی‌تواند Evidence Delete، Monitoring Disable، Bulk Export یا Credential Expansion را به‌عنوان Recovery مجاز کند.

P05-CON-385 — Degraded Output باید دقیقاً State، Missing Fact، Consequence، Allowed deny-only Action، Owner، Review/Retry Condition و Evidence Reference را بیان کند.

P05-CON-386 — User-facing Error می‌تواند Redacted باشد اما Protected Internal Record باید Exact Failure Basis و Source را حفظ کند.

P05-CON-387 — Unknown Resolution باید New Evidence/Source/Record و Supersession Link داشته باشد؛ Edit Label به `KNOWN` کافی نیست.

P05-CON-388 — Failure Recovery خودش باید Effect/Approval/Permission/AUT/Profile Classification مستقل داشته باشد.

P05-CON-389 — Repeated Failure، Conflicting Cache، Bypass Attempt یا Unexplained Downgrade باید Defect/Incident Trend و Root-cause Review متناسب ایجاد کند.

P05-DEN-145 — Fail Open، Best-effort Allow، Soft Warning-only یا Continue-and-log برای Missing Authority ممنوع است.

P05-DEN-146 — Availability، SLA، Deadline، Customer Impact یا Executive Request نمی‌تواند Unknown Authority را Allow کند.

P05-DEN-147 — Break-glass، Admin Console، Root Credential، Manual SQL/API، Provider Support یا Offline Token جای Approval/Lease نیست.

P05-DEN-148 — Safe Mode نباید External Write، Privileged Grant، Production Change، Sensitive Egress، Material Spend، Destruction یا E9 داشته باشد مگر خود Action از مسیر عادی و غیرممنوع مجاز شده باشد؛ در آن صورت دیگر Bypass Degraded محسوب نمی‌شود.

P05-DEN-149 — Cached `ALLOW` پس از Outage، Revocation Unknown یا Policy Conflict معتبر نیست.

P05-DEN-150 — Failure Report نباید Missing Record را Synthetic، Backdated یا Model-generated پر کند.

P05-DEN-151 — Unknown Outcome نباید با Automatic Retry Effect را تکرار کند.

P05-DEN-152 — Containment Profile نمی‌تواند Restoration Approval را از پیش شامل شود.

P05-DEN-153 — `APR-X`، `E9` و `R5/PROHIBITED` هیچ Degraded Execution Route ندارند.

P05-DEN-154 — Degraded Mode Label بدون Approved Policy/Scope/TTL/Evidence هیچ معنای permissive ندارد.

P05-FAIL-092 — Authority Resolver Unavailable نتیجه `AUTHORITY_RESOLUTION_UNAVAILABLE — DENY` دارد.

P05-FAIL-093 — Approval Source Unreachable نتیجه `APPROVAL_UNVERIFIABLE — DENY` دارد.

P05-FAIL-094 — Permission/Competence Source Conflict نتیجه `PERMISSION_CONFLICTED — DENY` دارد.

P05-FAIL-095 — Autonomy Manifest Missing/Stale نتیجه `AUTONOMY_CEILING_UNRESOLVED — DENY` دارد.

P05-FAIL-096 — Risk State Missing/Stale نتیجه `RISK_STATUS_UNKNOWN — DENY_MATERIAL_EFFECT` دارد.

P05-FAIL-097 — Budget Reservation/Cost Bound Missing نتیجه `COST_ADMISSION_FAILED — DO_NOT_COMMIT_COST` دارد.

P05-FAIL-098 — Data/Environment Classification Missing نتیجه `BOUNDARY_CLASSIFICATION_UNKNOWN — BLOCK_ACCESS_OR_EFFECT` دارد.

P05-FAIL-099 — Evidence Integrity Failure نتیجه `EVIDENCE_UNTRUSTED — BLOCK_HIGH_IMPACT_AND_RECONCILE` دارد.

P05-FAIL-100 — Outcome Ambiguity نتیجه `OUTCOME_UNKNOWN — STOP_RETRY_AND_RECONCILE` دارد.

P05-FAIL-101 — Degraded Mode TTL Expiry نتیجه Automatic Stop/Block و Review دارد؛ Silent Extension ممنوع است.

P05-FAIL-102 — Conflicting Policy/Source/Cache Result نتیجه `AUTHORITY_CONFLICTED — MOST_RESTRICTIVE_TEMPORARY_RESULT` دارد.

P05-FAIL-103 — Suspected Classification Downgrade/Bypass نتیجه Path Isolation و Independent Review دارد.

P05-FAIL-104 — E9 Path یا Approval Attempt نتیجه `HARD_DENY → ISOLATE → PRESERVE EVIDENCE → INC-0 → REMOVE PATH → INDEPENDENT REVIEW` دارد.

## 25. Verification Requirements و Part-level Acceptance Criteria

P05-REQ-027 — Verification آینده برای Contract این Part باید حداقل شامل موارد زیر باشد:

1. Enum/Schema Conformance برای `E0..E9`، `APR-0..APR-4/APR-X`، `PERM-A..PERM-E` و `AUT-0..AUT-5`؛
2. Legacy `A0..A5 → AUT-0..AUT-5` Migration و Ambiguous `A*` Rejection؛
3. Maximum Actual/Direct/Indirect/Transitive/Aggregated Effect Classification؛
4. Dependency Graph Closure، Nested Tool/Provider/Callback/Retry/Recovery و Target-cardinality Tests؛
5. Client/Model/Plugin/UI Effect-downgrade و Label-manipulation Tests؛
6. Effect-to-APR Floor و Stricter Domain Escalation Tests؛
7. Approval Request/Presentation/Target Digest، Scope، Nonce، Validity، Expiry، Consumption، Replay و Revocation Tests؛
8. Informedness، Competence، Delegation، Separation-of-duties، Coercion و Self-approval Negative Tests؛
9. Permission Domain، Tenant/Purpose/Environment/Operation Scope و Conflict Tests؛
10. AUT Ceiling، AUT-4 Human Boundary، AUT-5 No-autonomous-path و Manifest Change Tests؛
11. Exhaustive Cross-axis Intersection Permutations و Missing-axis Fail-closed Tests؛
12. Risk `R0..R5` Projection، Unknown/Stale Risk، Above-appetite/Tolerance/Capacity و Acceptance Authority Tests؛
13. Data Class، Egress/Destination/Residency و Environment Promotion/Identity Tests؛
14. Cost Fixed/Bounded/Variable/Material/Unbounded، Reservation Race، Retry/Fan-out و Reconciliation Tests؛
15. Irreversibility، Rollback/Compensation/Recovery/Destruction و Reclassification Tests؛
16. `LITE/STANDARD/FULL/DENY` Trigger Matrix و Strictness-order Tests؛
17. Exact 8/18/34/12 Section Completeness و Title/Order Tests؛
18. Aggregate Profile، Split-work، Shared Trigger، Upward/Downward Reclassification و Downgrade Prevention Tests؛
19. Approval/Profile/Authorization/Lease/Receipt/Outcome Record-separation Tests؛
20. Boundary Revalidation، Cache Freshness، Atomic Snapshot و Revocation Propagation Tests؛
21. Event Envelope/Extension/Ordering/Duplicate/Replay/Sampling/Privacy Tests؛
22. Resolver/Policy/Risk/Cost/Data/Time/Evidence Outage و Degraded-mode Tests؛
23. Emergency Exposure-reduction-only و Restoration-separate Tests؛
24. Source/Version/Digest/Status Preservation و Owner-boundary Tests؛
25. Exhaustive Direct/Indirect/Generic/Human-mediated/Archived/Forked/Successor E9 Path Negative Review.

P05-CON-390 — P13 مالک Test Method، Oracle، Dataset، Threshold/Tolerance، Equivalence، Coverage و Independent Assurance است؛ P05 فقط Claims و Required Test Classes را تحویل می‌دهد.

P05-CON-391 — Verification باید Positive، Negative، Adversarial، Boundary، Concurrency، Replay، Degraded، Recovery و Historical-state Cases را پوشش دهد؛ Happy Path کافی نیست.

P05-CON-392 — Exhaustive Cross-axis Tests باید هر Permissive-axis Combination با یک Restrictive/Unknown Axis را Deny نشان دهند.

P05-CON-393 — Effect Tests باید Declared Effect را با Actual Dependency/Target/Provider Behavior مقایسه و Underclassification را آشکار کنند.

P05-CON-394 — Approval Tests باید Mutation پس از Preview، Canonicalization Conflict، Cross-scope Reuse، Backdating، Coercion، Self-approval و Multi-use Misuse را پوشش دهند.

P05-CON-395 — Permission Tests باید Multi-domain Actor، Delegation، Competence Expiry، Conflict of Interest، Tenant/Purpose Drift و Admin-role Confusion را پوشش دهند.

P05-CON-396 — Autonomy Tests باید نشان دهند AUT Ceiling هیچ Approval/Permission نمی‌سازد و `AUT-5` هر Autonomous Attempt را Deny می‌کند بدون آنکه Non-E9 Human Route را خودکار Global Prohibition بنامد.

P05-CON-397 — E9 Tests باید Schema، Route، Credential، Adapter، Queue، Tool، Workflow، Retry، Recovery، Generic Endpoint، Human Mediation و Externalization را پوشش دهند؛ یک نمونه Path کافی نیست.

P05-CON-398 — Profile Tests باید Highest Trigger، Missing Classification، Exact Sections، Reference Reuse، Aggregation، Split-work و Downgrade Justification را بررسی کنند.

P05-CON-399 — Cost/Risk Tests باید Budget Authorization و Risk Acceptance را مستقل و Race/Expiry/Revocation/Outage-aware نگه دارند.

P05-CON-400 — Verification Evidence، Independent Review، Acceptance Record، Source Approval، Runtime Qualification و Production Evidence رکوردهای جدا هستند.

P05-CON-401 — Test Fixtures نباید Production Effect، Real Sensitive Egress، Unbounded Cost، Destruction یا E9 Path را فعال کنند؛ Environment و Blast Radius باید کنترل‌شده باشد.

P05-CON-402 — Coverage Claim باید Denominator/Exclusion Contract P12 را مصرف کند؛ `100%` بدون Reconstructable Population معتبر نیست.

P05-CON-403 — Formal/Model-based Verification می‌تواند Intersection/State Invariant را پشتیبانی کند، اما Implementation/Environment/Operation Evidence را جایگزین نمی‌کند.

P05-CON-404 — Verification Version باید دقیقاً Taxonomy، Policy Snapshot، Schema، Manifest، Dataset/Fixture، Environment و Toolchain را Bind کند.

P05-CON-405 — Any Failed/Inconclusive/Unknown Test باید Failure Rule از پیش تعریف‌شده را اعمال کند؛ Inconclusive Pass نیست.

P05-CON-406 — Independent Reviewer باید Competence، Independence، Scope، Evidence Access، Dissent و Limitation را ثبت کند.

P05-CON-407 — Historical Source Absence قابل Test-away نیست؛ فقط Successor Fresh Approval می‌تواند Normative Status آینده ایجاد کند.

P05-CON-408 — Verification این Prompt Part انجام نشده است؛ Requirements بالا Design Contract هستند.

P05-CON-409 — هیچ Test Result فرضی، Example، Static Review یا Internal Generation Audit نباید `VERIFIED` یا `PRODUCTION_READY` Claim ایجاد کند.

P05-DEN-155 — این Part هیچ Test، Simulation، Model Check، Penetration Test، Red Team، Benchmark، Fault Injection یا Deployment Validation اجرا نکرده است.

P05-DEN-156 — Clause Completeness یا Lint Pass Scientific/Operational/Security/Legal/Financial Correctness را ثابت نمی‌کند.

P05-DEN-157 — Synthetic Approval/Permission/Lease/Receipt نباید با Record واقعی اشتباه شود.

P05-DEN-158 — Missing Test Coverage، Failed Oracle یا Unresolved Counterexample نباید با Reviewer Opinion بسته شود.

P05-DEN-159 — E9 Negative Review هیچ Test Execution Path برای Spacecraft Command ایجاد نمی‌کند؛ فقط Static/Formal/Controlled Evidence بدون Operational Route مجاز است.

P05-REQ-028 — Acceptance این Part برای Assembly فقط وقتی قابل‌پیشنهاد است که:

1. Header، Start Anchor، End Anchor، Footer و Part Pointerها کامل و یکتا باشند؛
2. `PART_ID/INDEX/COUNT/TITLE` دقیقاً با Canonical Map منطبق باشد؛
3. Semantic Owner ID/Version/Status/Digest بدون Drift حفظ شود؛
4. Supporting Source ID/Version/Digest/Status دقیق باشد؛
5. Global Invariant Capsule بدون تغییر معنایی حاضر باشد؛
6. Objective، Scope، Exclusion و Owner Boundary کامل باشند؛
7. `E0..E9`، Actual/Transitive/Aggregated Effect و Server-side Truth کامل باشند؛
8. `APR-0..APR-4/APR-X` و Exact Binding/Validity/Revocation کامل باشند؛
9. `PERM-A..PERM-E` و Domain/Competence/Separation کامل باشند؛
10. `AUT-0..AUT-5`، Migration `A0..A5`، Ambiguous `A*` Rejection و `AUT-5 ≠ APR-X` روشن باشد؛
11. Effect، Approval، Permission، Autonomy، AuthorizationDecision و ExecutionLease مستقل بمانند؛
12. Risk/Data/Environment/Cost/Irreversibility Intersection و Deny-first Precedence کامل باشد؛
13. Budget Authorization، Risk Acceptance، Security Authorization و Human Approval مستقل بمانند؛
14. `LITE/STANDARD/FULL/DENY` Trigger، Exact Sections، Escalation و Mapping کامل باشد؛
15. ۳۴ عنوان `FULL` دقیق و به‌ترتیب Source حفظ شده باشد؛
16. Aggregation/Reclassification و Profile-downgrade Prevention کامل باشد؛
17. P01–P04 Reference شده و مالکیت آن‌ها بازتعریف نشده باشد؛
18. Architecture/Lifecycle/Record/Event/Failure/Unknown/Degraded Contract کامل باشد؛
19. Verification، Traceability، Orphan Detection و Acceptance قابل‌ممیزی باشد؛
20. Decision Projectionها `PROPOSED` و Semantic Owner `NOT_APPROVED/NOT_FROZEN` باقی بمانند؛
21. Historical Limitations و Open Issueها پنهان نشوند؛
22. هیچ Implementation، Execution، Spend، Test، Release، Deployment، Production یا Freeze ادعا یا مجاز نشود؛
23. E9/APR-X هیچ Waiver/Exit نداشته باشد؛
24. تمام Clause IDها یکتا و Fenceها بسته باشند؛
25. Handoff فقط P06 را به‌عنوان Part بعدی معرفی کند و P06 را آغاز نکند.

P05-PROC-003 — Part-level Internal Audit باید حداقل Source Binding، Clause ID Uniqueness، Anchor Uniqueness، Fence Closure، Required-section Coverage، Status Preservation، Owner-boundary Scan، Taxonomy Completeness، Profile-section Counts، Decision/Open-issue Preservation، Prohibited-path Negative Scan و Truncation Scan را اجرا کند.

P05-FAIL-105 — Missing Required Section، Duplicate Clause ID، Unclosed Fence، Truncation، Status Drift، Source/Owner Conflict، Taxonomy Gap، Profile Downgrade، Orphan Requirement یا Prohibited Authority Expansion نتیجه `REWORK_REQUIRED / PART_NOT_ACCEPTED` دارد.

## 26. Traceability، Source Binding و Orphan Detection

P05-REQ-029 — هر Requirement مادی P05 باید Owner، Source Artifact، Version، Digest، Status، Source Section، Consumer، Enforcement/Evidence Need، Conflict Status و Implementation Status قابل‌حل داشته باشد؛ Requirement بدون این Binding Orphan است.

P05-CON-410 — Machine-readable Required Trace Record و Semantic-compression Contract باید یک Schema Canonical واحد و Superset بدون تعارض از Assembly Contract §13.2، Gap 02 §5 و فیلدهای مادی Inline ثبت‌شده را حفظ کند. هر Record برای هر Clause مادی باید تمام فیلدهای زیر را، حتی در حالت `NOT_FOUND` یا `NOT_APPLICABLE` همراه با `limitations` و `open_issue_references`، به‌صورت جداگانه حمل کند:

~~~yaml
trace_schema_id: CSIP-EO-FMSP-TRACE-RECORD
trace_schema_version: 1
prompt_clause_id:
requirement_or_decision_id:
statement:
normative_keyword:
owner_part_id: CSIP-EO-FMSP-P05
semantic_owner_artifact_id: CSIP-EO-RS-STAGE-19
semantic_owner_version: 0.1.0-reconstituted-draft
semantic_owner_sha256: 30525213394593910a4bb0406ba3eb2ee784ddae05170933cea1a033654d8731
semantic_owner_status: RECONSTITUTED_DRAFT — REVIEW_READY — NOT_APPROVED — NOT_FROZEN
source_artifact_id:
source_version:
source_section:
source_sha256:
source_status:
supporting_source_bindings:
  - source_artifact_id:
    source_version:
    source_section:
    source_sha256:
    source_status:
upstream_clause_references: []
consumer_parts: []
mapped_stage: 19
mapped_control:
requirement_owner_role:
enforcement_reference:
evidence_reference:
verification_owner: P13
acceptance_test_reference:
conflict_status:
precedence:
compression_operation: DIRECT|PARAPHRASED_LOSSLESS|REFERENCED|DEDUPLICATED
reconstitution_operation:
implementation_status:
parent_requirement_or_decision_ids: []
derived_requirement_or_decision_ids: []
limitations: []
open_issue_references: []
~~~

Canonical Field و No-dual-schema Rules:

1. `prompt_clause_id` هویت Clause ماشین‌خوان `P05-*` را ثبت می‌کند؛ `requirement_or_decision_id` هویت Requirement/Decision مبدأ یا متناظر را ثبت می‌کند. این دو فیلد نباید Merge، Alias، Copy یا از یکدیگر استنتاج شوند؛ نبود مورد متناظر باید با `NOT_APPLICABLE` و دلیل قابل‌ممیزی ثبت شود.
2. `owner_part_id` مالک Part را ثبت می‌کند؛ چهار فیلد `semantic_owner_artifact_id/version/sha256/status` هویت و Status مالک معنایی را ثبت می‌کنند؛ و پنج فیلد `source_artifact_id/version/section/sha256/status` Source Binding اصلی Record را ثبت می‌کنند. هیچ‌یک جایگزین دیگری نیست.
3. `supporting_source_bindings` یک آرایۀ مرتب از Bindingهای ساخت‌یافته و Digest-bound است و نباید به فهرست مبهم نام‌ها یا Filenameها تقلیل یابد. `upstream_clause_references` نیز مستقل از Source Binding و Consumer Mapping باقی می‌ماند.
4. نام‌های زیر فقط Source/Legacy Input Label هستند و پیش از Serialization باید به Canonical Field تعیین‌شده Normalize شوند؛ هیچ‌کدام نباید به‌عنوان فیلد دوم یا Schema رقیب در Record نهایی باقی بمانند:

| Source/Legacy Input Label | Canonical Field / Normalization |
|---|---|
| `p05_clause_id` | `prompt_clause_id` |
| `requirement_id` | `requirement_or_decision_id` |
| `semantic_owner_part` | `owner_part_id` |
| `semantic_owner_digest` | `semantic_owner_sha256` |
| `source_document` | `source_artifact_id` |
| `source_digest` | `source_sha256` |
| `supporting_sources` | `supporting_source_bindings` |
| `owner_role` یا `owner_role_or_future_owner` | `requirement_owner_role` |
| `enforcement_point` یا `enforcement_point_or_future_boundary` | `enforcement_reference` |
| `evidence_type` | `evidence_reference` |
| `acceptance_test` | `acceptance_test_reference` |
| `evidence_or_acceptance_reference` | به `evidence_reference` و `acceptance_test_reference` تفکیک شود؛ اگر تفکیک Source-bound ممکن نیست، `limitations/open_issue_references` ثبت و حدس ممنوع است |
| `compression_or_reconstitution_operation` | به دو فیلد مستقل `compression_operation` و `reconstitution_operation` تفکیک شود |
| `parent_requirements` | `parent_requirement_or_decision_ids` |
| `derived_requirements` | `derived_requirement_or_decision_ids` |
| `open_issue_reference` | `open_issue_references` |

Semantic-compression Rules:

1. `compression_operation` دقیقاً یکی از `DIRECT`، `PARAPHRASED_LOSSLESS`، `REFERENCED` یا `DEDUPLICATED` است و برای Record مادی نباید خالی بماند.
2. `DIRECT` فقط وقتی مجاز است که Statement مادی مستقیماً با Source Binding دقیق حمل شده باشد.
3. `PARAPHRASED_LOSSLESS` فقط وقتی مجاز است که Normative Force، `MUST/MUST NOT`، Status، Scope، Exception، Failure Semantics، Scientific/Uncertainty Caveat و Anti-claim بدون کاهش حفظ شده باشند.
4. `REFERENCED` فقط با Reference دقیق و قابل‌حل در `upstream_clause_references` و Source Binding کامل مجاز است؛ Reference مبهم یا Filename-only کافی نیست.
5. `DEDUPLICATED` فقط وقتی مجاز است که تکرار حذف‌شده به Clause Canonical باقی‌مانده و Source دقیق آن قابل بازسازی باشد؛ حذف Requirement یا Open Issue به‌عنوان Deduplication ممنوع است.
6. `reconstitution_operation` مستقل از Compression است و باید `NONE` یا شرح دقیق و Source-bound عملیات Reconstitution را ثبت کند؛ این فیلد نباید Historical Byte Recovery، Byte-level Equality یا Digest برای Payload Inline غیرقابل‌دسترسی را القا کند. در آن حالت `INLINE_PAYLOAD_BYTES_NOT_ADDRESSABLE` باید در `limitations` و در صورت نیاز `open_issue_references` ثبت شود.
7. Enforcement، Evidence، Verification Owner و Acceptance Test چهار Concern مستقل‌اند و نباید در یک فیلد مبهم ادغام شوند.
8. Field گمشده، Alias حل‌نشده، `compression_operation` نامعتبر، Reconstitution بدون Source Binding یا ناتوانی در اثبات Losslessness باید در `conflict_status` و `limitations/open_issue_references` آشکار شود و Required Trace Record و Required-section Coverage را Fail کند.

P05-CON-411 — Exact Source Identity Registry این Part:

| نقش | Artifact ID / Version | SHA-256 | Status حفظ‌شده |
|---|---|---|---|
| Semantic Owner | `CSIP-EO-RS-STAGE-19 / 0.1.0-reconstituted-draft` | `30525213394593910a4bb0406ba3eb2ee784ddae05170933cea1a033654d8731` | `RECONSTITUTED_DRAFT — REVIEW_READY — NOT_APPROVED — NOT_FROZEN` |
| Harmonization Overlay | `CSIP-EO-AUDIT-GAP-02 / 0.1.0-candidate` | `fa400334a69702bf56e8588210449590573bccd3120d7c2cebd6ba9cc8fc161f` | `CANDIDATE — REVIEW_READY — NON_NORMATIVE_UNTIL_DIGEST_BOUND_APPROVAL` |
| Enterprise Mandate | `ENTERPRISE-TRUST-RISK-COST-EVIDENCE-REPRODUCIBILITY-MANDATE / verified-input-2026-07-28` | `1b5e7884a343589312d62259f181bd48f1a12b51e2613685c0d58c747a08dab4` | `PRESENT_VERIFIED_BYTES / SUPPLEMENTAL_CROSS_CUTTING_INPUT` |
| Assembly Contract | `CSIP-EO-PROMPT-ARCH-18P-C1 / 0.1.0-design-candidate` | `a4c80b938fccaab5d3d85c780351a41ee3444b4c6712920af45b493afbacb09b` | `DESIGN_CANDIDATE — REVIEW_READY — NOT_APPROVED — NOT_FROZEN` |
| Candidate Manifest | `CSIP-EO-GAP-RESOLUTION-MANIFEST-C1 / 0.1.0-candidate` | `349b590df9fad00c2e0ec317f4bd0b7ad747a5e22a1fead0f66f28c98e955216` | `REVIEW_READY_NOT_APPROVED` |

P05-CON-412 — Upstream Part Binding Registry:

| Part | Semantic Owner Digest | Exact Clause Binding | مصرف P05 |
|---|---|---|---|
| `CSIP-EO-FMSP-P01` | `a33bf602b5a5e5c8518b709b5dde7ab6b96617cc76ac86c66d2c795271422c50` | `P01-CON-002`؛ `P01-INV-015..018`؛ `P01-DEF-004..009`؛ `P01-CON-032..035`؛ `P01-DEN-017` | Scope، Invariant، Entity/Event/Time، Record Separation، Authority-axis Delegation |
| `CSIP-EO-FMSP-P02` | `b0ffc9a74b3bac68ee6f74176f732fdf3ea60277697546c9b009b54e5ab4cb6b` | `P02-CON-010..011`؛ `P02-DEN-010`؛ `P02-REQ-006`؛ `P02-CON-032..033`؛ `P02-CON-043` | Stage/Gate/Decision/Acceptance/Handoff Protocol |
| `CSIP-EO-FMSP-P03` | `3f16593a323f3024550a4515a1c48118872e53bfdbb60d3d7ae47385ab4ff249` | `P03-PROC-002`؛ `P03-CON-031..034`؛ `P03-CON-084` | Query/Command/Approval/Authorization/Lease/Receipt/Outcome Separation |
| `CSIP-EO-FMSP-P04` | `98c58b2fc8fe56e0d84f39c901421642d8b8b525c18979b9a1b2aaee25c5d75b` | `P04-CON-063..064`؛ `P04-CON-188..196`؛ `P04-CON-216..218`؛ `P04-CON-237` | Workflow/Human Checkpoint/State/Recovery/Profile Routing Context |

P05-CON-413 — Clause-range Source Mapping:

| P05 Clause Range | Primary Source Binding | P05 Ownership Operation |
|---|---|---|
| `P05-REQ-001..003` و Reception Denials | Assembly Contract §§8، 10؛ P01–P04 Reception Contracts | faithful assembly envelope |
| `P05-REQ-004..006` | Assembly Contract §6.5؛ RS19 §§0–1 | objective/scope/boundary elaboration |
| `P05-REQ-007..008` | RS19 §2؛ Gap 02 `CGR-REQ-011` | owned Effect taxonomy/truth contract |
| `P05-REQ-009..010` | RS19 §§3، 8، 9؛ `CGR-REQ-012` | owned Approval taxonomy/binding |
| `P05-REQ-011` | RS19 §4؛ `CGR-REQ-013` | owned Permission taxonomy |
| `P05-REQ-012` | RS19 §§5، 6، 9؛ Mandate Authority Levels؛ `CGR-REQ-014` | owned AUT taxonomy/crosswalk |
| `P05-REQ-013..014` | RS19 §§1، 7؛ `CGR-REQ-015` | owned fail-closed intersection |
| `P05-REQ-015` | RS19 §§1، 7، 10؛ Mandate §§7–8؛ `CGR-REQ-027` | owned admission boundary; external record authority preserved |
| `P05-REQ-016..021` | Gap 02 §6؛ Mandate Mandatory Output؛ `CGR-REQ-023` | owned report tailoring and denial routing |
| `P05-REQ-022` | P01–P04 Owner Contracts؛ Assembly Contract §§5–6 | cross-part binding, reference only outside P05 |
| `P05-REQ-023..026` | RS19 §§1، 7، 8، 10–11؛ P01–P04 integration | P05 architecture/lifecycle/event/failure implications |
| `P05-REQ-027..029` | Assembly Contract §§13.1–13.3؛ RS19 §11؛ Gap 02 §5 و §12 و `CGR-REQ-022`؛ P02/P13 acceptance contract | verifiable clauses، canonical trace schema و lossless semantic-compression contract؛ P13 method retained |

P05-CON-414 — `CGR-REQ-011` به `P05-REQ-007..008` و Effect-related `CON/DEN/FAIL`ها؛ `CGR-REQ-012` به `P05-REQ-009..010`؛ `CGR-REQ-013` به `P05-REQ-011`؛ `CGR-REQ-014` به `P05-REQ-012`؛ `CGR-REQ-015` به `P05-REQ-013..014`؛ `CGR-REQ-023` به `P05-REQ-016..021`؛ و `CGR-REQ-027` به `P05-REQ-015` Trace می‌شود.

P05-CON-415 — Supporting Source فقط وقتی Requirement را پشتیبانی می‌کند که Scope و Status آن حفظ و Semantic Owner P05 آشکار باشد؛ Overlay نمی‌تواند Successor Owner را Normative اعلام کند.

P05-CON-416 — Derived P05 Definitionهایی مانند `EffectClassificationRecord`، `AuthorityIntersectionRecord`، `CostExposureBand`، `IrreversibilityClass` و Exact Denial Record، Fresh Design در مالکیت واگذارشده P05 هستند و Statusشان همان `RECONSTITUTED_DRAFT — NOT_APPROVED — NOT_FROZEN` است.

P05-CON-417 — Risk Tier Projection از Mandate مصرف می‌شود اما Risk Methodology/Threshold/Authority نهایی P16-owned باقی می‌ماند؛ Data/Environment Vocabularyهای موقت Admission نیز Canonical Vocabulary Parts 10/11/14 را جایگزین نمی‌کنند.

P05-CON-418 — Trace Edge تولیدشده توسط AI یا Rule بدون Validation معتبر `CANDIDATE` است و نباید Orphan را Closed نشان دهد.

P05-CON-419 — Orphan Requirement انواع زیر را شامل می‌شود:

1. Missing Source/Owner/Digest/Status؛
2. Missing Consumer یا Enforcement Boundary برای Requirement مادی؛
3. Missing Verification/Evidence Path؛
4. Competing Owner بدون Conflict Record؛
5. Claim قوی‌تر از Source؛
6. Status بالاتر از Source؛
7. Downstream Requirement بدون Parent/Derivation؛
8. Test بدون Requirement/Risk/Threat Target؛
9. Decision بدون Rationale/Source/Authority؛
10. Open Issue بسته‌شده بدون Evidence/Disposition.

P05-CON-420 — Unsupported Claim Scan باید واژگان `APPROVED`، `FROZEN`، `IMPLEMENTED`، `VERIFIED`، `VALIDATED`، `QUALIFIED`، `RELEASED`، `DEPLOYED`، `PRODUCTION_READY` و `COMPLIANT` را در Context بررسی کند و فقط Status Source-bound را مجاز بداند.

P05-CON-421 — Owner-boundary Scan باید Definitionهای Event، Workflow State، API Record، Scientific Truth، AI Authority، Capability Qualification، Data Classification، Security Mechanism، Cost Ledger، Test Oracle، Environment Gate و Risk Constitution رقیب را پیدا کند.

P05-CON-422 — Taxonomy Coverage Scan باید هر Label `E0..E9`، `APR-0..APR-4/APR-X`، `PERM-A..PERM-E` و `AUT-0..AUT-5` را دقیقاً یک بار در Canonical Table و بدون Missing/Extra Class تأیید کند.

P05-CON-423 — Profile Coverage Scan باید Eligibility/Trigger و Exact Section Countهای `LITE=8`، `STANDARD=18`، `FULL=34` و `DENY=12` را تأیید کند.

P05-CON-424 — Clause ID Scan باید کل Pattern `P05-{INV|REQ|DEF|CON|PROC|DEN|FAIL|DEC|OI}-nnn` را بررسی و Duplicate را Blocking اعلام کند.

P05-CON-425 — Anchor/Fence Scan باید Start/End Anchor یکتا، Header/Footer کامل و تمام `~~~` Fenceها را زوج و بسته تأیید کند.

P05-CON-426 — Truncation Scan باید آخرین Handoff Clause، Reception Response، Footer Fields و End Anchor را موجود و پس از آن هیچ Payload اضافی نبیند.

P05-CON-427 — Status Preservation Scan باید Header، Source Registry، Decision Projection، Anti-claim و Footer را برای نبود Approval/Freeze/Implementation Drift کنترل کند.

P05-CON-428 — Source Digest Scan باید Semantic Owner و Supporting Source Digestها را با Manifest/Bytes قابل‌دسترس مقایسه کند؛ Mismatch برابر Conflict است.

P05-CON-429 — Required-section Coverage باید تمام ۲۰ مورد دستور صریح تولید P05 را به Section/Clause قابل‌حل Map کند؛ `PASS` فقط وقتی مجاز است که Required Trace Record شامل تمام Canonical Fieldهای P05-CON-410 باشد، تفکیک `prompt_clause_id` از `requirement_or_decision_id` برقرار بماند، Semantic-compression Contract برای چهار عملیات مجاز کامل باشد، Reconstitution مستقل و Source-bound ثبت شود و هیچ Alias مبهم یا Schema رقیب باقی نماند.

P05-CON-430 — Historical Limitation/Open Issue Scan باید Missing Historical Bytes، Fresh Approval Requirement، Stage 20 Domain Review، Unknown Organizational Facts و No Implementation Evidence را حفظ کند.

P05-CON-431 — Handoff Scan باید فقط `P06` را `NEXT_EXPECTED_PART` معرفی کند و هیچ Clause، Taxonomy، Scientific Definition یا Content متعلق به P06 تولید نکند.

P05-CON-432 — Trace Registry کامل Machine-readable برای کل ۱۸ Part هنوز Future Work است؛ Human Projection این Part Completion آن را ادعا نمی‌کند.

P05-DEN-160 — Requirement بدون Source/Owner نباید با «best practice» یا Model Knowledge Normative شود.

P05-DEN-161 — Filename، Similarity، Memory، Retrieval Rank یا Newer Timestamp Source Identity نیست.

P05-DEN-162 — Trace Matrix ناقص نباید با Coverage Percentage بدون Denominator Complete گزارش شود.

P05-DEN-163 — Orphan نباید با حذف Requirement یا تغییر آن به Informative بدون Owner Decision پنهان شود.

P05-DEN-164 — Supporting Source Status نباید به Semantic Owner Status منتقل شود.

P05-DEN-165 — Machine Scan Pass به‌تنهایی Human/Domain Review و Fresh Approval نیست.

P05-DEN-166 — P05 نباید Source Mapping برای P06 Content بسازد؛ فقط Handoff Pointer مجاز است.

P05-FAIL-106 — Missing/Invalid Trace Join نتیجه `TRACE_SOURCE_DIGEST_UNRESOLVED` و Block برای Normative Promotion دارد.

P05-FAIL-107 — Orphan Requirement نتیجه `ORPHAN_REQUIREMENT — REWORK_REQUIRED` دارد.

P05-FAIL-108 — Unsupported Claim یا Status Drift نتیجه `UNSUPPORTED_CLAIM — PART_NOT_ACCEPTED` دارد.

P05-FAIL-109 — Profile Section-count/Title Drift نتیجه `REPORT_PROFILE_CONFORMANCE_FAILED` دارد.

P05-FAIL-110 — End Pointer یا Handoff Content Drift نتیجه `PART_BOUNDARY_VIOLATION — REWORK_REQUIRED` دارد.

## 27. Decision Projection، Historical Limitations و Open Issueها

Decisionهای زیر Projection مستقیم `CSIP-EO-RS-STAGE-19` هستند؛ Historical Decision بازیابی‌شده نیستند و همگی `PROPOSED` باقی می‌مانند:

P05-DEC-001 — `RS19-DEC-001`: Canonical Effect Axis؛ `E0..E9` برابر Actual/Transitive Effect Truth — Status: `PROPOSED`.

P05-DEC-002 — `RS19-DEC-002`: Approval Axis؛ `APR-0..APR-4/APR-X` مستقل باقی می‌ماند — Status: `PROPOSED`.

P05-DEC-003 — `RS19-DEC-003`: Permission Axis؛ `PERM-A..PERM-E` Actor Domain را تعریف می‌کند — Status: `PROPOSED`.

P05-DEC-004 — `RS19-DEC-004`: Autonomy Rename؛ Mandate `A0..A5` به `AUT-0..AUT-5` تبدیل می‌شود — Status: `PROPOSED`.

P05-DEC-005 — `RS19-DEC-005`: Missing Mapping؛ Fail Closed و بدون Permission استنتاجی — Status: `PROPOSED`.

P05-DEC-006 — `RS19-DEC-006`: Effect Truth؛ Server Maximum Transitive Effect را محاسبه می‌کند — Status: `PROPOSED`.

P05-DEC-007 — `RS19-DEC-007`: Approval Binding؛ Exact Request/Target/Effect/Digest/Expiry — Status: `PROPOSED`.

P05-DEC-008 — `RS19-DEC-008`: Emergency؛ فقط Exposure Reduction و Restoration جدا — Status: `PROPOSED`.

P05-DEC-009 — `RS19-DEC-009`: Autonomous Prohibition؛ `AUT-5` از Global `APR-X` متمایز است — Status: `PROPOSED`.

P05-DEC-010 — `RS19-DEC-010`: Command Boundary؛ `E9` هیچ Approval یا Exit در CSIP-EO ندارد — Status: `PROPOSED`.

Decisionهای زیر Projection مستقیم Harmonization Overlay هستند و Status آن‌ها نیز فقط `PROPOSED` است:

P05-DEC-011 — `CGR-DEC-020`: محورهای Stage 19 Successor Canonical و مستقل‌اند — Status: `PROPOSED`.

P05-DEC-012 — `CGR-DEC-021`: Mandate `A0..A5` به `AUT-0..AUT-5` تغییر نام می‌یابد — Status: `PROPOSED`.

P05-DEC-013 — `CGR-DEC-024`: Precedence Source/Domain-aware و Fail-closed است — Status: `PROPOSED`.

P05-DEC-014 — `CGR-DEC-026`: Mandatory Output از Tailoring `LITE/STANDARD/FULL` و Prohibited/Deny Route استفاده می‌کند — Status: `PROPOSED`.

P05-CON-433 — وجود `P05-DEC-*`، `RS19-DEC-*` یا `CGR-DEC-*` در این Part Approval، Historical Recovery، Normative Activation، Implementation Decision یا Freeze ایجاد نمی‌کند.

### 27.1 محدودیت‌های تاریخی اجباری

P05-CON-434 — Bytes، Title قطعی، Version، Clauseها، Decision Register و Approval Provenance تاریخی `CSIP-EO-STAGE-19` بازیابی نشده‌اند.

P05-CON-435 — `CSIP-EO-RS-STAGE-19` Successor Candidate تازه است؛ Digest حاضر Fixity Bytes این Candidate را نشان می‌دهد، نه Historical Equivalence یا Approval.

P05-CON-436 — Downstream Attestation فقط مالکیت تاریخی کلی `E0..E9` و `APR-0..APR-X` را نشان می‌داد؛ تعریف‌های دقیق Historical Source `NOT_FOUND` باقی می‌مانند.

P05-CON-437 — Taxonomyهای تازه، Crosswalk و Report Tailoring Design-resolved اما Pending Fresh Review/Approval هستند و Normative Runtime نیستند.

P05-CON-438 — هیچ Implementation، Service، Policy Engine، Approval Broker، Registry، Event Schema Deployment، Test Evidence، Operational Owner یا Production Qualification برای این Part وجود ندارد.

P05-CON-439 — Ownerهای واقعی سازمانی، Approver Matrix، Competence Criteria، Delegation، Region/Provider، Budget/Currency/Ceiling، Risk Threshold/Appetite/Tolerance/Capacity، Data-class Mapping، Environment Promotion State، TTL/SLO/RPO/RTO و Escalation Route `NOT_FOUND/UNKNOWN` هستند تا Source Owner مربوط Evidence ارائه کند.

P05-CON-440 — `CSIP-EO-RS-STAGE-20` همچنان `DOMAIN_REVIEW_REQUIRED` است؛ P05 هیچ Scientific Review یا Approval برای آن انجام نمی‌دهد.

### 27.2 Open Issueهای اجباری

- `P05-OI-001` — Historical Bytes و Approval Provenance `CSIP-EO-STAGE-19` مفقود است و نباید Recovered اعلام شود.
- `P05-OI-002` — Exact Digest Successor باید مستقل بررسی و Fresh Digest-bound Approval دریافت کند تا بتواند Successor Manifest Normative آینده را به‌روزرسانی کند؛ این کار انجام نشده است.
- `P05-OI-003` — Canonicalization Profile و Cross-implementation Digest Semantics برای Approval Request/Presentation/Target هنوز انتخاب و Qualified نشده‌اند.
- `P05-OI-004` — Capability/Dependency Graph Registry و Complete Effect Mapping برای تمام Capabilityها هنوز پیاده‌سازی یا Validate نشده است.
- `P05-OI-005` — Canonical Organizational Permission/Competence/Delegation Matrix و Real Approver Identities `NOT_FOUND` هستند.
- `P05-OI-006` — Canonical Data Classification/Residency/Retention Mapping باید توسط P10/P11 ارائه شود و هنوز در این Part موجود نیست.
- `P05-OI-007` — Exact Environment Classes، Promotion/Release Gates و Production Identity باید توسط P14/P15 ارائه شود و هنوز موجود نیست.
- `P05-OI-008` — Risk Methodology، Appetite، Tolerance، Capacity، Limits، Owner و Acceptance Matrix باید توسط P16 Source-bound شود و هنوز موجود نیست.
- `P05-OI-009` — Cost Provider Rates، Currency، Budget Hierarchy، Materiality Threshold، Reservation/Settlement Implementation و Invoice Reconciliation باید توسط P12/P16 Source-bound شود و هنوز موجود نیست.
- `P05-OI-010` — Verification Oracle، Dataset/Fixtures، Coverage Denominator، Formal Model و Independent Assurance Plan باید توسط P13 تعریف و اجرا شود؛ انجام نشده است.
- `P05-OI-011` — Full Machine-readable Trace Graph برای تمام P05 Clauseها و تمام Consumer Parts هنوز Populate/Validate نشده است.
- `P05-OI-012` — Event Schema Extensionهای P05 هنوز در Schema Registry Version/Approve/Implement/Verify نشده‌اند.
- `P05-OI-013` — Degraded-mode Profiles، TTLها، Containment Ownerها و Recovery/Restoration Gates واقعی `NOT_FOUND` هستند.
- `P05-OI-014` — `CSIP-EO-RS-STAGE-20` نیازمند Review مستقل Astrodynamics/Scientific و Fresh Approval است؛ P05 این Gap را نمی‌بندد.
- `P05-OI-015` — Stage 32 همچنان `PROPOSED` است و Project Specification Freeze اجرا نشده است.

P05-CON-441 — هیچ Part، Summary، Review، Model، Assembly Acceptance یا File-completeness Check حق ندارد Open Issueهای بالا را بدون Evidence، Owner Decision، Source Status و Immutable Disposition ببندد.

P05-CON-442 — Open Issue Closure باید Closure Record تازه، Exact Evidence/Source/Digest، Competent Owner، Decision Status، Impacted Clause/Consumer و Residual Limitation داشته باشد.

P05-DEN-167 — Historical Gap نباید با Successor Similarity، Downstream Attestation یا Model Reconstruction بسته شود.

P05-DEN-168 — `PROPOSED` Decision نباید در Summary، Matrix، Handoff یا Consumer به `APPROVED` تبدیل شود.

P05-DEN-169 — Open Issue نباید به دلیل نبود زمان، Token، Reviewer یا Implementation Detail حذف یا `NOT_APPLICABLE` شود.

P05-FAIL-111 — Historical-recovery Claim یا Decision Status Drift نتیجه `HISTORICAL_STATUS_VIOLATION — REWORK_REQUIRED` دارد.

P05-FAIL-112 — Silent Open-issue Closure نتیجه `OPEN_ISSUE_DISPOSITION_INVALID` دارد.

## 28. Anti-claimها و تفسیرهای ممنوع

این Part، تدوین، کنترل داخلی، دریافت، Review یا پذیرش آن برای Assembly هیچ‌یک از ادعاها یا مجوزهای زیر را ایجاد نمی‌کند:

- بازیابی Historical Stage 19؛
- تصویب، Ratification، Normative Activation یا Freeze منبع `CSIP-EO-RS-STAGE-19`؛
- Approval تصمیم‌های `RS19-DEC-001..010` یا `CGR-DEC-020/021/024/026`؛
- Approved بودن Definitionهای تازه P05 مانند Record Schema، Cost Band، Irreversibility Class یا Denial Record؛
- انتخاب یا پیاده‌سازی Policy Engine، Approval Service، Authorization Engine، Registry، Database، Event Broker، Workflow Engine، Tool، Provider یا Cloud؛
- ایجاد Identity، Permission، Approval، AuthorizationDecision، ExecutionLease، Budget Authorization، Risk Acceptance یا Credential واقعی؛
- اجرای Query، ApplicationCommand، Workflow، Tool Call، Approval Flow، Effect، Retry، Compensation، Recovery یا Reconciliation واقعی؛
- Read/Write/Export/Delete/Egress/External Connection یا Spend؛
- اجرای Test، Benchmark، Simulation، Fault Injection، Migration، Build، Release، Deployment، Pilot، Production یا Operation؛
- اثبات Scientific Validity، Security، Privacy، Legal Compliance، Cost Accuracy، Risk Acceptability، Reliability یا Human Factors؛
- تأیید `CSIP-EO-RS-STAGE-20` یا رفع `DOMAIN_REVIEW_REQUIRED`؛
- تصویب Stage 32 یا اجرای Project Specification Freeze؛
- ایجاد مستقیم یا غیرمستقیم Spacecraft Command، Telecommand، Uplink، Flight Control یا Autonomous Maneuver Execution.

P05-DEN-170 — واژۀ `Canonical` در این Part هویت طراحی پیشنهادی Source-bound را نشان می‌دهد و به معنی Approved، Implemented، Verified یا Frozen نیست.

P05-DEN-171 — واژۀ `قطعی طراحی` یعنی Definition کامل در Scope مالکیت P05؛ به معنی Normative Approval، Runtime Activation یا Production Truth نیست.

P05-DEN-172 — `Server-computed` Requirement معماری است؛ Server یا Implementation واقعی ایجاد یا Verify نشده است.

P05-DEN-173 — `ALLOW`، `GO`، `PASS` یا `COMPLETE` در Report/Classification فقط Status همان Record در Scope تعریف‌شده است و Execution Authority نیست.

P05-DEN-174 — `APR-0` به معنی Public، Anonymous، Unlogged، Uncontrolled یا No-policy نیست.

P05-DEN-175 — `PERM-E` یا Governing Authority نمی‌تواند Law، Scientific Evidence، Entrenched Prohibition یا `APR-X` را Override کند.

P05-DEN-176 — `AUT-4` Approval را خودکار صادر نمی‌کند و `AUT-5` Human Route را برای E9 ایجاد نمی‌کند.

P05-DEN-177 — `FULL` Complete به معنی GO، Approved، Verified، Qualified، Deployable یا Production Ready نیست.

P05-DEN-178 — `DENY` برای E9 به Approval Request، Exception Request، External Handoff یا Human-only Route تبدیل نمی‌شود.

P05-DEN-179 — Digest/Signature Fixity را پشتیبانی می‌کند و Correctness/Competence/Informedness/Validity/Approval را به‌تنهایی ثابت نمی‌کند.

P05-DEN-180 — Complete Text یا Internal Audit Pass مجوز آغاز P06، Implementation یا هیچ Action دیگر نیست.

P05-DEN-181 — هیچ Clause این Part Legal Advice، Regulatory Certification، Scientific Qualification یا Safety Guarantee نیست.

P05-DEN-182 — واژگان `Risk Accepted`، `Budget Available`، `Human Approved`، `Admin`، `Safe`، `Dry Run` یا `Reversible` بدون Exact Record/Scope/Evidence اثر permissive ندارند.

## 29. تحویل کنترل‌شده به Part 06

P05-CON-443 — P06 باید Scientific Computation، Numerical Truth، Time/Frame/Unit/Covariance، Uncertainty، Validity Domain، Independent Verification و Scientific Promotion را در مالکیت خود تعریف کند و هر Scientific Request/Result/Promotion را به Effect/Approval/Permission/Autonomy/Cost-Risk/Profile Contract همین P05 Bind نماید.

P05-CON-444 — P05 هیچ Algorithm، Force Model، Numerical Threshold، Covariance Rule، Conjunction/Collision-risk Formula، Scientific Confidence، Engine Equivalence یا Verification Oracle متعلق به P06 را تعریف یا پیش‌تصویب نمی‌کند.

P05-CON-445 — P06 باید `Physics Before AI`، `Unknown ≠ Pass`، `Scientific Completion ≠ Scientific Validity` و `Independent Verification` را حفظ کند و Authority Taxonomy P05 را بازنویسی نکند.

P05-CON-446 — Scientific Evidence می‌تواند Approval Floor، Risk، Profile یا Authorization را سخت‌گیرانه‌تر کند؛ Governance/Approval نمی‌تواند Scientific Truth یا Uncertainty را با رأی تغییر دهد.

P05-CON-447 — هر Scientific Tool/Engine/Workflow/Promotion Future باید Actual/Transitive Effect، Target/Data/Environment/Cost، Permission Domain، AUT Ceiling، APR Floor، Exact Approval، AuthorizationDecision و Lease را مستقل Resolve کند.

P05-CON-448 — `CSIP-EO-RS-STAGE-20` طبق Global Invariant Capsule در وضعیت `DOMAIN_REVIEW_REQUIRED` باقی می‌ماند؛ Handoff حاضر Review، Approval یا Activation آن نیست.

P05-CON-449 — Part بعدی مورد انتظار فقط به‌صورت Pointer:

- Part ID: `CSIP-EO-FMSP-P06`
- Part Index: `06 of 18`
- Title: `Scientific Truth, Numerical Computation and Independent Verification | حقیقت علمی، محاسبۀ عددی و Verification مستقل`
- Semantic Owner: `CSIP-EO-RS-STAGE-20`
- Receive Mode: `CONTEXT_ONLY`
- Action Authority during reception: `NONE`
- Mandatory Limitation: `DOMAIN_REVIEW_REQUIRED — NOT_APPROVED — NOT_FROZEN`

P05-REQ-030 — Part 06 باید در پیام جداگانه و فقط پس از دریافت و بررسی این Part و دستور صریح کاربر ارسال شود. سکوت، تکمیل P05، آگاهی از عنوان/Owner/Digest یا وجود فایل Candidate مجوز آغاز یا تولید P06 نیست.

P05-REQ-031 — پس از دریافت سالم این قسمت، تنها پاسخ مجاز متن ثابت زیر است و هیچ عبارت دیگری نباید قبل یا بعد از آن قرار گیرد:

~~~text
قسمت ۰۵ از ۱۸ ابرپرامپت نهایی CSIP-EO با موفقیت دریافت و ثبت شد.
هیچ تحلیل، طراحی جدید، پیاده‌سازی یا اقدام اجرایی آغاز نمی‌شود.
منتظر قسمت ۰۶ هستم.
~~~

RECEIVER_MUST_WAIT_FOR_NEXT_PART: TRUE
PART_DECLARED_COMPLETE: TRUE
NEXT_EXPECTED_PART: P06
RECEPTION_ACTION: ACK_ONLY
<<<CSIP-EO-FMSP-18P|0.9.0-draft|P05|END>>>
