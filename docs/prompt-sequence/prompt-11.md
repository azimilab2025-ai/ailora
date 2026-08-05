<<<CSIP-EO-FMSP-18P|0.9.0-draft|P11|START>>>
CSIP_EO_PROMPT_PACKAGE_ID: CSIP-EO-FINAL-MASTER-SUPERPROMPT-18P
CSIP_EO_PROMPT_PACKAGE_VERSION: 0.9.0-draft
PART_ID: CSIP-EO-FMSP-P11
PART_INDEX: 11
PART_COUNT: 18
PART_TITLE: Security, Privacy, Threat Model and Trust Boundaries | امنیت، حریم خصوصی، مدل تهدید و مرزهای اعتماد
SEMANTIC_OWNER_ARTIFACT_ID: CSIP-EO-STAGE-25
SEMANTIC_OWNER_VERSION: 1.0.0-approved
SEMANTIC_OWNER_STATUS: APPROVED AND CLOSED
CANONICAL_MAP_SOURCE_STATUS: APPROVED
SEMANTIC_OWNER_SHA256: 39975398b6b08bb98875784e7e96a48af8a19f9a51955d9d7d67da7d98da04a3
SEMANTIC_OWNER_APPROVAL_SCOPE: APPROVED_SECURITY_AND_PRIVACY_ARCHITECTURE_DESIGN_SOURCE_ONLY — NO_IMPLEMENTED_CONTROL — NO_COMPLIANCE_OR_CERTIFICATION_CLAIM — NO_OPERATIONAL_SECURITY_EFFECT
PROMPT_PART_STATUS: DRAFT_ASSEMBLY_PART — NOT_SEPARATELY_APPROVED — NOT_FROZEN
SUPPORTING_SOURCE_BINDINGS: CSIP-EO-AUDIT-GAP-02/0.1.0-candidate/fa400334a69702bf56e8588210449590573bccd3120d7c2cebd6ba9cc8fc161f; ENTERPRISE-TRUST-RISK-COST-EVIDENCE-REPRODUCIBILITY-MANDATE/verified-input-2026-07-28/1b5e7884a343589312d62259f181bd48f1a12b51e2613685c0d58c747a08dab4; CSIP-EO-PROMPT-ARCH-18P-C1/0.1.0-design-candidate/a4c80b938fccaab5d3d85c780351a41ee3444b4c6712920af45b493afbacb09b; CSIP-EO-GAP-RESOLUTION-MANIFEST-C1/0.1.0-candidate/349b590df9fad00c2e0ec317f4bd0b7ad747a5e22a1fead0f66f28c98e955216
PRIOR_PART_ID: CSIP-EO-FMSP-P10
NEXT_PART_ID: CSIP-EO-FMSP-P12
PART_PAYLOAD_SHA256: SEE_EXTERNAL_PROMPT_PACKAGE_MANIFEST
RECEIVE_MODE: CONTEXT_ONLY
ACTION_AUTHORITY: NONE

# پرامپت قسمت ۱۱ از ابرپرامپت نهایی ۱۸ قسمتی CSIP-EO

# Security، Privacy، Threat Model و Trust Boundaries

## 0. دستور دریافت، مرز Part و قفل ضدتوهم

P11-REQ-001 — این پیام فقط «قسمت ۱۱ از ۱۸» یک زمینۀ مرجع به‌هم‌پیوسته است. قسمت‌های ۰۱ تا ۱۰ باید پیش از آن و به‌ترتیب دریافت و ثبت شده باشند. قسمت‌های ۱۲ تا ۱۸ در این پیام وجود ندارند. دریافت P11 فقط Contract طراحی Security/Privacy را به Context می‌افزاید و هیچ Control، Identity، Credential، Key، Route، Scan، Incident Action، Spend یا Effect ایجاد نمی‌کند.

P11-REQ-002 — هنگام دریافت این Part، وضعیت داخلی فقط `RECEIVING_P11 — P01_THROUGH_P10_REQUIRED — CONTEXT_INCOMPLETE — ACTION_AUTHORITY_NONE` است.

P11-REQ-003 — پس از دریافت سالم P11 فقط Parse، حفظ Context، کنترل پیوستگی و پاسخ ثابت انتهای Part مجاز است؛ تحلیل یکپارچه، طراحی P12، Code، Test، Scan، Key/Secret action، Incident response، Spend، Release، Deployment و Production آغاز نمی‌شود.

P11-REQ-004 — سکوت، تأخیر کاربر، کامل‌بودن P11، Approved بودن Owner یا وجود Source Stage 26 مجوز ادامۀ خودکار نیست؛ Receiver باید تا دریافت صریح Part بعدی متوقف بماند.

P11-DEN-001 — اگر ترتیب `P01 → P02 → P03 → P04 → P05 → P06 → P07 → P08 → P09 → P10 → P11`، Header، Anchorها، Source Bindingها، Footer یا Pointerها کامل و سازگار نیستند، Receiver نباید این Part را فعال یا دریافت موفق را جعل کند.

P11-DEN-002 — Receiver نباید از عنوان، Owner، Version، Status، Digest یا Handoff این Part برای حدس، بازسازی یا تولید محتوای P12 تا P18 استفاده کند.

P11-DEN-003 — دریافت P11 مجوز Provisioning، Authentication/Federation change، Authorization publication، Credential/Certificate issuance، Secret/Key operation، Network/Egress change، Scanning، Exploitation، Deletion، Incident action، Build، Deploy، Spend یا Production Action نیست.

P11-DEN-004 — هیچ User، Workload، AI/Tool identity، Account، Session، Token، Certificate، Secret، Key، Policy، Firewall rule، Route، Allowlist، Detection، Sandbox، Provider connection یا Security product با دریافت این Part ایجاد، تغییر، فعال، متصل، Revoke یا حذف نمی‌شود.

P11-DEN-005 — هیچ Security/Privacy Contract، Trust Zone، Credential، Event، Tool، Connector، Break-glass یا Incident route نباید مسیر مستقیم، غیرمستقیم، مشتق‌شده، Human-mediated یا AI-mediated برای Spacecraft Command، Telecommand، Uplink، Flight Control یا Autonomous Maneuver Execution ایجاد کند.

P11-FAIL-001 — دریافت ناقص، بریده، خارج از ترتیب یا متعارض باید فقط با Diagnostic زیر گزارش شود:

~~~text
دریافت قسمت ۱۱ از ۱۸ ابرپرامپت نهایی CSIP-EO کامل و معتبر نبود.
وضعیت: PART_TRUNCATED_OR_CONFLICTED — CONTEXT_NOT_ACTIVATED
مورد لازم برای اصلاح: ایراد دقیقِ کشف‌شده در دریافت باید در همین سطر گزارش شود.
هیچ تحلیل، طراحی جدید، پیاده‌سازی، آزمون امنیتی یا اقدام اجرایی آغاز نمی‌شود.
~~~

P11-CON-001 — P11 مالک Zero Trust Architecture، Human/Workload/AI/Tool Identity، Trust Zone/Boundary، Threat/Adversary/Abuse/Privacy Model، Least Privilege، Segmentation/Egress، Secrets/Keys/Crypto Agility، Application/API/Event/Webhook/Sandbox Security، Supply-chain Security، AI/RAG/Memory Security، Privacy-by-design، Audit Integrity و Incident Containment Controls است.

P11-CON-002 — P11 فقط Architecture، Control Contract و Qualification Requirement را مالک است؛ P10 مالک Purpose/Rights/Retention/Hold/Deletion Policy، P12 مالک SLI/SLO/Telemetry/Capacity و P13 مالک Testing/V&V/Assurance باقی می‌مانند.

P11-CON-003 — هر واژۀ `approved` در این Part که به Source Stage 25 یا `SEC-DEC-250..259` مربوط است فقط Approval طراحی در Scope دقیق Owner Source است و به Prompt Package، Implemented Control، Compliance، Certification، Runtime Qualification، Deployment یا Production منتقل نمی‌شود.

## 1. هویت منبع، Status Preservation و Approval Scope

P11-DEF-001 — مالک معنایی P11 دقیقاً `CSIP-EO-STAGE-25 / 1.0.0-approved / SHA-256 39975398b6b08bb98875784e7e96a48af8a19f9a51955d9d7d67da7d98da04a3 / APPROVED AND CLOSED` است.

P11-CON-004 — Source Identity فقط با Tuple `Artifact ID + Exact Version + Exact SHA-256 + Exact Status` معتبر است.

P11-CON-005 — Filename، Directory، Timestamp، Length، Retrieval Rank، Similarity، Summary، Translation، Memory، Inline Copy یا Model Output به‌تنهایی Source Identity یا Supersession ایجاد نمی‌کند.

P11-CON-006 — Digest مالک معنایی Fixity Bytes را نشان می‌دهد؛ Approval طراحی Source از Metadata/Approval Record همان Source می‌آید. هیچ‌کدام Implemented Security، Legal Applicability، Privacy Compliance، Certification، Absence of Vulnerability یا Production Fitness را ثابت نمی‌کنند.

P11-CON-007 — `APPROVED AND CLOSED` باید بدون Downgrade یا Laundering حفظ شود: Source در Scope طراحی مصوب است، اما این Prompt Part همچنان Draft Assembly Part و کل Package هنوز Approved/Frozen نیست.

P11-CON-008 — تصمیم‌های `SEC-DEC-250..259` در Source با Status `APPROVED` حفظ می‌شوند؛ P11 حق تغییر عنوان، Problem، Selected، Rationale، Consequence، Risk، Exit Strategy یا Status آن‌ها را ندارد.

P11-CON-009 — انتقال رسمی Source §0 حفظ می‌شود: Stage 24 و `DGV-DEC-240..249` مصوب‌اند؛ Stage 25 حق بازتفسیر خاموش Truth علمی P06، AI Boundary P07، Capability/Effect P08، Authority/Persistence P09 یا Data Governance P10 را ندارد.

P11-CON-010 — پذیرش P11 توسط کاربر فقط `PART_ACCEPTED_FOR_ASSEMBLY` برای Bytes تحویلی ایجاد می‌کند؛ نه Approval تازه برای Source، نه Security/Privacy/Legal Approval، نه Permission برای Test/Scan و نه Operational Effect.

P11-CON-011 — Supporting Overlayهای Gap Resolution، Enterprise Mandate، Assembly Contract و Candidate Manifest فقط در Scope خود مصرف می‌شوند و حق Override کردن Semantic Owner Approved Stage 25 را ندارند.

P11-CON-012 — نسخۀ هم‌نام Stage 25 با Digest `abeb4bbe53ba06ba40660182c98277df3c00a4afe2cde74bf29d4363ff283c95` Source فعال P11 نیست؛ تنها Bytes منطبق با Digest قطعی `39975398b6b08bb98875784e7e96a48af8a19f9a51955d9d7d67da7d98da04a3` مصرف می‌شود.

P11-DEN-006 — Status Approved Source نباید به `COMPLIANT`، `CERTIFIED`، `IMPLEMENTED`، `SECURE`، `PEN_TESTED`، `INCIDENT_READY`، `VERIFIED_RUNTIME`، `QUALIFIED`، `DEPLOYED`، `PRODUCTION_READY` یا `FROZEN_PROJECT` تبدیل شود.

P11-DEN-007 — Status Draft/Candidate Supporting Source نباید به‌دلیل مصرف در P11 Approved معرفی شود.

P11-DEN-008 — Approved Source نباید با Summary یا Compilation به Status ضعیف‌تر بازنویسی شود؛ محدودیت Scope باید افزوده شود، نه اینکه Approval واقعی Source حذف یا تحریف شود.

P11-FAIL-002 — تعارض در Owner ID، Version، Digest، Status یا Approval Scope نتیجۀ `SOURCE_BINDING_CONFLICT — PART_NOT_ACCEPTED` دارد.

## 2. Objective، Scope، Exclusion و مالکیت میان Parts

P11-REQ-005 — هدف P11 تدوین یک Contract واحد، Zero-trust، identity-explicit، purpose-bound، deny-by-default، least-privilege، privacy-engineered، compromise-aware، evidence-producing و Vendor-neutral برای Security، Privacy، Threat Model و Trust Boundaries است.

P11-REQ-006 — Scope مالک P11 حداقل شامل Asset/Mission-impact، Roles/SoD، Applicability/Control Overlay، Trust Zones/Crossing، Threat/Adversary/Abuse/Risk، Classification/Handling، Human/Workload/AI/Tool Identity، Federation/Session/Token، Authorization/Approval/Break-glass، Network/Tenant/Purpose Isolation، Secrets/Keys/Crypto Agility، Storage/Backup/Restore Security، API/Event/Webhook/Egress/Sandbox، Supply Chain/SBOM/VEX/Vulnerability/SDLC، AI/RAG/Memory/Prompt Injection، Privacy/DSAR/De-identification/Telemetry، Audit/Detection/Incident/Containment/Recovery/Deletion Security و Command Boundary است.

P11-REQ-007 — هر Trust-boundary crossing باید Subject/Actor chain، Tenant، Purpose، Resource/Action، Data/Security/Privacy Classification، Policy snapshot/digest، Approval/Lease در صورت نیاز، short-lived sender-constrained Credential، Runtime enforcement، Receipt و Verification reference قابل‌حل داشته باشد.

P11-REQ-008 — `CGR-REQ-019` در مالکیت مشترک P10/P11/P12 مصرف می‌شود؛ P11 privacy/cardinality و no-secret/no-unnecessary-PII constraints را تعریف می‌کند. `CGR-REQ-010/013/015/027/028/030` فقط در Scope Security مصرف می‌شوند و مالکیت P04/P05/P10/P12/P13/P16 منتقل نمی‌شود.

P11-CON-013 — P01 مالک Project Identity، Stable Core، Canonical Entity/Event Envelope و Technology Status است؛ P11 فقط Security/Privacy Extension Profileهای Applicability-bound را روی آن مصرف می‌کند.

P11-CON-014 — P02 مالک Stage/Gate/Decision/Handoff و استقلال Design، Implementation، Verification، Validation، Qualification، Release، Deployment، Operation و Freeze است.

P11-CON-015 — P03 مالک Query، ApplicationCommand، Event، Approval، AuthorizationDecision، ExecutionLease، Receipt و Outcome Semantics است؛ P11 Security Context/Decision/Receipt را بدون ادغام این هویت‌ها Bind می‌کند.

P11-CON-016 — P04 مالک Workflow، Human Checkpoint، Pause، Retry، Recovery و Reconciliation Semantics است؛ P11 فقط Policy/Control/Evidence requirementهای Workflow را تحویل می‌دهد.

P11-CON-017 — P05 تنها مالک `E0..E9`، `APR-*`، `PERM-*`، `AUT-*` و Authority Intersection است؛ P11 Effect level را از Client/AI/Tool نمی‌پذیرد و Security Gate را به همان Taxonomy Bind می‌کند.

P11-CON-018 — P06 مالک Scientific Truth، Time/Frame/Unit/Covariance، Numerical Status و Independent Verification است؛ P11 Scientific-integrity threats را کنترل می‌کند ولی Physics یا Scientific validity را تعیین نمی‌کند.

P11-CON-019 — P07 مالک AI Advisory، Model Gateway، RAG، Knowledge، Memory، AI Confidence و `UNTRUSTED_DATA_ONLY` است؛ P11 Isolation/Identity/Credential/Egress controls را اعمال می‌کند ولی AI authority یا Truth را بازتعریف نمی‌کند.

P11-CON-020 — P08 مالک Capability/Plugin/Adapter/Tool/Connector Lifecycle، Registry Qualification و Invocation Brokerage است؛ P11 Trust/Identity/Sandbox/Supply-chain Controls را به آن تحویل می‌دهد ولی Capability State را جعل نمی‌کند.

P11-CON-021 — P09 مالک Persistence Authority، Canonical↔Physical Mapping، Transaction، Projection، Migration، Backup/Restore و Recovery Mechanism است؛ P11 Access/Key/Integrity/Containment controls را تعریف و Mechanism را Reference می‌کند.

P11-CON-022 — P10 مالک Dataset Governance، Classification/Purpose/Rights/Residency/Retention/Hold/Archive/Deletion Policy است؛ P11 Security/Privacy controls را به Profile/Location/Hold/Deletion Graph Bind می‌کند و Encryption را جایگزین Lawfulness یا Purpose نمی‌کند.

P11-CON-023 — P12 مالک Observability، Reliability، SLO، Performance، Capacity، Telemetry، Evidence Store و Metric Denominator است؛ P11 unsampled critical Security/Authority/Privacy events، redaction و required SLI inputs را تحویل می‌دهد.

P11-CON-024 — P13 مالک Test Program، Threat/Control Oracle، Benchmark، Acceptance، Equivalence و Assurance Case است؛ P11 testable control requirements، abuse cases و failure semantics را تعریف می‌کند.

P11-CON-025 — P14/P15 مالک Environment/Placement/Deployment و SDLC/Repository/Change/Release/Incident؛ P16 مالک Constitution/Governance/Risk Authority؛ P17 مالک Roadmap؛ و P18 مالک Compilation/Conflict Disposition باقی می‌مانند.

P11-DEN-009 — P11 نباید Base API/Event Envelope، Workflow State Machine، Effect/Approval Taxonomy، Scientific Algorithm، AI Confidence، Capability Lifecycle، Persistence/Data-governance Policy، SLO Threshold، Test Oracle، Deployment Gate، Project Constitution یا Freeze Contract رقیب تعریف کند.

P11-DEN-010 — P11 هیچ IdP، CA/PKI، KMS/HSM، Secret manager، SIEM، WAF، EDR، DLP، Scanner، Sandbox، Policy engine، Cloud، Region، Provider، Route، Algorithm suite، Cryptoperiod، Detection threshold، Notification rule یا Product نهایی را بدون Facts/Benchmark/Review/Evidence انتخاب نمی‌کند.

P11-DEN-011 — این Part هیچ Code، Dependency، Repository، Account، Identity، Credential، Certificate، Key، Secret، Policy publication، Network mutation، Scan، Exploit، Provider connection، Data transfer، Incident action، Spend، Build، Test Run، Deployment یا Operational Effect مجاز نمی‌کند.

P11-DEN-012 — هیچ Security/Privacy Design نباید Command/uplink-related Identity، Credential، Route، Queue، Topic، Webhook، Endpoint، Tool، Adapter، Break-glass، Approval path یا Human-mediated Enabling Path بسازد.

## 3. کپسول ثابت جهانی برای تمام ۱۸ قسمت

P11-INV-001 — Domain فعال `EARTH_ORBIT_ONLY` است؛ Baselineهای Orbital شامل `LEO / MEO / GEO / HEO`، Deployment Baseline زمینی و On-orbit Runtime Deferred است.

P11-INV-002 — Physics Before AI و Evidence Before Claims حاکم است؛ واقعیت فیزیکی، Observation معتبر، Law/Measurement Science و Evidence صلاحیت‌دار بر AI، Security tool، Detection، Threat score و Policy preference مقدم‌اند.

P11-INV-003 — AI فقط Advisory است و هیچ Authority علمی، حقوقی، امنیتی، مالی، Risk Acceptance، Budget، Approval، Identity، Authorization، Incident Attribution، Recovery یا Operational ندارد.

P11-INV-004 — Unknown، Missing، Stale، Conflicted، Invalid، Unsupported، Unverified، Non-converged، Corrupted، Revoked یا Indeterminate هرگز به Pass، Allow، Trusted، Secure، Verified، Approved یا Executable تبدیل نمی‌شود.

P11-INV-005 — Recommendation، Decision، Approval، AuthorizationDecision، ExecutionLease، Attempt، ExecutionReceipt و ValidatedOutcome رکوردهای مستقل، Link‌شده و دارای Immutable History باقی می‌مانند.

P11-INV-006 — Explainability، Uncertainty as a First-Class Concept، Independent Verification، Reproducibility، Immutable History و Graceful Degradation در تمام Security/Privacy Journey حفظ می‌شوند.

P11-INV-007 — معماری Event-driven، Digital Twin، Zero Trust، Replaceability و Engine/Model/Protocol/Store/Provider-agnostic است؛ هیچ Model، Agent، Tool، Scanner، Network location یا Dashboard حق جعل Physics یا ایجاد Authority ندارد.

P11-INV-008 — Minimum Sufficient Complexity حاکم است؛ Identity، Trust Zone، Control، Key tier، Provider، Detection یا Security product تازه فقط با Use Case، Threat/Risk/Cost، Owner، Exit Strategy و Verifiability روشن مجاز است.

P11-INV-009 — هیچ Digest، Signature، SBOM، VEX، Green Test، Provider Attestation، Audit Checkpoint، Part Acceptance یا Context Assembly مجوز Spend، Release، Deployment، Production یا Project Freeze نیست.

P11-INV-010 — هر مسیر Spacecraft Command، Telecommand، Uplink، Flight Control یا Autonomous Maneuver Execution، مستقیم یا غیرمستقیم، `E9 / APR-X / INC-0 / HARD_DENY` و بدون Waiver، Break-glass، Risk Acceptance یا Exit داخل CSIP-EO است.

P11-CON-026 — تکرار این Capsule یک Safety Checksum برای انتقال چندبخشی است؛ مالکیت Foundations را از P01 منتقل و Approval تازه ایجاد نمی‌کند.

P11-DEN-013 — Benefit، Deadline، Budget، Network locality، Vendor feature، Security emergency، Incident pressure یا Executive preference نمی‌تواند Hard Invariant، Scientific Invalidity، Rights/Purpose/Tenant Boundary یا No-command Boundary را Trade-off کند.

## 4. Projection مستقیم و Digest-bound از مالک معنایی مصوب

P11-REQ-009 — تمام محتوای زیر از `CSIP-EO-STAGE-25 / 1.0.0-approved` با Digest قطعی Owner به‌صورت `DIRECT` و در Scope طراحی مصوب Projection شده است. عبارت `Stage 25` در این بخش به Semantic Owner اشاره دارد؛ نه به اجرای Stage، پیاده‌سازی Control، Compliance، Certification یا Authority این Prompt Part.

P11-CON-027 — Linkها، Laws، Frameworkها، Standards، Drafts، Versionها و Technology implications این Projection بخشی از Bytes Owner و Baseline پذیرفته‌شده در تاریخ طراحی Source هستند. در تدوین P11 هیچ External Web Retrieval انجام نشده و هیچ ادعای Currentness، Legal Advice، Certification، Conformance یا Adoption فراتر از Source ساخته نمی‌شود.

P11-CON-028 — Blockهای Source در زیر بخشی از Clause بلافاصلۀ دارای ID هستند؛ Bullet، Table، Mermaid، Code Block و Subheading داخل همان Clause باید با Force، Exception، Status و Failure Semantics خود حفظ شوند. فقط Fenceهای سه‌Backtick برای Copy-safety به `~~~` تبدیل شده‌اند؛ این تبدیل Authority یا معنا را تغییر نمی‌دهد.

### Owner §1. تصمیم اجرایی Stage 25

P11-REQ-010 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §1; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Stage 25 یک معماری **Zero-trust، identity-explicit، purpose-bound، least-privilege، deny-by-default، privacy-engineered، compromise-aware و evidence-producing** تعریف می‌کند.

P11-REQ-011 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §1; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

اصل مرکزی:

P11-REQ-012 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §1; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

> هیچ Subject، Workload، AI، Tool، Plugin، Administrator، Dataset، Event، Provider یا Network location ذاتاً قابل‌اعتماد نیست. هر عبور از مرز اعتماد باید با Identity مستقل، Tenant و Purpose معتبر، Policy snapshot نسخه‌قفل‌شده، Request digest دقیق، Approval لازم، Credential کوتاه‌عمر، Runtime enforcement و Receipt قابل‌اعتبارسنجی دوباره مجاز شود.

P11-REQ-013 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §1; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

نتیجه:

P11-REQ-014 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §1; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- «داخل شبکه» یا «سرویس داخلی» مجوز نیست.
- Authentication به‌تنهایی Authorization، Approval یا Scientific authority ایجاد نمی‌کند.
- AI، Retrieved content، Tool output و External content همگی `UNTRUSTED_DATA_ONLY` هستند.
- Policy engine فقط تصمیم محاسبه می‌کند؛ Effect واقعی فقط با Execution lease محدود و در Runtime کنترل‌شده رخ می‌دهد.
- Credential passthrough، Shared identity، Ambient secret و Standing destructive privilege ممنوع‌اند.
- امنیت و حریم خصوصی دو Overlay مستقل و هم‌زمان‌اند؛ قوی‌بودن Encryption، Processing غیرمجاز یا Over-collection را قانونی یا مناسب نمی‌کند.
- Incident response می‌تواند خودکار **Deny، Isolate، Revoke، Quarantine یا Suspend** کند؛ Restore access، Declassification، Data release یا Effect مخرب به Approval و Evidence جدید نیاز دارد.
- Unknown، Missing، Conflict، Stale، Revoked یا Unverifiable هرگز به Allow تبدیل نمی‌شود.
- `SEC-TZ9` برای Spacecraft/Mission command از نظر Interface، Route، Identity، Credential، Queue، Topic، Webhook، Tool و Data contract تهی و غیرقابل‌دسترسی می‌ماند.

### Owner §2. هدف

P11-REQ-015 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §2; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

هدف Stage 25 تثبیت موارد زیر است:

P11-REQ-016 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §2; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

1. Security architecture و Trust-zone model
2. Threat-model method، adversary model و abuse/misuse cases
3. Human، Workload، AI و Tool identity separation
4. Authentication، federation، session و token semantics
5. Authorization، policy-as-code، approval و break-glass constraints
6. Service-to-service trust، segmentation، egress و ingress control
7. Tenant، Purpose، Classification و Region isolation
8. Secret management، key hierarchy، encryption و cryptographic agility
9. Application، API، Event، Webhook و Async security
10. Tool sandbox، arbitrary-code و Live-web security
11. Software supply-chain، SBOM، VEX، provenance و vulnerability gating
12. AI/ML، RAG، Vector، Memory و prompt-injection security
13. Privacy-by-design، DSAR identity proof، de-identification و telemetry minimization
14. Audit، tamper evidence، WORM interface و trusted-time requirements
15. Detection، incident response، containment، recovery و ransomware controls
16. Backup/restore، deletion، crypto-erasure و media-sanitization security
17. Third-party، transfer، connector و provider trust
18. Insider، physical، availability، abuse و cost-exhaustion threats
19. Scientific-integrity attack detection
20. Machine-readable envelopes، events، failure codes، tests و acceptance gates

### Owner §3. محدوده

P11-REQ-017 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §3; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Stage 25 این دارایی‌ها و مسیرها را پوشش می‌دهد:

P11-REQ-018 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §3; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- User، Admin، Reviewer، Approver، Service، Job، Agent و Tool identities
- Authentication factors، Sessions، Tokens، Certificates و Workload credentials
- Policy، Approval، Lease، Capability manifest و Revocation records
- Source code، Build، Artifact، Container، Package، SBOM، VEX و Provenance
- API، Event bus، Queue، Webhook، Batch، Export و File-transfer interfaces
- Canonical stores، Object/artifact stores، Projections، Caches، Search، Graph و Vector
- AI prompts، System instructions، Context manifests، Model outputs و Memory proposals
- Tool runtimes، Plugin adapters، MCP edges، Browser-like retrieval و External egress
- Dataset catalog، Governance registry، Consent، DSAR، Hold و Deletion workflows
- KMS/HSM interfaces، Key hierarchy، Backup keys، Secret broker و Rotation records
- Logs، Audit، Metrics، Traces، Security alerts، Evidence و Incident records
- Backup، Restore، DR، Archive، Sanitization و Crypto-erasure paths
- External provider، Subprocessor، Support-access و Cross-border transfer paths
- Scientific source، observation، transform، orbit، covariance، conjunction و `Pc` artifacts

P11-REQ-019 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §3; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

برای هر مسیر، Stage 25 تعیین می‌کند:

P11-REQ-020 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §3; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- چه Subject و Resource identityهایی لازم‌اند.
- مرز اعتماد کجاست و عبور از آن چه Evidence می‌خواهد.
- چه Data/Privacy/Security overlayهایی اعمال می‌شوند.
- چه Threatها و Abuse caseهایی معتبرند.
- چه Control پیشگیرانه، آشکارساز، محدودکننده و بازیابی‌کننده‌ای لازم است.
- Failure چگونه Machine-readable و Fail-closed می‌شود.
- Effect/Approval در چه سطحی است.
- چه Test و Evidenceای پیش از Promotion لازم است.

### Owner §4. خارج از محدوده

P11-DEN-014 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §4; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

موارد زیر خارج از Stage 25 هستند:

P11-DEN-015 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §4; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- انتخاب نهایی Vendor، Cloud، Region، Product یا Commercial service
- صدور Certificate، Provision کردن User، ایجاد Key/Secret یا اتصال IdP واقعی
- تعیین RTO/RPO/SLO و Alert threshold عددی نهایی بدون Benchmark مرحلهٔ مقرر
- تعیین نهایی Network topology، Cluster، Account، Subscription یا Landing zone
- اجرای Penetration test یا Red team عملی روی Production
- ارائهٔ نظر حقوقی، Certification، Attestation یا Compliance guarantee
- تکمیل DPIA، TIA، ROPA، DSAR یا Breach notification واقعی
- تعیین تمام Retention durationها یا Jurisdiction facts حل‌نشدهٔ Stage 24
- انتخاب یا فعال‌سازی Live web، Connector، Plugin یا External provider
- فعال‌سازی Arbitrary code execution؛ این قابلیت در Baseline غیرفعال می‌ماند
- پیاده‌سازی Runtime، Workflow، Policy engine، KMS، SIEM یا Audit store
- Training، Fine-tuning، Model deployment یا Provider onboarding واقعی
- اجرای Crypto-shred، Media sanitization، Backup expiry یا Deletion واقعی
- هر نوع Spacecraft command، Telecommand، Mission-control action یا Upload-to-spacecraft

P11-DEN-016 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §4; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Stage 25 **Control architecture و qualification contract** را نهایی می‌کند؛ Factها، Products، Routes و Thresholdهای وابسته به Organization، Benchmark یا Provider تا محل مصوب خود Fail-closed باقی می‌مانند.

### Owner §5. زبان هنجاری، مرز حقوقی و مدل Assurance

P11-REQ-021 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §5; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

در این سند:

P11-REQ-022 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §5; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- **باید / MUST:** الزام قطعی Baseline
- **نباید / MUST NOT:** ممنوعیت قطعی Baseline
- **باید بهتر است / SHOULD:** پیش‌فرض قوی؛ انحراف نیازمند Decision Record و Risk acceptance معتبر
- **ممکن است / MAY:** گزینهٔ مجاز تحت Policy
- **Hard deny:** درخواست پیش از Effect رد می‌شود
- **Fail-closed:** Unknown، Missing، Conflict، Stale یا Invalid به Allow تبدیل نمی‌شود
- **Compromise assumed:** طراحی باید خرابی یا تصرف یک Zone را بدون اعتماد ضمنی به آن تحمل کند
- **Control evidence:** شاهد نسخه‌دار، قابل‌بازتولید و مستقل از ادعای Component

P11-REQ-023 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §5; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

این سند:

P11-REQ-024 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §5; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Engineering specification است، نه نظر حقوقی یا گواهی انطباق.
- ISO، NIST، OWASP، MITRE، SLSA یا هر Framework را برابر Certification نمی‌داند.
- هیچ Draft، Blog، Proposal، نسخهٔ `latest` یا Vendor claim را خودکار Normative نمی‌کند.
- NIS2، CRA، GDPR و سایر مقررات را فقط با Applicability تصمیم‌گیری‌شده اعمال می‌کند.
- هر Risk acceptance را زمان‌دار، Scope-bound و دارای Compensating control می‌خواهد؛ پذیرش Blanket یا دائمی معتبر نیست.

P11-REQ-025 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §5; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

سطوح Evidence:

P11-REQ-026 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §5; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

| سطح | معنا | نمونهٔ کافی |
|---|---|---|
| `SEC-EV0` | ادعا/طراحی | سند و Owner؛ برای Production کافی نیست |
| `SEC-EV1` | آزمون محلی | Test output نسخه‌دار |
| `SEC-EV2` | آزمون یکپارچه | Negative/abuse tests و signed receipt |
| `SEC-EV3` | آزمون مستقل | Reviewer یا محیط مستقل |
| `SEC-EV4` | Evidence عملیاتی محدود | Canary، telemetry و rollback proof |
| `SEC-EV5` | Evidence پیوسته | Drift، incident، requalification و trend |

P11-REQ-027 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §5; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

هیچ Capability پرخطر فقط با `SEC-EV0` یا Self-attestation Component به Production نمی‌رود.

### Owner §6. Invariantهای ارث‌رسیده

P11-INV-011 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §6; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

1. دامنهٔ فعال پروژه فقط `EARTH_ORBIT_ONLY` است.
2. Stage 25 حق گسترش دامنه به Moon، Mars، deep space یا spacecraft control را ندارد.
3. AI advisory است و Scientific، Legal، Security یا Operational authority نیست.
4. Model output و Tool call فقط Proposal هستند.
5. Effect واقعی فقط پس از Policy، Approval، Execution lease، isolated execution و validated receipt رخ می‌دهد.
6. Effect level را Client، Model، Tool، Plugin یا Adapter نمی‌تواند کاهش دهد.
7. Approval از AI، Plugin، Tool یا همان Actor مجری معتبر نیست.
8. Scientific truth فقط از Pipeline و قراردادهای Stage 20 می‌آید.
9. Missing covariance، HBR، Frame، Time scale، Unit یا uncertainty حدس زده نمی‌شود.
10. `Pc=NOT_COMPUTABLE`، `NOT_CONVERGED` و `DISAGREEMENT` به وضعیت امن یا عدد دلخواه تبدیل نمی‌شوند.
11. هر Data class دقیقاً یک Authoritative path دارد.
12. Vector، Search، Graph، Analytics و Cache Source of Truth نیستند.
13. Scientific revisionها immutable و Correctionها superseding هستند.
14. Artifact identity با Digest و Canonicalization profile ثابت می‌شود.
15. Raw SQL و Database credential برای AI، Plugin، Client یا Untrusted tool ممنوع است.
16. Token passthrough و Credential حضور‌یافته در Model context ممنوع‌اند.
17. Read، Write، Install، Enable، Approve، Execute و Verify Capabilityهای جدا هستند.
18. Retrieved content و Tool output همیشه `DATA_ONLY` و فاقد Instruction authority هستند.
19. Silent fallback، silent downgrade، silent scope expansion و silent protocol upgrade ممنوع‌اند.
20. Alias متغیر `latest` برای Dependency، Policy، Model، Tool، Schema یا Protocol معتبر نیست.
21. Tenant و Purpose باید در هر Hop حفظ و مستقل دوباره اعتبارسنجی شوند.
22. Cross-tenant یا Cross-purpose reuse بدون Policy صریح Hard deny است.
23. Unknown Classification، Residency، Rights یا Recipient برای Egress برابر Deny است.
24. Provider training/use از Data بدون Permission صریح ممنوع است.
25. Silent memory write ممنوع است و Memory غیرAuthoritative و expiring است.
26. Raw chain-of-thought مطالبه، ذخیره یا صادر نمی‌شود.
27. Backup موفق فقط با Restore مستقل و Validation اثبات می‌شود.
28. Restore حق replay کردن External effect یا resurrect کردن دادهٔ حذف‌شده/revoked را ندارد.
29. Retention expiration فقط `DELETION_CANDIDATE` می‌سازد.
30. Legal hold Access یا Purpose جدید ایجاد نمی‌کند.
31. Destructive scope پس از Approval قابل‌گسترش نیست.
32. Unknown effect پیش از Retry باید Reconcile شود.
33. Audit و Evidence نباید Secret، Token یا Personal data غیرضروری نگه دارند.
34. Security، Authority، Approval، Deletion و Command-denial eventها Sample نمی‌شوند.
35. هیچ Route، DNS، Proxy، Queue، Topic، Webhook، Credential، Adapter یا Data contract به Spacecraft command وجود ندارد.

### Owner §7. واژگان قطعی

P11-DEF-002 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §7; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

| اصطلاح | تعریف قطعی |
|---|---|
| `Subject` | انسان، Workload، Job، Tool یا Process دارای Identity مستقل |
| `Principal` | Subject احراز‌شده با Claims قابل‌اعتبارسنجی |
| `Actor chain` | زنجیرهٔ User، Host، AI proposal، Broker و Executor؛ هر عضو هویت مستقل دارد |
| `Resource` | Data، Capability، Policy، Key، Artifact، Route یا Administrative object |
| `Trust zone` | دامنه‌ای با کنترل و فرض شکست مشخص؛ نه معادل Subnet یا Account |
| `Trust boundary` | محل تغییر Authority، Identity، Data handling یا Compromise assumption |
| `Security overlay` | Confidentiality، Integrity، Availability و mission-impact controls |
| `Privacy overlay` | Personal-data، Purpose، Role، Rights، Minimization و transfer controls |
| `Authorization` | تصمیم Policy برای Subject/Action/Resource/Context مشخص |
| `Approval` | مجوز انسانی/سازمانی جدا از Authorization، برای Effect مشخص و زمان محدود |
| `Execution lease` | Capability token کوتاه‌عمر، one-purpose و digest-bound برای یک Effect |
| `Sender-constrained token` | Token غیرقابل‌استفاده بدون اثبات کلید Client/Workload |
| `Break-glass` | مسیر اضطراری محدود، زمان‌دار، دلیل‌دار، دوکنترلی و Post-review؛ نه حساب مشترک |
| `Secret` | داده‌ای که افشای آن امکان Auth، Signing، Decryption یا privilege می‌دهد |
| `Key hierarchy` | تفکیک Root/KEK/DEK/Signing/Backup/tenant-purpose keys و lifecycle آن‌ها |
| `SBOM` | فهرست Machine-readable اجزای Software و روابط Dependency |
| `VEX` | Assertion نسخه‌دار دربارهٔ Applicability/impact یک Vulnerability، با Evidence |
| `Reachability` | امکان واقعی رسیدن مسیر اجرای موردنظر به Component/vulnerable code |
| `Security incident` | رویداد تأییدشده یا محتمل که Confidentiality، Integrity، Availability، Privacy یا Authority را تهدید می‌کند |
| `Privacy threat` | قابلیت ایجاد Linking، Identification، Disclosure، Unawareness یا Non-compliance |
| `Tamper evidence` | امکان آشکارکردن تغییر؛ نه لزوماً جلوگیری فیزیکی از تغییر |
| `WORM interface` | مسیر Append/retention-lock کنترل‌شده با Evidence؛ نه ادعای مطلق تغییرناپذیری |
| `Command boundary` | مرز ممنوعی که هر نوع فرمان/کنترل فضاپیما را خارج از Baseline نگه می‌دارد |

### Owner §8. فرض‌های امنیتی، دارایی‌ها و Mission impact

#### Owner §8. 1 فرض‌های پایه

P11-DEF-003 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §8; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Internet، External provider، Web content، Package registry و User-supplied files خصمانه فرض می‌شوند.
- یک Tool sandbox یا Plugin می‌تواند تصرف شود.
- یک Credential می‌تواند Leak شود؛ Blast radius باید با Scope/TTL/tenant/purpose محدود شود.
- یک Insider می‌تواند Authorized access را برای Purpose نامعتبر استفاده کند.
- یک Dependency یا Build service می‌تواند Compromise شود.
- یک Source علمی می‌تواند اشتباه، جعلی، قدیمی یا Poisoned باشد.
- یک Backup می‌تواند آلوده، ناقص، rollbackشده یا دارای دادهٔ حذف‌شده باشد.
- Clock، DNS، Redirect، Queue delivery و Network response می‌توانند نامطمئن یا خصمانه باشند.
- Control plane نیز نیازمند کنترل است و «Trusted» به معنی «غیرقابل‌نفوذ» نیست.

#### Owner §8. 2 دارایی‌های Crown-jewel

P11-DEF-004 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §8; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

1. Policy، Approval و Execution-lease integrity
2. Human و Workload identity roots
3. Tenant/Purpose boundary و Authorization data
4. Key، Secret و Signing material
5. Scientific authoritative artifacts و Provenance
6. Source-authority و Governance registries
7. Deletion، Hold، Consent و Revocation journals
8. Build provenance، Source history و Artifact registry
9. Audit/evidence chain و trusted-time records
10. Backup/restore control و recovery credentials
11. Command-boundary deny policy و نبود مسیر `SEC-TZ9`

#### Owner §8. 3 Mission-impact classes

P11-DEF-005 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §8; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

| Class | توضیح | حداقل رفتار |
|---|---|---|
| `MI-0` | Public/low operational impact | Baseline controls |
| `MI-1` | Internal support | Auth، integrity، recoverability |
| `MI-2` | Sensitive business/privacy | Strong isolation، encryption، audit |
| `MI-3` | Scientific decision support | Provenance، immutability، dual validation |
| `MI-4` | Authority/security control plane | Strong identity، dual control، unsampled audit |
| `MI-5` | Destructive or irreversible data effect | بالاترین Profile قابل‌اعمال Stage 19 + explicit multi-role approval، fenced lease و independent verify |
| `MI-X` | Spacecraft/Mission command | `PROHIBITED / HARD_DENY` |

P11-DEF-006 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §8; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Mission impact با Data confidentiality یکی نیست؛ Public orbital data می‌تواند در مسیر Scientific integrity دارای `MI-3` باشد.

### Owner §9. اصول امنیت و حریم خصوصی

P11-INV-012 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §9; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

1. **Explicit trust:** هر اعتماد باید Scope، Owner، Evidence و Expiry داشته باشد.
2. **Deny by default:** نبود Rule مثبت و کامل برابر Deny است.
3. **Least privilege:** Action، Resource، Tenant، Purpose، Region، Time و Data fields حداقل می‌شوند.
4. **Separation of duties:** Request، Approval، Execution و Verification تا حد خطر از هم جدا هستند.
5. **Continuous verification:** Auth یک رخداد یک‌باره نیست؛ posture، revocation و context دوباره سنجیده می‌شوند.
6. **Compromise containment:** شکست یک Zone نباید Credential یا Authority Zone دیگر را بدهد.
7. **No ambient authority:** Runtime فقط Credential scoped و just-in-time دریافت می‌کند.
8. **Privacy by design/default:** Collection، retention، visibility و telemetry حداقل‌اند.
9. **Scientific integrity:** Security control نباید Scientific status یا uncertainty را تحریف کند.
10. **Secure failure:** Timeout، partial effect و dependency failure به Allow یا blind retry تبدیل نمی‌شوند.
11. **Deterministic enforcement:** Machine action فقط از Structured، schema-valid و policy-valid contracts می‌آید.
12. **Evidence over assertion:** Control با Test/Receipt اثبات می‌شود، نه Vendor claim.
13. **Version pinning:** Policy، Schema، Threat corpus، Runtime، Algorithm و Tool به نسخه/Digest مقیدند.
14. **Rebuild over hidden trust:** Projection، Index، Cache و Vector از Source معتبر قابل‌بازسازی‌اند.
15. **No security theater:** Badge، checklist یا Scan بدون Scope/Reachability/response کافی نیست.

### Owner §10. نقش‌ها و Separation of Duties

P11-CON-029 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §10; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

| نقش | اختیار مجاز | اختیار ممنوع |
|---|---|---|
| Security Architect | معماری و Control profile | Self-approve Production exception |
| Security Owner/CISO delegate | Risk disposition در Scope مصوب | تغییر Scientific truth |
| Privacy/DPO delegate | Privacy review و applicability advice | اجرای فنی یا حذف بدون Approval |
| IAM Administrator | Lifecycle identity تحت Workflow | دسترسی Data به‌خاطر نقش IAM |
| PKI/KMS Custodian | Key/Certificate operations | خواندن plaintext Dataset |
| Policy Administrator | انتشار Rule پس از review | Approve Effect خودش |
| Approver | Approval محدود به Effect/Scope | Execute یا Verify همان Effect پرخطر |
| Executor | اجرای Lease دقیق | گسترش Scope یا ساخت Approval |
| Independent Verifier | Receipt/Evidence validation | تغییر نتیجهٔ اجرا |
| Incident Commander | Containment هماهنگ | دائمی‌کردن emergency privilege |
| Data Owner/Steward | Data use/governance accountability | Override Security/Privacy hard deny |
| Developer | Source change در Branch کنترل‌شده | Direct Production deploy |
| Build service | Build محدود و attestشده | Production runtime access |
| AI/Model | تحلیل، پیشنهاد و Draft | Identity، Approval، Effect، Secret یا Policy authority |
| Tool/Plugin | اجرای Capability leased | Ambient credential یا Policy override |

P11-CON-030 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §10; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

الزامات:

P11-CON-031 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §10; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- هیچ Principal واحدی نباید Request، Approval، Execution و Verification یک Effect `E7/E8` را کامل کند.
- حساب مشترک انسانی ممنوع است.
- Break-glass یک Role دائمی یا Credential مشترک نیست.
- Admin access از Workload path، Developer path و Recovery path جداست.
- Service owner نمی‌تواند Vulnerability exception خودش را بدون Reviewer مستقل تصویب کند.
- Security team نمی‌تواند با برچسب «امنیت» Retention، Legal hold، Data access یا Scientific status را یک‌طرفه تغییر دهد.

### Owner §11. Baseline رسمی و نسخه‌قفل‌شده در تاریخ طراحی

P11-CON-032 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §11; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

این جدول «مبنای ارزیابی» است، نه انتخاب Product یا ادعای Certification.

P11-CON-033 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §11; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

| حوزه | Baseline پذیرفته‌شده | وضعیت Stage 25 |
|---|---|---|
| ISMS controls | `ISO/IEC 27001:2022` و `ISO/IEC 27002:2022` | Stable reference |
| Privacy framework | `ISO/IEC 29100:2024` | Stable reference |
| PIMS | `ISO/IEC 27701:2025` | Stable reference |
| Cloud PII | `ISO/IEC 27018:2025` | Stable reference |
| Identity framework | `ISO/IEC 24760-1/-2/-3:2025` | Stable reference |
| NIST control catalog | `SP 800-53 Rev.5`, Release `5.2.0` | Version-pinned overlay |
| Cybersecurity outcomes | `NIST CSF 2.0` | Governance/outcome map |
| Zero Trust | `NIST SP 800-207` و `SP 800-207A` | Architecture reference |
| Digital identity | `NIST SP 800-63-4` | Current final baseline |
| Incident response | `NIST SP 800-61 Rev.3` | Current final baseline |
| Secure development | `NIST SP 800-218 v1.1` | Stable SSDF reference |
| Supply-chain risk | `NIST SP 800-161 Rev.1 Update 1` | Stable reference |
| Key management | `NIST SP 800-57 Part 1 Rev.5` | Stable reference |
| PQC standards | `FIPS 203`, `FIPS 204`, `FIPS 205` | Crypto-agility candidates after profile/interop |
| Application verification | `OWASP ASVS 5.0.0` | Verification catalog |
| Web risks | `OWASP Top 10:2025` | Threat input |
| API risks | `OWASP API Security Top 10:2023` | Threat input |
| Web testing | `OWASP WSTG 4.2` | Stable test reference; v5 development not baseline |
| LLM risks | `OWASP Top 10 for LLM Applications 2025` | AI threat input |
| LLM verification | `OWASP LLMSVS 2.0` | Evaluation reference; not certification |
| Enterprise threats | `MITRE ATT&CK v19` snapshot `2026-04-28` | Snapshot/digest pinned |
| AI threats | `MITRE ATLAS` | Qualification-time snapshot/digest; no floating corpus |
| Threat methods | `STRIDE` + `LINDDUN` | Mandatory complementary methods |
| Build provenance | `SLSA v1.2` | Target levels by artifact class |
| SBOM/VEX | `CycloneDX 1.7` و `SPDX 3.0.1` | Dual interchange, internal neutral graph |
| Vulnerability scoring | `CVSS v4.0` specification document `1.2` | One input, never sole gate |
| Exploitation probability | `EPSS v4` | Time-varying input |
| Known exploitation | CISA `Known Exploited Vulnerabilities` catalog | Mandatory priority input |
| Media sanitization | `NIST SP 800-88 Rev.2` | Method/evidence profile |
| Privacy engineering | `NIST Privacy Framework 1.0` | Stable baseline |

#### Owner §11. 1 موارد صریحاً غیرBaseline

P11-CON-034 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §11; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- `NIST Privacy Framework 1.1` در تاریخ طراحی Initial Public Draft است.
- `NIST IR 8547` دربارهٔ گذار به Post-Quantum Cryptography Initial Public Draft است.
- `ISO/IEC 27017` Edition 2 و `ISO/IEC 29151` Edition 2 در وضعیت under publication هستند.
- OWASP WSTG v5 توسعه‌ای است.
- هر ATT&CK/ATLAS، KEV، EPSS، Browser rule، Model rule یا Provider policy شناور بدون Snapshot/Digest ممنوع است.
- هیچ Draft یا نسخهٔ آتی خودکار جای Baseline را نمی‌گیرد؛ Upgrade به Change record، Diff، Threat review، Regression و Re-promotion نیاز دارد.

#### Owner §11. 2 مقررات و Applicability

P11-CON-035 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §11; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- GDPR، NIS2 و Cyber Resilience Act فقط پس از ثبت Role، Entity، Product، Jurisdiction، Processing و تاریخ Applicability اعمال می‌شوند.
- CRA به‌صورت Blanket «اکنون کاملاً لازم‌الاجرا» فرض نمی‌شود؛ هر Chapter/Article تاریخ و Scope خودش را دارد.
- Breach/incident reporting clock فقط پس از Legal/Privacy applicability decision فعال می‌شود.
- Standard داوطلبانه، Technical baseline و قانون در Registry سه نوع جدا هستند.

#### Owner §11. 3 منابع رسمی نسخه‌ای

P11-CON-036 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §11; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- [NIST SP 800-63-4 — Digital Identity Guidelines](https://csrc.nist.gov/pubs/sp/800/63/4/final)
- [NIST SP 800-61 Rev.3 — Incident Response](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
- [NIST SP 800-53 Rev.5 / Release 5.2.0 planning note](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [NIST Privacy Framework 1.1 status](https://www.nist.gov/privacy-framework/new-projects/privacy-framework-version-11)
- [NIST SP 800-88 Rev.2 — Media Sanitization](https://csrc.nist.gov/pubs/sp/800/88/r2/final)
- [NIST finalized PQC standards announcement](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
- [OWASP ASVS 5.0.0](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP LLMSVS 2.0](https://owasp.org/www-project-llm-verification-standard/LLMSVS-v2.0-en.html)
- [MITRE ATT&CK v19 update](https://attack.mitre.org/resources/updates/updates-april-2026/)
- [SLSA specification v1.2](https://slsa.dev/spec/v1.2/)
- [CycloneDX v1.7 release](https://cyclonedx.org/news/cyclonedx-v1.7-released/)
- [SPDX specification 3.0.1](https://spdx.github.io/spdx-spec/v3.0.1/)
- [FIRST CVSS v4.0](https://www.first.org/cvss/) و [EPSS](https://www.first.org/epss/)
- [CISA Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [EU Cyber Resilience Act — Regulation 2024/2847](https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng)

### Owner §12. Applicability Registry و Control overlays

P11-CON-037 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §12; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

هر Deployment/Capability باید یک `SecurityApplicabilityProfile` نسخه‌دار داشته باشد:

P11-CON-038 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §12; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

~~~json
{
  "profile_id": "sap_...",
  "version": 1,
  "system_scope": ["service-or-capability-id"],
  "domain_scope": "EARTH_ORBIT_ONLY",
  "tenant_scope": ["tenant-id"],
  "purpose_scope": ["purpose-id"],
  "mission_impact": "MI-0..MI-5",
  "data_overlays": ["confidentiality", "privacy", "rights", "residency"],
  "threat_model_version": "tm_...@digest",
  "control_profiles": ["control-profile@digest"],
  "legal_applicability_refs": ["applicability-decision-id"],
  "accepted_exceptions": ["risk-acceptance-id"],
  "evidence_minimum": "SEC-EV0..SEC-EV5",
  "owner": "role-id",
  "reviewed_at": "RFC3339",
  "expires_at": "RFC3339",
  "digest": "sha256:..."
}
~~~

P11-CON-039 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §12; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

قواعد:

P11-CON-040 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §12; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Overlayهای Security، Privacy، Scientific integrity، Data rights و Availability مستقل‌اند.
- Conflict با Deny-overrides و «کنترل سخت‌گیرانه‌تر» حل می‌شود؛ Merge دستی Silent ممنوع است.
- Profile منقضی، نامعلوم یا فاقد Threat-model digest برای Production معتبر نیست.
- Risk acceptance بخشی از Profile است و Expiry/Scope/Owner/Compensating control دارد.
- تغییر Tenant، Purpose، Data class، External route، Algorithm، Provider یا Effect class Profile جدید می‌خواهد.

### Owner §13. معماری منطقی امنیت

P11-CON-041 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §13; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

~~~mermaid
flowchart TB
    U["SEC-TZ0/1: External + Edge"] --> I["SEC-TZ2: Identity"]
    I --> P["SEC-TZ3: Policy, Approval, Broker"]
    P --> C["SEC-TZ4: Scientific + Data Core"]
    P --> A["SEC-TZ5/6: AI + Tool Sandboxes"]
    A --> X["SEC-TZ7: Controlled Egress"]
    P --> S["SEC-TZ8: Keys, Audit, Recovery"]
    C --> S
    Z["SEC-TZ9: Spacecraft Command — No Route"]:::deny
    classDef deny fill:#5b1111,color:#fff,stroke:#b91c1c,stroke-width:2px
~~~

P11-CON-042 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §13; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

این Diagram **Connectivity مجاز را کامل توصیف نمی‌کند**؛ هر پیکان فقط نشان می‌دهد یک Boundary contract ممکن است تعریف شود. نبود پیکان به `SEC-TZ9` یک الزام معماری است.

P11-CON-043 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §13; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

مسیر Effect مجاز:

P11-CON-044 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §13; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

`Authenticated actor → Canonical request → Policy decision → Required approval → Scoped execution lease → Isolated executor → Validated receipt → Independent verification`

P11-CON-045 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §13; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

هیچ Component حق کوتاه‌کردن این مسیر را ندارد. Cache فقط می‌تواند Decision غیرمنقضی و دقیقاً Context-bound را نگه دارد؛ Approval یا Lease از Cache عمومی بازیابی نمی‌شود.

### Owner §14. Trust zones

P11-CON-046 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §14; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

| Zone | محتوا | فرض اعتماد/شکست | قیود |
|---|---|---|---|
| `SEC-TZ0` | Internet، external content، attacker-controlled input | خصمانه | هیچ Credential/Instruction authority |
| `SEC-TZ1` | UI، edge، API ingress، authenticated user device | Device/user compromise ممکن | Input validation، session binding، rate controls |
| `SEC-TZ2` | Identity، federation، CA validation، session service | High-value target | Dedicated admin، strong auth، revocation |
| `SEC-TZ3` | Policy، Approval، Capability broker، Lease issuer | Authority control plane | Dual control، signed/versioned decisions، no business payload |
| `SEC-TZ4` | Authoritative scientific/data services | Service compromise possible | Per-service identity، tenant/purpose/data controls |
| `SEC-TZ5` | AI inference، RAG assembly، evaluation | Output untrusted/advisory | No secret، no direct effect، structured validation |
| `SEC-TZ6` | Tool، Plugin، build/test sandbox | Compromise assumed | Ephemeral، rootless، no ambient network/secret |
| `SEC-TZ7` | Controlled egress، external providers/connectors | External party untrusted | Allowlist، classification، transfer، response quarantine |
| `SEC-TZ8` | KMS/HSM interface، audit، detection، admin/recovery plane | Highest assurance, still monitored | Separate identities، networks، approvals، immutable evidence |
| `SEC-TZ9` | Spacecraft/Mission command | خارج از Baseline | No interface، route، credential، queue، schema or exception |

P11-CON-047 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §14; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

قواعد Zone:

P11-CON-048 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §14; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Zone membership مجوز نیست.
- یک Principal برای هر Zone/role هویت جدا دارد.
- `SEC-TZ8` به معنی Superuser همه‌جا نیست؛ Key custodian، Audit writer، Detector، Responder و Recovery operator هویت و Scope جدا دارند.
- `SEC-TZ5/6` هرگز Credential اصلی `SEC-TZ3/4/8` را دریافت نمی‌کنند.
- Egress از `SEC-TZ4/5/6` فقط از `SEC-TZ7` و Policy route مشخص عبور می‌کند.
- Admin و Recovery traffic از مسیر User/data عمومی جدا و Just-in-time است.
- هر اتصال احتمالی به `SEC-TZ9` Build/qualification را Fail می‌کند.

### Owner §15. قرارداد عبور از Trust boundary

P11-CON-049 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §15; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

هر Boundary crossing باید Envelope زیر را حمل کند:

P11-CON-050 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §15; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

~~~json
{
  "request_id": "uuid",
  "actor_chain": [
    {"subject_id": "human-or-service", "subject_type": "HUMAN|WORKLOAD|TOOL"}
  ],
  "tenant_id": "tenant-id",
  "purpose_id": "purpose-id",
  "resource_id": "canonical-resource-id",
  "action": "typed-action",
  "data_classification": ["overlay@version"],
  "mission_impact": "MI-0..MI-5",
  "effect_level": "E0..E8",
  "policy_snapshot": "policy@sha256",
  "request_digest": "sha256:...",
  "approval_ref": "nullable-approved-record",
  "lease_ref": "nullable-short-lived-lease",
  "source_zone": "SEC-TZx",
  "destination_zone": "SEC-TZy",
  "issued_at": "RFC3339",
  "expires_at": "RFC3339",
  "nonce": "unique",
  "signature": "detached-signature-ref"
}
~~~

P11-CON-051 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §15; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Validator باید حداقل این موارد را دوباره محاسبه کند:

P11-CON-052 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §15; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Identity، key status و actor-chain continuity
- Tenant، Purpose، Resource و Action match
- Classification و transfer/region eligibility
- Effect level از Server-side taxonomy
- Policy/Schema version و digest
- Approval subject/action/resource/request exact match
- Lease audience، nonce، TTL، sender binding و replay status
- Source/destination Zone eligibility
- Rate/resource budget
- Command-boundary denial

P11-CON-053 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §15; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Missing، mismatch، expired، replayed، revoked، clock-invalid یا unknown → `HARD_DENY`.

### Owner §16. روش مدل‌سازی تهدید

P11-CON-054 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §16; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Stage 25 چهار لنز اجباری را ترکیب می‌کند:

P11-CON-055 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §16; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

1. **STRIDE** برای Spoofing، Tampering، Repudiation، Information disclosure، Denial of service و Elevation of privilege
2. **LINDDUN** برای Linking، Identifying، Non-repudiation، Detecting، Data disclosure، Unawareness و Non-compliance
3. **MITRE ATT&CK v19** برای Technique/Detection/mitigation mapping سازمانی
4. **MITRE ATLAS + OWASP LLM 2025/LLMSVS 2.0** برای AI/RAG/Model/Tool abuse

P11-CON-056 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §16; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

فرآیند:

P11-CON-057 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §16; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

1. Scope، Business/Scientific purpose و trust assumptions ثبت می‌شوند.
2. DFD، Data lifecycle، Actor chain و Trust boundaries نسخه‌گذاری می‌شوند.
3. دارایی، Adversary، Entry point و Abuse case استخراج می‌شوند.
4. STRIDE و LINDDUN برای هر Flow/Store/Process اجرا می‌شوند.
5. ATT&CK/ATLAS/OWASP mapping برای Coverage و Detection اضافه می‌شود.
6. Risk با Impact چندمحوری، Likelihood evidence، Exposure و Control strength محاسبه می‌شود.
7. Prevent، Detect، Contain، Recover و Verify controls تعیین می‌شوند.
8. Residual risk فقط توسط Risk owner مجاز، زمان‌دار و Scope-bound پذیرفته می‌شود.
9. Test و Evidence level تعیین می‌شود.
10. هر تغییر مادی، Incident یا Threat-corpus upgrade مدل را باطل یا نیازمند Review می‌کند.

P11-CON-058 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §16; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Threat model یک PDF ایستا نیست؛ Artifact نسخه‌دار با Digest، Owner، assumptions، unresolved threats، evidence links و expiry است.

### Owner §17. Adversary model

P11-CON-059 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §17; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

| Actor | توان فرض‌شده | هدف‌های نمونه |
|---|---|---|
| Anonymous Internet attacker | Scan، exploit، DoS، credential stuffing | Edge/API compromise |
| Authenticated malicious tenant | Valid account، crafted data/API | Cross-tenant access، cost abuse |
| Compromised user device | Session/token theft، UI manipulation | Privilege misuse |
| Malicious/compromised insider | Legitimate access و context | Exfiltration، suppression، policy abuse |
| Compromised workload | Service credential و network foothold | Lateral movement، data tamper |
| Supply-chain attacker | Package/build/source/registry manipulation | Backdoor و provenance forgery |
| External provider attacker | Response/content/control over hosted service | Data capture، prompt injection، silent change |
| Data/source poisoner | Crafted orbital/scientific data | False association، conjunction distortion |
| AI prompt attacker | Direct/indirect prompt injection | Secret extraction، tool proposal manipulation |
| Model/provider compromise | Model behavior/retention drift | Disclosure، targeted misinformation |
| Ransomware operator | Credential/destructive access | Encrypt/delete backups and stores |
| Availability/cost attacker | High-volume valid-looking requests | Resource exhaustion و bill shock |
| Policy/approval abuser | Misissued approval یا stale policy | Unauthorized effect |
| Recovery-path attacker | Backup/restore/admin credential | Rollback، resurrection، persistence |

P11-CON-060 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §17; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Out of assumption:

P11-CON-061 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §17; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- مقاومت در برابر Actor دارای اختیار قانونی مطلق روی همهٔ زیرساخت‌های فیزیکی تضمین نمی‌شود؛ چنین ریسکی با deployment/sovereignty انتخاب‌های Stage 28 کاهش می‌یابد.
- امنیت Endpoint شخصی ناشناخته تضمین نمی‌شود؛ Session و Effect control باید Blast radius را محدود کنند.
- هیچ assumptionی اجازهٔ ساخت Command path یا کاهش `SEC-TZ9` را نمی‌دهد.

### Owner §18. Threat record و مدل Risk

P11-CON-062 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §18; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

هر Threat:

P11-CON-063 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §18; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

~~~json
{
  "threat_id": "THR-25-...",
  "model_version": "tm@digest",
  "asset_ids": ["asset-id"],
  "zones": ["SEC-TZx"],
  "boundary_ids": ["boundary-id"],
  "actor": "adversary-profile-id",
  "preconditions": ["..."],
  "abuse_story": "...",
  "stride": ["T", "E"],
  "linddun": ["D", "Nc"],
  "attack_refs": ["ATT&CK/ATLAS snapshot refs"],
  "privacy_impacts": ["..."],
  "scientific_impacts": ["..."],
  "security_impacts": ["C", "I", "A"],
  "mission_impact": "MI-0..MI-X",
  "likelihood_basis": ["evidence-ref"],
  "inherent_risk": "LOW|MEDIUM|HIGH|CRITICAL|PROHIBITED",
  "controls": ["control-id"],
  "detection": ["detection-id"],
  "tests": ["test-id"],
  "residual_risk": "LOW|MEDIUM|HIGH|CRITICAL|PROHIBITED",
  "owner": "role-id",
  "disposition": "MITIGATE|AVOID|TRANSFER|ACCEPT|PROHIBIT",
  "acceptance_ref": "nullable",
  "expires_at": "RFC3339",
  "status": "OPEN|CONTROLLED|ACCEPTED|PROHIBITED"
}
~~~

P11-CON-064 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §18; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Risk score عددی واحد حقیقت نیست. تصمیم حداقل این محورها را جدا نگه می‌دارد:

P11-CON-065 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §18; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Confidentiality
- Integrity
- Availability
- Privacy/right impact
- Scientific correctness
- Authority/approval integrity
- Tenant blast radius
- Recoverability
- Exploit evidence و reachability
- Regulatory/contract applicability

P11-CON-066 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §18; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

`MI-X`، Spacecraft command، Credential در Model context، Cross-tenant wildcard یا Approval bypass با Risk acceptance قابل‌مجازشدن نیست.

### Owner §19. Security classification و Handling

P11-DEF-007 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §19; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Security classification یک محور مستقل از Privacy، Rights، Scientific status و Retention است:

P11-DEF-008 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §19; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

| Security class | نمونه | Handling baseline |
|---|---|---|
| `SC-PUBLIC` | محتوای مصوب برای انتشار | Integrity، provenance و release approval |
| `SC-INTERNAL` | مستندات و Metadata داخلی | Authenticated access، no public egress |
| `SC-CONFIDENTIAL` | Contract، tenant data، operational details | Need-to-know، encryption، audit |
| `SC-RESTRICTED` | Identity evidence، sensitive security findings | Strong separation، field minimization، no broad export |
| `SC-SECRET-MATERIAL` | Private key، token، recovery secret | فقط Secret/KMS interface؛ هرگز Dataset/Log/AI |
| `SC-CONTROL-PLANE` | Policy، approval، lease، deny rules | Integrity-first، dual control، unsampled audit |

P11-DEF-009 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §19; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

قواعد:

P11-DEF-010 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §19; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- `SC-PUBLIC` به معنی Scientific authority، Open license، no-personal-data یا no-integrity-impact نیست.
- `SC-SECRET-MATERIAL` نباید در Prompt، Tool args، URL، Event، Log، Trace، SBOM، Error، Clipboard workflow یا Support bundle قرار گیرد.
- `SC-CONTROL-PLANE` و `MI-4/5` الزام Integrity و availability بالاتر از محرمانگی صرف دارند.
- Classification downgrade نیازمند Owner مجاز، justification، Policy و Evidence مستقل است.
- Unknown class برای Egress، Provider، Export، AI context یا broad query برابر Deny است.
- Derived data classification از Sourceها با Rule محافظه‌کارانه و Re-identification/aggregation risk محاسبه می‌شود.

### Owner §20. مدل Identity

P11-DEF-011 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §20; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Identityها به این انواع تقسیم می‌شوند:

P11-DEF-012 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §20; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- `HUMAN_USER`
- `HUMAN_PRIVILEGED`
- `WORKLOAD_SERVICE`
- `WORKLOAD_JOB`
- `BUILD_IDENTITY`
- `DEPLOY_IDENTITY`
- `RECOVERY_IDENTITY`
- `TOOL_EXECUTOR`
- `EXTERNAL_PROVIDER`
- `AI_PROPOSER` فقط برای Attribution؛ نه Authority

P11-DEF-013 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §20; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

هر Identity باید:

P11-DEF-014 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §20; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Issuer، Subject، Type، Tenant، Role/attributes، Lifecycle state و Assurance level داشته باشد.
- Unique و non-recycled identifier داشته باشد؛ نام نمایشی شناسه نیست.
- Owner، sponsor، creation evidence، expiry/review و revocation path داشته باشد.
- از Identity نوع دیگر قابل‌تفکیک باشد؛ User token به Workload credential تبدیل ضمنی نمی‌شود.
- Actor chain را حفظ کند؛ On-behalf-of semantics بدون ثبت Human و Service هر دو ممنوع است.
- Privilege را از Group/Role/Policy محاسبه کند، نه Claim دلخواه Client.

P11-DEF-015 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §20; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

چرخه:

P11-DEF-016 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §20; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

`PROPOSED → VERIFIED → ACTIVE → SUSPENDED → REVOKED → CLOSED`

P11-DEF-017 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §20; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

`SUSPENDED/REVOKED/CLOSED` هرگز با Cache قدیمی فعال نمی‌شود. Re-activation نیازمند Evidence و Approval مسیر مربوط است.

### Owner §21. Human identity، Authentication و Account recovery

P11-CON-067 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §21; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Baseline:

P11-CON-068 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §21; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Privileged و high-impact approvalها به Phishing-resistant MFA نیاز دارند.
- Password-only برای `HUMAN_PRIVILEGED` و Effectهای `E5+` کافی نیست.
- Authentication assurance باید با NIST SP 800-63-4-aligned profile و Risk واقعی route نگاشت شود.
- Enrollment، recovery، authenticator binding و factor replacement به اندازهٔ Login محافظت می‌شوند.
- Recovery نباید با Knowledge-based question، support chat بدون proof یا Email-only برای Privileged account انجام شود.
- Session پس از factor/role/tenant/risk change باید Re-evaluate یا Re-authenticate شود.
- Step-up باید Action/Resource/Request digest را به User نشان دهد؛ «Approve» مبهم معتبر نیست.
- User-presence و User-verification برای approvalهای پرخطر ثبت می‌شوند.
- Impossible travel یا IP reputation به‌تنهایی تصمیم قطعی نیست؛ Signal در Risk engine است.
- Biometric raw/template در سامانهٔ اصلی ذخیره نمی‌شود؛ اگر Authenticator محلی استفاده شد، Server فقط attestation/verification result حداقل را می‌بیند.

P11-CON-069 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §21; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Account lifecycle:

P11-CON-070 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §21; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Joiner/mover/leaver با authoritative HR/organization evidence؛ در نبود منبع واقعی، provisioning غیرفعال.
- Dormant privilege و orphaned account به‌صورت دوره‌ای Review/Revoke می‌شوند.
- Role change، tenant departure و contract end باید Session، token و JIT grants را Revoke کند.
- Helpdesk نمی‌تواند MFA یا Tenant boundary را یک‌نفره دور بزند.

### Owner §22. Workload identity و PKI

P11-CON-071 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §22; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

هر Service، Job، Build و Executor هویت جدا دارد:

P11-CON-072 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §22; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Shared service account و static API key عمومی ممنوع است.
- Credential کوتاه‌عمر، audience-bound، service-instance/workload-bound و قابل‌چرخش است.
- Workload attestation باید Runtime، namespace/account، artifact digest و environment را در حد profile اثبات کند.
- Certificate/credential issuance فقط از `SEC-TZ2/8` و با Policy انجام می‌شود.
- Private key export تا حد امکان ممنوع؛ Key operation از signer/KMS interface.
- mTLS برای Service authentication مجاز است، اما Authorization را جایگزین نمی‌کند.
- Routeهایی که Bearer token theft ریسک مهم دارند باید sender-constrained profile مانند mTLS-bound یا DPoP-compatible token داشته باشند.
- انتخاب mTLS/DPoP یا ترکیب آن‌ها route-specific و مبتنی بر Interop/performance test است؛ هیچ‌کدام Blanket نیست.
- SPIFFE-like naming ممکن است فقط پس از namespace، trust-domain، federation و revocation design استفاده شود؛ نام تکنولوژی Authority ایجاد نمی‌کند.
- Certificate expiry، issuer revocation، artifact drift یا workload posture mismatch باید access را متوقف کند.

P11-CON-073 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §22; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Build، Deploy و Runtime identities:

P11-CON-074 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §22; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Build identity Source می‌خواند و Artifact/Provenance می‌نویسد؛ Production secret نمی‌خواند.
- Deploy identity Artifact digest مصوب را Promote می‌کند؛ Source تغییر نمی‌دهد.
- Runtime identity فقط Resourceهای لازم در Environment خودش را می‌بیند.
- Recovery identity فقط در Incident/DR workflow، کوتاه‌عمر و دوکنترلی فعال می‌شود.

### Owner §23. AI، Agent و Tool identity

P11-CON-075 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §23; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Model یک Legal/Human/Workload principal نیست.
- `AI_PROPOSER` فقط Model/provider/prompt/policy/context version را برای Attribution ثبت می‌کند.
- AI حق دریافت User bearer token، refresh token، private key، database credential، KMS unwrap یا signing key ندارد.
- Tool call باید با Actor chain شامل Human/Service initiator و AI proposal origin ثبت شود.
- Tool executor Identity مستقل و Capability-specific دارد.
- Model نمی‌تواند `tenant_id`، `purpose_id`، `effect_level`، Approval requirement یا Credential scope را تعیین کند؛ Server آن‌ها را Canonical می‌کند.
- Model output نمی‌تواند Authentication challenge، Approval receipt، Policy decision، Security finding closure یا deletion verification باشد.
- AI نمی‌تواند نقش Incident commander، DPO، Risk acceptor یا independent verifier را بگیرد.
- Context isolation میان Tenant، User، Purpose، Task و Evaluation اجباری است.
- Provider-side identity/retention/training behavior باید Contract و Technical verification داشته باشد؛ Provider claim کافی نیست.

### Owner §24. Federation، Session و Token security

#### Owner §24. 1 Federation

P11-CON-076 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §24; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Issuer، metadata، signing key، algorithms، audience و tenant mapping نسخه‌قفل می‌شوند.
- Dynamic/floating issuer discovery برای Production ممنوع است مگر allowlisted و digest/evidence-bound.
- Algorithm confusion، key substitution، issuer mix-up و confused-deputy test اجباری است.
- External identity به Internal role مستقیم map نمی‌شود؛ entitlement از Policy/registry داخلی می‌آید.

#### Owner §24. 2 Session

P11-CON-077 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §24; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Session ID تصادفی، rotate-on-auth/step-up و HttpOnly/Secure/SameSite profile دارد.
- CSRF، session fixation، token replay، parallel session و logout/revocation tests اجباری‌اند.
- Privileged session از normal session جدا و کوتاه‌تر است.
- Risk/context change می‌تواند Session را محدود یا terminate کند، اما Denial explanation نباید Security secret افشا کند.

#### Owner §24. 3 Token

P11-CON-078 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §24; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Token باید:

P11-CON-079 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §24; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Audience، Resource، Action، Tenant، Purpose، Effect ceiling، TTL، issuer و subject دقیق داشته باشد.
- کوتاه‌عمر و sender-constrained باشد.
- `jti`/nonce و replay defense داشته باشد.
- Scope wildcard برای Tenant، destructive action یا admin ممنوع داشته باشد.
- در Query string، Prompt، Event payload، Log یا Tool result قرار نگیرد.
- با Token exchange فقط از Broker مجاز و با Downscope صادر شود.
- Refresh token در Tool sandbox، browser-like runtime یا AI plane نداشته باشد.

P11-CON-080 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §24; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Token introspection/cache باید Revocation freshness معلوم داشته باشد؛ در Route پرخطر، unavailable/unknown برابر Deny است.

### Owner §25. Authorization و Policy-as-code

P11-CON-081 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §25; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

تصمیم Authorization تابع زیر است:

P11-CON-082 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §25; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

`Allow = Identity ∩ Tenant ∩ Purpose ∩ Resource ∩ Action ∩ Classification ∩ Region ∩ MissionImpact ∩ Effect ∩ PolicyVersion ∩ Context ∩ Time ∩ Approval ∩ Lease`

P11-CON-083 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §25; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

همهٔ اجزا باید معتبر باشند. Policy model:

P11-CON-084 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §25; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Default deny
- Explicit allow
- Deny overrides
- No implicit inheritance across Tenant/Purpose
- Server-computed resource/action/effect
- Exact policy snapshot و digest
- Deterministic evaluation
- Bounded evaluation time/resource
- Signed publication و rollback-safe versioning
- Decision explanation مناسب Audit، بدون افشای sensitive rule internals به Caller

P11-CON-085 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §25; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Policy changes:

P11-CON-086 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §25; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Source review، schema/test، semantic diff، simulation against fixtures، conflict detection و approval می‌خواهند.
- Policy compiler/generator output untrusted است تا Test و Review شود.
- Emergency deny ممکن است سریع منتشر شود؛ Allow/restore نیازمند full gate است.
- Policy rollback به نسخهٔ دارای Vulnerability یا expired applicability ممنوع است.
- Cache key باید تمام Contextهای اثرگذار را شامل شود؛ missing dimension موجب Cache bypass/deny.

### Owner §26. Approval، Step-up و Break-glass

P11-CON-087 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §26; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Approval record:

P11-CON-088 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §26; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

~~~json
{
  "approval_id": "apr_...",
  "request_digest": "sha256:...",
  "actor_id": "requester",
  "approver_ids": ["independent-approver"],
  "tenant_id": "tenant",
  "purpose_id": "purpose",
  "resource_manifest_digest": "sha256:...",
  "action": "typed-action",
  "effect_level": "E0..E8",
  "constraints": {"count_max": 0, "region": [], "time_window": "..."},
  "step_up_evidence": "ref",
  "policy_snapshot": "policy@sha256",
  "issued_at": "RFC3339",
  "expires_at": "RFC3339",
  "status": "APPROVED|REVOKED|EXPIRED|CONSUMED",
  "signatures": ["..."]
}
~~~

P11-CON-089 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §26; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

قواعد:

P11-CON-090 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §26; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Approval متن آزاد به‌تنهایی نیست؛ Exact request/manifest digest دارد.
- Scope expansion، resource addition، action change یا policy change Approval را باطل می‌کند.
- Approval reuse فقط برای Batch ثابت، bounded، کوتاه‌عمر و مصوب؛ Standing broad delete/install/export approval ممنوع است.
- Approver باید Effect، Scope، Data class، recipient، irreversibility و uncertainty را ببیند.
- AI-generated summary می‌تواند کمک کند، اما Canonical diff/manifest باید نمایش داده شود.
- Revocation پیش از Lease issuance و در Effectهای destructive پیش از commit دوباره بررسی می‌شود.

P11-CON-091 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §26; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Break-glass:

P11-CON-092 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §26; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- فقط برای Availability/containment تعریف می‌شود، نه دورزدن Privacy، Tenant یا Command boundary.
- JIT، time-bound، reason-coded، two-person یا post-incident independent review بر اساس Effect.
- Session/credential جدا، Action allowlist و unsampled audit دارد.
- نمی‌تواند Data export، Declassification، Key destruction، permanent delete یا `SEC-TZ9` را مجاز کند.
- پایان Incident همهٔ grants را Revoke و Evidence review را Trigger می‌کند.

### Owner §27. Service-to-service، Network و Segmentation

P11-CON-093 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §27; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Network location هیچ Trust خودکاری ایجاد نمی‌کند.
- Default-deny ingress/egress و explicit service/resource graph لازم است.
- هر Flow Owner، Purpose، protocol، port، identity، data class و expiry/review دارد.
- East-west traffic نیز authenticate، authorize و encrypt می‌شود.
- DNS response، service discovery و redirect قابل‌اعتماد فرض نمی‌شوند.
- Metadata service، loopback، link-local، private control endpoint و internal admin endpoint از Tool/Web egress مسدودند.
- Admin plane، Data plane، Build plane و Recovery plane از نظر route/identity/control جدا هستند.
- Firewall/security-group rule wildcard یا permanent debug route نیازمند Hard deny یا time-bound exception است.
- Network policy drift و unexpected path به Alert/qualification failure تبدیل می‌شود.
- `SEC-TZ9` باید با automated negative reachability test از همهٔ Zoneها و CI artifactها بررسی شود.

P11-CON-094 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §27; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Service mesh یا proxy در صورت استفاده:

P11-CON-095 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §27; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Policy source-of-truth نیست؛ Enforcement point است.
- Sidecar/agent compromise در Threat model می‌آید.
- mTLS success برابر Application authorization نیست.
- Header identity از Client قابل‌پذیرش نیست مگر از trusted, authenticated hop با signature/binding.

### Owner §28. Tenant، Purpose و Administrative isolation

P11-CON-096 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §28; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Tenant ID از authenticated context و canonical resource گرفته می‌شود؛ Client body authority ندارد.
- Cross-tenant query/join/export به Capability جدا، Policy صریح، Approval و evidence نیاز دارد؛ پیش‌فرض ممنوع.
- Database RLS دفاع در عمق است، نه تنها مرز.
- Runtime owner، superuser یا `BYPASSRLS` برای application path ممنوع است.
- Cache، Queue، Object prefix، Index، Vector collection، log view و backup manifest نیز tenant-aware هستند.
- Purpose باید در Actor chain و Data access ثبت شود؛ یک User با Access مجاز نمی‌تواند Data را برای Purpose دیگر استفاده کند.
- Support access JIT، ticket-bound، field-minimized، visible/audited و time-limited است.
- Admin UI و bulk interfaces بیشترین محدودیت را دارند، نه کمترین.
- Tenant deletion/closure با credential/session/recovery/backup/deletion graph هماهنگ می‌شود.
- Enumeration resistance نباید Owner مجاز را از مشاهدهٔ Error قابل‌اقدام محروم کند؛ Error detail بر اساس Role تفکیک می‌شود.

### Owner §29. Secret management

P11-CON-097 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §29; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Secret lifecycle:

P11-CON-098 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §29; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

`GENERATED → ACTIVE → ROTATING → RETIRED → REVOKED → DESTROYED`

P11-CON-099 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §29; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Baseline:

P11-CON-100 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §29; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Secret در Repository، Image، IaC state plaintext، Prompt، Log، Event، Ticket یا Chat ممنوع است.
- Secret فقط از Broker/Secret interface و برای Workload authenticated، Purpose/Resource مشخص، TTL کوتاه تحویل می‌شود.
- Prefer non-exportable operation؛ در صورت تحویل، memory-only، no disk، no child-process inheritance و redaction.
- Static long-lived secret Exception است و نیازمند Owner، rotation، compensating controls و expiry.
- Secret scanner pre-commit، build، artifact و repository history را پوشش می‌دهد؛ Scan claim جای rotation/revocation را نمی‌گیرد.
- Suspected exposure فوراً `COMPROMISED_PENDING` می‌سازد و Rotation/Revocation workflow را آغاز می‌کند.
- Rotation باید overlap امن، consumer inventory، rollback و stale-secret detection داشته باشد.
- Secret name/reference هم ممکن است sensitive باشد و در telemetry حداقل‌سازی می‌شود.
- AI و Tool هرگز Secret value نمی‌بینند؛ در صورت نیاز فقط opaque capability/secret handle به Broker server-side داده می‌شود.

### Owner §30. Key hierarchy و Envelope encryption

P11-CON-101 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §30; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

حداقل تفکیک:

P11-CON-102 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §30; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Root of trust/HSM-backed root
- Key-encryption keys بر اساس Environment/Region/Tenant/Purpose
- Data-encryption keys برای Dataset/Object/Partition profile
- Signing keys برای Policy، Artifact، Event و Approval؛ از Encryption keys جدا
- Backup/Archive keys از Runtime keys جدا
- Recovery keys با dual control و offline/isolated profile
- Pseudonymization/tokenization keys از encryption و signing جدا

P11-CON-103 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §30; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

قواعد:

P11-CON-104 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §30; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Key ID و version ثبت می‌شود؛ Key material ثبت نمی‌شود.
- Envelope header شامل algorithm suite، key ref/version، nonce/IV، associated-data profile و ciphertext integrity است.
- Associated data باید Tenant، Purpose، Resource ID، Schema/Profile و context لازم را bind کند.
- Key scope باید با Copy/Derived/Backup graph قابل‌اثبات باشد.
- Rotation، rewrap و re-encryption رویدادهای جدا با Evidence هستند.
- Key deletion قبل از اثبات Copy/key scope، backup residual، legal hold و approval ممنوع است.
- Loss of key availability یک Availability incident است؛ Recovery نباید bypass authorization ایجاد کند.
- Multi-tenant shared key فقط با Risk profile مصوب؛ پیش‌فرض per-tenant/purpose separation برای کلاس‌های حساس.
- KMS/HSM administrator نمی‌تواند plaintext data را بخواند و Data admin نمی‌تواند Key policy را تغییر دهد.

### Owner §31. Cryptographic profile، Agility و PQC

P11-CON-105 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §31; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

هر Route/Artifact یک `CryptoProfile` نسخه‌دار دارد:

P11-CON-106 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §31; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Approved algorithms/modes
- Minimum key/security strength
- TLS/protocol versions و cipher constraints
- Certificate/signature profile
- Randomness requirements
- Nonce/IV construction
- Key use، cryptoperiod و rotation trigger
- Deprecation date و migration plan
- Hardware/software boundary
- Interoperability/evidence fixtures

P11-CON-107 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §31; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

قواعد:

P11-CON-108 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §31; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Custom cryptography ممنوع است.
- Algorithm name بدون Parameter، Mode، Key usage و Library/runtime version کافی نیست.
- Weak/legacy algorithm فقط برای bounded read/migration path و با no-new-write policy ممکن است.
- Crypto downgrade و fallback Silent ممنوع‌اند.
- FIPS 203/204/205 استانداردهای نهایی‌اند، اما Adoption خودکار نیست؛ implementation maturity، interoperability، side-channel، key/ciphertext/signature size و protocol fit باید آزمون شوند.
- Hybrid profile فقط با مشخصات دقیق، downgrade resistance و failure semantics مجاز است.
- `NIST IR 8547` تا نهایی‌شدن فقط Research input است.
- Cryptographic inventory باید محل Algorithm، key type، dependency، protocol، data longevity و migration owner را نشان دهد.
- Store-now-decrypt-later risk برای دادهٔ بلندعمر در Stage 27/28 ارزیابی می‌شود.

### Owner §32. Data، Storage، Backup و Restore security

P11-CON-109 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §32; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Encryption in transit، at rest، backup، archive و export برای کلاس لازم اعمال می‌شود.
- Encryption جای Tenant/Purpose/Access control نیست.
- Canonical، Projection، Cache، Search، Graph و Vector ACL مستقل و least-privilege دارند.
- Object/artifact write با content digest، conditional write و immutable revision انجام می‌شود.
- Backup identity از Runtime جدا و write/delete privilege تفکیک‌شده دارد.
- Backup manifest signed، encrypted، completeness-checked و location/key/profile-bound است.
- Restore فقط در isolated environment آغاز می‌شود.
- Restore باید malware/integrity، manifest، key، schema، scientific provenance، tenant، policy، tombstone، erasure و consent-revocation را اعتبارسنجی کند.
- Restore قبل از Serving، Projectionها را از Source معتبر rebuild و suppression journals را اعمال می‌کند.
- Restore حق replay کردن external tool effect، email/webhook/export یا destructive action را ندارد.
- Production promotion پس از Restore به fencing، independent verification و Approval نیاز دارد.
- Ransomware resistance شامل separate credential، retention lock profile، offline/logical isolation و restore drills است؛ «immutable backup» Vendor claim کافی نیست.
- Backup deletion/expiry با Stage 24 semantics و NIST SP 800-88 Rev.2-aligned media/provider evidence هماهنگ است.

### Owner §33. Application و API security

P11-CON-110 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §33; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Baseline حداقل با ASVS 5.0.0 و API Security Top 10:2023 traceability دارد:

P11-CON-111 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §33; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Strict schema، type، length، range، enum، format و semantic validation
- Canonicalization قبل از signature/digest/policy
- Object-level و function-level authorization
- Mass-assignment protection و server-owned fields
- Injection protection برای SQL/NoSQL/template/path/header/command
- SSRF protections، redirect/DNS revalidation و egress allowlist
- CSRF/CORS/cookie/session profiles
- Pagination، filtering، export و bulk-action resource budgets
- Idempotency key scope و replay semantics
- Error redaction با machine-readable failure code
- Rate/abuse control per subject/tenant/resource/cost
- Versioned OpenAPI contract و compatibility/security diff
- Generated client/server code به‌عنوان untrusted change؛ review/test لازم
- No undocumented admin/debug endpoint
- File upload quarantine، type/content validation، malware/safe extraction و size limits
- Response header/cache controls متناسب با Data class

P11-CON-112 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §33; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

API success به معنی Effect success نیست؛ Receipt باید final/partial/unknown semantics داشته باشد.

### Owner §34. Event، Queue و Webhook security

P11-CON-113 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §34; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

هر Event:

P11-CON-114 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §34; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Schema ID/version و canonical serialization
- Event ID، causation/correlation ID
- Producer workload identity
- Tenant، Purpose و classification
- Occurred/recorded time با clock-quality
- Policy/contract digest
- Payload digest و signature/integrity
- Expiry/retention و replay policy
- Effect classification

P11-CON-115 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §34; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

قواعد:

P11-CON-116 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §34; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Broker ACL به‌تنهایی Consumer authorization نیست.
- Consumer باید schema، producer، tenant، purpose، replay و freshness را اعتبارسنجی کند.
- Topic/queue wildcard برای cross-tenant یا control-plane event ممنوع است.
- Event redelivery فقط برای Idempotent/non-effect یا reconciled effect.
- Dead-letter queue Governed، encrypted، access-controlled و دارای retention است.
- Webhook destination allowlisted، DNS/redirect revalidated و sender/receiver authenticated است.
- Inbound webhook signature، timestamp، nonce و replay window دارد.
- Outbound webhook secret در payload/log نیست.
- Event schema هیچ Spacecraft command verb/payload ندارد؛ encoded/opaque payload نیز Content policy و type allowlist می‌خواهد.

### Owner §35. Egress، Live web و External retrieval

P11-CON-117 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §35; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Live web یک Capability محدود است، نه General browser:

P11-CON-118 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §35; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- وضعیت پیش‌فرض `DISABLED_BY_DEFAULT`.
- نیازمند `DATA_READ_EXTERNAL` و `NETWORK_EGRESS` جدا.
- Scheme، exact host/domain، port، path class، method، redirect و response type allowlist.
- فقط Read-only؛ form submit، upload، account session، arbitrary cookie و active browser profile ممنوع.
- Private/loopback/link-local/multicast/metadata/admin ranges و DNS rebinding مسدود.
- هر Redirect و DNS resolution دوباره validate می‌شود.
- Request headerها حداقل و بدون internal credential/identifier غیرضروری‌اند.
- Response size، decompression ratio، resource count، duration و cost محدود است.
- Archive/compressed file، active content، script، macro و executable quarantine می‌شوند.
- Safe extraction، malware scanning و text/data isolation اجباری است.
- Source URI، retrieval time، digest، terms/license profile و provenance ثبت می‌شود.
- Retrieved instructions authority ندارند؛ `UNTRUSTED_DATA_ONLY`.
- Cache/retention/redistribution و Personal-data handling per-source از Stage 24 می‌آید.
- Unknown rights، region، recipient یا transfer route برابر Deny.

P11-CON-119 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §35; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Crawler، scraping، General browser automation یا authenticated website interaction Capability جدا و در Baseline غیرفعال است.

### Owner §36. Tool sandbox و Arbitrary code execution

P11-CON-120 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §36; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Tool sandbox:

P11-CON-121 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §36; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Ephemeral، rootless و one-task/one-lease
- Read-only base image و minimal scoped scratch
- No host filesystem، home، SSH agent، cloud metadata، browser profile، runtime socket یا device access
- No privileged mode، namespace escape، kernel capability یا mount injection
- Default-deny network و explicit egress profile
- No ambient secret؛ opaque brokered handle only
- CPU، memory، process، file، time، output، network و cost quotas
- Syscall/process/file policy متناسب با Runtime
- Pinned image/runtime digest، signed provenance و SBOM
- Output quarantine، schema/content validation و DATA_ONLY treatment
- Secure cleanup و no cross-task reuse

P11-CON-122 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §36; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Arbitrary code execution:

P11-CON-123 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §36; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- در Baseline `DISABLED`.
- فعال‌سازی آینده Capability جدا، APR-3 یا بالاتر، fixed runtime digest و Red-team مستقل می‌خواهد.
- Shell، package install، network، secret، host mount، dynamic loader path و persistent state پیش‌فرض ممنوع‌اند.
- Code-generated output هرگز خودکار به Build/Deploy/Effect نمی‌رود.
- Sandbox escape، dependency confusion، zip slip، fork bomb، output flooding و covert exfiltration test اجباری است.

### Owner §37. Software supply-chain architecture

P11-CON-124 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §37; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

زنجیره:

P11-CON-125 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §37; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

`Source identity → reviewed change → hermetic/controlled build → signed provenance → artifact digest → SBOM/VEX → scan/test → admission → staged promotion → runtime attestation`

P11-CON-126 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §37; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

قواعد:

P11-CON-127 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §37; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Source، Build، Registry، Deploy و Runtime identities جدا هستند.
- Protected branch، mandatory review و two-party review برای control/security code لازم است.
- Tag یا mutable label identity Artifact نیست؛ Digest مرجع است.
- Build inputها، dependencies، toolchain و environment نسخه‌قفل می‌شوند.
- Build نباید Production credential یا Network unrestricted داشته باشد.
- Provenance باید Builder identity، source digest، parameters، dependencies و output digest را bind کند.
- Registry mutation/tag replacement detectable و denied است.
- Admission بدون verified provenance/SBOM/security status ممنوع است.
- Artifact پس از Test تغییر نمی‌کند؛ هر rebuild Digest/qualification جدید می‌خواهد.
- Runtime باید Artifact digest مصوب و attestation لازم را اثبات کند.
- Emergency patch full traceability را حذف نمی‌کند؛ Gate زمان‌فشرده ولی ثبت‌شده است.

P11-CON-128 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §37; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

SLSA target:

P11-CON-129 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §37; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Control-plane، identity، policy، lease، KMS/broker و destructive executor: حداقل Build L3 و Source L4 target
- سایر Production services: حداقل Build L2، با مسیر ارتقا به L3
- Third-party binary بدون provenance کافی: Quarantine/Risk exception محدود یا رد

P11-CON-130 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §37; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Target سطح SLSA گواهی خودکار نیست؛ Evidence برای هر Artifact لازم است.

### Owner §38. SBOM، VEX و Component intelligence

P11-CON-131 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §38; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

تصمیم Interchange:

P11-CON-132 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §38; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- مدل داخلی **format-neutral component/dependency/evidence graph** است.
- `CycloneDX 1.7` پروفایل اصلی Security/VEX/Service/ML-BOM interchange است.
- `SPDX 3.0.1` برای License، provenance، ecosystem interoperability و security relationship import/export پشتیبانی می‌شود.
- Conversion باید loss report داشته باشد؛ Round-trip کامل فرض نمی‌شود.

P11-CON-133 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §38; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

هر Component record:

P11-CON-134 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §38; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Stable component identity، version، supplier، hashes و package coordinates
- Direct/transitive/development/runtime relationship
- Source/build/provenance refs
- License/rights refs
- Deployment/reachability inventory
- Vulnerability/KEV/CVSS/EPSS/VEX status
- Fix/mitigation/exception و expiry

P11-CON-135 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §38; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

VEX:

P11-CON-136 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §38; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- `not_affected` فقط با product/version/config/reachability evidence.
- Self-authored VEX از همان supplier به‌تنهایی برای Critical/KEV کافی نیست.
- Environment drift یا new exploit evidence VEX را invalidate/review می‌کند.
- Unknown Component identity یا unmatched version برای Production high-impact برابر fail-closed.

### Owner §39. Vulnerability management و Promotion gate

P11-CON-137 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §39; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Risk gate ترکیبی است:

P11-CON-138 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §39; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

`Decision = KEV ∪ ExploitEvidence ∪ CVSS4 ∪ EPSS4 ∪ Reachability ∪ Exposure ∪ Privilege ∪ Data/MissionImpact ∪ VEX ∪ FixAvailability ∪ ControlStrength`

P11-CON-139 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §39; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

قواعد:

P11-CON-140 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §39; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- CVSS score تنها Gate نیست.
- EPSS احتمال کوتاه‌مدت است و Impact یا absence of risk را اثبات نمی‌کند.
- KEV یا exploitation observed بالاترین اولویت بررسی/containment را دارد.
- `not affected` بدون VEX/Evidence معتبر پذیرفته نیست.
- Scanner result باید component identity/version/environment را match کند.
- False positive closure دارای evidence، reviewer و expiry است.
- Unknown severity/reachability در Internet-exposed یا `MI-4/5` برابر Quarantine/Deny.
- Exception زمان‌دار، ownerدار، compensating controlدار و re-evaluated است.
- Fix می‌تواند Regression بسازد؛ patch، configuration mitigation و feature disable همگی Test می‌شوند.
- Detection-only جای Fix برای risk بحرانیِ reachable را دائماً نمی‌گیرد.
- Numeric remediation SLOها در Stage مقرر با Organization/operational facts نهایی می‌شوند؛ تا آن زمان hard safety gates Fail-closed هستند.

P11-CON-141 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §39; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Promotion حداقل:

P11-CON-142 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §39; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Provenance verified
- SBOM complete-enough profile
- No unresolved prohibited/critical condition
- KEV/exploit review
- VEX/reachability evidence
- Security/unit/integration/negative tests
- Policy/Schema compatibility
- Rollback/containment proof

### Owner §40. Secure SDLC، Source و Build controls

P11-CON-143 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §40; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Security requirements و Abuse cases پیش از implementation به tests تبدیل می‌شوند.
- Threat model change trigger جزو Definition of Done است.
- Branch protection، signed/verified identity، review و merge controls لازم‌اند.
- Security-sensitive code paths به Reviewer تخصصی/ownership rule نیاز دارند.
- Secret، dependency، SAST، IaC، container، license و provenance scans layered هستند.
- Generated code و AI-authored code همان Review/Test/ownership را دارند؛ AI attribution مجوز نیست.
- Test fixture نباید Production secret یا unminimized Personal data داشته باشد.
- Fuzzing برای parsers، canonicalization، schemas، token/event/file handling و boundary validators انجام می‌شود.
- Dependency update با semantic/security diff و regression است؛ auto-merge برای control-plane/high-impact ممنوع.
- Reproducible یا independently verifiable build برای Crown-jewel artifacts هدف است.
- Release note باید security-relevant change، migration، rollback و known residual risk را ثبت کند.
- Source deletion/history rewrite برای پنهان‌کردن secret incident ممنوع؛ secret revoke/rotate و evidence preservation لازم است.
- Unsupported/EOL runtime یا dependency Production admission را مسدود می‌کند مگر bounded exception.

### Owner §41. Configuration، IaC و Runtime hardening

P11-CON-144 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §41; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Configuration schema versioned، typed و server-validated است.
- Secure default در Code/Template اعمال می‌شود؛ Documentation-only کافی نیست.
- Environment-specific override ثبت، diff و approved است.
- IaC plan قبل از Apply با Policy، security diff و destructive effect classification بررسی می‌شود.
- Drift detection read-only می‌تواند خودکار باشد؛ remediation effect مطابق Stage 19 approval می‌خواهد.
- Debug mode، test endpoint، verbose secret logging و permissive CORS در Production Hard deny هستند.
- Runtime image minimal، read-only و non-root است.
- Unneeded package، shell، compiler، service و port حذف/غیرفعال می‌شوند.
- Kernel/runtime/container/orchestrator profile نسخه‌قفل و hardening-tested است.
- Resource limit، health/readiness، graceful shutdown و circuit breaker برای جلوگیری از cascade لازم‌اند.
- Clock source، DNS، certificate trust store و entropy health کنترل/monitor می‌شوند.
- Administrative change با separate identity، JIT privilege و audit انجام می‌شود.
- Configuration backup و recovery به‌اندازهٔ Data backup محافظت می‌شود؛ Rollback به insecure config ممنوع است.

### Owner §42. AI/ML security

P11-CON-145 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §42; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

AI security بر مبنای Stage 21 و threat inputs جاری OWASP LLM/LLMSVS و ATLAS است:

P11-CON-146 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §42; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Model، Prompt، Adapter، Provider، Corpus و Evaluation هر کدام version/digest و qualification جدا دارند.
- System/developer policy از User، Retrieved content و Tool output جدا و دارای precedence قطعی است.
- Model output untrusted است و قبل از Machine use به schema، authority، citation، numeric و policy validation نیاز دارد.
- Model نمی‌تواند Effect، Approval، Identity، Scope، Credential یا Security classification صادر کند.
- Provider/model fallback Silent ممنوع؛ تغییر Model یا Region requalification می‌خواهد.
- Training، Fine-tuning، RAG، evaluation و production inference datasets جدا و governed هستند.
- Prompt/template changes مانند Code change review، tests و rollback دارند.
- Model theft، inversion، membership inference، sensitive disclosure، denial/cost و targeted misinformation در Threat model می‌آیند.
- Safety filter نتیجهٔ Scientific یا Security authority نیست و Failures آن با deterministic controls پوشش داده می‌شود.
- Model/provider telemetry نمی‌تواند Raw sensitive context یا Secret را دریافت کند.
- AI-generated security finding یا code fix تا deterministic reproduction/review «پیشنهاد» باقی می‌ماند.
- Autonomous recursive agents، self-install، self-permission و self-promotion در Baseline ممنوع‌اند.

### Owner §43. RAG، Vector، Memory و Knowledge security

P11-CON-147 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §43; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Source artifact immutable و authoritative status آن جدا از Index است.
- Index، Embedding، Vector، Graph و Cache مشتق‌شده، versioned، tenant/purpose-scoped و قابل‌بازسازی‌اند.
- Corpus admission به Source authority، rights، classification، malware/content safety و prompt-injection scan نیاز دارد.
- Retrieval ranking Authority ایجاد نمی‌کند.
- Claim-level evidence map و citation validation اجباری است؛ Unsupported claim باید حذف یا با abstention پاسخ داده شود.
- Document chunk مرز Security/Privacy را حذف نمی‌کند؛ ACL و provenance در Chunk/Embedding حفظ می‌شوند.
- Cross-tenant nearest-neighbor، global embedding cache و shared memory بدون isolation اثبات‌شده ممنوع‌اند.
- Embedding به‌عنوان potential derived personal/sensitive data Governed می‌شود.
- RAG output، filenames، metadata و links قبل از Context assembly کمینه و Sanitized می‌شوند.
- Poisoning، corpus rollback، stale index، deleted-data resurrection و citation swapping test می‌شوند.
- Memory write ابتدا `PROPOSED`، typed، source-linked، verified، purpose-bound و TTLدار است.
- Memory هرگز Authorization، identity proof، scientific truth یا approval source نیست.
- Revocation/deletion به Corpus، chunks، embeddings، cache و model-impact graph منتشر می‌شود.

### Owner §44. Prompt، Tool و Indirect-injection isolation

P11-CON-148 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §44; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Instruction precedence:

P11-CON-149 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §44; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

1. System/constitutional policy
2. Versioned application/developer policy
3. Authenticated user intent در Scope مجاز
4. Tool schema و typed control metadata
5. Retrieved/Tool/External content فقط `DATA_ONLY`

P11-CON-150 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §44; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

کنترل‌ها:

P11-CON-151 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §44; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Content نمی‌تواند خود را System/Policy/Approval/Tool instruction معرفی کند.
- Context assembler channel/type/authority را ساختاری نگه می‌دارد؛ concatenation مبهم ممنوع است.
- Model-proposed Tool call از Canonical server-side parser و policy pipeline عبور می‌کند.
- Tool description/annotation trust یا Effect level ایجاد نمی‌کند.
- URL، file، attachment یا output خودکار fetch/open/execute نمی‌شود.
- Active content، hidden text، encoded instruction، metadata instruction و multilingual injection در Red-team هستند.
- Exfiltration via URL parameters، image alt/OCR، markdown link، tool argument و error channel مسدود/آزموده می‌شود.
- High-risk action نیازمند نمایش Canonical manifest به Human است، نه summary مدل.
- Model refusal یا compliance به‌تنهایی Control نیست؛ Runtime همیشه enforce می‌کند.
- Suspicious content می‌تواند Retrieval/Tool proposal را Quarantine کند، اما false-positive resolution Authority boundary را دور نمی‌زند.

### Owner §45. Privacy architecture

P11-CON-152 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §45; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Privacy controls با LINDDUN و Stage 24 governance ترکیب می‌شوند:

P11-CON-153 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §45; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Purpose، legal/applicability basis، controller/processor role، recipient و retention پیش از Processing مشخص‌اند.
- Data minimization در Collection، Field، Precision، Frequency، History، Query، Log، Trace و Support view اعمال می‌شود.
- Privacy default: no public visibility، no provider training، no secondary use، no cross-tenant، no indefinite retention.
- Pseudonymization با access/key separation انجام می‌شود؛ pseudonymized data همچنان Personal data است.
- Linkability میان Datasetها، Tenantها و Purposes یک Threat مستقل است.
- User notice/choice، consent/withdrawal و access visibility نسخه‌دار و قابل‌اثبات‌اند.
- Privacy control نباید Scientific fidelity لازم را خاموشانه حذف کند؛ conflict با Data minimization profile مستند حل می‌شود.
- DPIA/TIA triggerها Machine-readable هستند، اما تصمیم حقوقی توسط نقش مجاز انجام می‌شود.
- Security detection نمی‌تواند بهانهٔ collection نامحدود یا indefinite retention باشد.
- Privacy breach triage از Security incident جدا ولی متصل است.
- Re-identification عمدی فقط برای Purpose/Authority مجاز، environment محدود و logging دقیق ممکن است؛ baseline غیرمجاز.

### Owner §46. DSAR identity verification و Rights workflow

P11-CON-154 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §46; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

اصل:

P11-CON-155 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §46; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

> Identity proof باید متناسب با ریسک افشای داده یا تغییر باشد؛ نه آن‌قدر ضعیف که دادهٔ شخص دیگری افشا شود و نه آن‌قدر افراطی که دادهٔ اضافی جمع‌آوری یا حق فرد عملاً مسدود شود.

P11-CON-156 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §46; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Workflow:

P11-CON-157 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §46; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

1. Request دریافت و case ID ساخته می‌شود.
2. Applicable role/jurisdiction/right بررسی می‌شود.
3. Requested scope و identity uncertainty تعیین می‌شود.
4. Existing authenticated channel ترجیح داده می‌شود.
5. Step-up/proof متناسب با Data sensitivity و requested effect اعمال می‌شود.
6. Proof data حداقل، جدا، restricted و retention-bound نگهداری می‌شود.
7. Matching با deterministic rules و human review در ambiguity؛ AI فقط assist.
8. Response/export/rectification/deletion از approval و effect pipeline عبور می‌کند.
9. Third-party/representative authority جداگانه verify می‌شود.
10. Receipt حداقل و قابل‌اثبات ثبت می‌شود.

P11-CON-158 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §46; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

قواعد:

P11-CON-159 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §46; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Collecting full ID document پیش‌فرض نیست.
- Support agent نمی‌تواند Tenant/identity mismatch را Override کند.
- Failure to verify باید appeal/alternative channel داشته باشد.
- Scientific record rectification با Supersession انجام می‌شود، نه history overwrite.
- DSAR export نیازمند recipient-bound secure delivery و expiry است.
- AI verification یا face matching به‌تنهایی proof معتبر نیست.

### Owner §47. De-identification، Re-identification و Synthetic data

P11-CON-160 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §47; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

هر `DeidentificationProfile` شامل:

P11-CON-161 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §47; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Dataset/use context
- Direct/quasi identifiers
- Linkage sources و attacker model
- Population، sparsity و temporal/geospatial uniqueness
- Technique/parameters
- Utility/scientific fidelity constraints
- Attack tests و residual risk
- Access/contract/environment controls
- Reviewer، expiry و re-evaluation triggers

P11-CON-162 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §47; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

قواعد:

P11-CON-163 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §47; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Hashing یا encryption برابر anonymization نیست.
- Pseudonymization کلید/lookup separation و rotation دارد.
- K-anonymity یا یک metric منفرد proof کافی نیست.
- Re-identification risk Context-specific و با auxiliary data تغییرپذیر است.
- Synthetic data به‌طور خودکار anonymous نیست؛ memorization، outlier leakage، membership/attribute inference آزمون می‌شود.
- Release عمومی سخت‌ترین Attacker model و independent review را می‌خواهد.
- Numeric thresholds فقط پس از Stage 27 benchmark/data facts نهایی می‌شوند.
- Unknown risk برای Public/External release برابر Deny.
- Re-identification testing فقط در isolated, authorized environment و بدون انتشار reconstructed identities انجام می‌شود.

### Owner §48. Privacy-safe Telemetry، Logs و Diagnostics

P11-CON-164 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §48; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Telemetry schema هر Field را با purpose، class، retention و access profile تعریف می‌کند.
- Token، Secret، raw credential، full prompt/context، raw personal identifier و sensitive payload پیش‌فرض ممنوع‌اند.
- Stable global user identifiers در Metrics/Traces ممنوع؛ scoped opaque identifiers ترجیح دارند.
- URL/query/header/body logging allowlist-based است.
- Error stack و support bundle قبل از خروج redaction/scan می‌شوند.
- Security/authority events unsampled هستند، اما payload-minimal باقی می‌مانند.
- Product analytics و Security telemetry purpose/retention جدا دارند.
- Debug logging زمان‌دار، approved، narrowly scoped و auto-expiring است.
- Trace propagation Tenant/Purpose را با opaque authenticated context حفظ می‌کند، نه raw sensitive fields.
- Access به Logs/Search views least-privilege و audited است.
- Telemetry export به Provider از transfer/classification/contract gates عبور می‌کند.
- حذف/withdrawal اثر خود را طبق Stage 24 بر telemetry applicable منتشر می‌کند؛ audit proof حداقل حفظ می‌شود.

### Owner §49. Audit، Tamper evidence، WORM و Trusted time

P11-CON-165 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §49; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Audit record حداقل:

P11-CON-166 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §49; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Event ID و sequence/link
- Actor chain و authenticated identities
- Tenant/Purpose
- Action/Resource canonical identifiers
- Policy/Approval/Lease refs و digests
- Effect/result/failure code
- Source/destination zone
- Occurred/recorded time و clock quality
- Evidence/receipt digests
- Privacy-minimal reason/metadata

P11-CON-167 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §49; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Integrity:

P11-CON-168 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §49; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Append-only interface، signed/hash-linked batches و independently stored checkpoints.
- WORM/retention-lock implementation باید Capability، bypass/admin path، clock و deletion conflict را اثبات کند؛ Marketing label کافی نیست.
- Audit writer توان Read all یا delete ندارد.
- Audit administrator توان forge event ندارد.
- Trusted time profile، drift/rollback detection و multiple-source evidence برای high-impact events لازم است.
- Sequence gap، duplicate، late event و partition باید detectable باشند.
- Exported evidence manifest signed، encrypted و recipient-bound است.
- Raw content/Secret برای اثبات Event ذخیره نمی‌شود؛ digest و minimal fact کافی است مگر Rule applicable دیگری لازم باشد.
- Audit retention از erased content جداست و Blanket forever نیست.

### Owner §50. Detection engineering و Monitoring

P11-CON-169 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §50; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Detection catalog برای هر Rule:

P11-CON-170 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §50; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Threat/ATT&CK/ATLAS/LINDDUN reference
- Data sources و field contracts
- Preconditions و coverage limits
- Logic/version/digest
- Severity و confidence dimensions
- Tenant/data/privacy impact
- Expected false-positive/negative risks
- Automated action ceiling
- Runbook، owner و tests
- Expiry/review و drift monitor

P11-CON-171 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §50; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Minimum detection families:

P11-CON-172 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §50; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Authentication anomalies و recovery abuse
- Privilege/role/policy/approval changes
- Token replay، issuer/audience mismatch و stale credential
- Cross-tenant/purpose attempts
- Secret access/rotation/exposure
- Unexpected egress، DNS/redirect/metadata access
- Tool sandbox escape/limit abuse
- Build/source/provenance/registry tamper
- KEV/reachable-vulnerability exposure
- Data exfiltration/bulk export
- Scientific/source poisoning و provenance break
- Audit gaps/time rollback
- Backup/restore/key/recovery anomalies
- Command-boundary attempts

P11-CON-173 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §50; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Detection می‌تواند خودکار Deny/Quarantine/Revoke/Isolate کند. Restore privilege، public release، destructive purge یا attribution قطعی نیازمند Review/Approval است.

### Owner §51. Incident response

P11-CON-174 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §51; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

چرخهٔ NIST SP 800-61 Rev.3-aligned:

P11-CON-175 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §51; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

1. **Govern/Prepare:** roles، contacts، authority، evidence، communication و exercises
2. **Detect/Analyze:** triage، scope، confidence، privacy/scientific impact
3. **Contain:** narrow deny/revoke/isolate/quarantine/fence
4. **Eradicate:** credential rotation، fix، artifact replacement، persistence removal
5. **Recover:** isolated restore، validation، staged promotion و monitoring
6. **Learn/Improve:** root cause، control/test/threat-model updates و requalification

P11-CON-176 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §51; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Incident record:

P11-CON-177 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §51; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Incident ID، severity dimensions، affected tenants/assets
- Timeline با clock quality
- Evidence custody/digests
- Decisions، actors و authority
- Containment effects و blast radius
- Privacy/legal applicability/notification decisions
- Scientific integrity impact و correction needs
- Recovery gates و residual risk
- Post-incident actions، owners و deadlines

P11-CON-178 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §51; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

قواعد:

P11-CON-179 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §51; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Severity یک عدد تنها نیست؛ Security، Privacy، Scientific و Authority impacts جدا هستند.
- AI می‌تواند cluster/summarize کند، اما severity، attribution، notification و closure authority ندارد.
- Evidence collection minimization و chain-of-custody دارد.
- Public communication و regulator/customer notice توسط نقش مجاز و applicability clock انجام می‌شود.
- Incident closure بدون corrective-action/test evidence مجاز نیست.

### Owner §52. Containment، Revocation و Kill switches

P11-CON-180 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §52; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Automatable containment:

P11-CON-181 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §52; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Deny new sessions/tokens
- Revoke specific credential/lease
- Disable Capability/route/provider
- Quarantine Artifact/Dataset/Tool/Model
- Isolate Workload/tenant slice
- Freeze promotion or export
- Enforce read-only safe mode
- Block source/domain/digest

P11-CON-182 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §52; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Constraints:

P11-CON-183 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §52; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Scope باید حداقل و evidence-driven باشد.
- Broad tenant/system shutdown نیازمند predefined authority و availability impact consideration است.
- Containment نباید داده را حذف، Key را destroy یا Scientific status را rewrite کند.
- Kill switch state signed/versioned/audited و independently visible است.
- Fail-safe behavior برای Control-plane outage تعریف می‌شود؛ high-risk allow cache ممنوع.
- Re-enable فقط پس از Cause evidence، remediation، regression، risk review و Approval مناسب.
- Expired emergency deny می‌تواند در صورت unresolved threat Deny بماند؛ Allow خودکار نمی‌شود.
- `SEC-TZ9` deny قابل‌غیرفعال‌سازی یا break-glass نیست.

### Owner §53. Recovery، Restore و Ransomware

P11-CON-184 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §53; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Recovery principle:

P11-CON-185 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §53; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

`Known-clean identity + Known-clean control plane + Known-clean artifact + Verified data + Reapplied governance/deletion + Staged promotion`

P11-CON-186 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §53; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

الزامات:

P11-CON-187 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §53; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Recovery credential/keys جدا، offline/logically isolated و dual-controlled.
- Golden config/artifact با signed provenance و independent copy.
- Restore در Environment جدا و بدون outbound effect.
- Malware/persistence، schema، cryptographic integrity، audit continuity و scientific provenance validation.
- Policy، deny، revoked identity، tombstone، consent withdrawal و deletion journal دوباره اعمال می‌شوند.
- Clock/timeline و backup generation دقیق انتخاب و ثبت می‌شود.
- Failover با fencing؛ split-brain writer ممنوع.
- Restore test شامل adversarial backup، poisoned config، missing key، stale policy و deleted-data resurrection است.
- RTO/RPO عددی بعداً با Stageهای metric/infrastructure تعیین می‌شوند؛ inability to prove recovery مانع Production promotion است.
- Recovery تمام External effects را suppress می‌کند تا Reconciliation.
- Post-recovery heightened monitoring و independent approval برای Serving لازم است.

### Owner §54. Deletion، Crypto-erasure و Media sanitization security

P11-CON-188 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §54; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Stage 24 deletion semantics حفظ می‌شود:

P11-CON-189 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §54; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Deletion plan گراف Canonical، Derived، Provider، Export، Archive، Backup و Restore را پوشش می‌دهد.
- Dry-run و immutable manifest پیش از Approval.
- Lease fenced، scope-fixed، one-purpose و کوتاه‌عمر.
- Legal hold/retention/applicability بلافاصله پیش از destructive commit دوباره بررسی می‌شود.
- Unknown outcome پیش از Retry Reconcile می‌شود.
- Verifier مستقل از Executor است.

P11-CON-190 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §54; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Crypto-erasure:

P11-CON-191 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §54; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- فقط اگر Key scope تمام ciphertext copies را پوشش دهد.
- Alternate key، plaintext، cache، export، replica، snapshot و backup residual بررسی می‌شود.
- Shared-key blast radius مانع erasure انتخابی می‌شود.
- Key destroy E8 و غیرقابل‌بازگشت است؛ explicit multi-role approval مطابق Stage 19، dual control و Evidence لازم.

P11-CON-192 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §54; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Media sanitization:

P11-CON-193 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §54; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Method بر اساس media type، sensitivity، reuse/disposal و Provider capability با NIST SP 800-88 Rev.2 profile تعیین می‌شود.
- Clear/Purge/Destroy واژگان اختیاری بدون Technique/evidence کافی نیستند.
- Provider certificate به‌تنهایی scope/completion را ثابت نمی‌کند.
- Failed/partial sanitization به Quarantine و escalation می‌رود.
- Audit فقط minimal proof را نگه می‌دارد، نه erased content.

### Owner §55. Third-party، Provider، Connector و Transfer security

P11-CON-194 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §55; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Admission حداقل:

P11-CON-195 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §55; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Legal/role/transfer/applicability decision
- Security architecture و shared-responsibility map
- Data/metadata/content flow و region/support access
- Identity/federation/token/secret model
- Encryption/key-control و deletion/backup semantics
- Subprocessor/dependency inventory
- Incident notification، vulnerability و change terms
- Availability/exit/portability plan
- Independent evidence/attestation متناسب با Risk
- Technical sandbox/canary/negative tests

P11-CON-196 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §55; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

قواعد:

P11-CON-197 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §55; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Certification/attestation به‌تنهایی Admission نیست.
- Provider admin/support access JIT، scoped و evidenced می‌خواهد.
- Silent terms، model، region، subprocessor، retention یا security-control change باعث re-evaluation می‌شود.
- Data egress حداقل، classified، recipient-bound و purpose-bound است.
- Token passthrough به Provider ممنوع؛ brokered/downscoped credential.
- Connector response `UNTRUSTED_DATA_ONLY`.
- Provider outage یا policy conflict نباید Silent fallback به Provider دیگر بسازد.
- Exit شامل Data/export validation، credential revoke، deletion request/verification و residual status است.
- Cross-border route تا `OI-24-007` و specific TIA/safeguards حل نشود غیرفعال می‌ماند.

### Owner §56. Personnel، Insider و Physical security

P11-CON-198 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §56; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Background/contract/training controls فقط در Applicable employment/legal context اعمال می‌شوند.
- Security/Privacy training role-based و scenario-driven است.
- Privileged action JIT، dual control، screen/session restrictions متناسب و audited است.
- Conflict of interest، vendor access، departing staff و contractor expiry مدیریت می‌شوند.
- Insider detection به Privacy minimization، purpose limitation و due process مقید است.
- Bulk access/export، unusual support access و policy override نیازمند detection/review‌اند.
- Physical access به hosting/key/backup media در Stage 28 با Provider/site evidence تعیین می‌شود.
- Hardware/firmware provenance، secure boot و device disposal برای control/key plane باید qualification شوند.
- Removable media پیش‌فرض ممنوع؛ exception inventory، encryption، scanning، chain-of-custody و sanitization می‌خواهد.
- Social engineering برای Helpdesk، Approver، PKI/KMS custodian و Incident team تمرین می‌شود.
- هیچ monitoring پنهان نامحدود یا automated employee attribution بدون applicable governance پذیرفته نیست.

### Owner §57. Availability، DoS، Abuse و Cost controls

P11-CON-199 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §57; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Resource budget per Subject/Tenant/Purpose/Capability.
- Rate، concurrency، queue depth، payload، query complexity، retrieval count، token usage و egress bytes محدود.
- Admission control و backpressure قبل از collapse.
- Circuit breaker، bulkhead، timeout و bounded retry با jitter.
- Effectful operation blind retry ندارد.
- Expensive query/export/AI request نیازمند estimate، budget و cancellation.
- Untrusted compressed/nested content به decompression/recursion limit مقید است.
- Cost anomaly detection و hard ceiling برای Provider/AI/egress.
- Degraded mode Scientific status، freshness و limitations را آشکار می‌کند؛ stale result تازه نشان داده نمی‌شود.
- Availability control نباید cross-tenant data leak یا auth bypass ایجاد کند.
- DDoS provider/edge یک defense layer است، نه تنها لایه.
- Queue overflow/drop policy برای Security/Authority events lossless/fail-safe طراحی می‌شود.

### Owner §58. Scientific-integrity threat controls

P11-CON-200 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §58; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

تهدیدها:

P11-CON-201 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §58; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Source spoofing و authority impersonation
- Observation tampering/replay
- Time scale/frame/unit/precision manipulation
- Covariance/HBR حذف یا تعویض
- Object identity/association poisoning
- Conjunction/Pc result substitution
- Stale ephemeris یا rollback
- Provenance gap و model/source disagreement suppression
- Ranking-based authority inflation
- Data poisoning via web/connector

P11-CON-202 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §58; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

کنترل‌ها:

P11-CON-203 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §58; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Source identity/authority profile و signed/digest evidence
- Immutable raw/source artifacts و superseding revisions
- End-to-end provenance و transform/tool/parameter versions
- Schema + scientific semantic validation
- Time/frame/unit/covariance status preservation
- Multi-source disagreement و freshness detection
- Independent recomputation/benchmark where required
- Claim-level citations و abstention
- Projection/index rebuild from source
- No AI rewrite of scientific status
- Incident/correction workflow بدون history overwrite

P11-CON-204 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §58; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Security validation نباید `NOT_COMPUTABLE`، `NOT_CONVERGED` یا `DISAGREEMENT` را به Safe/zero تبدیل کند.

### Owner §59. Command boundary

P11-INV-013 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §59; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

هر مورد زیر `E9 / APR-X / PROHIBITED / HARD_DENY / SECURITY_AUDIT` است:

P11-INV-014 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §59; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Spacecraft/mission command generation، scheduling، signing، upload یا transmission
- Attitude/orbit control command
- Payload activation/deactivation
- Ground-station uplink command
- Command key، credential، protocol، frame یا endpoint
- Tool/API/Event/Queue/Webhook/File/Export با command semantics
- Encoded، encrypted، compressed یا euphemistic command payload
- Human approval workflow برای command
- Test/simulation interface که به route واقعی قابل‌تبدیل باشد
- «Emergency» یا break-glass command

P11-INV-015 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §59; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

معماری باید اثبات کند:

P11-INV-016 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §59; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- هیچ Schema/verb/resource type برای Command وجود ندارد.
- هیچ Credential/Trust root/route/adapter به Command system وجود ندارد.
- DNS/egress allowlist و network graph Command endpoint ندارد.
- Build dependency و Plugin manifest Command capability ندارد.
- Policy language هیچ Allow rule برای `MI-X` ندارد.
- Negative tests مستقیم، indirect، encoded و chained را رد می‌کنند.
- Attempt unsampled و security-reviewed است؛ payload حساس حداقل/hashed می‌شود.

P11-INV-017 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §59; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

این ممنوعیت Open Issue قابل‌حل یا Risk قابل‌پذیرش نیست.

### Owner §60. Security envelopes و Control contracts

#### Owner §60. 1 `SecurityContext`

P11-CON-205 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §60; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

~~~json
{
  "context_id": "secctx_...",
  "actor_chain": ["identity-ref"],
  "tenant_id": "tenant",
  "purpose_id": "purpose",
  "session_assurance": "profile-ref",
  "workload_attestation": "nullable-ref",
  "source_zone": "SEC-TZx",
  "destination_zone": "SEC-TZy",
  "mission_impact": "MI-0..MI-5",
  "classification_overlays": ["ref"],
  "threat_model": "tm@digest",
  "policy_snapshot": "policy@digest",
  "risk_signals": ["typed-ref"],
  "issued_at": "RFC3339",
  "expires_at": "RFC3339",
  "signature": "ref"
}
~~~

#### Owner §60. 2 `SecurityDecision`

P11-CON-206 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §60; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

~~~json
{
  "decision_id": "secd_...",
  "request_digest": "sha256:...",
  "outcome": "ALLOW|DENY|STEP_UP|REQUIRE_APPROVAL|QUARANTINE",
  "effect_level": "E0..E9",
  "required_approval": "APR-0|APR-1|APR-2|APR-3|APR-X",
  "obligations": ["redact", "audit", "field-filter", "egress-route"],
  "denial_codes": ["SEC-*"],
  "policy_snapshot": "policy@digest",
  "evaluated_at": "RFC3339",
  "expires_at": "RFC3339",
  "signature": "ref"
}
~~~

#### Owner §60. 3 `SecurityReceipt`

P11-CON-207 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §60; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

~~~json
{
  "receipt_id": "secr_...",
  "request_digest": "sha256:...",
  "decision_ref": "secd_...",
  "approval_ref": "nullable",
  "lease_ref": "lease_...",
  "executor_identity": "workload-ref",
  "artifact_digest": "sha256:...",
  "effect_state": "NONE|COMMITTED|PARTIAL|UNKNOWN|RECONCILED",
  "resource_manifest_digest": "sha256:...",
  "evidence_refs": ["..."],
  "started_at": "RFC3339",
  "completed_at": "RFC3339",
  "signature": "ref"
}
~~~

P11-CON-208 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §60; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Envelope/schema change backward/forward compatibility، security diff و version migration test می‌خواهد.

### Owner §61. Security event contracts

P11-CON-209 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §61; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Event families:

P11-CON-210 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §61; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- `IdentityLifecycleChanged`
- `AuthenticationRiskChanged`
- `CredentialRevoked`
- `PolicyPublished`
- `ApprovalIssued|Revoked|Expired|Consumed`
- `ExecutionLeaseIssued|Rejected|Expired`
- `BoundaryCrossingDenied`
- `SecretExposureSuspected`
- `KeyLifecycleChanged`
- `ArtifactAdmissionChanged`
- `VulnerabilityDispositionChanged`
- `ProviderSecurityChanged`
- `ThreatModelInvalidated`
- `DetectionTriggered`
- `IncidentDeclared|Contained|Recovered|Closed`
- `RestoreValidationChanged`
- `DeletionSecurityStateChanged`
- `CommandBoundaryAttempted`

P11-CON-211 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §61; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

هر Event schema/version، producer، actor chain، Tenant/Purpose، timestamps/clock quality، classification، cause، policy/threat-model digest و integrity دارد.

P11-CON-212 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §61; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Eventهای Security/Authority:

P11-CON-213 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §61; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Sample نمی‌شوند.
- Payload secret/personal حداقل دارند.
- Replay و duplicate semantics روشن دارند.
- نمی‌توانند خودشان Destructive effect را ایجاد کنند؛ Consumer مجدداً Policy/Approval/Lease را بررسی می‌کند.
- `CommandBoundaryAttempted` هیچ raw command/secret را نگه نمی‌دارد مگر fragment حداقل و safe hash/evidence طبق incident policy.

### Owner §62. Security Failure Codes

#### Identity و Session

P11-FAIL-003 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §62; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- `SEC-ID-001` `IDENTITY_MISSING`
- `SEC-ID-002` `IDENTITY_UNVERIFIED`
- `SEC-ID-003` `IDENTITY_SUSPENDED_OR_REVOKED`
- `SEC-ID-004` `AUTH_ASSURANCE_INSUFFICIENT`
- `SEC-ID-005` `SESSION_EXPIRED_OR_REVOKED`
- `SEC-ID-006` `ACTOR_CHAIN_INVALID`
- `SEC-ID-007` `WORKLOAD_ATTESTATION_INVALID`

#### Authorization، Approval و Lease

P11-FAIL-004 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §62; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- `SEC-AZ-001` `POLICY_DEFAULT_DENY`
- `SEC-AZ-002` `TENANT_MISMATCH`
- `SEC-AZ-003` `PURPOSE_MISMATCH`
- `SEC-AZ-004` `ACTION_OR_RESOURCE_MISMATCH`
- `SEC-AZ-005` `EFFECT_LEVEL_MISMATCH`
- `SEC-AP-001` `APPROVAL_REQUIRED`
- `SEC-AP-002` `APPROVAL_INVALID_OR_EXPIRED`
- `SEC-AP-003` `APPROVAL_SCOPE_CHANGED`
- `SEC-LS-001` `LEASE_INVALID_OR_EXPIRED`
- `SEC-LS-002` `LEASE_REPLAY_DETECTED`

#### Credential، Key و Secret

P11-FAIL-005 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §62; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- `SEC-CR-001` `TOKEN_AUDIENCE_OR_BINDING_INVALID`
- `SEC-CR-002` `CREDENTIAL_PASSTHROUGH_PROHIBITED`
- `SEC-SR-001` `SECRET_IN_UNSAFE_CHANNEL`
- `SEC-SR-002` `SECRET_COMPROMISE_SUSPECTED`
- `SEC-KY-001` `KEY_SCOPE_UNPROVEN`
- `SEC-KY-002` `CRYPTO_PROFILE_UNSUPPORTED`
- `SEC-KY-003` `KEY_STATE_INVALID`

#### Boundary، Egress و Sandbox

P11-FAIL-006 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §62; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- `SEC-BD-001` `TRUST_BOUNDARY_CONTEXT_INCOMPLETE`
- `SEC-BD-002` `ZONE_ROUTE_NOT_ALLOWED`
- `SEC-EG-001` `EGRESS_DESTINATION_NOT_ALLOWED`
- `SEC-EG-002` `SSRF_OR_DNS_REBINDING_BLOCKED`
- `SEC-EG-003` `EXTERNAL_CONTENT_QUARANTINED`
- `SEC-SB-001` `SANDBOX_POLICY_VIOLATION`
- `SEC-SB-002` `RESOURCE_LIMIT_EXCEEDED`
- `SEC-SB-003` `ARBITRARY_CODE_DISABLED`

#### Supply chain و Vulnerability

P11-FAIL-007 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §62; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- `SEC-SC-001` `ARTIFACT_PROVENANCE_INVALID`
- `SEC-SC-002` `SBOM_INCOMPLETE_OR_UNMATCHED`
- `SEC-SC-003` `UNAPPROVED_ARTIFACT_DIGEST`
- `SEC-VU-001` `REACHABLE_CRITICAL_VULNERABILITY`
- `SEC-VU-002` `KEV_OR_EXPLOIT_EVIDENCE_PRESENT`
- `SEC-VU-003` `VEX_INVALID_OR_STALE`

#### AI، Data و Privacy

P11-FAIL-008 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §62; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- `SEC-AI-001` `UNTRUSTED_INSTRUCTION_IGNORED`
- `SEC-AI-002` `MODEL_OUTPUT_VALIDATION_FAILED`
- `SEC-AI-003` `AI_AUTHORITY_PROHIBITED`
- `SEC-PR-001` `PRIVACY_PURPOSE_OR_BASIS_INVALID`
- `SEC-PR-002` `DSAR_IDENTITY_UNVERIFIED`
- `SEC-PR-003` `REIDENTIFICATION_RISK_UNKNOWN`
- `SEC-DT-001` `CLASSIFICATION_UNKNOWN`
- `SEC-DT-002` `SCIENTIFIC_INTEGRITY_INVALID`

#### Audit، Incident، Recovery و Deletion

P11-FAIL-009 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §62; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- `SEC-AU-001` `AUDIT_INTEGRITY_OR_SEQUENCE_INVALID`
- `SEC-AU-002` `CLOCK_QUALITY_INSUFFICIENT`
- `SEC-IN-001` `SECURITY_INCIDENT_ACTIVE`
- `SEC-RC-001` `RESTORE_VALIDATION_INCOMPLETE`
- `SEC-RC-002` `RECOVERY_IDENTITY_OR_FENCING_INVALID`
- `SEC-DE-001` `DESTRUCTIVE_SCOPE_UNVERIFIED`
- `SEC-DE-002` `ERASURE_OR_SANITIZATION_UNVERIFIED`
- `SEC-DE-003` `EFFECT_UNKNOWN_RECONCILIATION_REQUIRED`

#### Command boundary

P11-FAIL-010 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §62; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- `SEC-CM-001` `SPACECRAFT_COMMAND_PROHIBITED`
- `SEC-CM-002` `COMMAND_ROUTE_OR_SCHEMA_DETECTED`
- `SEC-CM-003` `ENCODED_OR_CHAINED_COMMAND_ATTEMPT`

P11-FAIL-011 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §62; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Failure code Success را جعل نمی‌کند؛ HTTP status، Error text و Retry policy از Effect state و code محاسبه می‌شوند.

### Owner §63. Effect و Approval Mapping

P11-CON-214 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §63; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

| Operation | Effect | حداقل Approval | رفتار |
|---|---:|---:|---|
| Read public security baseline | `E0` | `APR-0` | rate/audit مناسب |
| Read own low-risk security posture | `E1` | `APR-0` | subject/tenant scoped |
| Create threat/finding draft | `E2` | `APR-0/1` | no closure/effect |
| Submit policy/config change for review | `E2` | `APR-1` | proposal only |
| Issue/revoke ordinary user session | `E3` | `APR-1/2` | policy-bound |
| Change ordinary role/entitlement | `E4` | `APR-2` | SoD و review |
| Publish deny-only emergency rule | `E4/E5` | `APR-2` | auto-expiry، audit |
| Re-enable disabled Capability | `E5` | `APR-3` | remediation evidence |
| Publish allow policy/control-plane change | `E5/E6` | `APR-3` | dual review |
| Onboard provider/egress route | `E5/E6` | `APR-3` | privacy/transfer/security gates |
| Issue privileged/JIT admin grant | `E6` | `APR-3/4` | short-lived، step-up |
| Bulk export or cross-tenant approved operation | `E6/E7` | `APR-3` + Data/Privacy approval | fixed manifest |
| Restore/failover production promotion | `E7/E8` | Explicit executive/incident approval طبق Stage 19 | independent verification/fencing |
| Logical deletion/provider erasure | `E7/E8` | Explicit scoped destructive approval طبق Stage 19/24 | Stage 24 graph |
| Physical purge/backup expiry/media sanitization | `E8` | Explicit multi-role destructive approval طبق Stage 19/24 | destructive evidence |
| Destroy encryption/key material | `E8` | Explicit multi-role destructive approval طبق Stage 19/24 | dual control، scope proof |
| Spacecraft command or enabling route | `E9` | `APR-X` | `PROHIBITED / HARD_DENY` |

P11-CON-215 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §63; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Actual approval level می‌تواند توسط Stage 19 یا Policy سخت‌گیرانه‌تر شود، اما هرگز توسط Client/AI/Tool کاهش نمی‌یابد.

### Owner §64. Denial and Failure Matrix

P11-DEN-017 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §64; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

| وضعیت | تصمیم | Retry |
|---|---|---|
| Identity/Session missing، expired یا revoked | Hard deny | فقط پس از re-auth/repair |
| Tenant/Purpose mismatch | Hard deny + audit | خیر با همان request |
| Policy missing/stale/conflict | Deny | پس از valid publication |
| Approval missing/expired/scope mismatch | Deny | approval جدید |
| Lease expired/replayed/binding mismatch | Deny + incident signal | lease جدید پس از review |
| Classification/Region/Rights unknown | Deny egress/use | پس از governance resolution |
| Token/Secret در unsafe channel | Reject + redact/rotate | پس از incident handling |
| Tool/External content دارای instruction | Treat as data/quarantine | safe extraction ممکن |
| Artifact provenance/SBOM invalid | Quarantine | پس از rebuild/qualification |
| KEV/reachable critical unresolved | Block promotion/contain | پس از fix/accepted bounded exception |
| Audit/time integrity invalid | Stop high-impact effects | پس از restore evidence |
| Restore validation incomplete | No serving | پس از complete verification |
| Deletion effect unknown | Freeze + reconcile | blind retry ممنوع |
| Security control outage | Low-risk profile-specific; high-risk deny | پس از recovery |
| Command semantics/route | Permanent hard deny + security audit | هرگز |

### Owner §65. Threat–Control Matrix

P11-CON-216 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §65; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

| تهدید | Prevent | Detect | Contain/Recover |
|---|---|---|---|
| Credential phishing/replay | phishing-resistant MFA، sender binding | auth/replay analytics | revoke/session isolate |
| Workload impersonation | attestation، short-lived PKI | issuer/artifact mismatch | revoke identity، quarantine |
| Cross-tenant access | canonical tenant، ABAC/RLS defense-in-depth | denied access/canary tests | isolate tenant path |
| Policy/approval tamper | signed/versioned policy، SoD | semantic diff/audit chain | deny publication، rollback safe |
| Secret leakage | broker، no prompt/log، scan | secret detection/access anomalies | rotate/revoke، incident |
| SSRF/egress abuse | allowlist، DNS/redirect validation | blocked destination patterns | disable route/tool |
| Sandbox escape | rootless/ephemeral/syscall/no secret | runtime violations | terminate/quarantine artifact |
| Supply-chain compromise | review، SLSA provenance، digest admission | SBOM/registry/build drift | block/revoke artifact |
| Exploited vulnerability | KEV/reachability gate | exploit/behavior signals | patch/disable/isolate |
| Prompt injection | authority/data isolation، structured calls | injection/red-team signals | quarantine content/capability |
| RAG poisoning | source admission، immutable snapshot | disagreement/provenance/index checks | revoke source، rebuild index |
| Data exfiltration | least privilege، egress/field controls | volume/destination anomaly | revoke/export freeze |
| Audit tamper | append/hash/sign/checkpoint | gap/sequence/time checks | isolate writer، external evidence |
| Ransomware | separated identity، recovery copies | mass mutation/key anomalies | fence، isolated restore |
| Scientific manipulation | immutable raw/provenance/semantic validation | source disagreement/recompute | quarantine/correct by supersession |
| Command attempt | no schema/route/credential | unsampled attempt event | permanent deny/investigation |

### Owner §66. Privacy Threat–Control Matrix

P11-CON-217 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §66; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

| LINDDUN threat | نمونه | Control |
|---|---|---|
| Linking | اتصال log، vector و user activity | scoped opaque IDs، separation، minimization |
| Identifying | re-identification از orbital/support metadata | contextual risk test، access/precision limits |
| Non-repudiation excess | Audit اثباتی فراتر از Purpose | content-minimal proof، retention |
| Detecting | فهم حضور فرد/tenant در Dataset | enumeration resistance، response shaping |
| Data disclosure | cross-tenant/export/provider leakage | ABAC، encryption، recipient/transfer gate |
| Unawareness | Processing یا AI use نامشخص | versioned notice، purpose/choice visibility |
| Non-compliance | retention/DSAR/transfer mismatch | applicability registry، workflows، evidence |

P11-CON-218 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §66; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Privacy Risk acceptance بدون DPO/qualified role در Scope applicable و expiry معتبر نیست. Security need به‌تنهایی Purpose نامحدود ایجاد نمی‌کند.

### Owner §67. Testing Requirements

#### Owner §67. 1 Identity و Authorization

P11-REQ-028 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §67; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Enrollment، recovery، factor replacement، revocation و leaver tests
- Token issuer/audience/resource/scope/binding/replay tests
- Cross-tenant، cross-purpose، IDOR/BOLA و privilege-escalation tests
- Policy conflict، stale cache، deny-overrides و rollback tests
- Approval digest/scope/expiry/revocation/reuse tests
- Break-glass expiry، restriction و review tests

#### Owner §67. 2 Boundary، Network و Sandbox

P11-REQ-029 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §67; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Default-deny ingress/egress و unexpected-route tests
- DNS rebinding، redirect، SSRF، metadata/loopback/private IP tests
- mTLS/DPoP route-specific interoperability و theft tests
- Sandbox escape، host mount، runtime socket، device، syscall و secret tests
- CPU/memory/process/file/output/decompression/cost exhaustion
- `SEC-TZ9` reachability/schema/credential negative tests

#### Owner §67. 3 Application، API و Event

P11-REQ-030 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §67; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- ASVS/API Top 10 traceable verification
- Fuzz/canonicalization/injection/mass-assignment/file tests
- CSRF/CORS/session/cookie/error/cache tests
- Event producer/schema/signature/replay/order/tenant tests
- Unknown effect، idempotency و reconciliation tests
- Webhook destination/signature/replay/redirect tests

#### Owner §67. 4 Supply chain

P11-REQ-031 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §67; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Source review/branch protection bypass tests
- Reproducibility/provenance signature/subject tests
- Dependency confusion، typosquat و mutable-tag tests
- SBOM completeness/identity/conversion-loss tests
- KEV/CVSS/EPSS/VEX/reachability fixtures
- Registry replacement، admission و runtime-digest drift tests

#### Owner §67. 5 AI، RAG و Privacy

P11-REQ-032 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §67; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Direct/indirect/multilingual/encoded prompt injection
- Tool-output and citation manipulation
- Sensitive data/model output leakage
- Corpus poisoning، stale index و deleted-data resurrection
- Cross-tenant embedding/cache/memory tests
- DSAR weak/overcollection/representative identity tests
- Re-identification، linkage، synthetic leakage و telemetry minimization tests

#### Owner §67. 6 Detection، Incident و Recovery

P11-REQ-033 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §67; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Detection unit/backtest/purple-team fixtures
- Audit gap/duplicate/time rollback/tamper tests
- Credential compromise، provider outage و policy corruption exercises
- Ransomware/poisoned-backup/isolated-restore tests
- Tombstone/revocation/consent reapplication
- Failover fencing و split-brain tests
- Key recovery، crypto-erasure scope و sanitization evidence tests

P11-REQ-034 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §67; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

هر Test artifact باید version/digest، environment، fixture classification، expected/actual، evidence، reviewer و regression link داشته باشد.

### Owner §68. Security Red-team و Adversarial qualification

P11-REQ-035 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §68; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Red-team طراحی باید حداقل این Campaignها را پوشش دهد:

P11-REQ-036 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §68; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

1. Human auth/recovery و approval social engineering
2. Workload credential theft و lateral movement
3. Tenant/purpose boundary bypass
4. Policy/approval/lease replay و confused deputy
5. Secret extraction از Prompt، logs، errors و tool arguments
6. SSRF، DNS rebinding و egress tunneling
7. Sandbox escape و covert exfiltration
8. Supply-chain/source/build/registry compromise
9. Vulnerability/VEX exception abuse
10. Prompt injection و excessive agency
11. RAG/data poisoning و citation laundering
12. Privacy linkage/re-identification و DSAR impersonation
13. Audit/time/evidence tamper
14. Ransomware، backup poisoning و recovery-path compromise
15. Scientific time/frame/covariance/source manipulation
16. Direct، indirect، encoded و chained spacecraft-command attempt

P11-REQ-037 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §68; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

قواعد:

P11-REQ-038 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §68; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Production active exploitation بدون Scope/authorization واقعی ممنوع است.
- Test data synthetic/minimized و environment isolated است.
- Red team یافتهٔ خودش را بدون independent verification نمی‌بندد.
- Critical finding مانع Promotion است.
- Retest و Regression پیش از closure لازم‌اند.
- Test coverage به ATT&CK/ATLAS/STRIDE/LINDDUN و Control IDs نگاشت می‌شود.
- Numeric pass thresholds در Stage 27 نهایی می‌شوند؛ Hard-deny invariants از همین Stage قطعی‌اند.

### Owner §69. Observability، Metrics و SLO inputs

P11-CON-219 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §69; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Stage 25 Metric contract را تعریف می‌کند؛ Threshold/SLO عددی در Stage 26/27 و Infrastructure capacity در Stage 28 نهایی می‌شوند.

P11-CON-220 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §69; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Metric families:

P11-CON-221 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §69; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Auth success/failure/recovery و assurance distribution
- Revocation propagation latency
- Policy decision deny/step-up/approval/cache freshness
- Lease issuance/replay/expiry
- Cross-tenant/purpose denial
- Secret age/rotation/exposure
- Key/certificate expiry و crypto-profile drift
- Egress destination/blocked SSRF
- Sandbox policy/resource violations
- Artifact provenance/SBOM/admission status
- KEV/reachable vulnerability/exception age
- Prompt-injection/content quarantine
- Audit gap/clock quality/checkpoint
- Detection coverage/latency/false-positive review
- Incident contain/recover/evidence completeness
- Backup restore validation و resurrection suppression
- Privacy request/verification/minimization
- Command-boundary attempt و zero-route conformance

P11-CON-222 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §69; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

قواعد:

P11-CON-223 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §69; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Security/Authority metrics نباید Sample شوند اگر Sampling باعث از‌دست‌رفتن Event شود.
- Label cardinality و identifiers privacy-safe هستند.
- Metric «zero incidents» اثبات Security نیست.
- SLO breach می‌تواند Promotion را متوقف یا Capability را محدود کند، ولی Scientific status را تغییر نمی‌دهد.
- OpenTelemetry semantic conventions در صورت استفاده profile-pinned می‌شوند؛ وضعیت Mixed/unstable بخش‌ها خاموشانه وارد Baseline نمی‌شود.

### Owner §70. Acceptance Criteria

P11-REQ-039 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §70; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Stage 25 فقط زمانی قابل تأیید است که:

P11-REQ-040 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §70; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

1. Stage 24 و تصمیم‌های `DGV-DEC-240` تا `DGV-DEC-249` به‌عنوان مبنای مصوب حفظ شده باشند.
2. دامنهٔ فعال تمام Controls و Capabilities فقط `EARTH_ORBIT_ONLY` باشد.
3. هیچ Interface، Route، Credential، Schema یا Approval path به Spacecraft command وجود نداشته باشد.
4. `SEC-TZ9` در تمام Architecture، IaC، API، Event، Tool و Network tests غیرقابل‌دسترسی باشد.
5. AI همچنان Advisory و فاقد Security، Legal، Scientific یا Operational authority باشد.
6. Model output و Tool call فقط Proposal تلقی شوند.
7. Effect level فقط Server-side و از Taxonomy مصوب محاسبه شود.
8. Client، AI، Tool، Plugin یا Adapter نتواند Effect یا Approval را کاهش دهد.
9. هر System/Capability یک `SecurityApplicabilityProfile` نسخه‌دار و digest-pinned داشته باشد.
10. Profile منقضی، ناقص یا دارای Threat model نامعتبر برای Production پذیرفته نشود.
11. Security، Privacy، Scientific integrity، Rights و Availability Overlayهای مستقل باشند.
12. Conflict control با Deny-overrides و Rule سخت‌گیرانه‌تر حل شود.
13. Risk acceptance دارای Scope، Owner، Compensating control و Expiry باشد.
14. Prohibited invariant با Risk acceptance یا Break-glass قابل‌مجازشدن نباشد.
15. هر Trust boundary در DFD و Boundary registry ثبت و نسخه‌گذاری شود.
16. Zone membership یا Network location به‌تنهایی Trust/Access ایجاد نکند.
17. هر Boundary crossing Actor chain، Tenant، Purpose، Action، Resource و Policy digest را حمل کند.
18. Missing، stale، revoked، conflicting یا unknown boundary context برابر Hard deny باشد.
19. Human، Privileged human، Workload، Build، Deploy، Recovery و Tool identities جدا باشند.
20. حساب انسانی مشترک و shared workload credential ممنوع باشد.
21. Identifierها unique و non-recycled و دارای lifecycle/owner باشند.
22. Privileged/high-impact access به phishing-resistant MFA و Step-up مناسب نیاز داشته باشد.
23. Enrollment، Recovery و Factor replacement به‌اندازهٔ Login محافظت شوند.
24. Leaver/role change همهٔ Session، Token و JIT grantهای مربوط را Revoke کند.
25. هر Workload credential کوتاه‌عمر، audience-bound و workload-bound باشد.
26. Build، Deploy، Runtime و Recovery identities نتوانند جای یکدیگر استفاده شوند.
27. mTLS یا DPoP فقط پس از Route-specific threat/interoperability profile استفاده شود.
28. Authentication به‌تنهایی Authorization یا Approval ایجاد نکند.
29. Token دارای Tenant، Purpose، Resource، Action، Audience، TTL و sender binding باشد.
30. Token passthrough و Refresh token در AI/Tool sandbox ممنوع باشد.
31. Token، Secret یا Private key در Prompt، URL، Event، Log یا Tool output ظاهر نشود.
32. Token replay، issuer/audience mismatch و revoked credential Fail-closed باشند.
33. Authorization default-deny، explicit-allow و deny-overrides باشد.
34. Tenant/Purpose از authenticated/canonical context گرفته شود، نه Client-controlled field.
35. Policy، Schema و compiler/generator output versioned، reviewed و tested باشند.
36. Policy cache تمام Context dimensions را key کند و high-risk stale allow نداشته باشد.
37. هر Approval به Request و Resource-manifest digest دقیق مقید باشد.
38. Scope expansion یا Policy/action/resource change Approval را باطل کند.
39. Standing broad approval برای Export، Delete، Install، Key destroy یا Admin ممنوع باشد.
40. Request، Approval، Execution و Verification برای Effectهای `E7/E8` تفکیک شوند.
41. Break-glass JIT، time-bound، reason-coded و audited باشد.
42. Break-glass نتواند Privacy/Tenant boundary، destructive action یا Command prohibition را دور بزند.
43. هر Flow شبکه Owner، Purpose، Identity، Data class و Review/expiry داشته باشد.
44. Ingress و Egress پیش‌فرض Deny و Service-to-service traffic authenticated/authorized باشد.
45. Admin، Build، Data و Recovery planes از نظر Identity و Route جدا باشند.
46. DNS rebinding، Redirect، SSRF و Metadata/private endpoint access مسدود و آزموده شوند.
47. `SEC-TZ5/6` هیچ Credential اصلی Control/Data/Key plane دریافت نکند.
48. Secret فقط از Broker و برای Workload/Purpose/TTL مشخص ارائه شود.
49. Secret lifecycle، Rotation، Revocation و suspected-exposure workflow قابل‌آزمون باشد.
50. Key hierarchy، Signing، Encryption، Backup، Recovery و Pseudonymization uses را جدا کند.
51. Envelope encryption Tenant/Purpose/Resource/Profile را در Associated data bind کند.
52. Key destroy بدون Copy/key scope، Hold و Approval proof ممنوع باشد.
53. Crypto profile Algorithm، Mode، Parameter، Key use و Deprecation را نسخه‌دار کند.
54. Custom crypto، silent downgrade و floating crypto profile ممنوع باشد.
55. PQC/Hybrid adoption فقط پس از interop، performance و downgrade tests ممکن باشد.
56. Canonical، Projection، Cache، Search، Graph و Vector هر کدام ACL/isolation معتبر داشته باشند.
57. Backup credential از Runtime جدا و Backup manifest signed/encrypted باشد.
58. Restore فقط isolated و بدون External effect آغاز شود.
59. Restore پیش از Serving Revocation، Tombstone، Erasure و Consent-withdrawal را دوباره اعمال کند.
60. Failover با Fencing انجام شود و Split-brain writer ممکن نباشد.
61. APIها strict schema، canonicalization، object/function authorization و resource budget داشته باشند.
62. Mass assignment، injection، CSRF/CORS/session، file و error-leakage tests گذرانده شوند.
63. OpenAPI/Async contracts version-pinned باشند و Generated code untrusted review شود.
64. Event/Webhook producer، schema، signature، Tenant/Purpose، freshness و replay اعتبارسنجی شوند.
65. Effectful event یا timeout blind retry نشود و unknown effect Reconcile شود.
66. Live web همچنان `DISABLED_BY_DEFAULT` و Read-only/allowlisted باقی بماند.
67. Live-web response `UNTRUSTED_DATA_ONLY`، quarantined و provenance-bound باشد.
68. Unknown rights، transfer، region یا destination برای Egress برابر Deny باشد.
69. Tool sandbox ephemeral، rootless، no-host، no-ambient-secret و resource-bounded باشد.
70. Arbitrary code execution در Baseline غیرفعال باشد.
71. Source، Build، Registry، Deploy و Runtime identities جدا باشند.
72. Production Artifact فقط با digest، provenance، SBOM، test و admission مشخص اجرا شود.
73. Control-plane/Crown-jewel buildها هدف حداقل SLSA Build L3 و Source L4 داشته باشند.
74. CycloneDX 1.7 و SPDX 3.0.1 با internal neutral graph و conversion-loss report پشتیبانی شوند.
75. VEX بدون exact product/version/config/reachability evidence معتبر نباشد.
76. KEV، exploit evidence، CVSS4، EPSS4، reachability و Mission impact با هم در Gate استفاده شوند.
77. CVSS یا EPSS به‌تنهایی Promotion/closure را تعیین نکند.
78. Unknown reachable risk برای Internet-facing یا `MI-4/5` برابر Quarantine/Deny باشد.
79. Unsupported/EOL dependency بدون bounded approved exception وارد Production نشود.
80. AI prompt/template/model/provider/corpus changes versioned و requalified باشند.
81. Context assembler Instruction/Data precedence را ساختاری حفظ کند.
82. Tool description، retrieved instruction یا model confidence Authority ایجاد نکند.
83. Machine action فقط از structured، schema/policy/authority-valid output بیاید.
84. RAG/Vector/Memory tenant/purpose-scoped، derived و rebuildable باشند.
85. Corpus/source poisoning، stale index و deleted-data resurrection آزمون شوند.
86. Memory ابتدا `PROPOSED`، source-linked، verified، purpose-bound و TTLدار باشد.
87. Privacy minimization در Collection، Query، Log، Trace، Support و Provider egress اعمال شود.
88. Pseudonymized یا Synthetic data خودکار Anonymous تلقی نشود.
89. Public/external release با unknown re-identification risk برابر Deny باشد.
90. DSAR identity proof متناسب، حداقل و مستقل از AI-only verification باشد.
91. Telemetry Secret، raw credential، full sensitive context یا global stable identifier نگه ندارد.
92. Audit Actor chain، Policy، Approval، Lease، Effect، Time quality و Evidence digest را حفظ کند.
93. Audit/WORM claim با append، tamper، sequence، clock و admin-bypass tests اثبات شود.
94. Detection catalog Threat mapping، coverage limits، automated-action ceiling و tests داشته باشد.
95. Incident response Security، Privacy، Scientific و Authority impacts را جدا ارزیابی کند.
96. Containment خودکار فقط Deny، Revoke، Isolate، Quarantine یا Suspend کند.
97. Recovery به known-clean identities/artifacts/policies و independent validation متکی باشد.
98. Deletion، Crypto-erasure و Sanitization از fixed manifest، fenced lease و independent verification عبور کنند.
99. تمام Critical failureها Machine-readable و تمام defectهای اصلاح‌شده Regression test داشته باشند.
100. هیچ Critical Open Issue حل‌نشده‌ای Capability وابسته را Fail-open نکند.

### Owner §71. Open Issues جدید Stage 25

P11-CON-224 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §71; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

| ID | موضوع | محل بستن |
|---|---|---|
| `OI-25-001` Roster نهایی CISO/Security owner، DPO/Privacy owner، Risk acceptor و Incident authority | Pre-implementation governance |
| `OI-25-002` Asset inventory و Mission-impact/Control-profile mapping واقعی | Stage 27 qualification |
| `OI-25-003` IdP/Federation provider، tenant topology و account-recovery UX | Stage 28/29 |
| `OI-25-004` Phishing-resistant authenticator profiles و exact step-up matrix | Stage 27 benchmark + Stage 29 |
| `OI-25-005` Workload identity، CA/PKI، trust domains و revocation topology | Stage 28 |
| `OI-25-006` Route-specific انتخاب/Benchmark بین mTLS، DPoP و ترکیب آن‌ها | Stage 27/28 |
| `OI-25-007` Policy engine/language/compiler و decision-cache implementation | Stage 27/29 |
| `OI-25-008` Secret manager، KMS، HSM، key custody، region و recovery product/topology | Stage 28 |
| `OI-25-009` Algorithm suite، cryptoperiod و PQC/hybrid migration profile عددی | Stage 27/28 |
| `OI-25-010` Tenant placement، key separation و administrative isolation topology | Stage 28 |
| `OI-25-011` Network segmentation، ingress/egress proxy و concrete allowlist | Stage 28/29 |
| `OI-25-012` Sandbox runtime و تصمیم نهایی دربارهٔ نیاز به arbitrary code execution | Stage 27/29؛ disabled until resolved |
| `OI-25-013` CycloneDX/SPDX canonical conversions و loss/round-trip fixtures | Stage 27/29 |
| `OI-25-014` Exact SLSA targets/exceptions برای تمام artifact classها و third parties | Stage 27 qualification |
| `OI-25-015` Numeric vulnerability remediation SLO، severity و exception thresholds | Stage 26/27 |
| `OI-25-016` Audit/WORM store، trusted-time و retention-partition topology | Stage 28 |
| `OI-25-017` SIEM/detection platform، telemetry schema و exact OTel profile | Stage 26/28/29 |
| `OI-25-018` Incident severity، notification applicability، contacts و communication matrix | Governance/Legal + Stage 26 |
| `OI-25-019` Live-web concrete domains، cache/terms، threat profile و archive behavior | Stage 27/29؛ disabled until resolved |
| `OI-25-020` De-identification/re-identification و Synthetic leakage thresholds | Stage 27 benchmark |
| `OI-25-021` DSAR identity-verification implementation، alternative channel و UX | Privacy review + Stage 29 |
| `OI-25-022` Backup/restore، key recovery، crypto-erasure و media-sanitization provider topology | Stage 27/28/29 |
| `OI-25-023` Independent penetration test/Red-team scope، provider و evidence acceptance | Stage 27 pre-promotion |
| `OI-25-024` هر نوع Spacecraft/Mission command capability یا enabling route | خارج از Baseline؛ `PROHIBITED` |

P11-CON-225 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §71; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

این Open Issueها Design blocker نیستند، زیرا:

P11-CON-226 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §71; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Contract، denial behavior، evidence minimum، Owner class و closure stage آن‌ها تعریف شده است.
- Capability وابسته تا حل `DISABLED`، `QUARANTINED`، `RESEARCH_ONLY` یا Fail-closed می‌ماند.
- هیچ Product، Provider، Region، Route، Algorithm، Threshold، Contact یا Role واقعی حدس زده نشده است.
- `OI-25-024` گزینهٔ انتخابی نیست؛ ممنوعیت دائمی Baseline است.

### Owner §72. اثر Stage 25 بر Open Issueهای قبلی

#### Open Issueهای Stage 22

P11-CON-227 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §72; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

| Open Issue | وضعیت پس از Stage 25 | نتیجه |
|---|---|---|
| `OI-22-002` Policy engine/language | `CONTROL CONTRACT RESOLVED — PRODUCT PENDING` | Deny-overrides، context، version/digest، simulation و publication gate تثبیت شد؛ `OI-25-007` |
| `OI-22-004` Workload identity/PKI | `ARCHITECTURE RESOLVED — TOPOLOGY PENDING` | Identity types، attestation، separation و revocation؛ `OI-25-005` |
| `OI-22-005` DPoP vs mTLS | `ROUTE PROFILE RESOLVED — BENCHMARK PENDING` | Sender constraint اجباری بر اساس Risk؛ `OI-25-006` |
| `OI-22-006` Secret manager | `BOUNDARY RESOLVED — PRODUCT PENDING` | No secret in AI/tool، broker، lifecycle؛ `OI-25-008` |
| `OI-22-007` Sandbox runtime | `CONTROL PROFILE RESOLVED — RUNTIME PENDING` | Ephemeral/rootless/no ambient authority؛ `OI-25-012` |
| `OI-22-008` SLSA target | `TARGET ARCHITECTURE RESOLVED — CLASS MAPPING PENDING` | Crown-jewel L3/L4 target؛ `OI-25-014` |
| `OI-22-009` SPDX/CycloneDX | `INTERCHANGE DECISION RESOLVED — CONVERSION TEST PENDING` | Internal neutral graph، CycloneDX 1.7 primary security interchange، SPDX 3.0.1 supported؛ `OI-25-013` |
| `OI-22-010` Vulnerability/VEX thresholds | `GATE LOGIC RESOLVED — NUMERIC SLO PENDING` | KEV+exploit+CVSS4+EPSS4+reachability+VEX؛ `OI-25-015` |
| `OI-22-012` Codegen policy | `DESIGN RESOLVED` | Generated code untrusted و نیازمند pinned generator/review/tests |
| `OI-22-013` Live web security | `CONTROL CONTRACT RESOLVED — ALLOWLIST PENDING` | SSRF/DNS/redirect/quarantine؛ `OI-25-019` |
| `OI-22-015` Code execution | `REMAINS DISABLED` | فعال‌سازی فقط Capability جدا با qualification؛ `OI-25-012` |
| `OI-22-017` Approval TTL/reuse | `SEMANTICS RESOLVED — NUMERIC MATRIX PENDING` | Exact digest، bounded batch، no standing destructive approval |
| `OI-22-021` Protocol upgrade governance | `DESIGN RESOLVED` | No floating/latest؛ diff، regression و re-promotion |
| `OI-22-023` Unknown effect reconciliation | `SECURITY CONTRACT RESOLVED — IMPLEMENTATION PENDING` | Freeze/reconcile before retry |
| `OI-22-024` Spacecraft command | `PROHIBITED — PERMANENT` | `SEC-TZ9` و `OI-25-024` |

#### Open Issueهای Stage 23

P11-CON-228 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §72; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

| Open Issue | وضعیت پس از Stage 25 | نتیجه |
|---|---|---|
| `OI-23-003` Artifact store consistency | `SECURITY REQUIREMENTS RESOLVED — PRODUCT PENDING` | digest، conditional write، key/access، restore validation |
| `OI-23-009` Audit append/WORM | `INTERFACE/THREAT MODEL RESOLVED — TOPOLOGY PENDING` | signed/hash-linked، checkpoint، clock، admin bypass tests؛ `OI-25-016` |
| `OI-23-011` Migration framework | `SECURITY GATE RESOLVED — IMPLEMENTATION PENDING` | signed artifact، rehearsal، policy/schema/rollback controls |
| `OI-23-017` Tenant placement | `SECURITY CONSTRAINTS RESOLVED — TOPOLOGY PENDING` | identity، key، admin، store/projection isolation؛ `OI-25-010` |
| `OI-23-018` Encryption/KMS/HSM | `KEY ARCHITECTURE RESOLVED — PRODUCT/PROFILE PENDING` | hierarchy، envelope، custody، crypto agility؛ `OI-25-008/009` |
| `OI-23-019` Backup media/method/location/cadence | `SECURITY/RESTORE CONTRACT RESOLVED — INFRASTRUCTURE PENDING` | separate identity، manifest، isolated restore؛ `OI-25-022` |
| `OI-23-024` Spacecraft command | `PROHIBITED — PERMANENT` | هیچ persistence/event path |

#### Open Issueهای Stage 24

P11-CON-229 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §72; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

| Open Issue | وضعیت پس از Stage 25 | نتیجه |
|---|---|---|
| `OI-24-005` Live-web allowlist | `SECURITY PROFILE RESOLVED — DOMAINS PENDING` | `OI-25-019` |
| `OI-24-007` Transfer/TIA safeguards | `SECURITY GATES RESOLVED — ROUTES/LEGAL FACTS PENDING` | provider/recipient/encryption/support access contract |
| `OI-24-011` De-identification thresholds | `METHOD RESOLVED — NUMERIC TEST PENDING` | LINDDUN/contextual attacker model؛ `OI-25-020` |
| `OI-24-013` DSAR identity verification | `SECURITY/PRIVACY WORKFLOW RESOLVED — UX PENDING` | proportional proof، alternative channel؛ `OI-25-021` |
| `OI-24-016` Audit/WORM | `CONTROL CONTRACT RESOLVED — PRODUCT PENDING` | `OI-25-016` |
| `OI-24-017` Deletion orchestrator | `SECURITY CONTRACT RESOLVED — IMPLEMENTATION PENDING` | fixed plan، fenced lease، separate verifier |
| `OI-24-018` Backup residual/expiry | `SECURITY/RESTORE CONTRACT RESOLVED — TOPOLOGY PENDING` | suppression/revocation reapplication؛ `OI-25-022` |
| `OI-24-019` KMS/HSM/key hierarchy | `ARCHITECTURE RESOLVED — PRODUCT PENDING` | `OI-25-008/009` |
| `OI-24-020` Sanitization method | `SELECTION METHOD RESOLVED — MEDIA/PROVIDER FACT PENDING` | NIST SP 800-88 Rev.2 profile؛ `OI-25-022` |
| `OI-24-024` Spacecraft command | `PROHIBITED — PERMANENT` | `OI-25-024` |

### Owner §73. Rejected Alternatives

##### Perimeter-only security

P11-DEN-018 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ «داخل شبکه» Identity، Tenant، Purpose یا least privilege را ثابت نمی‌کند.

##### Authentication equals authorization

P11-DEN-019 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ Principal احراز‌شده می‌تواند Action/Resource/Purpose نامجاز درخواست کند.

##### One shared service account

P11-DEN-020 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ Attribution، revocation و blast-radius isolation را از بین می‌برد.

##### Long-lived bearer tokens

P11-DEN-021 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ سرقت Token به privilege پایدار و replay تبدیل می‌شود.

##### Token passthrough to tools/providers

P11-DEN-022 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ Audience/Scope و actor chain را می‌شکند.

##### Client-declared tenant/effect level

P11-DEN-023 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ confused deputy و privilege downgrade ایجاد می‌کند.

##### Network allowlist as sole control

P11-DEN-024 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ DNS، compromised workload و application abuse را پوشش نمی‌دهد.

##### Service mesh equals Zero Trust

P11-DEN-025 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ Mesh یک Enforcement component است، نه Policy/Approval/Identity proof کامل.

##### Encrypt everything with one key

P11-DEN-026 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ Blast radius، selective erasure، custody و rotation را ناممکن می‌کند.

##### Custom cryptography

P11-DEN-027 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ reviewability، interoperability و assurance کافی ندارد.

##### Immediate PQC migration everywhere

P11-DEN-028 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ استاندارد نهایی به‌تنهایی maturity و protocol fit implementation را تضمین نمی‌کند.

##### CVSS-only vulnerability gate

P11-DEN-029 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ exploit evidence، reachability، environment و impact را نادیده می‌گیرد.

##### Vendor VEX as automatic closure

P11-DEN-030 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ assertion بدون exact reachability/config evidence کافی نیست.

##### SBOM presence equals supply-chain security

P11-DEN-031 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ completeness، identity، provenance، vulnerability response و runtime match لازم‌اند.

##### Signed artifact equals safe artifact

P11-DEN-032 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ Signature فقط signer/integrity را نشان می‌دهد، نه نبود Vulnerability یا malicious source.

##### General browser for live web

P11-DEN-033 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ authenticated session، form/upload، cookies و arbitrary navigation attack surface را گسترش می‌دهند.

##### Sandbox with ambient cloud credentials

P11-DEN-034 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ Sandbox compromise را به Control/Data-plane compromise تبدیل می‌کند.

##### Prompt filter as sole AI defense

P11-DEN-035 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ Runtime authority، structured validation و egress/credential boundaries لازم‌اند.

##### RAG ranking equals source authority

P11-DEN-036 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ Similarity یا popularity صحت و مجوز را ثابت نمی‌کند.

##### Hashing equals anonymization

P11-DEN-037 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ Linkability و dictionary/auxiliary-data attacks باقی می‌مانند.

##### Collect more identity proof for every DSAR

P11-DEN-038 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ Over-collection و حق‌مسدودکنی ایجاد می‌کند؛ proof باید proportional باشد.

##### Log everything forever for security

P11-DEN-039 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ Secret/privacy leakage و retention violation ایجاد می‌کند.

##### WORM vendor label equals immutability

P11-DEN-040 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ Admin bypass، retention lock، clock، sequence و deletion conflict باید آزمون شوند.

##### Automated incident attribution by AI

P11-DEN-041 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ evidence uncertainty و پیامدهای حقوقی/عملیاتی نیازمند authority انسانی است.

##### Auto-remediate every detection

P11-DEN-042 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ false positive می‌تواند destructive effect یا outage بسازد؛ automation ceiling محدود است.

##### Restore directly into production

P11-DEN-043 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ malware، stale policy، revoked identity و deleted-data resurrection را پنهان می‌کند.

##### Backup is immutable because provider says so

P11-DEN-044 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ Credential، policy، admin، key و restore behavior باید مستقلاً اثبات شوند.

##### Crypto-shred without key/copy graph

P11-DEN-045 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ alternate key/plaintext/backup residual ممکن است داده را قابل‌بازیابی نگه دارد.

##### Permanent break-glass administrator

P11-DEN-046 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ emergency path به standing privilege تبدیل می‌شود.

##### Risk acceptance for spacecraft command

P11-DEN-047 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §73; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

رد شد؛ `E9 / APR-X / PROHIBITED` است و هیچ Exception ندارد.

### Owner §74. Technology Implications

P11-CON-230 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §74; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Runtime آینده باید قابلیت اثبات این موارد را داشته باشد:

P11-CON-231 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §74; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- Versioned Security applicability، threat و control registries
- Human/workload/tool identity separation و phishing-resistant/JIT profiles
- Short-lived sender-constrained credentials و revocation
- Policy-as-code با deterministic deny-overrides و signed publication
- Exact-digest approval، execution lease و independent receipt verification
- Default-deny segmentation و controlled egress
- Secret broker، KMS/HSM interface، envelope encryption و key hierarchy
- Crypto inventory، agility و migration testing
- API/Event/Webhook schema، canonicalization و replay controls
- Ephemeral rootless sandbox با no ambient authority
- SLSA-aligned source/build/provenance/admission pipeline
- CycloneDX 1.7، SPDX 3.0.1، VEX، KEV، CVSS4، EPSS4 و reachability graph
- AI/RAG context isolation، output validation و prompt-injection quarantine
- Purpose-bound privacy، proportional DSAR proof و de-identification testing
- Privacy-safe telemetry، append/tamper-evident audit و trusted time
- Detection catalog، incident/containment/recovery orchestration
- Isolated restore، fencing، ransomware and resurrection tests
- Fenced deletion، crypto-erasure و sanitization verification
- Negative reachability و schema tests برای `SEC-TZ9`

P11-CON-232 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §74; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

Stage 25 هیچ IdP، CA، KMS، HSM، SIEM، WAF، EDR، Scanner، Sandbox، Policy engine، Cloud، Region، Provider یا Product نهایی انتخاب نمی‌کند.

### Owner §75. Decision Records

#### `SEC-DEC-250` — Zero-trust Zones with an Unreachable Command Boundary

P11-CON-233 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §75; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- **Problem:** Network/internal trust می‌تواند lateral movement، confused deputy و command-path leakage ایجاد کند.
- **Selected:** Explicit `SEC-TZ0..9`، continuous identity/policy verification و `SEC-TZ9` بدون route/interface/credential.
- **Rationale:** Trust باید per-request و compromise-aware باشد.
- **Consequences:** Boundary registry، segmentation و negative reachability tests لازم‌اند.
- **Risk:** Control complexity و availability dependency.
- **Exit strategy:** Automation و cached low-risk evidence محدود؛ نه implicit trust.
- **Status:** `APPROVED`

#### `SEC-DEC-251` — Human, Workload, AI and Tool Identities Are Distinct

P11-CON-234 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §75; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- **Problem:** Shared/impersonated identity Attribution، revocation و least privilege را از بین می‌برد.
- **Selected:** Identity types مستقل، actor chain، short-lived sender-constrained credentials و no token passthrough.
- **Rationale:** blast-radius containment و verifiable authority.
- **Consequences:** PKI/federation/broker lifecycle پیچیده‌تر.
- **Risk:** Identity-control outage.
- **Exit strategy:** redundant control plane و bounded fail-safe profiles؛ نه shared credential.
- **Status:** `APPROVED`

#### `SEC-DEC-252` — Authorization Is Deny-overrides Policy; Approval Is Exact and Separate

P11-CON-235 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §75; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- **Problem:** Auth-only، Client scope یا broad approval می‌تواند Effect نامجاز بسازد.
- **Selected:** Deterministic policy-as-code با Tenant/Purpose/Effect/Context و exact-digest approval/lease.
- **Rationale:** Fail-closed و non-repudiable effect control.
- **Consequences:** Policy/version/test/approval infrastructure لازم است.
- **Risk:** False denial و operational friction.
- **Exit strategy:** simulation، explainability و narrow pre-approved profiles؛ نه weaker controls.
- **Status:** `APPROVED`

#### `SEC-DEC-253` — Secrets and Keys Use Brokered, Separated, Crypto-agile Hierarchies

P11-CON-236 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §75; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- **Problem:** Ambient secrets، shared keys و static crypto compromise را گسترده و erasure را مبهم می‌کنند.
- **Selected:** Secret broker، non-exportable operation، envelope encryption، separated key uses و versioned CryptoProfile.
- **Rationale:** least exposure، rotation، selective containment و migration.
- **Consequences:** KMS/HSM/key-recovery design و inventory لازم است.
- **Risk:** Key loss یا provider lock-in.
- **Exit strategy:** tested recovery، portability و crypto agility؛ نه plaintext fallback.
- **Status:** `APPROVED`

#### `SEC-DEC-254` — Threat Models Combine STRIDE, LINDDUN, ATT&CK and ATLAS

P11-CON-237 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §75; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- **Problem:** یک Threat lens امنیت، privacy، AI و abuse paths را کامل پوشش نمی‌دهد.
- **Selected:** STRIDE+LINDDUN اجباری، ATT&CK v19 و ATLAS/OWASP snapshot-pinned mapping، change-triggered review.
- **Rationale:** coverage چندبعدی و قابل‌آزمون.
- **Consequences:** Model maintenance و evidence mapping بیشتر.
- **Risk:** Checklist behavior یا stale corpus.
- **Exit strategy:** abuse stories، independent review و snapshot refresh with regression.
- **Status:** `APPROVED`

#### `SEC-DEC-255` — Privacy Is Purpose-bound Engineering, Not a Confidentiality Label

P11-CON-238 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §75; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- **Problem:** Encryption نمی‌تواند over-collection، linking، unlawful purpose یا re-identification را حل کند.
- **Selected:** LINDDUN overlays، minimization، proportional DSAR proof و contextual de-identification.
- **Rationale:** Privacy risk مستقل از CIA است.
- **Consequences:** Data-flow، notice، proof و risk tests پیچیده‌تر.
- **Risk:** Utility/verification friction.
- **Exit strategy:** scoped profiles و benchmark؛ نه blanket collection.
- **Status:** `APPROVED`

#### `SEC-DEC-256` — Supply-chain Evidence Uses a Neutral Graph with Dual SBOM Interchange

P11-CON-239 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §75; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- **Problem:** یک Format یا signature به‌تنهایی provenance، license، vulnerability و reachability را کامل پوشش نمی‌دهد.
- **Selected:** Internal neutral graph؛ CycloneDX 1.7 primary security/VEX interchange و SPDX 3.0.1 supported import/export؛ SLSA targets by class.
- **Rationale:** interoperability بدون format lock-in یا evidence loss پنهان.
- **Consequences:** conversion/loss tests و component identity resolution لازم است.
- **Risk:** Mapping complexity.
- **Exit strategy:** versioned profiles و explicit loss reports.
- **Status:** `APPROVED`

#### `SEC-DEC-257` — Vulnerability Decisions Combine Exploit, Score, Reachability and Evidence

P11-CON-240 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §75; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- **Problem:** CVSS-only یا Vendor VEX false confidence ایجاد می‌کند.
- **Selected:** KEV، exploit evidence، CVSS4، EPSS4، reachability، mission impact، VEX و control strength در Gate واحد.
- **Rationale:** Environment-specific و action-oriented risk.
- **Consequences:** Asset/component/runtime correlation لازم است.
- **Risk:** Unknown data و false blocking.
- **Exit strategy:** bounded exception with expiry/controls؛ unknown high-impact همچنان deny.
- **Status:** `APPROVED`

#### `SEC-DEC-258` — Audit Is Tamper-evident and Privacy-minimal; Response Automation Only Reduces Authority

P11-CON-241 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §75; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- **Problem:** Audit می‌تواند tamper شود یا data-hoarding بسازد؛ auto-response نیز می‌تواند destructive شود.
- **Selected:** Append/hash/sign/checkpoint، trusted-time، minimal payload؛ automation فقط deny/revoke/isolate/quarantine/suspend.
- **Rationale:** Accountability بدون authority escalation یا unnecessary surveillance.
- **Consequences:** Separate audit/detection/incident services و review لازم‌اند.
- **Risk:** Evidence gaps یا over-containment.
- **Exit strategy:** independent checkpoints، exercises و approval-bound restore.
- **Status:** `APPROVED`

#### `SEC-DEC-259` — AI, Tools and External Content Are Untrusted Data with No Direct Effect

P11-CON-242 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §75; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- **Problem:** Prompt injection، tool compromise و provider content می‌توانند Credential/Effect/Policy را تصاحب کنند.
- **Selected:** Instruction/Data isolation، structured validation، no secret، sandbox/egress controls و proposal-only tool calls.
- **Rationale:** AI usefulness بدون انتقال Authority.
- **Consequences:** More abstention، quarantine و workflow latency.
- **Risk:** Coverage/automation کمتر.
- **Exit strategy:** curated sources، deterministic validators و risk-based approvals؛ نه autonomous authority.
- **Status:** `APPROVED`

### Owner §76. وضعیت نهایی Stage 25

P11-CON-243 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §76; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

**Stage 24:** `APPROVED AND CLOSED`  
**تصمیم‌های `DGV-DEC-240` تا `DGV-DEC-249`:** `APPROVED`

P11-CON-244 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §76; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

**Stage 25:** `APPROVED AND CLOSED`  
**تصمیم‌های `SEC-DEC-250` تا `SEC-DEC-259`:**

P11-CON-245 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §76; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

`APPROVED`

#### نتیجهٔ قطعی مصوب

P11-CON-246 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §76; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

- معماری Zero-trust و trust zones `SEC-TZ0..9` تعریف شد.
- Identity انسان، Workload، AI، Tool، Build، Deploy و Recovery از هم جداست.
- Token passthrough، shared credential و ambient secret ممنوع‌اند.
- Authorization، Approval و Execution lease مستقل و exact-digest هستند.
- Policy deny-overrides، version-pinned و change-controlled است.
- Secret broker، key hierarchy، envelope encryption و crypto agility تثبیت شدند.
- Threat model از STRIDE، LINDDUN، ATT&CK v19، ATLAS و OWASP AI inputs استفاده می‌کند.
- CycloneDX 1.7 و SPDX 3.0.1 با internal neutral graph و SLSA targets پذیرفته شدند.
- Vulnerability gate از KEV، exploit evidence، CVSS4، EPSS4، reachability، VEX و impact استفاده می‌کند.
- Live web محدود و غیرفعال پیش‌فرض؛ arbitrary code execution غیرفعال است.
- AI، RAG، Tool و External content همگی `UNTRUSTED_DATA_ONLY` و فاقد Direct effect هستند.
- Privacy-by-design، DSAR verification، contextual de-identification و minimal telemetry تعریف شدند.
- Audit tamper-evident و privacy-minimal است؛ incident automation فقط Authority را کاهش می‌دهد.
- Restore بدون reapplied revocation/erasure/consent و independent validation اجازهٔ Serving ندارد.
- Deletion، Key destruction و Sanitization fixed-scope، approval-bound و independently verified هستند.
- هیچ Break-glass، Risk acceptance یا Admin path به Spacecraft/Mission command وجود ندارد.

P11-CON-247 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §76; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

در Stage 25 هیچ Identity، Account، Certificate، Token، Secret، Key، Rule، Route، Sandbox، Scan، Test exploit، Provider، Product، Deployment، Deletion، Sanitization یا Incident action واقعی ایجاد، اجرا، متصل، منتشر یا حذف نشده و هیچ هزینه یا Effect عملیاتی ایجاد نشده است.

P11-CON-248 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §76; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

گام بعدی مصوب:

P11-CON-249 — Projection مستقیم و Source-bound از `CSIP-EO-STAGE-25` §76; متن زیر با Status `APPROVED AND CLOSED — DESIGN SCOPE` و بدون Compliance/Implementation/Effect inference حفظ می‌شود:

**Stage 26 — Observability, Reliability, SLO, Performance and Capacity Engineering**

## 5. قرارداد یکپارچۀ Trust، Risk، Cost، Evidence و Reproducibility

P11-REQ-041 — هر Security/Privacy Journey باید Evidence chain قابل Correlation از Asset/Subject/Actor chain/Tenant/Purpose/Resource/Action تا Applicability profile، Threat/Risk، Policy/Approval/Lease، Credential/Key، Boundary crossing، Enforcement، Receipt، Detection/Containment، Independent Verification و Final residual status داشته باشد.

P11-REQ-042 — Locked-input set هر Security Decision باید حداقل Identity/attestation، actor chain، tenant/purpose، resource/action/effect، data/security/privacy classification، threat/control profile، policy/version/digest، approval/lease، credential binding/TTL، route/egress/sandbox context، risk/cost record، evidence readiness و verification reference را Bind کند.

P11-CON-250 — Authentication، Authorization، Approval، Execution، Verification، Privacy Applicability، Scientific Validity، Risk، Cost، Evidence و Reproducibility Gateهای مستقل‌اند؛ Pass شدن یکی Failure یا Unknown دیگری را Override نمی‌کند.

P11-CON-251 — P11 فقط Security/Privacy-specific inputs و enforcement requirements این Gateها را تعریف می‌کند؛ Authority و Method نهایی مطابق Ownerهای P05، P06، P10، P12، P13 و P16 باقی می‌ماند.

P11-CON-252 — Security Cost باید Identity/PKI، Policy evaluation، Key/HSM operation، Segmentation/Egress، Sandbox، Supply-chain scanning، Vulnerability response، Audit/Detection، Incident/Forensics، Restore/Requalification و Decommissioning را قابل Attribution نگه دارد.

P11-CON-253 — Budget Availability مجوز Access، Egress، Secret/Key operation، Control bypass، Exception، Scan، Data movement، Incident action یا Risk Acceptance نیست؛ Security Authorization نیز Budget Reservation ایجاد نمی‌کند.

P11-CON-254 — Threat/Risk Assessment باید Credential theft، confused deputy، cross-tenant/purpose leakage، prompt/tool injection، supply-chain compromise، vulnerable reachability، key loss، audit tamper، insider abuse، ransomware، restore resurrection، privacy re-identification، scientific-integrity attack، DoS/cost exhaustion و Unknown Effect را قابل‌حل نگه دارد.

P11-CON-255 — Evidence Completeness و Evidence Correctness مستقل‌اند؛ وجود Signature، SBOM، VEX، Scanner result، Policy allow، SIEM alert، WORM claim، Backup success یا Provider attestation بدون Identity/Scope/Applicability/Independent Verification کافی نیست.

P11-CON-256 — Reproducibility نباید Secret، Private key، Raw personal data یا privileged environment را در Artifact/Log نگه دارد؛ Hermetic evidence باید با protected reference، redaction، key separation و least privilege سازگار باشد.

P11-CON-257 — Risk Register، Threat Model، Control Profile، Exception، Acceptance، Treatment و Evidence باید Versioned و Immutable-history باشند؛ Dashboard/Search/Graph آنها فقط Projection قابل‌بازسازی است.

P11-CON-258 — High/Critical Access، Admin/Key/Export/Delete/Restore action، Policy publication، Privilege promotion، External Egress یا Security-evidence mutation بدون Context کامل، Approval لازم و Verification Path آماده Fail-closed می‌ماند.

P11-CON-259 — Containment automation فقط می‌تواند Authority را کاهش دهد: Deny، Revoke، Isolate، Quarantine یا Suspend؛ Re-enable، Restore access، Declassification، Data release یا Destructive remediation Effect تازه و Approval/Verification مستقل می‌خواهد.

P11-DEN-048 — Evidence Gap نباید با AI Explanation، Vendor claim، CVSS/EPSS تنها، Network location، Signature تنها، SBOM presence، Recent Scan، Green Dashboard یا Absence of Incident پر شود.

P11-DEN-049 — Cost-saving Route، shared credential، broader token، weaker isolation، reduced telemetry، skipped verification یا automatic closure نباید Tenant/Purpose، Privacy، Scientific Integrity، Approval، Evidence یا Command prohibition را خاموشانه کاهش دهد.

P11-FAIL-012 — اگر Identity/Actor chain، Tenant/Purpose، Resource/Action/Effect، Classification، Policy/Approval/Lease، Credential/Key status، Route/Egress/Sandbox context، Threat/Risk، Evidence یا Outcome critical نامعلوم باشد، عملیات نتیجه `SECURITY_PRIVACY_INDETERMINATE — FAIL_CLOSED — DO_NOT_ALLOW_EXECUTE_RELEASE_RESTORE_OR_RETRY_BLINDLY` دارد.

## 6. Technology-status Preservation، Version-locked References و Vendor-neutral Boundary

P11-CON-260 — Stage 25 هیچ IdP، Federation provider، CA/PKI، KMS/HSM، Secret manager، Policy engine، WAF، EDR، SIEM، DLP، Scanner، Sandbox، Service mesh، Cloud، Region یا Security product نهایی انتخاب نمی‌کند.

P11-CON-261 — Laws، Regulations، Standards، Frameworks، Threat corpora، Drafts، Proposals، Vocabularyها و URIهای Owner Source یک Design Snapshot با تاریخ `2026-07-23` و Version/Statusهای همان Source هستند؛ P11 هیچ Latestness، Current-law، Certification یا Compliance تازه ادعا نمی‌کند.

P11-CON-262 — STRIDE، LINDDUN، MITRE ATT&CK v19، MITRE ATLAS، OWASP inputs، SLSA، CycloneDX 1.7، SPDX 3.0.1، CVSS4، EPSS4، KEV، NIST/ISO references و PQC implications فقط در Scope دقیق Owner Source حفظ می‌شوند و به Implementation، Adoption یا Conformance تبدیل نمی‌شوند.

P11-CON-263 — Technology Statusهای P01 بدون Drift مصرف می‌شوند؛ Security Architecture Approved Status هیچ `PROVISIONAL_SELECTION`، `SHORTLISTED`، `RESEARCH_TRACK` یا `APPROVED_PRINCIPLE` را به Final Product/Deployment ارتقا نمی‌دهد.

P11-CON-264 — Live web `DISABLED_BY_DEFAULT` و read-only/allowlisted باقی می‌ماند؛ Arbitrary Code Execution در Baseline غیرفعال است؛ فعال‌سازی آینده فقط با Capability جدا، Qualification P13، Environment P14 و Change P15 ممکن است.

P11-CON-265 — Exact organizational roles، IdP/PKI/KMS topology، Algorithms/Cryptoperiods، Network routes، Sandbox runtime، WORM/SIEM platform، Numeric thresholds، Contacts، Providers و Regions Open Facts هستند و از Source approval، popularity یا vendor defaults استنتاج نمی‌شوند.

P11-DEN-050 — `APPROVED` Source، informative reference، compatible interchange یا aligned profile نباید به Adopted Law، Legal Advice، Certified Compliance، Installed Control یا Production Conformance تبدیل شود.

P11-DEN-051 — وجود Product feature، Zero Trust label، encryption، signature، SBOM، VEX، WORM، backup immutability یا security marketing هیچ Effective Control، Complete Coverage، Privacy Lawfulness یا Absence of Vulnerability را ثابت نمی‌کند.

P11-FAIL-013 — هر Technology/Standard/Threat-corpus/Legal Status Drift نتیجه `STATUS_OR_VERSION_LAUNDERING — REWORK_REQUIRED` دارد.

## 7. Traceability، Source Binding، Compression و Orphan Detection

P11-REQ-043 — هر Clause مادی P11 باید Owner، Requirement/Decision ID، Source Identity، Supporting Binding، Upstream Clause، Consumer، Enforcement، Evidence، Verification Owner، Acceptance Test، Conflict، Compression/Reconstitution، Implementation Status، Limitation و Open Issue قابل‌حل داشته باشد.

P11-REQ-044 — `prompt_clause_id` و `requirement_or_decision_id` دو هویت مستقل‌اند و هرگز Merge یا Copy نمی‌شوند.

P11-REQ-045 — Semantic Compression فقط `DIRECT|PARAPHRASED_LOSSLESS|REFERENCED|DEDUPLICATED` است و نباید MUST/MUST NOT، Scope، Status، Exception، Failure، Security/Privacy/Scientific/AI/Legal Caveat، Uncertainty، Anti-claim یا Source Binding را حذف کند.

P11-PROC-001 — Required Trace Record Projection برای Clauseهای P11 دقیقاً از Schema مشترک زیر استفاده می‌کند:

~~~yaml
trace_schema_id: CSIP-EO-FMSP-TRACE-RECORD
trace_schema_version: 1
prompt_clause_id:
requirement_or_decision_id:
statement:
normative_keyword:
owner_part_id: CSIP-EO-FMSP-P11
semantic_owner_artifact_id: CSIP-EO-STAGE-25
semantic_owner_version: 1.0.0-approved
semantic_owner_sha256: 39975398b6b08bb98875784e7e96a48af8a19f9a51955d9d7d67da7d98da04a3
semantic_owner_status: APPROVED AND CLOSED
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
mapped_stage: 25
mapped_control:
requirement_owner_role:
enforcement_reference:
evidence_reference:
verification_owner: P13_AND_P16_AND_COMPETENT_SECURITY_PRIVACY_LEGAL_DOMAIN_REVIEW
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

P11-CON-266 — `prompt_clause_id` باید Pattern `P11-{INV|REQ|DEF|CON|PROC|DEN|FAIL|DEC|OI}-nnn` داشته باشد.

P11-CON-267 — Owner Part و چهار Field Semantic Owner مستقل از پنج Field Primary Source Binding هستند؛ هیچ‌کدام جای دیگری نیست.

P11-CON-268 — `supporting_source_bindings` آرایۀ Structured، Ordered، Version/Digest/Status-bound است؛ Filename List کافی نیست.

P11-CON-269 — `compression_operation` برای Record مادی خالی نمی‌ماند؛ Losslessness باید قابل Audit باشد.

P11-CON-270 — `reconstitution_operation` مستقل است و برای P11 برابر `NONE — APPROVED OWNER BYTES AVAILABLE; PROMPT DERIVATION ONLY` یا شرح دقیق دیگر است؛ هیچ Historical Recovery Claim لازم یا مجاز نیست.

P11-CON-271 — Inline/Memory Payload غیر Byte-addressable نباید Digest یا Byte-equality جعلی دریافت کند؛ Limitation `INLINE_PAYLOAD_BYTES_NOT_ADDRESSABLE` در صورت Applicability ثبت می‌شود.

P11-CON-272 — Enforcement، Evidence، Verification Owner و Acceptance Test چهار Concern مستقل‌اند و در Field مبهم ادغام نمی‌شوند.

P11-CON-273 — Trace Edge تولیدشده توسط AI تا Validation Rule/Human فقط `CANDIDATE` است و Normative relation نمی‌سازد.

P11-CON-274 — Requirement بدون Source/Authority یا Verification Path `ORPHAN_REQUIREMENT` و Test بدون Requirement/Risk/Threat Target `UNJUSTIFIED_TEST` است.

P11-CON-275 — Conflict، Supersession، Supporting Overlay و Consumer باید صریح باشند؛ شباهت متنی یا Filename coincidence Link معتبر نیست.

P11-CON-276 — Consumer Parts P12 تا P18 فقط Reference می‌گیرند و حق تغییر Owner Source P11 یا Decision Status را ندارند.

P11-DEN-052 — هیچ Clause مادی نباید Source/Digest/Status خالی، مبهم یا inferred-only داشته باشد.

P11-DEN-053 — Traceability نباید Secrets، Tokens، Private keys، Raw sensitive payload یا unnecessary personal data را Inline کند؛ protected reference/digest لازم است.

P11-DEN-054 — Compression نباید Failure code، Deny، Risk uncertainty، Privacy limitation، Open Issue، Version lock یا No-command invariant را حذف کند.

P11-FAIL-014 — Source Digest ناموجود/نامنطبق نتیجه `TRACE_SOURCE_DIGEST_UNRESOLVED` دارد.

P11-FAIL-015 — Requirement بدون Owner/Source/Verification نتیجه `TRACE_ORPHAN_BLOCKING` دارد.

P11-FAIL-016 — Schema رقیب یا Alias مبهم نتیجه `TRACE_SCHEMA_CONFLICT` دارد.

## 8. Decision Records، Open Issues و Status Honesty

P11-REQ-046 — تمام Decision Recordهای قطعی Source باید با ID، Title و Status دقیق حفظ شوند؛ متن کامل هر Decision در Projection مستقیم Owner وجود دارد.

P11-DEC-001 — Source Decision `SEC-DEC-250` — Zero-trust Zones with an Unreachable Command Boundary. Status: `APPROVED`; Owner: `CSIP-EO-STAGE-25`; هیچ Prompt-level، Implementation، Compliance یا Production inference مجاز نیست.

P11-DEC-002 — Source Decision `SEC-DEC-251` — Human, Workload, AI and Tool Identities Are Distinct. Status: `APPROVED`; Owner: `CSIP-EO-STAGE-25`; هیچ Prompt-level، Implementation، Compliance یا Production inference مجاز نیست.

P11-DEC-003 — Source Decision `SEC-DEC-252` — Authorization Is Deny-overrides Policy; Approval Is Exact and Separate. Status: `APPROVED`; Owner: `CSIP-EO-STAGE-25`; هیچ Prompt-level، Implementation، Compliance یا Production inference مجاز نیست.

P11-DEC-004 — Source Decision `SEC-DEC-253` — Secrets and Keys Use Brokered, Separated, Crypto-agile Hierarchies. Status: `APPROVED`; Owner: `CSIP-EO-STAGE-25`; هیچ Prompt-level، Implementation، Compliance یا Production inference مجاز نیست.

P11-DEC-005 — Source Decision `SEC-DEC-254` — Threat Models Combine STRIDE, LINDDUN, ATT&CK and ATLAS. Status: `APPROVED`; Owner: `CSIP-EO-STAGE-25`; هیچ Prompt-level، Implementation، Compliance یا Production inference مجاز نیست.

P11-DEC-006 — Source Decision `SEC-DEC-255` — Privacy Is Purpose-bound Engineering, Not a Confidentiality Label. Status: `APPROVED`; Owner: `CSIP-EO-STAGE-25`; هیچ Prompt-level، Implementation، Compliance یا Production inference مجاز نیست.

P11-DEC-007 — Source Decision `SEC-DEC-256` — Supply-chain Evidence Uses a Neutral Graph with Dual SBOM Interchange. Status: `APPROVED`; Owner: `CSIP-EO-STAGE-25`; هیچ Prompt-level، Implementation، Compliance یا Production inference مجاز نیست.

P11-DEC-008 — Source Decision `SEC-DEC-257` — Vulnerability Decisions Combine Exploit, Score, Reachability and Evidence. Status: `APPROVED`; Owner: `CSIP-EO-STAGE-25`; هیچ Prompt-level، Implementation، Compliance یا Production inference مجاز نیست.

P11-DEC-009 — Source Decision `SEC-DEC-258` — Audit Is Tamper-evident and Privacy-minimal; Response Automation Only Reduces Authority. Status: `APPROVED`; Owner: `CSIP-EO-STAGE-25`; هیچ Prompt-level، Implementation، Compliance یا Production inference مجاز نیست.

P11-DEC-010 — Source Decision `SEC-DEC-259` — AI, Tools and External Content Are Untrusted Data with No Direct Effect. Status: `APPROVED`; Owner: `CSIP-EO-STAGE-25`; هیچ Prompt-level، Implementation، Compliance یا Production inference مجاز نیست.

P11-CON-277 — Decision Approved در Stage 25 فقط Design choice همان Source است؛ Product selection، Runtime control effectiveness، Pen-test result، Legal applicability یا Certification نیست.

P11-CON-278 — هر تغییر در Decision به Decision Record تازه، Impact/Threat/Risk/Cost/Privacy analysis، Evidence، Approval و Source revision/digest تازه نیاز دارد.

P11-CON-279 — P11 هیچ Decision متعلق به P01 تا P10 را Reopen، Merge، Supersede یا Downgrade نمی‌کند.

P11-REQ-047 — تمام Open Issueهای Stage 25 باید آشکار، Owner/Disposition-bound و Fail-closed باقی بمانند؛ P11 هیچ Product، Provider، Region، Route، Algorithm، Threshold، Contact یا Role واقعی را حدس نمی‌زند.

P11-OI-001 — Source Open Issue `OI-25-001` — Roster نهایی CISO/Security owner، DPO/Privacy owner، Risk acceptor و Incident authority. محل Disposition: Pre-implementation governance. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-002 — Source Open Issue `OI-25-002` — Asset inventory و Mission-impact/Control-profile mapping واقعی. محل Disposition: Stage 27 qualification. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-003 — Source Open Issue `OI-25-003` — IdP/Federation provider، tenant topology و account-recovery UX. محل Disposition: Stage 28/29. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-004 — Source Open Issue `OI-25-004` — Phishing-resistant authenticator profiles و exact step-up matrix. محل Disposition: Stage 27 benchmark + Stage 29. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-005 — Source Open Issue `OI-25-005` — Workload identity، CA/PKI، trust domains و revocation topology. محل Disposition: Stage 28. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-006 — Source Open Issue `OI-25-006` — Route-specific انتخاب/Benchmark بین mTLS، DPoP و ترکیب آن‌ها. محل Disposition: Stage 27/28. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-007 — Source Open Issue `OI-25-007` — Policy engine/language/compiler و decision-cache implementation. محل Disposition: Stage 27/29. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-008 — Source Open Issue `OI-25-008` — Secret manager، KMS، HSM، key custody، region و recovery product/topology. محل Disposition: Stage 28. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-009 — Source Open Issue `OI-25-009` — Algorithm suite، cryptoperiod و PQC/hybrid migration profile عددی. محل Disposition: Stage 27/28. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-010 — Source Open Issue `OI-25-010` — Tenant placement، key separation و administrative isolation topology. محل Disposition: Stage 28. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-011 — Source Open Issue `OI-25-011` — Network segmentation، ingress/egress proxy و concrete allowlist. محل Disposition: Stage 28/29. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-012 — Source Open Issue `OI-25-012` — Sandbox runtime و تصمیم نهایی دربارهٔ نیاز به arbitrary code execution. محل Disposition: Stage 27/29؛ disabled until resolved. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-013 — Source Open Issue `OI-25-013` — CycloneDX/SPDX canonical conversions و loss/round-trip fixtures. محل Disposition: Stage 27/29. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-014 — Source Open Issue `OI-25-014` — Exact SLSA targets/exceptions برای تمام artifact classها و third parties. محل Disposition: Stage 27 qualification. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-015 — Source Open Issue `OI-25-015` — Numeric vulnerability remediation SLO، severity و exception thresholds. محل Disposition: Stage 26/27. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-016 — Source Open Issue `OI-25-016` — Audit/WORM store، trusted-time و retention-partition topology. محل Disposition: Stage 28. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-017 — Source Open Issue `OI-25-017` — SIEM/detection platform، telemetry schema و exact OTel profile. محل Disposition: Stage 26/28/29. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-018 — Source Open Issue `OI-25-018` — Incident severity، notification applicability، contacts و communication matrix. محل Disposition: Governance/Legal + Stage 26. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-019 — Source Open Issue `OI-25-019` — Live-web concrete domains، cache/terms، threat profile و archive behavior. محل Disposition: Stage 27/29؛ disabled until resolved. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-020 — Source Open Issue `OI-25-020` — De-identification/re-identification و Synthetic leakage thresholds. محل Disposition: Stage 27 benchmark. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-021 — Source Open Issue `OI-25-021` — DSAR identity-verification implementation، alternative channel و UX. محل Disposition: Privacy review + Stage 29. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-022 — Source Open Issue `OI-25-022` — Backup/restore، key recovery، crypto-erasure و media-sanitization provider topology. محل Disposition: Stage 27/28/29. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-023 — Source Open Issue `OI-25-023` — Independent penetration test/Red-team scope، provider و evidence acceptance. محل Disposition: Stage 27 pre-promotion. Status: `OPEN — FAIL_CLOSED_WHERE_APPLICABLE`.

P11-OI-024 — Source Open Issue `OI-25-024` — هر نوع Spacecraft/Mission command capability یا enabling route. محل Disposition: خارج از Baseline؛ `PROHIBITED`. Status: `PROHIBITED — NO CLOSURE/WAIVER ROUTE INSIDE CSIP-EO`.

P11-CON-280 — Open Issue فقط با Closure Record تازه، Exact Evidence/Source/Digest، Competent Owner، Decision Status، Impacted Clause/Consumer و Residual Limitation بسته می‌شود.

P11-CON-281 — Capability وابسته تا Closure معتبر `DISABLED`، `QUARANTINED`، `RESEARCH_ONLY` یا Fail-closed می‌ماند.

P11-DEN-055 — Summary، Part Acceptance، Model Output، Vendor Claim، Self-attestation، Internal Audit، Healthy Dashboard یا Absence of Incident هیچ Open Issue را نمی‌بندد.

P11-DEN-056 — `OI-25-024` هیچ Closure/Approval/Waiver/Break-glass/Risk-Acceptance Route داخل CSIP-EO ندارد؛ تنها Disposition مجاز حفظ Prohibition و حذف هر Enabling Path است.

P11-FAIL-017 — Silent Open-issue Closure نتیجه `OPEN_ISSUE_DISPOSITION_INVALID` دارد.

P11-FAIL-018 — Decision Status Drift نتیجه `DECISION_STATUS_LAUNDERING` دارد.

## 9. Part-level Acceptance، Audit و Anti-claimها

P11-REQ-048 — P11 فقط وقتی برای Assembly قابل‌پیشنهاد است که Header/Anchor/Footer/Pointer، Owner/Source Digest/Status، Approval Scope، Owner Boundary، تمام Mandatory Domains Assembly §6.11، Trace Schema، Decision/Open Issue، Handoff و No-command Boundary کامل و سازگار باشند.

P11-REQ-049 — Audit داخلی باید روی Bytes واقعی Final File حداقل Clause ID/Sequence، Fence، YAML، Anchor، Source Digest، Status، Required-section، Owner-boundary، Trace-contract، Unsupported-claim، P12 Intrusion و Truncation را کنترل کند.

P11-REQ-050 — عبور از Structural/Semantic Audit فقط `PART_AUDITED — READY_FOR_USER_REVIEW` ایجاد می‌کند؛ Security/Privacy/Legal Approval، Implemented Control، Certification، Runtime Qualification، Approval کل Package یا Production Readiness نیست.

P11-PROC-002 — Checklist اجباری Part-level شامل Filename، Package/Part Metadata، Anchor یکتا، Prior/Next Pointer، Owner/Supporting Digest، Status Preservation، Global Capsule، Assembly §6.11 Coverage، Unique/Gapless IDs، Balanced Fence، Parse-valid YAML، 35-field Trace Schema، No competing schema، No unsupported claim/status promotion، No downstream content، Fixed ACK، Footer، Line/Byte/SHA-256، Visible End Anchor و No truncation است.

P11-CON-282 — Required-section Coverage باید دقیقاً identity-explicit/purpose-bound/default-deny crossings؛ separate human/workload/AI/tool identities؛ authentication/authorization/approval/execution separation؛ trust zones/unreachable command boundary؛ threat/adversary/abuse/privacy models؛ least privilege/short-lived credential/segmentation/egress؛ crypto agility/key hierarchy/secret broker؛ app/API/event/webhook/sandbox؛ supply chain/SBOM/VEX/provenance/vulnerability؛ RAG/memory/prompt injection؛ و privacy-minimal tamper-evident audit/containment-only automation را Map کند.

P11-CON-283 — Clause Scan Pattern دقیق `P11-{INV|REQ|DEF|CON|PROC|DEN|FAIL|DEC|OI}-nnn` است.

P11-CON-284 — Duplicate Clause ID یا Gap در Sequence هر Prefix استفاده‌شده Blocking است.

P11-CON-285 — Fence Scan باید هر `~~~text`، `~~~yaml`، `~~~mermaid` یا `~~~` را دقیقاً متوازن ببیند.

P11-CON-286 — YAML Parse باید تمام YAML Blocks را با Parser واقعی بررسی کند؛ Model Confidence کافی نیست.

P11-CON-287 — Source Digest Scan باید Bytes Materialized معتبر را با Registry تطبیق دهد؛ Digest جعلی ممنوع است.

P11-CON-288 — Status Scan باید Source `APPROVED AND CLOSED` را در Design Scope، Decisionهای Source را `APPROVED`، Supporting Candidate/Draft Statusها و Prompt/Package non-approval را هم‌زمان حفظ کند.

P11-CON-289 — Unsupported-claim Scan باید Source-approved Design Statement را از Claim Implemented/Secure/Compliant/Certified/Pen-tested/Incident-ready/Production-ready جدا کند.

P11-CON-290 — Owner-boundary Scan باید P03 Semantics، P05 Authority، P06 Science، P07 AI/Memory، P08 Capability، P09 Persistence، P10 Data Governance، P12 Reliability/Telemetry و P13 Assurance Ownership را حفظ کند.

P11-CON-291 — Trace Audit باید ۳۵ Canonical Top-level Field، Clause/Requirement Separation، چهار Compression Operation و Reconstitution مستقل را بررسی کند.

P11-CON-292 — Handoff Audit فقط P12 را Next معرفی می‌کند و SLI/SLO، Error Budget، Telemetry Denominator، Capacity Threshold یا Recovery Objective متعلق به P12 را تولید نمی‌کند.

P11-CON-293 — Truncation Audit باید Fixed ACK، Footer و End Anchor را در انتهای Payload ببیند.

P11-CON-294 — Audit Numbers، Line Count، Byte Count و SHA-256 فقط از Final Bytes محاسبه و خارج Self-hashed Payload گزارش می‌شوند.

P11-CON-295 — Internal Audit Correctness حقوقی/Privacy/Security/Scientific/Cost/Operational، Control Effectiveness، Runtime Qualification یا Conformance را اثبات نمی‌کند.

P11-CON-296 — هر Post-acceptance Edit Revision/Digest/Audit تازه می‌خواهد و Prior Bytes/Status حفظ می‌شود.

P11-CON-297 — تمام Future Implementation/Test/Qualification/Release/Deployment/Operation/Freeze Gates مستقل باقی می‌مانند.

P11-CON-298 — P11 Complete Text هیچ Action Authority ایجاد نمی‌کند.

P11-CON-299 — Global Project State پس از دریافت تمام ۱۸ Part فقط `CONTEXT_ASSEMBLED — AWAITING_EXPLICIT_TASK` می‌تواند باشد و آن نیز Freeze/Implementation/Production نیست.

P11-DEN-057 — متن کامل یا Audit Pass Security Control، Privacy Approval، Legal Opinion، Penetration Test، Certification یا Qualification نیست.

P11-DEN-058 — Part Acceptance Technology/Product/Provider/Region/Route/Algorithm/Threshold Selection یا Source Reapproval نیست.

P11-DEN-059 — Part Digest Effective Security، Confidentiality، Integrity، Availability، Privacy Lawfulness، Non-repudiation یا Vulnerability Absence را ثابت نمی‌کند.

P11-DEN-060 — YAML/Structure Pass Domain Correctness، Threat Coverage، Control Effectiveness یا Test Coverage نیست.

P11-DEN-061 — No Finding به معنی No Threat/No Vulnerability/No Incident/No Residual Risk نیست.

P11-DEN-062 — `PART_DECLARED_COMPLETE` Project/Package Complete نیست.

P11-DEN-063 — `PART_ACCEPTED_FOR_ASSEMBLY` Implemented/Secure/Compliant/Certified/Production Ready نیست.

P11-DEN-064 — P11 نباید همراه P12 تحویل یا تولید شود.

P11-DEN-065 — Audit/Delivery هیچ Spacecraft-command Path مجاز نمی‌کند.

P11-FAIL-019 — Missing Required Section نتیجه `P11_REQUIRED_COVERAGE_FAILED — REWORK_REQUIRED` دارد.

P11-FAIL-020 — Structural/Trace Audit Failure نتیجه `PART_NOT_ACCEPTED` دارد.

P11-FAIL-021 — Unsupported Security/Privacy/Compliance/Certification/Qualification Claim نتیجه `P11_STATUS_HONESTY_FAILED` دارد.

P11-FAIL-022 — P12 Intrusion نتیجه `PART_BOUNDARY_VIOLATION` دارد.

P11-FAIL-023 — Truncated End/ACK/Footer نتیجه `PART_TRUNCATED — CONTEXT_NOT_ACTIVATED` دارد.

P11-FAIL-024 — Command/Uplink Path نتیجه `E9/APR-X/INC-0/HARD_STOP` دارد.

### 9.1 Anti-claimهای صریح

P11-CON-300 — این Part، تدوین، Audit، Delivery، Review یا پذیرش آن برای Assembly هیچ‌یک از موارد زیر را ایجاد یا اثبات نمی‌کند:

- Implemented security/privacy control، Zero Trust deployment، secure architecture effectiveness یا absence of vulnerability؛
- Legal opinion، DPO/Privacy approval، DPIA/TIA/ROPA/DSAR completion، Regulatory compliance، Certification یا Attestation؛
- ایجاد User/Account/Identity، Enrollment، MFA، Session، Token، Certificate، Workload credential، Secret، Key، Policy، Rule، Route، Allowlist، Sandbox یا Detection؛
- نصب/انتخاب IdP، CA/PKI، KMS/HSM، Secret manager، SIEM، WAF، EDR، DLP، Scanner، Policy engine، Service mesh، Cloud، Region یا Provider؛
- Authentication، Authorization، Approval، Execution lease، Risk Acceptance، Budget Authorization، Spend یا Effect؛
- Penetration test، Red team، Active scan، Exploit، Malware execution، Credential test، Phishing simulation، Incident containment، Restore یا Recovery؛
- SBOM/VEX completeness، SLSA attainment، Artifact safety، Vulnerability closure، WORM immutability، Backup integrity یا Crypto-erasure completion؛
- Lawful processing، Purpose validity، Rights clearance، Retention/Hold/Deletion decision، Anonymity، De-identification sufficiency یا Provider trust؛
- Scientific validity، Reliability/SLO achievement، Capacity proof، Test assurance، Runtime Qualification یا Production Fitness؛
- Build، Release، Deployment، Pilot، Production، Operation یا Project Freeze؛
- Command، Telecommand، Uplink، Flight Control یا Autonomous Maneuver Execution.

## 10. تحویل کنترل‌شده به Part 12

P11-CON-301 — P12 باید Observability، Reliability، SLI/SLO، Performance، Capacity، Recovery، Alerting، Overload، Cost و Metric Denominator را در مالکیت خود تعریف و P11 Security/Privacy/Threat/Identity/Trust/Containment constraints را Reference کند.

P11-CON-302 — P11 هیچ SLI eligibility predicate، SLO target، Error-budget policy، latency/deadline/retry budget، capacity/headroom threshold، recovery objective، alert window یا telemetry-store topology متعلق به P12 را تعریف یا پیش‌تصویب نمی‌کند.

P11-CON-303 — P12 باید Telemetry/Trace/Metric/Log controls را به P11 privacy minimization، no-secret، no-unnecessary-PII، actor-chain integrity، unsampled critical Security/Authority/Deletion/Scientific-integrity/Command-denial events و tamper-evidence requirements Bind کند.

P11-CON-304 — P12 نباید Availability، SLO، Performance، Cost یا Observability need را جایگزین Deny-by-default، Tenant/Purpose Boundary، Credential/Key safety، Privacy minimization، Approval یا Command prohibition کند.

P11-CON-305 — P12 نمی‌تواند P05 Authority، P06 Scientific Status، P07 AI Boundary، P08 Capability State، P09 Authoritative-store Semantics، P10 Governance Decision یا P11 Security/Privacy Decision را Override کند.

P11-CON-306 — Part بعدی فقط Pointer زیر است:

- Part ID: `CSIP-EO-FMSP-P12`
- Part Index: `12 of 18`
- Title: `Observability, Reliability, SLO, Performance and Capacity | مشاهده‌پذیری، قابلیت اطمینان، SLO، کارایی و ظرفیت`
- Semantic Owner: `CSIP-EO-STAGE-26`
- Semantic Owner Version/Status: `1.0.0-approved / APPROVED`
- Semantic Owner SHA-256: `5624dea1b906ae276a84d59d485c7d8a3b2ce8a387957a89b7cebdbeaf14280a`
- Receive Mode: `CONTEXT_ONLY`
- Action Authority: `NONE`

P11-CON-307 — Approved Status Source P12 فقط Source Design Status است و Prompt Part، SLO Achievement، Telemetry Evidence، Capacity، Deployment یا Production را خودکار Approved نمی‌کند.

P11-REQ-051 — P12 فقط در پیام/فایل جداگانه و پس از پذیرش صریح P11 و مجوز روشن کاربر آغاز می‌شود؛ سکوت، تکمیل P11، عنوان/Owner/Digest معلوم یا وجود Source Approved مجوز نیست.

P11-REQ-052 — پس از دریافت سالم این قسمت، تنها پاسخ مجاز متن ثابت زیر است و هیچ عبارت دیگری نباید قبل یا بعد از آن قرار گیرد:

~~~text
قسمت ۱۱ از ۱۸ ابرپرامپت نهایی CSIP-EO با موفقیت دریافت و ثبت شد.
هیچ تحلیل، طراحی جدید، پیاده‌سازی یا اقدام اجرایی آغاز نمی‌شود.
منتظر قسمت ۱۲ هستم.
~~~

P11-DEN-066 — Receiver نباید پس از P11 تحلیل یکپارچه، P12 Generation، Implementation، Security Test یا Action را خودکار آغاز کند.

P11-DEN-067 — ACK دریافت، Package Approval، Implementation Authorization، Security/Privacy Qualification، Compliance یا Project Freeze نیست.

P11-DEN-068 — Handoff Pointer P12 محتوای P12 یا مجوز تولید آن نیست.

P11-DEN-069 — هیچ Handoff، ACK یا Future Part مسیر Spacecraft Command/Uplink/Execution ایجاد نمی‌کند.

RECEIVER_MUST_WAIT_FOR_NEXT_PART: TRUE
PART_DECLARED_COMPLETE: TRUE
NEXT_EXPECTED_PART: P12
RECEPTION_ACTION: ACK_ONLY
<<<CSIP-EO-FMSP-18P|0.9.0-draft|P11|END>>>
