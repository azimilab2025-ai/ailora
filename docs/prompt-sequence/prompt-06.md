<<<CSIP-EO-FMSP-18P|0.9.0-draft|P06|START>>>
CSIP_EO_PROMPT_PACKAGE_ID: CSIP-EO-FINAL-MASTER-SUPERPROMPT-18P
CSIP_EO_PROMPT_PACKAGE_VERSION: 0.9.0-draft
PART_ID: CSIP-EO-FMSP-P06
PART_INDEX: 06
PART_COUNT: 18
PART_TITLE: Scientific Truth, Numerical Computation and Independent Verification | حقیقت علمی، محاسبۀ عددی و Verification مستقل
SEMANTIC_OWNER_ARTIFACT_ID: CSIP-EO-RS-STAGE-20
SEMANTIC_OWNER_VERSION: 0.1.0-reconstituted-draft
SEMANTIC_OWNER_STATUS: RECONSTITUTED_DRAFT — REVIEW_READY — DOMAIN_REVIEW_REQUIRED — NOT_APPROVED — NOT_FROZEN
CANONICAL_MAP_SOURCE_STATUS: RECONSTITUTED_DRAFT_SCIENTIFIC_REVIEW_REQUIRED
SEMANTIC_OWNER_SHA256: 8e12aa3c7d1c9c03d8d20fcc9cf556a0e8a2e1462d1a9698c7d689d45c6bb8a4
REQUIRED_STATUS_SENTINEL: DOMAIN_REVIEW_REQUIRED — NOT_NORMATIVELY_ACTIVATED
SUPPORTING_SOURCE_BINDINGS: CSIP-EO-AUDIT-GAP-02/0.1.0-candidate/fa400334a69702bf56e8588210449590573bccd3120d7c2cebd6ba9cc8fc161f; ENTERPRISE-TRUST-RISK-COST-EVIDENCE-REPRODUCIBILITY-MANDATE/verified-input-2026-07-28/1b5e7884a343589312d62259f181bd48f1a12b51e2613685c0d58c747a08dab4; CSIP-EO-PROMPT-ARCH-18P-C1/0.1.0-design-candidate/a4c80b938fccaab5d3d85c780351a41ee3444b4c6712920af45b493afbacb09b; CSIP-EO-GAP-RESOLUTION-MANIFEST-C1/0.1.0-candidate/349b590df9fad00c2e0ec317f4bd0b7ad747a5e22a1fead0f66f28c98e955216
PRIOR_PART_ID: CSIP-EO-FMSP-P05
NEXT_PART_ID: CSIP-EO-FMSP-P07
PART_PAYLOAD_SHA256: SEE_EXTERNAL_PROMPT_PACKAGE_MANIFEST
RECEIVE_MODE: CONTEXT_ONLY
ACTION_AUTHORITY: NONE

# پرامپت قسمت ۰۶ از ابرپرامپت نهایی ۱۸ قسمتی CSIP-EO
# حقیقت علمی، محاسبۀ عددی و Verification مستقل

## 0. دستور دریافت، مرز Part و قفل ضدتوهم

این پیام فقط «قسمت ۰۶ از ۱۸» یک زمینۀ مرجع به‌هم‌پیوسته است. قسمت‌های ۰۱ تا ۰۵ باید پیش از آن و به‌ترتیب دریافت و ثبت شده باشند. قسمت‌های ۰۷ تا ۱۸ در این پیام وجود ندارند. دریافت این Part فقط Contract علمی و عددی را به Context می‌افزاید و هیچ Authority، اجرای محاسبه، تأیید علمی، پیاده‌سازی یا اثر عملیاتی ایجاد نمی‌کند.

P06-REQ-001 — هنگام دریافت این قسمت، وضعیت داخلی خود را دقیقاً چنین در نظر بگیر:

`RECEIVING_P06 — P01_THROUGH_P05_REQUIRED — CONTEXT_INCOMPLETE — DOMAIN_REVIEW_REQUIRED — ACTION_AUTHORITY_NONE`

P06-DEN-001 — اگر ترتیب `P01 → P02 → P03 → P04 → P05 → P06`، Header، Anchorها، Source Bindingها، Footer یا Part Pointerها کامل و سازگار نیستند، این Part را فعال نکن و موفقیت دریافت را جعل نکن.

P06-DEN-002 — از این Part برای حدس، بازسازی، خلاصه‌سازی جایگزین یا تولید محتوای P07 تا P18 استفاده نکن؛ آگاهی از عنوان، Owner، Version، Status یا Digest یک Part بعدی مجوز ساخت آن نیست.

P06-DEN-003 — دریافت P06 مجوز اجرای Propagation، Orbit Determination، Frame/Time Conversion، Conjunction Screening، Collision Probability، Monte Carlo، Simulation، Verification Run، Engine Invocation، Tool Call یا External Retrieval نیست.

P06-DEN-004 — این Part هیچ مسیر مستقیم، غیرمستقیم، Generic، Human-mediated یا Enabling برای Spacecraft Command، Telecommand، Uplink، Flight Control یا Autonomous Maneuver Execution ایجاد نمی‌کند.

P06-REQ-002 — پس از دریافت سالم این Part فقط Parse، حفظ Context، کنترل پیوستگی و بازگرداندن پاسخ ثابت انتهای Part مجاز است؛ تحلیل یکپارچۀ پروژه، طراحی Part بعدی، کد، تست، Spend، Build، Release، Deployment و Production آغاز نمی‌شود.

P06-FAIL-001 — دریافت ناقص، بریده، خارج از ترتیب یا متعارض باید فقط چنین گزارش شود:

~~~text
دریافت قسمت ۰۶ از ۱۸ ابرپرامپت نهایی CSIP-EO کامل و معتبر نبود.
وضعیت: PART_TRUNCATED_OR_CONFLICTED — CONTEXT_NOT_ACTIVATED
مورد لازم برای اصلاح: ایراد دقیقِ کشف‌شده در دریافت باید در همین سطر گزارش شود.
هیچ تحلیل، طراحی جدید، پیاده‌سازی یا اقدام اجرایی آغاز نمی‌شود.
~~~

P06-REQ-003 — سکوت، تأخیر کاربر، کامل‌بودن P06 یا وجود Source مربوط به Stage 21 مجوز ادامۀ خودکار نیست؛ تا ارسال صریح Part بعدی در وضعیت انتظار باقی بمان.

P06-CON-001 — این Part مالک Contractهای علمی Engine-neutral برای Time، Frame، Unit، Convention، Covariance، Propagation، Estimation، Ephemeris، Conjunction، Collision Risk، Scenario Analysis، Digital-twin Scientific State و Independent Verification است.

P06-CON-002 — P06 حقیقت علمی را تعریف و محدود می‌کند؛ P05 همچنان مالک Effect/Approval/Permission/Autonomy و Report Routing، و P13 همچنان مالک Assurance Program، Test Oracle و Package-level Equivalence Semantics است.

P06-CON-003 — هر استفاده از واژۀ `valid`، `verified`، `confidence`، `tier` یا `candidate` در این Part فقط معنای دقیق تعریف‌شده در Scope علمی را دارد و نباید به Approval، Authority، Qualification، Release یا Operational Fitness تعمیم داده شود.

## 1. هویت منبع، وضعیت و محدودیت تاریخی

P06-DEF-001 — مالک معنایی این Part چنین است:

- Artifact ID: `CSIP-EO-RS-STAGE-20`
- Version: `0.1.0-reconstituted-draft`
- SHA-256: `8e12aa3c7d1c9c03d8d20fcc9cf556a0e8a2e1462d1a9698c7d689d45c6bb8a4`
- Status: `RECONSTITUTED_DRAFT — REVIEW_READY — DOMAIN_REVIEW_REQUIRED — NOT_APPROVED — NOT_FROZEN`
- Canonical-map source status token: `RECONSTITUTED_DRAFT_SCIENTIFIC_REVIEW_REQUIRED`
- Successor candidate of: `CSIP-EO-STAGE-20`
- Historical source state: `MISSING_NORMATIVE_ARTIFACT`
- Title status: `RECONSTITUTED_SUCCESSOR_TITLE`
- Required prompt sentinel: `DOMAIN_REVIEW_REQUIRED — NOT_NORMATIVELY_ACTIVATED`
- Domain scope: `EARTH_ORBIT_ONLY`
- Deployment baseline: `TERRESTRIAL_BASELINE — ON_ORBIT_RUNTIME_DEFERRED`

P06-CON-004 — Source Identity فقط با Tuple زیر معتبر است:

`Artifact ID + Exact Version + Exact SHA-256 + Exact Status`

P06-CON-005 — Filename، Directory، Timestamp، Length، Retrieval Rank، Similarity، Memory، Summary، Translation، Inline Copy یا Model Output به‌تنهایی Source Identity یا Supersession ایجاد نمی‌کند.

P06-CON-006 — Digest مالک معنایی Fixity Bytes همین Successor Candidate را نشان می‌دهد؛ Historical Equivalence، Correctness، Scientific Approval، Qualification یا Runtime Verification را ثابت نمی‌کند.

P06-CON-007 — `REVIEW_READY` فقط آمادگی Candidate برای Review را بیان می‌کند؛ نتیجۀ Review یا Normative Activation نیست.

P06-CON-008 — `DOMAIN_REVIEW_REQUIRED` فقط با Review صلاحیت‌دار Astrodynamics/Scientific Computing، Independent Challenge، Fresh Digest-bound Approval و Successor-manifest Registration قابل رفع در Revision آینده است؛ هیچ‌یک در این Part انجام نشده است.

P06-CON-009 — پذیرش این Prompt Part برای Assembly فقط `PART_ACCEPTED_FOR_ASSEMBLY` ایجاد می‌کند و Status مالک معنایی، کل Package یا Project را ارتقا نمی‌دهد.

P06-DEN-005 — `CSIP-EO-RS-STAGE-20` نباید Historical Stage 20 بازیابی‌شده، Approved Stage 20، Normative Scientific Baseline یا Qualified Operational Contract معرفی شود.

P06-DEN-006 — Review عمومی Architecture، پذیرش کاربر، Internal Audit، Source Digest Match یا کامل‌بودن متن جای Review علمی صلاحیت‌دار را نمی‌گیرد.

P06-DEN-007 — هیچ Summary، Compilation، Downstream Approved Source یا Majority Vote حق Status Laundering برای این Owner را ندارد.

P06-DEN-008 — Historical Bytes و Approval Provenance مفقود نباید با شباهت، بازنویسی مدل، Downstream Attestation یا Fresh Successor جعل شوند.

## 2. هدف، Scope، Exclusion و مالکیت میان Parts

P06-REQ-004 — هدف P06 ایجاد یک Contract واحد، Explicit، Engine-neutral، Uncertainty-aware، Evidence-bound و Independently Verifiable برای Claims علمی و عددی Earth Orbit است، بدون ادعای اجرای محاسبه یا صلاحیت عملیاتی.

P06-REQ-005 — Scope تحت مالکیت این Part شامل موارد زیر است:

1. Observation Normalization لازم برای محاسبۀ عددی؛
2. Epoch، Time Scale، Clock Quality و Conversion Provenance؛
3. Reference Frame، Realization، Origin، Orientation و Transform؛
4. Unit، Dimension، Coordinate Representation و Convention؛
5. State، Covariance، Uncertainty و Confidence؛
6. Force-model/Algorithm/Estimator Profile؛
7. Orbit Propagation، Orbit Determination و State Estimation؛
8. Ephemeris، Trajectory و Digital-twin Scientific State؛
9. Conjunction Screening، Encounter Geometry، HBR و `Pc`؛
10. Scenario/Maneuver Analysis فقط برای Decision Support زمینی؛
11. Independent Verification، Discrepancy، Equivalence و Reproducibility؛
12. Scientific Failure، Non-convergence، Invalidity و Indeterminacy.

P06-REQ-006 — هر Scientific Request، Result، Promotion یا Publication آینده باید علاوه بر صحت علمی، Contractهای P03، P04 و P05 را مستقل مصرف کند؛ Scientific Validity به‌تنهایی AuthorizationDecision، ExecutionLease یا Operational Authority نیست.

P06-CON-010 — P01 مالک Project Identity، Active Domain، Global Invariant، Canonical Entity، TemporalStamp، Base Event Envelope، Extension Registry و Technology Status است؛ P06 فقط Scientific Semantics لازم را Reference می‌کند.

P06-CON-011 — P02 مالک Stage/Gate/Decision/Handoff و جداسازی Design، Implementation، Verification، Validation، Qualification، Release، Deployment، Operation و Freeze است.

P06-CON-012 — P03 مالک Query/ApplicationCommand/Event/Approval/AuthorizationDecision/ExecutionLease/Receipt/Outcome Record Semantics و API Invocation Boundary است؛ Scientific Envelopes P06 Domain Payload هستند، نه جایگزین P03.

P06-CON-013 — P04 مالک Workflow State، Step، Checkpoint، Pause، Retry، Compensation، Reconciliation و Human-control است؛ P06 Scientific Preconditions، Status و Evidence را به آن تحویل می‌دهد.

P06-CON-014 — P05 مالک `E0..E9`، `APR-*`، `PERM-*`، `AUT-*`، Fail-closed Intersection و `LITE/STANDARD/FULL/DENY` است؛ P06 هیچ Mapping رقیب نمی‌سازد.

P06-CON-015 — P07 مالک AI Advisory، RAG، Knowledge و Memory Boundary است؛ P06 فقط ممنوعیت Fabrication/Promotion علمی توسط AI و شکل Scientific Evidence ورودی/خروجی را تعیین می‌کند.

P06-CON-016 — P08 مالک Plugin/Adapter/Tool/Capability Qualification است؛ P06 فقط Conformance علمی Adapter و Engine Mapping را الزام می‌کند و هیچ Tool را Qualify نمی‌نماید.

P06-CON-017 — P09/P10 مالک Persistence Mechanism و Data Governance؛ P11 مالک Security/Privacy؛ P12 مالک Observability/Evidence/Metric Denominator؛ P13 مالک V&V/Assurance/Equivalence Oracle؛ P14/P15 مالک Deployment/Release؛ P16 مالک Governance/Risk Authority؛ P17 مالک Roadmap؛ و P18 مالک Compilation/Conflict Disposition باقی می‌مانند.

P06-DEN-009 — P06 نباید Base Event Envelope، Generic API Record، Workflow State Machine، Authority Taxonomy، Capability Qualification، Database Schema، Data Classification، Security Mechanism، SLO، Test Program، Deployment Gate، Risk Constitution یا Package Conflict Taxonomy رقیب تعریف کند.

P06-DEN-010 — Governance Decision، Budget، Schedule، Approval یا Operational Need نمی‌تواند Physical Invalidity، Missing Uncertainty، Non-convergence یا Material Scientific Discrepancy را به Truth تبدیل کند.

P06-DEN-011 — Scientific Result معتبر به‌تنهایی Recommendation، Decision، Approval، Authorization، Lease، Execution یا Outcome نیست.

P06-DEN-012 — این Part هیچ Engine Call، Dataset Mutation، External Connection، Code، Test، Simulation، Spend، Procurement، Deployment یا Production Action مجاز نمی‌کند.

## 3. کپسول ثابت جهانی برای تمام ۱۸ قسمت

این کپسول باید بدون تغییر معنایی در هر ۱۸ Part حضور داشته باشد:

P06-INV-001 — Domain فعال `EARTH_ORBIT_ONLY` است؛ Baselineهای Orbital شامل `LEO / MEO / GEO / HEO`، Deployment Baseline زمینی و On-orbit Runtime Deferred است.

P06-INV-002 — Physics Before AI و Evidence Before Claims حاکم است؛ واقعیت فیزیکی، Observation معتبر، Law/Measurement Science و Evidence صلاحیت‌دار بر AI Output و Governance Preference مقدم‌اند.

P06-INV-003 — AI فقط Advisory است و هیچ Authority علمی، حقوقی، امنیتی، مالی، Risk Acceptance، Budget، Approval یا Operational ندارد.

P06-INV-004 — Unknown، Missing، Stale، Conflicted، Invalid، Unsupported، Unverified، Non-converged یا Indeterminate هرگز به Pass، Success، Ready، Valid، Verified یا Approved تبدیل نمی‌شود.

P06-INV-005 — Recommendation، Decision، Approval، AuthorizationDecision، ExecutionLease، Execution، ExecutionReceipt و ValidatedOutcome رکوردهای مستقل، Link‌شده و دارای Immutable History باقی می‌مانند.

P06-INV-006 — Explainability، Uncertainty as a First-Class Concept، Independent Verification، Reproducibility، Immutable History و Graceful Degradation باید در تمام Claims علمی حفظ شوند.

P06-INV-007 — معماری Event-driven، Digital Twin، Zero Trust، Replaceability و Engine-agnostic Contracts است؛ هیچ Model، Agent، Tool، Plugin یا Workflow حق جعل Physics یا ایجاد Authority ندارد.

P06-INV-008 — Minimum Sufficient Complexity حاکم است؛ Complexity بیشتر فقط با Use Case، Evidence، Validity Domain، Risk/Cost و Verifiability روشن مجاز است.

P06-INV-009 — هیچ Digest، Signature، Green Test، Document Approval، Part Acceptance یا Context Assembly مجوز Implementation، Spend، Release، Deployment، Production یا Project Freeze نیست.

P06-INV-010 — هر مسیر Spacecraft Command، Telecommand، Uplink، Flight Control یا Autonomous Maneuver Execution، مستقیم یا غیرمستقیم، `E9 / APR-X / INC-0 / HARD_DENY` و بدون Waiver یا Exit داخل CSIP-EO است.

P06-CON-018 — تکرار این Capsule یک Safety Checksum برای انتقال چندبخشی است؛ مالکیت Foundations را از P01 منتقل و Approval تازه ایجاد نمی‌کند.

P06-DEN-013 — Benefit، Deadline، Scientific Curiosity، User Request، Executive Preference یا Emergency نمی‌تواند Hard Invariant یا Scientific Invalidity را Trade-off کند.

## 4. سلسله‌مراتب حقیقت علمی و جداسازی Claimها

P06-REQ-007 — در Scope علمی قابل‌اعمال، ترتیب Authority باید چنین حفظ شود:

1. Physical Reality و Observationهای معتبر؛
2. Physical Law، Measurement Science و Evidence؛
3. Approved Canonical Scientific Contract و Algorithm Profile برای Scope دقیق؛
4. Qualified Implementation و Exact Configuration؛
5. Independently Verified Result و Uncertainty Evidence؛
6. Derived Projection، Visualization و Decision-support Product؛
7. AI Explanation، Narrative یا Summary.

P06-DEF-002 — `Scientific Claim` گزاره‌ای Testable و Scope-bound درباره State، Dynamics، Observation، Estimate، Prediction، Geometry، Probability، Uncertainty یا Validity است.

P06-DEF-003 — `Scientific Artifact` Payload یا Record Immutable/Versioned است که Claim، Input، Algorithm، Configuration، Evidence، Uncertainty، Status و Provenance را قابل بازسازی می‌کند.

P06-DEF-004 — `Canonical Scientific Contract` Schema/Profile تصویب‌شده برای یک Scope دقیق است؛ وجود تعریف Candidate در این Part به معنی Approved بودن Contract نیست.

P06-DEF-005 — `Scientific Promotion` تغییر یک Artifact از Draft/Exploratory/Estimated به State مرجع یا قابل‌مصرف در Decision با Impact بالاتر است؛ Promotion یک Effect جدا و مشمول P05/P03/P04/P13 است.

P06-DEF-006 — `Validity Domain` مجموعۀ صریح Conditions است که Claim در آن پشتیبانی می‌شود، شامل Time Span، Orbit Regime، Data Quality، Model/Force Assumptions، Precision/Tolerance، Frame/Scale، Uncertainty و Intended Use.

P06-DEF-007 — `Scientific Truth Status` وضعیت Evidence-bound یک Claim است و با Approval Status، Workflow State، Publication State، Operational Readiness یا Human Confidence یکی نیست.

P06-CON-019 — Governance می‌تواند Method قابل‌مصرف را برای یک Context انتخاب یا استفاده را محدود کند؛ نمی‌تواند نتیجۀ فیزیکی نامعتبر را معتبر کند.

P06-CON-020 — اختلاف علمی باید با Method، Evidence، Validity Domain، Uncertainty، Counterevidence، Independent Computation و Competent Adjudication حل شود، نه Majority Vote یا LLM Synthesis.

P06-CON-021 — هر Claim باید Subject، Scope، Epoch/Interval، Status، Evidence، Uncertainty، Limitations، Source و Responsible Scientific Owner قابل‌حل داشته باشد.

P06-CON-022 — Claimهای Observation، Estimated State، Propagated State، Conjunction Geometry، `Pc`، Recommendation و Decision باید جدا و با Causal Reference متصل باشند.

P06-CON-023 — Statusهای علمی حداقل `VALID`، `VALID_WITH_LIMITATIONS`، `NOT_COMPUTABLE`، `NOT_CONVERGED`، `DISPUTED`، `INDETERMINATE` و `INVALID` را بدون Collapse حفظ می‌کنند.

P06-CON-024 — `VALID` فقط در Validity Domain و برای Exact Inputs/Profiles/Evidence تعریف می‌شود؛ Universal Truth یا Future Validity ایجاد نمی‌کند.

P06-CON-025 — `VALID_WITH_LIMITATIONS` باید Limitations را Machine-readable و User-visible نگه دارد و برای Use خارج از آن‌ها به `INDETERMINATE/INVALID_FOR_USE` تبدیل شود.

P06-CON-026 — Projection، Visualization، Dashboard، Report یا AI Narrative Derivative است و حق Silent Override یا Status Promotion نسبت به Scientific Artifact ندارد.

P06-CON-027 — Digest/Signature می‌تواند Fixity، Integrity یا Origin را پشتیبانی کند؛ Correctness، Calibration، Convergence، Validity یا Independence را به‌تنهایی ثابت نمی‌کند.

P06-CON-028 — Publication یا Human Acceptance یک Claim، Scientific Evidence و Validity Domain آن را تغییر نمی‌دهد.

P06-CON-029 — Counterevidence، Failed Assumption، Auxiliary-data Revision یا Discrepancy تازه باید Revalidation و در صورت لزوم Supersession را فعال کند؛ History حذف نمی‌شود.

P06-CON-030 — Claim Narrowing برای حفظ بخش پشتیبانی‌شده مجاز است فقط اگر Scope جدید، Evidence و Exclusionها صریح و Revision تازه باشد؛ Silent Goalpost Shift ممنوع است.

P06-DEN-014 — Missing Observation، Model Parameter، Time Scale، Frame، Unit، Covariance یا Auxiliary Data نباید توسط Assumption پنهان یا AI Completion به Truth تبدیل شود.

P06-DEN-015 — `approved`, `published`, `operational`, `high confidence`, `expert reviewed` یا `consensus` جای Scientific Status و Evidence نیست.

P06-DEN-016 — Numerical Precision بالا، Runtime طولانی، Model Complexity یا Engine Reputation به‌تنهایی Accuracy یا Validity را اثبات نمی‌کند.

P06-DEN-017 — Result Selection پس از دیدن خروجی برای عبور از Threshold، بدون Predeclared Rule و Disclosure، مجاز نیست.

P06-DEN-018 — هیچ Summary نباید Failure، Limitation، Counterevidence، Uncertainty یا Disagreement مادی را حذف کند.

P06-FAIL-002 — Claim بدون Subject/Scope/Epoch/Evidence/Uncertainty/Status نتیجه `SCIENTIFIC_CLAIM_CONTEXT_INCOMPLETE — DO_NOT_PROMOTE` دارد.

P06-FAIL-003 — Conflict میان Physical Evidence و Governance/AI Preference نتیجه `SCIENTIFIC_PRECEDENCE_CONFLICT — PHYSICS_AND_EVIDENCE_CONTROL` دارد.

P06-FAIL-004 — Unsupported Status Promotion نتیجه `SCIENTIFIC_STATUS_LAUNDERING — REWORK_REQUIRED` دارد.

## 5. Context علمی اجباری و Snapshot بازتولیدپذیر

P06-REQ-008 — هر Scientific Input و Output باید، در حد Applicability، Context زیر را بدون Semantic Loss حفظ کند:

~~~yaml
scientific_context_id:
context_schema_version:
subject_and_object_references: []
observation_references: []
epoch:
validity_interval:
time_scale_profile:
reference_frame_contract:
coordinate_representation:
unit_contract:
convention_profile_ids: []
state_vector_representation:
covariance_representation:
uncertainty_and_confidence:
force_model_profile_id:
estimator_profile_id:
algorithm_profile_ids: []
auxiliary_data_snapshot:
source_observation_manifest:
engine_build_and_configuration_digests: []
precision_tolerance_and_convergence:
validity_domain:
limitations: []
provenance_reference:
context_digest:
~~~

P06-DEF-008 — `AuxiliaryDataSnapshot` Manifest Digest-bound از Leap Seconds، EOP، Gravity/Atmosphere/Solar/Geomagnetic/Ephemeris/Constants و هر Data خارجی Applicable است، همراه Source، Version، Validity، Freshness و Quality.

P06-CON-031 — Applicability هر Field باید با Rule/Profile و Rationale تعیین شود؛ Field خالی مساوی `NOT_APPLICABLE` نیست.

P06-CON-032 — Context باید Object Revision و Observation Revision را Fix کند؛ Mutable Pointer بدون Resolved Revision برای Reproduction کافی نیست.

P06-CON-033 — Epoch، Validity Interval، Observation Time، Ingest Time، Transaction Time و Publication Time باید از هم جدا بمانند.

P06-CON-034 — State Vector بدون Coordinate Representation، Frame، Epoch و Unit Contract فاقد Context معتبر است.

P06-CON-035 — Covariance بدون Epoch، Frame، Basis، Ordering، Unit Semantics، Confidence Interpretation و Estimation/Propagation Provenance معتبر نیست.

P06-CON-036 — Profile IDs باید Versioned و Digest-bound باشند؛ Label آزاد مانند `high fidelity` یا `standard` هویت Profile نیست.

P06-CON-037 — Algorithm، Engine، Build، Dependencies، Constants، Configuration، Platform و Numerical Library باید در حد لازم برای Reproduction/Verification قابل‌حل باشند.

P06-CON-038 — Precision، Tolerance، Stopping Rule، Iteration Limit، Conditioning، Random Seed/Stream و Stochastic Protocol باید پیش از ارزیابی Result مشخص باشند.

P06-CON-039 — Validity Domain باید Intended Use و Excluded Use را ثبت کند؛ Absence of Exclusion مجوز Universal Use نیست.

P06-CON-040 — Provenance باید Source Observation، Transform، Filter/Weight/Reject، Algorithm Step، Derived Artifact و Supersession Chain را قابل Audit سازد.

P06-CON-041 — Context Digest باید Canonicalization Profile و Artifact Membership را مشخص کند؛ Digest مبهم یا Self-referential معتبر نیست.

P06-CON-042 — Revision Auxiliary Data یا Convention باید Artifact جدید یا Explicit Revalidation تولید کند؛ Silent Recompute/Overwrite ممنوع است.

P06-CON-043 — اگر Context Critical فقط از External Provider قابل‌دسترسی است، Provider Version، Retrieval Evidence، License/Rights Reference و Local Fixity/Protected Reference باید حفظ شود؛ این Part Retrieval را مجاز نمی‌کند.

P06-DEN-019 — Critical Field نباید به‌دلیل Serialization Success، UI Simplicity، Storage Cost یا Model Token Limit حذف شود.

P06-DEN-020 — Unit، Frame، Epoch، Covariance Ordering یا Time Scale نباید از نام Field، Magnitude، Common Practice یا Prior Record حدس زده شود.

P06-DEN-021 — `latest`، `default`، `current`، `production` یا Filename به‌تنهایی Auxiliary-data/Profile Identity نیست.

P06-DEN-022 — Derived Artifact نباید Provenance را به یک Human-readable Citation بدون Machine-resolvable Binding تقلیل دهد.

P06-DEN-023 — Unknown Context نباید با Zero، Mean، Nominal، Identity Transform، Default Covariance یا LLM Estimate جایگزین شود.

P06-DEN-024 — Context Snapshot ناقص نباید Reproducible یا Independently Verifiable معرفی شود.

P06-DEN-025 — Sensitive/Restricted Source Presence حق Data-use، Egress یا Publication ایجاد نمی‌کند؛ P10/P11/P05 همچنان حاکم‌اند.

P06-FAIL-005 — حذف Critical Scientific Field نتیجه `SCIENTIFIC_CONTEXT_LOSS — HARD_FAIL` دارد.

P06-FAIL-006 — Unresolved Profile یا Auxiliary Data نتیجه `SCI_AUXILIARY_DATA_STALE_OR_MISSING — NOT_COMPUTABLE_OR_LIMITED` دارد.

P06-FAIL-007 — Mutable/Unresolved Input Revision نتیجه `SCIENTIFIC_INPUT_REVISION_UNBOUND — DO_NOT_COMPUTE_OR_PROMOTE` دارد.

P06-FAIL-008 — Digest/Canonicalization Conflict نتیجه `SCIENTIFIC_CONTEXT_DIGEST_CONFLICTED — INDETERMINATE` دارد.

## 6. Contract زمان، Epoch و Ordering علمی

P06-REQ-009 — تمام Time Valueهای علمی باید Scale-explicit، Source-bound و Uncertainty-aware باشند و Conversion Provenance را حفظ کنند.

P06-DEF-009 — `ScientificTemporalStamp` توسعۀ Domain-specific بر `TemporalStamp` مالک P01 است و حداقل مفاهیم زیر را Reference می‌کند؛ این Schema Base P01 را Replace نمی‌کند:

~~~yaml
temporal_stamp_reference:
instant:
time_scale: UTC|TAI|TT|UT1|OTHER_PROFILE_BOUND
source_clock:
clock_quality:
uncertainty:
epoch_semantics:
leap_second_table_reference:
eop_source_reference:
conversion_profile_id:
rounding_and_precision:
provenance_reference:
~~~

P06-DEF-010 — `TimeConversionRecord` نگاشت Immutable از Input Instant/Scale به Output Instant/Scale با Exact Tables، EOP، Algorithm، Precision، Uncertainty و Digest است.

P06-CON-044 — Scaleهای مجاز می‌توانند `UTC`، `TAI`، `TT`، `UT1` و سایر Scaleهای Astronomical صریحاً Adopted باشند؛ Presence در این فهرست به‌تنهایی Profile Approval نیست.

P06-CON-045 — `RFC 3339` فقط Representation متن است و Scientific Time Semantics، Scale یا Leap-second Treatment را کامل نمی‌کند.

P06-CON-046 — هر Conversion باید Input/Output Scale، Leap-second Table Version، EOP Source/Version، Algorithm/Profile، Clock Quality، Uncertainty، Rounding و Provenance را ثبت کند.

P06-CON-047 — Observation Time، Measurement Integration Interval، State Epoch، TCA، Validity Interval، Event Occurrence، Ingest، Record، Publish و Transaction Times مفاهیم مستقل‌اند.

P06-CON-048 — Ordering باید Causality/Sequence و Time Uncertainty را جدا کند؛ Timestamp Equality یا Arrival Order به‌تنهایی Causal Order نیست.

P06-CON-049 — Leap-second Boundary، EOP Gap/Prediction، Clock Drift، Truncated Precision و Scale Conversion باید Explicit Quality/Uncertainty تولید کند.

P06-CON-050 — UT1-dependent Computation بدون EOP Source و Validity نمی‌تواند Valid معرفی شود.

P06-CON-051 — Conversion Round-trip باید با Predeclared Tolerance و Non-injective Cases ارزیابی شود؛ Text Equality شرط همیشگی Scientific Equivalence نیست.

P06-CON-052 — Epoch Format و Calendar Convention باید Profile-bound باشند؛ Ambiguous Civil Time، Local Time یا Missing Offset مردود است.

P06-CON-053 — Auxiliary Time Data Staleness باید بر Result Status و Validity Domain اثر صریح داشته باشد.

P06-CON-054 — Predicted EOP یا Extrapolated Time Data باید از Final/Observed Data جدا، Tagged و دارای Horizon/Uncertainty باشد.

P06-CON-055 — Time Conversion Chain باید هر Step را حفظ کند؛ Composite Result بدون Step Provenance فقط در صورت Equivalence/Trace Rule تصویب‌شده مجاز است.

P06-CON-056 — Precision بیش از Source Clock/Data Resolution نباید به‌عنوان Accuracy نمایش داده شود.

P06-CON-057 — Time Conflict میان Sources باید `CONFLICTED/INDETERMINATE` باقی بماند تا Competent Disposition؛ Newer Timestamp به‌تنهایی برنده نیست.

P06-CON-058 — Expiry، Approval Validity و Lease Time Semantics متعلق به P03/P05/P11 است؛ P06 فقط Scientific Time Evidence را فراهم می‌کند.

P06-CON-059 — Scientific Eventها باید Base Event TemporalStamp P01 را حمل کنند و در صورت Applicability به `EVT-SCI` Time Extension Bind شوند.

P06-DEN-026 — Bare Timestamp بدون Time Scale برای Scientific State/Observation/Result قابل‌پذیرش نیست.

P06-DEN-027 — UTC، TAI، TT و UT1 نباید Alias یا Interchangeable تلقی شوند.

P06-DEN-028 — Missing Leap/EOP Data نباید با Host Clock، System Default یا AI Guess جایگزین شود.

P06-DEN-029 — Arrival Time نباید Observation Time یا State Epoch فرض شود.

P06-DEN-030 — Rounding یا Truncation نباید بدون Error/Precision Evidence پنهان شود.

P06-DEN-031 — Time-scale Conversion Success در API به‌تنهایی Scientific Correctness را ثابت نمی‌کند.

P06-FAIL-009 — Time Scale مفقود نتیجه `SCI_TIME_SCALE_MISSING — INVALID_CONTEXT` دارد.

P06-FAIL-010 — Epoch نامعتبر یا Ambiguous نتیجه `SCI_EPOCH_INVALID — NOT_COMPUTABLE` دارد.

P06-FAIL-011 — Leap/EOP Dependency نامعتبر نتیجه `SCI_AUXILIARY_DATA_STALE_OR_MISSING` و Status محدود/نامعتبر متناسب دارد.

P06-FAIL-012 — Clock/Ordering Uncertainty غیرقابل‌Bound نتیجه `SCIENTIFIC_TIME_INDETERMINATE` دارد.

P06-FAIL-013 — Conversion خارج از Validity Domain نتیجه `SCI_VALIDITY_DOMAIN_EXCEEDED` دارد.

## 7. Reference Frame، Coordinate، Unit و Convention

P06-REQ-010 — هیچ State، Observation، Covariance، Relative Geometry یا Ephemeris بدون Frame، Epoch، Coordinate Representation، Unit و Convention قابل‌حل نباید Valid تلقی شود.

P06-DEF-011 — `ReferenceFrameContract` حداقل Schema زیر را دارد:

~~~yaml
frame_id:
frame_family:
frame_realization:
origin:
orientation:
epoch_or_validity:
transform_profile:
auxiliary_data_versions: []
~~~

P06-DEF-012 — `UnitContract` Dimensions، Canonical Units، Display Units، Conversion Profiles، Precision/Loss و Forbidden Inference را برای هر Field ثبت می‌کند.

P06-DEF-013 — `ConventionProfile` مجموعۀ Versioned از Axis Ordering، Sign، Handedness، Angle Range، Earth/Body Constants، Coordinate/Element Definition و Singular-case Handling است.

P06-CON-060 — Frame Family و Realization هر دو لازم‌اند؛ Label کلی مانند `ECI`، `ECEF` یا `inertial` به‌تنهایی هویت کامل Frame نیست.

P06-CON-061 — Origin، Orientation، Epoch/Validity و Transform Profile باید صریح باشند؛ Frame Name نباید این Fields را Implicit کند.

P06-CON-062 — Transform باید Source/Target Frame، Epoch، Method، Auxiliary Data، Interpolation، Precision و Validity را ثبت کند.

P06-CON-063 — State Transform و Covariance Transform باید Semantically هماهنگ باشند و Jacobian/Method و Coordinate Basis را در صورت Applicability ثبت کنند.

P06-CON-064 — Covariance Ordering، Basis و Units باید پیش و پس از Transform صریح و قابل‌تطبیق باشند.

P06-CON-065 — Angular، Distance، Time، Velocity، Acceleration، Area، Mass و Probability Unitها هرگز از Magnitude یا Field Name استنتاج نمی‌شوند.

P06-CON-066 — SI یا Domain Unit فقط وقتی قابل‌مصرف است که Unit ID و Lossless/Bounded Conversion Rule Adopted باشد.

P06-CON-067 — Orbital Elements باید Element Set، Central Body، Frame، Epoch، Angle Convention و Singular/near-singular Handling را ثبت کنند.

P06-CON-068 — Cartesian، Keplerian، Equinoctial یا دیگر Representationها نباید بدون Conversion Evidence و Uncertainty Propagation جای هم بنشینند.

P06-CON-069 — Rotation/Attitude Representation در 6-DOF باید Quaternion/Euler/DCM Convention، Normalization و Singularity Handling را ثبت کند؛ Basilisk Role این Requirement را فعال می‌کند اما Qualify نمی‌کند.

P06-CON-070 — Constant Set و Gravity/Earth Model بخشی از Convention/Profile است و Silent Default مجاز نیست.

P06-CON-071 — Frame/Unit Round-trip باید Expected Loss و Tolerance Predeclared داشته باشد؛ Exact Equality فقط در صورت Applicability لازم است.

P06-CON-072 — Transform Chain باید Intermediate Frames و Data Versions را حفظ یا با یک Profile Proven-equivalent Replace کند.

P06-CON-073 — Encounter-plane Mapping باید Relative State، Plane Definition، Basis، Covariance Mapping و Degeneracy Handling را ثبت کند.

P06-CON-074 — Display Layer می‌تواند Unit/Frame را تبدیل کند اما Source Artifact، Original Context، Rounding و Conversion Evidence باید باقی بمانند.

P06-CON-075 — Frame/Convention Conflict باید Domain-scientific Review و Explicit Disposition دریافت کند؛ Compiler یا UI حق انتخاب Silent ندارد.

P06-CON-076 — Adapterهای Engine-specific باید Canonical Frame/Unit/Convention را با Versioned Loss Analysis Map کنند.

P06-DEN-032 — Frame Aliasهای مبهم و Environment/Engine Defaultهای Hidden ممنوع‌اند.

P06-DEN-033 — Degree/Radian، km/m، s/day، probability/percent یا Coordinate Order نباید از Context حدس زده شود.

P06-DEN-034 — Identity Transform نباید برای Unknown Frame یا Missing Epoch استفاده شود.

P06-DEN-035 — Covariance نباید مانند State Vector بدون Jacobian/Basis Transform شود.

P06-DEN-036 — Conversion موفق بدون Validity/Precision Evidence نباید `lossless` نامیده شود.

P06-DEN-037 — Visualization Frame نباید Canonical Analysis Frame یا Source Truth را Silent Replace کند.

P06-DEN-038 — Engine-native Field Name به‌تنهایی Canonical Semantic Contract نیست.

P06-FAIL-014 — Frame مفقود/Unsupported نتیجه `SCI_FRAME_MISSING_OR_UNSUPPORTED` دارد.

P06-FAIL-015 — Unit ناشناخته/ناسازگار نتیجه `SCI_UNIT_UNKNOWN` یا `SCIENTIFIC_DIMENSION_MISMATCH` دارد.

P06-FAIL-016 — Transform Profile/Validity نامعتبر نتیجه `SCIENTIFIC_TRANSFORM_INVALID` دارد.

P06-FAIL-017 — Covariance Transform ناسازگار نتیجه `SCI_COVARIANCE_INVALID` دارد.

P06-FAIL-018 — Convention Conflict حل‌نشده نتیجه `SCIENTIFIC_CONVENTION_CONFLICTED — INDETERMINATE` دارد.

## 8. Scientific Request Envelope

P06-REQ-011 — هر Computation Intent باید پیش از اجرا به Scientific Request Engine-agnostic، Digest-bound، Immutable و قابل‌اعتبارسنجی تبدیل شود:

~~~yaml
scientific_request_id:
request_type: PROPAGATE|ESTIMATE|TRANSFORM|EPHEMERIS|SCREEN_CONJUNCTION|COMPUTE_PC|SCENARIO|VERIFY
request_schema_version:
generic_request_or_application_command_reference:
object_references: []
input_artifact_digests: []
epoch_and_time_contract:
frame_contract:
unit_contract:
uncertainty_contract:
algorithm_profile_id:
force_model_profile_id:
estimator_profile_id:
auxiliary_data_snapshot:
precision_and_tolerance_profile:
validity_domain:
resource_and_deadline_envelope:
independence_requirement:
requested_output_contract:
effect_and_authority_context_reference:
workflow_reference:
request_digest:
~~~

P06-DEF-014 — `ScientificRequest` Domain Payload برای محاسبۀ مشخص است؛ Approval، AuthorizationDecision، ExecutionLease یا Evidence انجام محاسبه نیست.

P06-CON-077 — Request Type باید Closed/Versioned Vocabulary باشد؛ Free-form Operation یا Generic Code/Tool Instruction Scientific Request معتبر نیست.

P06-CON-078 — Generic Request/ApplicationCommand Reference باید Semantics P03 را حفظ کند و Domain Payload P06 را با Transport/Authority ادغام نکند.

P06-CON-079 — Input Artifactها باید Exact Digest، Schema Version و Status داشته باشند؛ Query Result موقت بدون Snapshot کافی نیست.

P06-CON-080 — Algorithm/Force/Estimator Profile باید برای Request Type و Intended Use Applicable باشد؛ Presence ID به معنی Approved/Qualified بودن نیست.

P06-CON-081 — Uncertainty Contract باید Source، Representation، Confidence Meaning، Correlation Assumption و Propagation Expectation را تعیین کند.

P06-CON-082 — Resource/Deadline Envelope می‌تواند Limit ایجاد کند؛ حق کاهش Profile، حذف Verification یا جعل Convergence ندارد.

P06-CON-083 — Independence Requirement باید پیش از Result، Dimensions و Minimum Evidence را مشخص کند.

P06-CON-084 — Requested Output باید Schema، Epoch/Grid، Frame، Unit، Precision، Artifact Class، Status Set و Limitation Handling را تعیین کند.

P06-CON-085 — Request Digest باید پس از Canonicalization تمام Scientific Inputs و Applicable Context را Bind کند.

P06-CON-086 — Material تغییر Request، Input Revision، Profile، Auxiliary Snapshot، Tolerance، Engine Mapping یا Intended Use Request تازه/Revision تازه می‌خواهد.

P06-CON-087 — AI می‌تواند Draft Request یا Missing-field Finding پیشنهاد کند؛ هیچ Field علمی مفقود را Authoritative پر، Profile را کاهش یا Request را Self-approve نمی‌کند.

P06-CON-088 — Effect/Authority Context P05، Workflow P04 و Authorization/Lease P03/P11 خارج از Scientific Validity اما قبل از هر Effectful Execution مستقل لازم‌اند.

P06-CON-089 — `VERIFY` Request باید Claim/Artifact، Verification Profile، Independence Dimensions، Oracle/Tolerance Reference و Expected Discrepancy Handling را Bind کند.

P06-CON-090 — Scientific Request Completion فقط Syntactic/Contract Readiness است و هیچ Result یا Validity ایجاد نمی‌کند.

P06-DEN-039 — Client، Model، Tool یا Engine نباید Server/Policy-resolved Profile، Context یا Effect را Downgrade کند.

P06-DEN-040 — Missing Scientific Value نباید با Default Engine Setting یا Prompt Completion پر شود.

P06-DEN-041 — Deadline/Cost Pressure نباید Tolerance، Verification یا Validity Domain را پس از Unblinding تغییر دهد.

P06-DEN-042 — Request ID یا Digest نباید میان Input/Scopeهای متفاوت Reuse شود.

P06-DEN-043 — Scientific Request نباید Arbitrary Shell، Code، SQL، URL، Uplink یا Generic Tool Payload حمل کند.

P06-DEN-044 — `SCENARIO` یا `VERIFY` Request هیچ Command/Execution Route برای Spacecraft ایجاد نمی‌کند.

P06-FAIL-019 — Invalid Request Schema نتیجه `SCIENTIFIC_REQUEST_INVALID — DO_NOT_EXECUTE` دارد.

P06-FAIL-020 — Unbound Input/Profile نتیجه `SCI_PROFILE_UNAPPROVED_OR_UNRESOLVED` و Block متناسب دارد.

P06-FAIL-021 — Request Digest Mismatch نتیجه `SCIENTIFIC_REQUEST_DIGEST_MISMATCH — REJECT` دارد.

P06-FAIL-022 — Prohibited Payload نتیجه `SCI_COMMAND_PATH_PROHIBITED — E9/APR-X/INC-0/HARD_DENY` دارد.

## 9. Scientific Result Envelope و Status Semantics

P06-REQ-012 — هر Output محاسباتی باید به Scientific Result Engine-agnostic با Status صریح، Evidence، Uncertainty، Validity و Provenance تبدیل شود:

~~~yaml
scientific_result_id:
request_digest:
result_schema_version:
status: VALID|VALID_WITH_LIMITATIONS|NOT_COMPUTABLE|NOT_CONVERGED|DISPUTED|INDETERMINATE|INVALID
result_artifact_reference:
epoch_and_time_contract:
frame_contract:
unit_contract:
covariance_and_uncertainty:
algorithm_profile_id:
engine_identity_and_digest:
configuration_digest:
auxiliary_data_snapshot:
precision_and_tolerance_evidence:
convergence_evidence:
validity_domain:
independent_verification_status:
discrepancy_record_references: []
limitations: []
provenance_reference:
execution_receipt_references: []
result_digest:
~~~

P06-DEF-015 — `ScientificResult` Claim/Evidence Artifact است؛ ExecutionReceipt فقط وقوع Attempt را گزارش می‌کند و ValidatedOutcome/Decision Record جدا می‌ماند.

P06-CON-091 — Result باید Exact Request Digest را Bind کند؛ Orphan Output یا Result مربوط به Request Revision دیگر معتبر نیست.

P06-CON-092 — `VALID` فقط با Context کامل، Convergence قابل‌قبول، Domain/Tolerance رعایت‌شده، Evidence کافی و نبود Invalidating Discrepancy در Scope قابل‌اعمال است.

P06-CON-093 — `VALID_WITH_LIMITATIONS` باید Limitation، Impacted Use، Residual Uncertainty و Blocked Promotion Level را صریح حمل کند.

P06-CON-094 — `NOT_COMPUTABLE` یعنی Preconditions/Data/Method برای Result کافی نیست؛ نباید به Zero یا No-risk تفسیر شود.

P06-CON-095 — `NOT_CONVERGED` Outcome علمی مستقل است؛ آخرین Iteration یا Best-so-far Result فقط با Label Exploratory و بدون Promotion ممکن است حفظ شود.

P06-CON-096 — `DISPUTED` نیازمند Discrepancy Record، Competing Results، Shared Dependencies، Impact و Route به Review است.

P06-CON-097 — `INDETERMINATE` وقتی Truth/Validity از Evidence موجود Resolve نمی‌شود حفظ می‌گردد و هر Use requiring determinate status Block می‌شود.

P06-CON-098 — `INVALID` باید Reason/Failure Code، Affected Scope و Evidence را حفظ کند؛ Deletion یا Silent Recompute ممنوع است.

P06-CON-099 — Precision/Tolerance Evidence باید Actual Observed Metrics، Denominator/Population و Predeclared Rules را از Configuration جدا کند.

P06-CON-100 — Convergence Evidence حداقل Iterations، Residual/Objective History، Stopping Rule، Conditioning/Warnings و Failure/Restart History را در حد Applicability حفظ می‌کند.

P06-CON-101 — Result Artifact، Configuration Digest، Auxiliary Snapshot و Engine Build باید Immutable-linked و Reconstructable باشند.

P06-CON-102 — Independent Verification Status بدون Verification Artifact/Dimensions/Discrepancy Record نباید `VERIFIED` نمایش داده شود.

P06-CON-103 — Result Revision تازه باید Supersedes/Superseded-by Link و Reason داشته باشد؛ Original History Immutable می‌ماند.

P06-CON-104 — Result Presentation باید Original Status، Uncertainty، Limitations و Validity Domain را در Human و Machine Views حفظ کند.

P06-CON-105 — Result Receipt، Queue Ack، File Write، HTTP 200 یا Engine Success Code به‌تنهایی Scientific Validity نیست.

P06-DEN-045 — Failure State با Zero، Nominal، Average، Prior Result، Default یا LLM Estimate جایگزین نمی‌شود.

P06-DEN-046 — Error/Warning Log نباید از Result Artifact جدا و دورریختنی باشد اگر بر Validity اثر دارد.

P06-DEN-047 — Result بدون Uncertainty نباید با Point Estimate تنها برای Risk/Promotion مصرف شود مگر Profile صریحاً آن Use را Limited و Non-authoritative تعریف کند.

P06-DEN-048 — Display Rounding نباید Threshold Crossing یا Scientific Status را تغییر دهد.

P06-DEN-049 — Result از Engine متفاوت نباید فقط به دلیل نزدیک‌بودن Output Equivalent اعلام شود.

P06-DEN-050 — Human Selection از میان Results نباید Discrepancy را حذف یا Independence جعل کند.

P06-DEN-051 — Scientific Result هیچ Approval، Lease، Maneuver Decision یا Command ایجاد نمی‌کند.

P06-FAIL-023 — Result/Request Mismatch نتیجه `SCIENTIFIC_RESULT_ORPHANED — INVALID` دارد.

P06-FAIL-024 — Missing Status/Evidence نتیجه `SCIENTIFIC_RESULT_ENVELOPE_INCOMPLETE` دارد.

P06-FAIL-025 — Non-finite/NaN/Inf یا Numerical Exception نامدیریت‌شده نتیجه `SCI_NUMERICAL_INSTABILITY — INVALID_OR_NOT_COMPUTABLE` دارد.

P06-FAIL-026 — Convergence Claim بدون Evidence نتیجه `SCI_NOT_CONVERGED_OR_UNPROVEN` دارد.

P06-FAIL-027 — Status/Presentation Drift نتیجه `SCIENTIFIC_PRESENTATION_MISREPRESENTATION — BLOCK` دارد.

## 10. مرز Engine-agnostic و نقش Engineها

P06-REQ-013 — Canonical Scientific Request/Result باید مستقل از API، Object Model و Defaultهای هر Engine باشد؛ Adapter فقط با Mapping Versioned، Loss-analyzed و Tested قابل‌مصرف آینده است.

| Engine | نقش ثبت‌شده و حفظ‌شده | Anti-claim اجباری |
|---|---|---|
| Orekit | `Primary Operational Astrodynamics Candidate` | نه Qualified، نه Approved، نه Production-fit |
| GMAT | `Independent Verification Candidate` | نام مستقل به‌تنهایی Independence کامل نیست |
| Tudat/TudatPy | `Research and Comparative Analysis` | Research Output خودکار Canonical نیست |
| Basilisk | `6-DOF and Advanced Dynamics Simulation` | هیچ Flight-control/Command Route مجاز نیست |

P06-CON-106 — نقش‌های بالا Technology Status ثبت‌شده‌اند و این Part آن‌ها را Promote، Downgrade، Freeze یا Replace نمی‌کند.

P06-CON-107 — Engine Name، Popularity، Vendor، Open-source Status، Prior Success یا Citation Count Qualification نیست.

P06-CON-108 — Exact Version، Build، Dependencies، Compiler/Runtime، Numerical Libraries، Constants، Data Files، Platform، Profile و Configuration باید Identity قابل‌حل داشته باشند.

P06-CON-109 — Adapter Mapping باید Field-by-field Semantic Mapping، Unit/Frame/Time Conversion، Default Override، Unsupported Feature، Precision Loss و Failure Translation را ثبت کند.

P06-CON-110 — Engine Default فقط اگر در Adopted Profile صریح، Versioned، Evidence-bound و Review‌شده باشد قابل‌مصرف است.

P06-CON-111 — Qualification در یک Profile/Use/Build به Engine Family یا Version دیگر منتقل نمی‌شود.

P06-CON-112 — Engine Replacement باید Contract Conformance، Equivalence Class، Regression/Challenge Evidence و Discrepancy Analysis تازه داشته باشد.

P06-CON-113 — Independent Verification با GMAT فقط وقتی ادعاپذیر است که Dimensions استقلال، Shared Dependencies و Configuration Validation صریح باشند.

P06-CON-114 — استفاده از دو Wrapper، دو Process، دو Container یا دو Adapter روی یک Engine استقلال Codebase ایجاد نمی‌کند.

P06-CON-115 — Shared Constants، EOP، Gravity Model، Atmosphere، Initial State، Covariance یا Preprocessor می‌توانند Common-cause Risk ایجاد کنند و باید ثبت شوند.

P06-CON-116 — Engine Error Code باید به Scientific Status بدون Semantic Loss Map شود؛ Success Code به `VALID` تبدیل خودکار نمی‌شود.

P06-CON-117 — Performance/Capacity Constraints متعلق به P12 است و نمی‌تواند Fidelity/Verification را Silent Downgrade کند.

P06-CON-118 — Tool/Plugin Supply-chain Qualification متعلق به P08/P11/P13/P15 است؛ P06 فقط Scientific Conformance Need را تحویل می‌دهد.

P06-CON-119 — هیچ Engine Adapter نباید Generic Invocation، Arbitrary Code یا External Command Channel ایجاد کند.

P06-CON-120 — Basilisk 6-DOF Output فقط Simulation/Analysis Artifact زمینی است و هیچ On-orbit Runtime یا Flight-control Authority ایجاد نمی‌کند.

P06-DEN-052 — Engine Role نباید به Procurement Selection، Exclusive Architecture یا Production Approval تفسیر شود.

P06-DEN-053 — Engine-native Schema نباید Canonical Contract را Replace کند.

P06-DEN-054 — Default Parameter، Auto-detected Unit/Frame یا Silent Fallback ممنوع است.

P06-DEN-055 — Same Engine در دو Configuration بدون Independence Profile، Independent Verification نیست.

P06-DEN-056 — Benchmark Speed/Throughput Scientific Accuracy یا Qualification را ثابت نمی‌کند.

P06-DEN-057 — Engine Disagreement با Average کردن Outputs یا انتخاب Preferred Engine بدون Evidence حل نمی‌شود.

P06-DEN-058 — هیچ Engine، Adapter یا Simulation Mode حق تولید Telecommand/Uplink/Flight-control Payload ندارد.

P06-FAIL-028 — Engine Identity/Build نامشخص نتیجه `SCI_ENGINE_UNQUALIFIED_OR_UNRESOLVED` دارد.

P06-FAIL-029 — Adapter Semantic Loss حل‌نشده نتیجه `SCIENTIFIC_ADAPTER_MAPPING_INVALID` دارد.

P06-FAIL-030 — Hidden Default یا Unsupported Feature نتیجه `SCIENTIFIC_ENGINE_PROFILE_CONFLICTED` دارد.

P06-FAIL-031 — Command-enabling Engine Path نتیجه `SCI_COMMAND_PATH_PROHIBITED — E9/APR-X/INC-0/HARD_STOP` دارد.

## 11. Propagation، Force-model Profile و Fidelity Tier

P06-REQ-014 — هر Propagation باید Initial State/Covariance، Time/Frame/Unit Context، Force-model Profile، Auxiliary Snapshot، Integrator/Numerical Profile، Output Contract و Validity Domain را به Request و Result Bind کند.

P06-REQ-015 — محور `T0..T4` فقط Fidelity/Assurance Profile برای Intended Use است و Universal Accuracy، Ranking مطلق، Qualification یا Permission ایجاد نمی‌کند:

| Tier | Intended Use | حداقل Characteristic | Limitation اجباری |
|---:|---|---|---|
| `T0` | Coarse Screening / Research | Simplified Model | Assumptionها و Exclusionها صریح |
| `T1` | Routine Catalog-scale Screening | Bounded Operational Profile و Validated Domain موردنیاز | Validation واقعی باید جدا اثبات شود |
| `T2` | Refined Analysis | Higher-fidelity Force/Auxiliary Profile و Stronger Uncertainty Handling | هزینه/پیچیدگی جای Evidence نیست |
| `T3` | High-consequence Assessment | Independent Verification، Sensitivity و Discrepancy Analysis | Material Discrepancy Promotion را Block می‌کند |
| `T4` | Specialized Research / High-fidelity Simulation | Case-specific Model، Expert Review و Strict Validity Envelope | Result به Case دقیق محدود است |

P06-DEF-016 — `PropagationProfile` Contract Versioned برای Dynamics، Force Terms، Constants، Auxiliary Data، Numerical Method، Tolerance، Step Control، Event Detection، Output Grid و Validity Domain است.

P06-DEF-017 — `ForceModelProfile` فهرست Explicit از Included/Excluded Forces، Model/Order/Degree، Data Sources، Parameter Values/Uncertainty و Applicability است؛ Label Tier جای آن را نمی‌گیرد.

P06-CON-121 — Tier Selection باید از Intended Decision، Orbit Regime، Time Horizon، Data Quality، Uncertainty، Sensitivity، Risk/Effect، Cost و Required Assurance مشتق و ثبت شود.

P06-CON-122 — Tier بالاتر همیشه بهتر نیست؛ Model Complexity نامتناسب می‌تواند Conditioning، Parameter Identifiability، Cost یا Reproducibility را بدتر کند.

P06-CON-123 — Initial State باید Revision، Epoch، Frame، Units، Covariance/Uncertainty، Authority Status و Provenance داشته باشد.

P06-CON-124 — Force Terms حداقل Central Gravity، Non-spherical Gravity، Third-body، Drag، Solar Radiation Pressure و Relativistic/Other Applicable Effects را با Include/Exclude Rationale ارزیابی می‌کنند؛ این فهرست انتخاب Profile واقعی نیست.

P06-CON-125 — Atmosphere، Space Weather، Solar/Geomagnetic Index، Area/Mass/Drag/SRP Coefficient و Attitude Assumption باید Source، Version، Uncertainty و Validity داشته باشند اگر Applicable باشند.

P06-CON-126 — Integrator/Propagator Method، Step Policy، Absolute/Relative Tolerance، Event Detection، Interpolation و Precision باید صریح باشند.

P06-CON-127 — Output Sampling/Grid و Interpolation Artifact باید از Integration Steps جدا و دارای Error/Validity Evidence باشند.

P06-CON-128 — Propagation Horizon باید بر اساس Model/Data Validity و Uncertainty Growth محدود شود؛ Horizon طولانی بدون Evidence نباید Valid باقی بماند.

P06-CON-129 — Covariance/Uncertainty Propagation Method باید Profile-bound باشد و Assumptionهای Linearity، Process Noise، Correlation و Numerical Stabilization را ثبت کند.

P06-CON-130 — Eventهای Discontinuity، Maneuver Hypothesis، Shadow Boundary، Atmospheric Regime یا Data Gap باید Explicitly Modeled یا Limitation شوند.

P06-CON-131 — Force-model Change یا Auxiliary Revision Result Revision تازه می‌سازد؛ Output قدیمی Silent Overwrite نمی‌شود.

P06-CON-132 — Sensitivity Analysis باید Parameters/Range، Sampling/Method، Output Metrics و Decision Relevance را Predeclare کند.

P06-CON-133 — Model Truncation Error، Numerical Error، Input Uncertainty و Epistemic Assumption باید تا حد ممکن از هم جدا گزارش شوند.

P06-CON-134 — Comparison با Reference Ephemeris باید Source Authority، Frame/Time/Unit Alignment، Tolerance و Correlation را کنترل کند.

P06-CON-135 — Propagated State یک Derived Scientific Artifact است و Current Authoritative State را خودکار Replace نمی‌کند.

P06-CON-136 — Batch/Catalog Propagation باید Per-object Failure و Aggregate Completeness/Denominator را حفظ کند؛ Partial Success نباید 100% معرفی شود.

P06-CON-137 — Graceful Degradation فقط می‌تواند Horizon، Resolution، Use Scope یا Confidence را کاهش و Limitation را آشکار کند؛ Truth/Authority را افزایش نمی‌دهد.

P06-CON-138 — Tier Downgrade در Runtime به‌علت Cost/Deadline فقط با Policy/Workflow Pause، Explicit Reclassification و Result Status محدود ممکن است؛ Silent Fallback ممنوع است.

P06-CON-139 — Propagation Run باید Deterministic Inputs/Seeds یا Stochastic Protocol، Resource/Platform Evidence و Complete Result Manifest را نگه دارد.

P06-CON-140 — هیچ Propagation/Simulation Output یا Maneuver Hypothesis به Spacecraft Command، Flight Dynamics System یا Uplink Route متصل نمی‌شود.

P06-DEN-059 — Tier Number نباید Accuracy Percentage یا Confidence Probability تفسیر شود.

P06-DEN-060 — `T3/T4` نباید بدون Independent Evidence یا Expert Review مربوط به Case ادعا شود.

P06-DEN-061 — Simplified Model نباید خارج از Declared Screening/Research Use برای High-impact Promotion مصرف شود.

P06-DEN-062 — Missing Force/Auxiliary Data نباید با Engine Default پنهان شود.

P06-DEN-063 — Propagation Disagreement نباید با Average، Preferred-engine Override یا Longest Runtime حل شود.

P06-DEN-064 — Precision Display نباید Numerical/Model Error را کوچک‌تر نشان دهد.

P06-DEN-065 — Propagation Success هیچ Maneuver Recommendation، Approval یا Execution Authority ایجاد نمی‌کند.

P06-FAIL-032 — Initial Context نامعتبر نتیجه `PROPAGATION_INPUT_INVALID — NOT_COMPUTABLE` دارد.

P06-FAIL-033 — Force/Profile خارج از Validity Domain نتیجه `SCI_VALIDITY_DOMAIN_EXCEEDED` دارد.

P06-FAIL-034 — Integrator Instability/Step Failure نتیجه `SCI_NUMERICAL_INSTABILITY` یا `SCI_NOT_CONVERGED` دارد.

P06-FAIL-035 — Unbounded Uncertainty Growth نتیجه `PROPAGATION_UNCERTAINTY_UNBOUNDED — INDETERMINATE` دارد.

P06-FAIL-036 — Silent Tier/Profile Fallback نتیجه `SCIENTIFIC_PROFILE_DOWNGRADE_VIOLATION` دارد.

## 12. Orbit Determination، State Estimation و Covariance

P06-REQ-016 — Orbit Determination/State Estimation باید Observation Selection، Association، Weighting، Bias، Rejection، Dynamics، Estimator، Prior، Process Noise، Convergence، Residual، Conditioning و Sensitivity را Versioned و Evidence-bound کند.

P06-REQ-017 — Covariance/Uncertainty Metadata اختیاری نیست؛ Epoch، Frame، Basis، Ordering، Units، Confidence Interpretation، Correlation، Provenance و Numerical Health باید صریح باشند.

P06-REQ-018 — Estimated State، Hypothesis/Track، Candidate Association و Current Authoritative State باید تا Promotion معتبر جدا بمانند و هر Promotion به P05/P03/P04/P13 Bind شود.

P06-DEF-018 — `ObservationUseManifest` فهرست Immutable از Observation Revisionها، Included/Excluded State، Weight، Bias Correction، Rejection Reason، Quality و Provenance است.

P06-DEF-019 — `EstimationProfile` Algorithm، State/Parameter Vector، Dynamics، Measurement Models، Prior، Noise Models، Robustness/Outlier Rules، Convergence و Output Uncertainty Contract را Version می‌کند.

P06-DEF-020 — `CovarianceContract` Matrix Meaning، Epoch، Frame، Coordinate Basis، State Ordering، Units، Confidence/Scaling، Correlation Scope، PSD/Conditioning Status و Provenance را ثبت می‌کند.

P06-CON-141 — Observation Identity باید Sensor/Source، Epoch/Scale، Measurement Type/Unit، Frame، Calibration/Quality، Rights/Provenance و Revision را حفظ کند.

P06-CON-142 — Observation Selection/Exclusion باید Rule، Operator/Process، Reason و Impact Evidence داشته باشد؛ Cherry-picking ممنوع است.

P06-CON-143 — Weight، Bias و Outlier Handling باید پیش از Unblinded Outcome یا با Controlled Revision/Disclosure تعیین شوند.

P06-CON-144 — Multiple Hypotheses/Tracks تا وقتی Association Evidence کافی نیست Distinct و دارای Probability/Uncertainty Semantics صریح باقی می‌مانند.

P06-CON-145 — State Vector/Estimated Parameters و Covariance Ordering باید One-to-one و Machine-validatable باشند.

P06-CON-146 — Residualها باید Observation Type/Source، Pre/post-fit، Unit، Whitening/Normalization، Time Ordering و Exclusion را قابل‌حل کنند.

P06-CON-147 — Convergence Evidence باید Stopping Rule، Iterations، Objective/Residual Evolution، Parameter Update، Conditioning و Warningها را نگه دارد.

P06-CON-148 — Convergence عددی به Minimum محلی یا Stable Iteration لزوماً Scientific Validity یا Identifiability نیست.

P06-CON-149 — Covariance باید Symmetry، Finiteness، Positive-semidefinite/Definiteness Applicable، Conditioning و Scale Checks داشته باشد.

P06-CON-150 — Numerical Repair مانند Symmetrization، Eigenvalue Clipping، Jitter یا Regularization باید Method/Amount/Impact را ثبت و Result را محدود کند.

P06-CON-151 — Covariance Transform باید Jacobian/Method، Linearization Point، Frame/Basis/Unit Mapping و Approximation Validity را ثبت کند.

P06-CON-152 — Marginal/Conditional Covariance، Information Matrix، Normal Matrix، Ensemble Spread و Sample Covariance نباید بدون Type Label یکسان تلقی شوند.

P06-CON-153 — Confidence Level/Probability Content برای Ellipsoid/Interval باید Dimension، Distribution/Assumption و Scaling Convention داشته باشد.

P06-CON-154 — Cross-object/measurement/parameter Correlation باید در صورت Materiality حفظ شود؛ فرض Independence باید Explicit و Evidence/Limitations داشته باشد.

P06-CON-155 — Process Noise و Model-error Treatment بخشی از Estimation Profile است و با Measurement Noise ادغام مبهم نمی‌شود.

P06-CON-156 — Prior/Initial Covariance Source، Authority، Age، Frame/Epoch و Transformation History باید ثبت شود.

P06-CON-157 — Missing Uncertainty فقط با Assumption Profile صریح، Non-authoritative Label و Use محدود قابل Exploration است و هرگز Default Canonical Covariance نمی‌شود.

P06-CON-158 — Estimated State Revision باید Observation Cutoff، Solution Epoch، Fit Span، Predict Span و Supersession Chain داشته باشد.

P06-CON-159 — Comparison Solutions باید Input-set Overlap و Shared Bias/Common-cause Sources را آشکار کنند.

P06-CON-160 — Filter Smoothing، Batch Estimation، Sequential Estimation یا Hybrid Method باید Output Semantics/Latency/Correlation خاص خود را حفظ کند.

P06-CON-161 — Catalog-scale Estimation باید Per-object Status، Missing/Failed Population و Denominator Contract را نگه دارد.

P06-CON-162 — Authoritative Promotion فقط پس از Scientific Evidence، Independent Verification متناسب، Workflow/Human Review و Authority Gates جدا ممکن است؛ این Part آن را انجام نمی‌دهد.

P06-CON-163 — Counterevidence یا New Observation ممکن است State را Supersede کند؛ Prior Artifact حذف یا Backdated نمی‌شود.

P06-CON-164 — Covariance/State Consistency باید در هر Transform، Propagation، Association و Conjunction Step قابل Trace باشد.

P06-CON-165 — Uncertainty باید در Explanation/Visualization نیز قابل‌مشاهده باشد؛ Point-only Display برای High-impact Use ممنوع است.

P06-DEN-066 — Default Covariance بدون Explicit Assumption Profile و Non-authoritative Label ممنوع است.

P06-DEN-067 — Residual کم به‌تنهایی Correct Model، Calibrated Uncertainty یا Valid State را ثابت نمی‌کند.

P06-DEN-068 — Outlier Rejection نباید برای رسیدن به Desired Result بدون Predeclared Rule انجام شود.

P06-DEN-069 — PSD Repair نباید Original Invalidity یا Repair Magnitude را پنهان کند.

P06-DEN-070 — Covariance با Frame/Epoch/Ordering نامعلوم نباید مصرف یا Transform شود.

P06-DEN-071 — Multiple Tracks نباید با Name/Nearest-state Heuristic Silent Merge شوند.

P06-DEN-072 — Estimated State نباید خودکار Current Authoritative State شود.

P06-DEN-073 — Missing Correlation نباید Zero Correlation فرض شود مگر Profile/Limitations صریح.

P06-DEN-074 — Numerical Convergence نباید Validation/Verification/Approval نامیده شود.

P06-DEN-075 — Human Preference نباید Covariance یا Observation Weight را پس از Result بدون Change Record تغییر دهد.

P06-DEN-076 — Estimator Output هیچ Command، Tasking یا Maneuver Execution ایجاد نمی‌کند.

P06-FAIL-037 — Covariance Schema/Health نامعتبر نتیجه `SCI_COVARIANCE_INVALID` دارد.

P06-FAIL-038 — Estimator عدم همگرایی نتیجه `SCI_NOT_CONVERGED` دارد و Last Iterate Valid نیست.

P06-FAIL-039 — Observation Association نامعین نتیجه `OD_ASSOCIATION_INDETERMINATE` و حفظ Hypothesisهای جدا دارد.

P06-FAIL-040 — Conditioning/Identifiability نامعتبر نتیجه `OD_SOLUTION_ILL_CONDITIONED — VALID_WITH_LIMITATIONS_OR_INVALID` دارد.

P06-FAIL-041 — State/Covariance Basis Mismatch نتیجه `OD_STATE_COVARIANCE_MISMATCH — INVALID` دارد.

P06-FAIL-042 — Observation Provenance Gap نتیجه `OD_OBSERVATION_PROVENANCE_INCOMPLETE` دارد.

P06-FAIL-043 — Unsupported Promotion نتیجه `SCIENTIFIC_STATE_PROMOTION_BLOCKED` دارد.

P06-FAIL-044 — Track Merge بدون Evidence نتیجه `OD_HYPOTHESIS_CONFLATION — REWORK_REQUIRED` دارد.

## 13. Ephemeris، Trajectory و Digital-twin Scientific State

P06-REQ-019 — هر Ephemeris/Trajectory/Digital-twin Scientific State باید Source Solution، Propagation Profile، Epoch Grid، Time/Frame/Unit/Covariance Context، Validity، Revision و Provenance را حفظ کند.

P06-DEF-021 — `DigitalTwinScientificState` Projection زمان‌مند و Versioned از Observation/Estimate/Propagated/Scenario Artifacts است؛ Physical Reality، Current Authoritative State، Workflow State یا Command State نیست.

P06-CON-166 — Ephemeris باید Start/End، Grid/Interpolation، Frame، Time Scale، Units، State Components، Uncertainty Availability و Generation Profile را ثبت کند.

P06-CON-167 — Sparse Knot/Polynomial/Chebyshev/Other Representation باید Interpolation Method، Order، Segment Boundary، Error Bound و Validity داشته باشد.

P06-CON-168 — Trajectory Nominal، Estimated، Predicted، Reference، Scenario و Postulated باید Distinct Type و Source داشته باشند.

P06-CON-169 — Digital Twin باید Observation Time، Estimate Epoch، Simulation Time و Display Time را جدا نگه دارد.

P06-CON-170 — Twin Update باید Revision/Event-driven باشد و Out-of-order Data را با Source Revision/Causality Reconcile کند؛ Last-arrival-wins ممنوع است.

P06-CON-171 — Twin Confidence/Uncertainty باید با Scientific State همراه و در Time Propagate/Degrade شود.

P06-CON-172 — Twin Projection/Cache قابل Rebuild است و Source Scientific Artifact را Replace نمی‌کند.

P06-CON-173 — Scenario Branch باید Parent State/Digest، Branch Assumptions، Applied Changes و Non-authoritative Status را حفظ کند.

P06-CON-174 — Twin Visualization می‌تواند LOD/Sampling داشته باشد اما Scientific Artifact و Uncertainty را Silent تغییر نمی‌دهد.

P06-CON-175 — Staleness باید نسبت به Use/Orbit Regime/Horizon تعریف و Visible باشد؛ یک TTL عمومی Scientific Validity نیست.

P06-CON-176 — External Ephemeris Compare باید Frame/Time/Unit/Source Authority و Overlap Window را Align کند.

P06-CON-177 — Twin State Promotion یا Publication Effect مستقلی است و به P05/P03/P04/P09/P13 Bind می‌شود.

P06-CON-178 — Digital Twin در Baseline فقط Terrestrial Decision Support است و On-orbit Runtime Deferred باقی می‌ماند.

P06-DEN-077 — Digital Twin نباید با Physical Truth، Flight Software یا Command Authority یکی دانسته شود.

P06-DEN-078 — Visualization Smoothness یا Animation Continuity Accuracy/Validity را ثابت نمی‌کند.

P06-DEN-079 — Interpolation خارج از Segment/Validity Domain ممنوع است مگر Result صریح Extrapolated/Limited باشد.

P06-DEN-080 — Stale Twin State نباید Current یا Ready نمایش داده شود.

P06-DEN-081 — Scenario Branch نباید Canonical State را Silent Replace کند.

P06-DEN-082 — Twin Event یا State Change هیچ Spacecraft Effect ایجاد نمی‌کند.

P06-FAIL-045 — Ephemeris Context ناقص نتیجه `EPHEMERIS_CONTRACT_INVALID` دارد.

P06-FAIL-046 — Interpolation Error/Domain Breach نتیجه `EPHEMERIS_VALIDITY_EXCEEDED` دارد.

P06-FAIL-047 — Twin Source/Projection Conflict نتیجه `DIGITAL_TWIN_STATE_CONFLICTED — RECONCILE` دارد.

P06-FAIL-048 — Twin-to-command Coupling نتیجه `SCI_COMMAND_PATH_PROHIBITED — INC-0/HARD_STOP` دارد.

## 14. Conjunction، Encounter Geometry، HBR و Collision Probability

P06-REQ-020 — هر Conjunction Product باید Object Identity/Revision، Screening Configuration، TCA/Geometry، Relative State/Frame، Covariance Sources/Mapping، HBR Profile، `Pc` Method، Numerical Status، Sensitivity، Limitations و Independent Verification را حفظ کند.

P06-REQ-021 — Threshold Crossing فقط Analytical/Human-review Workflow را Trigger می‌کند؛ Recommendation، Decision، Approval، Maneuver Execution یا Command را خودکار ایجاد نمی‌کند.

P06-DEF-022 — `ConjunctionAssessment` Artifact Versioned برای یک Primary/Secondary Pair، Exact Revisions، Screening Run/Profile و Time Window است.

P06-DEF-023 — `HardBodyRadiusProfile` Source، Geometry Model، Object-specific/Combined Radius، Orientation/Assumption، Units، Uncertainty و Validity را ثبت می‌کند.

P06-DEF-024 — `CollisionProbabilityResult` Result شرطی بر Relative State، Covariance، Encounter Mapping، HBR، Probability Method و Assumptions دقیق است؛ Risk/Decision کلی نیست.

P06-CON-179 — Primary/Secondary Object IDs و Catalog/Source Revisions باید Stable و Exact باشند؛ Name-only Identity کافی نیست.

P06-CON-180 — Screening Window، Spatial/Probability/Miss-distance Threshold، Candidate-generation Method و Completeness/Denominator باید Versioned باشند.

P06-CON-181 — TCA باید Time Scale، Precision، Uncertainty، Search/Optimization Method و Validity Window داشته باشد.

P06-CON-182 — Encounter Geometry باید Relative Position/Velocity، Frame، Basis، Angle/Plane Definition، Units و Degenerate-case Status را ثبت کند.

P06-CON-183 — Covariance هر Object باید Source Solution، Epoch، Frame/Basis/Ordering، Propagation Method و Health/Confidence را حفظ کند.

P06-CON-184 — Covariance Correlation/Shared Observation یا Common Catalog Source باید ارزیابی و Assumptionها صریح باشند.

P06-CON-185 — Encounter-plane Mapping باید Jacobian/Method، Linearization/Approximation، Conditioning و Dimensional Reduction را ثبت کند.

P06-CON-186 — HBR باید Source/Profile و Uncertainty داشته باشد؛ Constant Global Default برای Canonical `Pc` بدون Approved Profile معتبر نیست.

P06-CON-187 — `Pc` Method باید Distribution، Integration/Approximation، Dimensional Assumption، Numerical Tolerance و Edge-case Handling را ثبت کند.

P06-CON-188 — Miss Distance، `Pc`، Covariance Quality، Time to TCA، Sensitivity و Consequence مفاهیم جدا هستند و هیچ‌یک به‌تنهایی Collision Risk کلی نیست.

P06-CON-189 — `Pc` بدون Covariance، Method و HBR Context نامعتبر است حتی اگر عدد در Range `[0,1]` باشد.

P06-CON-190 — Probability Unit باید Fraction یا Percent صریح باشد؛ Conversion/Display نباید Threshold را تغییر دهد.

P06-CON-191 — Small/Zero `Pc` ممکن است از Missing/Underestimated Covariance یا Numerical Failure ناشی شود و به‌تنهایی Safety Evidence نیست.

P06-CON-192 — Sensitivity باید به Covariance Scaling/Orientation، HBR، TCA، Relative State، Method و Data Revision در حد Applicability پرداخته و Range را گزارش کند.

P06-CON-193 — Multiple `Pc` Methods باید Method-specific Resultهای جدا و Discrepancy Record داشته باشند؛ Average یک Canonical `Pc` نیست.

P06-CON-194 — Screening Candidate، Refined Assessment، Verified Assessment و Decision-support Publication Revision/Statusهای مستقل‌اند.

P06-CON-195 — High-consequence Assessment حداقل Tier/Confidence مناسب، Independent Verification Profile و Material-discrepancy Gate می‌خواهد؛ Exact Threshold/Policy توسط Owners مربوط تعیین می‌شود.

P06-CON-196 — Re-screening با New Orbit/Covariance/Auxiliary Data Artifact تازه می‌سازد و Prior Alert History را حفظ می‌کند.

P06-CON-197 — False Positive/Negative، Missed Pair و Catalog Coverage باید با Denominator Contract P12/P13 قابل سنجش باشند؛ Sampled Success Rate کافی نیست.

P06-CON-198 — Recommendation باید Scientific Inputs/Uncertainty را Reference کند اما Record جدا تحت P03/P05/P04/P07/P17 باقی بماند.

P06-CON-199 — Decision Maker می‌تواند Risk/Operational Constraints را اعمال کند اما نباید Scientific Result را Rewrite کند.

P06-CON-200 — Conjunction Event باید Base Event Envelope P01 و `EVT-SCI` Extension را مصرف کند؛ Event Command نیست.

P06-CON-201 — Out-of-order Assessment باید بر Object Revision/TCA/Run Digest Reconcile شود؛ Latest Arrival برنده نیست.

P06-CON-202 — Public/External Dissemination اثر و Data/Governance Gate جدا دارد و Scientific Validity به‌تنهایی آن را مجاز نمی‌کند.

P06-CON-203 — Maneuver Option Generation فقط Scenario Analysis زمینی است و از Recommendation/Decision/Execution جدا می‌ماند.

P06-CON-204 — No-conjunction Finding فقط برای Exact Screening Window، Catalog Population، Threshold/Profile و Completeness Evidence معتبر است.

P06-CON-205 — Unknown Object/Covariance/Geometry باید Unknown باقی بماند؛ Absence of Computable `Pc` به Zero Risk تبدیل نمی‌شود.

P06-DEN-083 — Miss Distance به‌تنهایی Collision Risk یا Maneuver Need نیست.

P06-DEN-084 — `Pc` بدون Covariance/Method/HBR نامعتبر است.

P06-DEN-085 — Zero/Small `Pc` نباید Safe تفسیر شود اگر Context/Uncertainty نامعتبر یا ناقص است.

P06-DEN-086 — Threshold Crossing نباید Auto-command، Auto-maneuver، Auto-approval یا Risk Acceptance ایجاد کند.

P06-DEN-087 — Covariance دو Object نباید بدون Frame/Epoch Alignment ترکیب شود.

P06-DEN-088 — HBR نباید از Object Type/Name یا Engine Default حدس زده شود.

P06-DEN-089 — Probability Outputs متفاوت نباید Average یا Winner-take-all شوند بدون Predeclared Scientific Rule.

P06-DEN-090 — Alert Closure نباید با Missing Update یا Silence انجام شود.

P06-DEN-091 — No Event/No Candidate نباید No Risk تلقی شود بدون Coverage Evidence.

P06-DEN-092 — Visualization of Encounter نباید Geometry/Uncertainty/Scale را Misrepresent کند.

P06-DEN-093 — Human Concern یا Calmness Scientific `Pc` را تغییر نمی‌دهد.

P06-DEN-094 — External Operator Message یا Maneuver Coordination متعلق به این Part نیست و هیچ ارسال خارجی مجاز نشده است.

P06-DEN-095 — هیچ Schema، Adapter یا Export در P06 نباید Telecommand-compatible Payload بسازد.

P06-FAIL-049 — Conjunction Context ناقص نتیجه `CONJUNCTION_ASSESSMENT_INVALID` دارد.

P06-FAIL-050 — Covariance/Encounter Mapping نامعتبر نتیجه `SCI_COVARIANCE_INVALID` دارد.

P06-FAIL-051 — HBR مفقود/نامعتبر نتیجه `PC_HBR_CONTEXT_MISSING — NOT_COMPUTABLE` دارد.

P06-FAIL-052 — `Pc` Numerical Failure نتیجه `PC_NOT_COMPUTABLE_OR_NUMERICALLY_UNSTABLE` دارد و Zero نمی‌شود.

P06-FAIL-053 — Material Method Disagreement نتیجه `SCI_MATERIAL_DISCREPANCY — PROMOTION_BLOCKED` دارد.

P06-FAIL-054 — Screening Coverage نامعلوم نتیجه `CONJUNCTION_SCREENING_COMPLETENESS_INDETERMINATE` دارد.

P06-FAIL-055 — Threshold-to-execution Coupling نتیجه `SCI_COMMAND_PATH_PROHIBITED — INC-0/HARD_STOP` دارد.

P06-FAIL-056 — Object Revision Mismatch نتیجه `CONJUNCTION_OBJECT_REVISION_CONFLICTED` دارد.

P06-FAIL-057 — Stale Assessment نتیجه `CONJUNCTION_ASSESSMENT_STALE — RECOMPUTE_OR_LIMIT` دارد.

## 15. Scenario و Maneuver Analysis فقط برای Decision Support زمینی

P06-REQ-022 — Scenario/Maneuver Analysis باید Branch-based، Assumption-explicit، Reversible در فضای تحلیلی و کاملاً جدا از Recommendation، Decision، Approval، Authorization، Execution و Spacecraft Command باشد.

P06-DEF-025 — `ScenarioBranch` Derived Scientific Artifact با Parent State Digest، Hypothesis، Parameter Changes، Time Horizon، Profiles، Outputs، Uncertainty، Validity و Non-authoritative Status است.

P06-CON-206 — Baseline/Counterfactual Branchها باید Parent، Delta، Assumption و Input Revision یکسان/متفاوت را صریح کنند.

P06-CON-207 — Maneuver Hypothesis باید Epoch/Window، Delta-v Vector/Frame/Units، Execution-error Model، Constraints و Uncertainty را فقط به‌عنوان Analysis Input ثبت کند.

P06-CON-208 — Fuel/Resource/Operational Constraint اگر Source-bound نیست `UNKNOWN` است و نباید توسط AI یا Typical Value جعل شود.

P06-CON-209 — Scenario Outcome باید Post-scenario Ephemeris/Conjunction/Risk Metrics، Sensitivity، Trade-offs و Limitations را جدا گزارش کند.

P06-CON-210 — Comparison باید Common Baseline، Common Evaluation Window، Aligned Frames/Units، Same/Declared Profiles و Predeclared Decision Metrics داشته باشد.

P06-CON-211 — Optimization Objective/Constraints باید Versioned و Multi-objective Trade-offها Visible باشند؛ یک Scalar Score حقیقت کامل نیست.

P06-CON-212 — Feasible numerically به معنی Operationally feasible، Approved، Safe یا Authorized نیست.

P06-CON-213 — Scenario Rank/Recommendation باید Scientific Result و Uncertainty را Reference کند و AI/Human Decision-support Record جدا باشد.

P06-CON-214 — Scenario Branch هیچ Current State را Mutate نمی‌کند و Promotion فقط با Gateهای مستقل ممکن است.

P06-CON-215 — Maneuver Analysis می‌تواند `T0..T4`/`PHY-C*` را برای Evidence Maturity نشان دهد اما هیچ Autonomy/Approval Class از آن استنتاج نمی‌شود.

P06-CON-216 — High-impact Scenario نیازمند Independent Verification/Discrepancy Analysis متناسب است؛ دقیق‌بودن Threshold به P05/P13/P16 واگذار می‌شود.

P06-CON-217 — Scenario Stochastic/Monte Carlo Run باید Seed/Stream، Distribution، Sample Count/Stopping Rule، Convergence و Confidence Interval را ثبت کند.

P06-CON-218 — Scenario Analysis با Unknown Constraint باید Limited/Indeterminate بماند و Constraint Missing را آشکار کند.

P06-CON-219 — Scenario Artifact باید `ANALYSIS_ONLY — NO_COMMAND_OR_EXECUTION_ROUTE` را Machine-readable حمل کند.

P06-CON-220 — Export برای Visualization/Review نیز نباید Format یا Fields قابل‌مصرف برای Uplink/Flight Control را ایجاد کند.

P06-CON-221 — Cancellation/Retry/Branching Workflow Semantics متعلق به P04 است؛ P06 فقط Scientific Artifact Lineage را تعریف می‌کند.

P06-CON-222 — Scenario Use در Roadmap P17 فقط Context/Plan است و Implementation Authorization ایجاد نمی‌کند.

P06-DEN-096 — Scenario Result نباید Command Plan، Flight Plan، Telecommand یا Executable Maneuver Product نامیده شود.

P06-DEN-097 — Optimal Scenario به‌تنهایی Recommendation/Decision/Approval نیست.

P06-DEN-098 — Missing Operational Constraint نباید Zero/Unlimited فرض شود.

P06-DEN-099 — AI نباید Delta-v، Epoch یا Constraint مفقود را به‌عنوان Canonical Truth بسازد.

P06-DEN-100 — Scenario Branch نباید Authoritative State را Silent Modify کند.

P06-DEN-101 — Scientific Verification نباید Operational Readiness یا Mission Approval نامیده شود.

P06-DEN-102 — هیچ External Message، Scheduling، Tasking یا Coordination Effect از Scenario مجاز نیست.

P06-DEN-103 — Human Approval هم Route ممنوع Spacecraft Command را در CSIP-EO ایجاد نمی‌کند.

P06-DEN-104 — Emergency هیچ استثنایی برای Command Boundary ندارد.

P06-FAIL-058 — Scenario Parent/Input Mismatch نتیجه `SCENARIO_LINEAGE_INVALID` دارد.

P06-FAIL-059 — Unknown Critical Constraint نتیجه `SCENARIO_FEASIBILITY_INDETERMINATE` دارد.

P06-FAIL-060 — Optimization/Simulation Non-convergence نتیجه `SCI_NOT_CONVERGED` دارد.

P06-FAIL-061 — Scenario-to-authoritative Promotion بدون Gate نتیجه `SCENARIO_PROMOTION_BLOCKED` دارد.

P06-FAIL-062 — Executable/Command-compatible Output نتیجه `SCI_COMMAND_PATH_PROHIBITED — E9/APR-X/INC-0` دارد.

P06-FAIL-063 — Stochastic Evidence ناقص نتیجه `SCENARIO_STATISTICAL_EVIDENCE_INCOMPLETE` دارد.

## 16. Physics Confidence — `PHY-C0..PHY-C5`

P06-REQ-023 — `PHY-C0..PHY-C5` فقط Evidence Maturity برای Result/Claim دقیق است؛ Authority، Probability of Truth، Operational Permission یا Universal Quality Score نیست:

| Level | معنای Source-bound | Minimum Interpretation |
|---:|---|---|
| `PHY-C0` | No valid scientific result؛ Context missing/invalid | Block scientific use |
| `PHY-C1` | Exploratory؛ major unvalidated assumptions | Research only؛ limitations prominent |
| `PHY-C2` | Contract-valid در Scope محدود/Research؛ Independent Evidence incomplete | No high-impact promotion |
| `PHY-C3` | Validated within declared domain and tolerance | Validation evidence required; not claimed by this Part |
| `PHY-C4` | Independently verified؛ uncertainty reconciled؛ no material unresolved discrepancy | Exact independence/evidence required |
| `PHY-C5` | High-assurance for exact scoped use/config/evidence package | Not universal truth or operational authority |

P06-DEF-026 — `PhysicsConfidenceRecord` Level، Claim/Artifact Digest، Evidence Set، Validation/Verification Scope، Independence Dimensions، Discrepancy Status، Validity Domain، Limitations، Assessor و Expiry/Revalidation Trigger را ثبت می‌کند.

P06-CON-223 — Level باید Per-claim/Per-result باشد؛ Engine، Team، Project یا Artifact Family سطح دائمی دریافت نمی‌کند.

P06-CON-224 — Level فقط پس از Evidence-bound Assessment قابل انتساب است؛ این Prompt Part هیچ Result را Levelدهی نمی‌کند.

P06-CON-225 — `PHY-C0` Default برای Result نامعتبر/Context ناقص است و به Zero-risk یا No-event تفسیر نمی‌شود.

P06-CON-226 — `PHY-C1` باید Assumptionهای Major، Unsupported Inputs و Forbidden Uses را صریح کند.

P06-CON-227 — `PHY-C2` Contract Validity محدود را از Independent Verification ناقص جدا می‌کند.

P06-CON-228 — `PHY-C3` نیازمند Validation Evidence در Declared Domain/Tolerance است؛ Source Candidate یا Unit Test به‌تنهایی کافی نیست.

P06-CON-229 — `PHY-C4` نیازمند Independence Profile، Verification Artifacts، Reconciled Uncertainty و نبود Material Unresolved Discrepancy است.

P06-CON-230 — `PHY-C5` فقط برای Exact Use، Configuration، Data/Evidence Package و Validity Window است و با تغییر Material کاهش/انقضا می‌یابد.

P06-CON-231 — Confidence Level باید با New Counterevidence، Data/Profile/Engine Revision، Domain Exceedance، Staleness یا Independence Loss Reassess شود.

P06-CON-232 — Unknown Evidence یا Missing Verification نمی‌تواند با Human Confidence یا AI Confidence جبران شود.

P06-CON-233 — Physics Confidence، AI Confidence، Data Quality، Risk Tier و Approval Class محورهای مستقل‌اند.

P06-CON-234 — Display باید Level، Scope، Evidence Date/Revision، Limitations و Status Sentinel Owner را کنار هم نشان دهد.

P06-CON-235 — Aggregate Confidence فقط با Predeclared Composition/Denominator و بدون پنهان‌کردن Weakest Material Claim قابل‌گزارش است.

P06-CON-236 — Level Downgrade History و Trigger Immutable می‌ماند؛ Prior High Level حذف نمی‌شود اما Current Status صریح است.

P06-CON-237 — `PHY-C*` نباید مستقیم به `E*`، `APR-*`، `AUT-*`، Release Gate یا Risk Acceptance Map شود.

P06-CON-238 — Scientific Promotion ممکن است Minimum Level بخواهد ولی Exact Policy/Authority متعلق به P05/P13/P16 است.

P06-CON-239 — هیچ Levelی مسیر Spacecraft Command ایجاد نمی‌کند.

P06-DEN-105 — `PHY-C5` Universal Truth، Guaranteed Accuracy، Safe-to-operate یا Command Permission نیست.

P06-DEN-106 — Level نباید از Engine Name، Tier، Reviewer Count یا Model Confidence استنتاج شود.

P06-DEN-107 — Missing Evidence نباید میانگین‌گیری یا Imputation شود.

P06-DEN-108 — Confidence Percentage بدون Calibrated Definition/Denominator نباید جای Level بنشیند.

P06-DEN-109 — `PHY-C3+` نباید فقط با Internal Validation یا Same-team Review ادعا شود اگر Independence لازم است.

P06-DEN-110 — Level نباید پس از Material Change Grandfather شود.

P06-DEN-111 — Human Approval Level علمی را بالا نمی‌برد.

P06-DEN-112 — AI Summary نباید Level یا Evidence Scope را تغییر دهد.

P06-FAIL-064 — Confidence Claim بدون Evidence Record نتیجه `PHYSICS_CONFIDENCE_UNSUPPORTED` دارد.

P06-FAIL-065 — Scope/Artifact Mismatch نتیجه `PHYSICS_CONFIDENCE_MISBOUND` دارد.

P06-FAIL-066 — Material Discrepancy با Level بالا نتیجه `PHYSICS_CONFIDENCE_DOWNGRADE_OR_BLOCK` دارد.

P06-FAIL-067 — Stale/Changed Evidence نتیجه `PHYSICS_CONFIDENCE_REASSESSMENT_REQUIRED` دارد.

P06-FAIL-068 — Level-to-authority Inference نتیجه `SCIENTIFIC_AUTHORITY_CONFLATION — DENY` دارد.

## 17. Independent Verification و Discrepancy

P06-REQ-024 — Verification Profile باید پیش از Result مشخص کند کدام Dimensions مستقل‌اند و کدام Shared Dependencies/Common-cause Risks باقی می‌مانند.

P06-REQ-025 — Discrepancy State باید دقیقاً یکی از این Source-bound Values باشد:

`AGREED_WITHIN_TOLERANCE | EXPLAINED_DIFFERENCE | MATERIAL_DISCREPANCY | INDETERMINATE`

P06-DEF-027 — `IndependenceProfile` Implementation، Algorithm، Configuration/Data Validation، Operator/Reviewer، Library/Constant/Auxiliary Dependency و Organizational Separation را Dimension-by-dimension ثبت می‌کند.

P06-DEF-028 — `VerificationArtifact` Verification Request، Independent Inputs/Configuration، Outputs، Oracle/Tolerance، Comparison Metrics، Discrepancy State، Reviewer/Competence Evidence و Provenance را Bind می‌کند.

P06-DEF-029 — `DiscrepancyRecord` Competing Artifacts، Metric/Difference، Tolerance، Root-cause Hypothesis/Evidence، Materiality، Impacted Claims، Resolution/Status و Residual Limitation را نگه می‌دارد.

P06-CON-240 — Independence Implementation یعنی Codebase/Implementation Path متفاوت؛ Wrapper/Container/Process جداسازی آن نیست.

P06-CON-241 — Algorithmic Independence باید Formulation متفاوت را در حد Feasibility ثبت کند؛ Same Formula with same defects می‌تواند Common Cause باشد.

P06-CON-242 — Configuration/Data Validation باید توسط Path/Reviewer مستقل انجام و Shared Input Digestها آشکار شوند.

P06-CON-243 — Operator/Reviewer Independence نیازمند Identity، Competence، Conflict-of-interest و Separation Evidence است؛ Job Title کافی نیست.

P06-CON-244 — Shared Libraries، Constants، EOP، Gravity/Atmosphere، Observation Preprocessing، Initial State یا Covariance باید در Common-cause Analysis ثبت شوند.

P06-CON-245 — Required Independence Strength باید با Impact/Risk/Scientific Materiality افزایش یابد؛ Exact Gate توسط P05/P13/P16 تعیین می‌شود.

P06-CON-246 — Comparison باید Time/Frame/Unit/Convention/Validity و Artifact Scope را Align کند؛ Misaligned Outputs Discrepancy علمی قابل‌تفسیر نیستند.

P06-CON-247 — Tolerance/Decision Rule باید پیش از Unblinded Comparison Fix شود و Absolute/Relative/Scale-floor/Uncertainty Handling را مشخص کند.

P06-CON-248 — `AGREED_WITHIN_TOLERANCE` فقط برای Dataset/Domain/Metric/Tolerance دقیق معتبر است؛ Bitwise Equality یا Universal Equivalence نیست.

P06-CON-249 — `EXPLAINED_DIFFERENCE` نیازمند Causal Explanation Evidence-bound و Demonstration است؛ Story یا Plausibility کافی نیست.

P06-CON-250 — `MATERIAL_DISCREPANCY` High-impact Promotion و `PHY-C4+` را Block می‌کند تا Resolution یا Claim Narrowing معتبر.

P06-CON-251 — `INDETERMINATE` وقتی Root Cause/Materiality/Comparability قابل‌حل نیست حفظ و مانند Agreement تفسیر نمی‌شود.

P06-CON-252 — Resolution باید Corrected Artifact/Configuration، Re-run/Analysis Evidence، Reviewer و Residual Risk/Limitation داشته باشد.

P06-CON-253 — Selecting one Result as Canonical نیازمند Domain-owner Decision و Evidence است؛ حذف Losing Artifact ممنوع است.

P06-CON-254 — Verification Run خود یک Effect/Cost/Data Use است و Authority Contract P05 را مستقل می‌خواهد؛ این Part آن را اجرا نمی‌کند.

P06-CON-255 — Independent Challenge باید Assumption، Boundary، Adversarial Cases، Counterexample و Failure Semantics را پوشش دهد، نه فقط Happy-path Reproduction.

P06-CON-256 — Verification Evidence باید Raw/Protected Inputs، Configuration، Logs، Outputs، Metrics و Analysis را Immutable-link کند.

P06-CON-257 — Repeated Runs روی Same Defect استقلال ایجاد نمی‌کنند؛ Statistical Confidence و Systematic Error جدا هستند.

P06-CON-258 — Correlated Engines/Teams/Data باید Claimed Independence را Downgrade و Limitations را Visible کنند.

P06-CON-259 — Verification Status باید `NOT_REQUESTED|REQUIRED|IN_PROGRESS|PASSED_WITH_SCOPE|FAILED|DISPUTED|INDETERMINATE|STALE` را بدون Collapse نگه دارد؛ Vocabulary اجرایی نهایی با P13 Harmonize می‌شود.

P06-CON-260 — `PASSED_WITH_SCOPE` فقط Verification Claim است، نه Scientific Approval یا Operational Fitness.

P06-CON-261 — New Version/Input/Profile یا Discovered Shared Cause Verification را Stale می‌کند مگر Equivalence/Impact Evidence P13 خلاف آن را ثابت کند.

P06-CON-262 — Human Adjudication باید Exact Evidence Presentation Digest و Dissent/Counterevidence را ثبت کند.

P06-CON-263 — Verification Result باید به Workflow P04 و Scientific Result P06 Reference شود ولی Approval/Outcome Records مستقل بمانند.

P06-CON-264 — Command-path Negative Verification فقط Static/Formal/Controlled Evidence بدون ایجاد Operational Route مجاز است.

P06-DEN-113 — دو Wrapper روی یک Engine Full Independence نیستند.

P06-DEN-114 — Same Input Preprocessor/Common Constants نباید پنهان شود.

P06-DEN-115 — Agreement بدون Predeclared Tolerance و Aligned Context معتبر نیست.

P06-DEN-116 — Explained Difference با Narrative بدون Test/Evidence بسته نمی‌شود.

P06-DEN-117 — Material Discrepancy نباید Average، Vote، Management Override یا AI Arbitration شود.

P06-DEN-118 — Reviewer Seniority یا Count به‌تنهایی Competence/Independence نیست.

P06-DEN-119 — Verification Success نباید Source Owner را Approved/Normative کند.

P06-DEN-120 — Failed Verification نباید با حذف Test/Datum یا تغییر Tolerance پس از Result پنهان شود.

P06-DEN-121 — Shared-cause Unknown نباید Independence کامل فرض شود.

P06-DEN-122 — Verification Artifact نباید Receipt یا Log Summary تنها باشد.

P06-DEN-123 — Scientific Adjudication هیچ Risk Acceptance/Budget/Release Approval صادر نمی‌کند.

P06-DEN-124 — Independent Verification هیچ Command Path مجاز نمی‌کند.

P06-FAIL-069 — Verification Missing در Use الزام‌آور نتیجه `SCI_VERIFICATION_MISSING — PROMOTION_BLOCKED` دارد.

P06-FAIL-070 — Independence Evidence ناقص نتیجه `INDEPENDENCE_INDETERMINATE` دارد.

P06-FAIL-071 — Misaligned Comparison نتیجه `SCIENTIFIC_VERIFICATION_NONCOMPARABLE` دارد.

P06-FAIL-072 — Material Discrepancy نتیجه `SCI_MATERIAL_DISCREPANCY` دارد.

P06-FAIL-073 — Post-hoc Tolerance Change نتیجه `VERIFICATION_ORACLE_TAMPERING — INVALID` دارد.

P06-FAIL-074 — Hidden Shared Cause نتیجه `INDEPENDENCE_CLAIM_INVALID` دارد.

P06-FAIL-075 — Verification Artifact Stale نتیجه `SCI_VERIFICATION_STALE — REVERIFY_OR_LIMIT` دارد.

P06-FAIL-076 — Command-route Test Path نتیجه `SCI_COMMAND_PATH_PROHIBITED — INC-0/HARD_STOP` دارد.

## 18. Numerical Equivalence، Scientific Relation و Reproducibility

P06-REQ-026 — Scientific/Numerical Acceptance باید پیش از Unblinded Result، Artifact Class، Dataset، Validity Domain، Oracle، Absolute/Relative Tolerance، Scale Floor، Uncertainty، Platform، Rounding، Stochastic Protocol، Exclusions و Decision Rule را Fix کند.

P06-REQ-027 — Source labels Stage 20 باید بدون ایجاد Taxonomy رقیب به Equivalence Classes مالک P13/Gap 02 Map شوند:

| Source Stage-20 label | P13/Gap-02 canonical owner mapping | شرط P06 |
|---|---|---|
| `BITWISE_IDENTICAL` | `EQ-BITWISE` | bytes، length، digest و algorithm یکسان |
| `NUMERICALLY_EQUIVALENT` | `EQ-NUMERIC` | dataset/tolerance/uncertainty/domain ثابت |
| `SCIENTIFICALLY_EQUIVALENT_WITHIN_VALIDITY_DOMAIN` | `EQ-NUMERIC` با Scientific Validity Oracle صریح | Claim فقط در Domain دقیق |
| `BEHAVIORALLY_EQUIVALENT_FOR_DECLARED_TESTS` | `EQ-BEHAVIORAL` | فقط Behaviorهای Test Declaration |
| `NOT_REPRODUCIBLE_BUT_INDEPENDENTLY_VERIFIABLE` | `EQ-VERIFIABLE` | Provenance قوی + Verification مستقل |
| `UNKNOWN_BLOCKED` | `EQ-UNKNOWN` | Promotion/Release Blocked |

P06-DEF-030 — `NumericalEquivalenceProfile` Metricها، Tolerance Formula، Scale Floor، Unit/Frame Alignment، Dataset/Population، Uncertainty Treatment، Hardware/Runtime، Rounding، Stochastic Protocol و Pass Rule را Version می‌کند.

P06-DEF-031 — `ReproducibilityManifest` Source/Input/Profile/Engine/Build/Configuration/Auxiliary/Platform/Seed/Artifact Digests و Instructions/Evidence لازم برای تکرار را Bind می‌کند.

P06-DEF-032 — `ScientificReproductionResult` Attempt برای بازتولید Artifact است و باید از Independent Verification و Equivalence Acceptance جدا گزارش شود.

P06-CON-265 — P13 مالک Canonical Equivalence/Assurance Semantics و Acceptance Oracle است؛ P06 فقط Scientific/Numeric Application و Required Context را تعیین می‌کند.

P06-CON-266 — `EQ-BITWISE` برای Floating/Platform-sensitive Results پیش‌فرض نیست؛ اگر Technically invalid باشد Class مناسب از پیش انتخاب می‌شود.

P06-CON-267 — `EQ-NUMERIC` باید Absolute و Relative Tolerance را با Scale Floor/Zero Handling و Unit Alignment مشخص کند.

P06-CON-268 — Tolerance باید نسبت به Measurement/Model/Numerical Uncertainty و Intended Decision Justified باشد؛ Arbitrary Loose Bound ممنوع است.

P06-CON-269 — Scientific Equivalence فقط در Validity Domain و Claim Set دقیق است؛ Equality یک Scalar کل Artifact را Equivalent نمی‌کند.

P06-CON-270 — `EQ-BEHAVIORAL` فقط Declared Observables/Tests را پوشش می‌دهد و Numerical Truth خارج از آن‌ها را اثبات نمی‌کند.

P06-CON-271 — Stochastic/Monte Carlo Result باید در صورت Applicable از `EQ-DISTRIBUTIONAL` متعلق به P13 با Repeated-run Protocol، Seed Policy، Distribution Metrics و Error Bounds استفاده کند.

P06-CON-272 — `EQ-VERIFIABLE` نبود Bitwise Reproduction را پنهان نمی‌کند و به Strong Provenance/Independent Evidence محدود است.

P06-CON-273 — `EQ-UNKNOWN` Block است؛ Similarity، Close Chart یا Expert Impression جای Acceptance نیست.

P06-CON-274 — Hardware/OS/Runtime/Library Variation باید در Equivalence Profile یا Exclusion/Residual Limitation ثبت شود.

P06-CON-275 — Floating-point Mode، Precision، FMA/Vectorization، Parallel Reduction و Nondeterministic Ordering می‌توانند Result را تغییر دهند و باید Profile-bound باشند.

P06-CON-276 — Rounding/Serialization Difference باید از Scientific Difference جدا، اما هر Semantic Impact آزموده شود.

P06-CON-277 — Dataset باید Version/Digest، Membership، Sampling، Exclusion و Ground/reference Authority داشته باشد.

P06-CON-278 — Metric Denominator/Eligible Population باید با P12 Contract Reconstructable باشد؛ Pass Percentage بدون آن معتبر نیست.

P06-CON-279 — Reproduction Success با Same Build/Input می‌تواند Reproducibility را نشان دهد، نه Independence یا Correctness.

P06-CON-280 — Independent Verification بدون Reproduction ممکن است در `EQ-VERIFIABLE` پذیرفتنی باشد فقط طبق P13 Profile و Limitations صریح.

P06-CON-281 — Reproducibility Failure باید Root-cause/Scope و Artifact Evidence را حفظ کند؛ Failure حذف نمی‌شود.

P06-CON-282 — Predeclared Oracle/Threshold پس از Result فقط با Invalidated Run، New Version و Disclosure تغییر می‌کند.

P06-CON-283 — Equivalence Claim باید Source/Target Artifact Digests و Direction/Symmetry/Transitivity Assumptions را ثبت کند؛ Transitivity خودکار نیست.

P06-CON-284 — Different Validity Domains نباید با Overlap جزئی Universal Equivalent اعلام شوند.

P06-CON-285 — Engine Adapter Equivalence باید Schema/Status/Failure/Uncertainty Semantics را علاوه بر Numeric Outputs پوشش دهد.

P06-CON-286 — Model/Algorithm Update نیازمند Impact Analysis و Equivalence/Regression Evidence تازه است.

P06-CON-287 — Reproduction Artifactها باید Immutable، Source-bound و قابل Audit باشند؛ Screenshot/Chart تنها کافی نیست.

P06-CON-288 — Proprietary/Constrained Service می‌تواند فقط `EQ-VERIFIABLE` Candidate باشد اگر Evidence کافی و Policy اجازه دهد؛ این Part Approval نمی‌کند.

P06-CON-289 — هیچ Equivalence Classی Authority، Release، Production یا Command Permission نیست.

P06-DEN-125 — Universal Same-digest Rule برای تمام Artifact Classes ممنوع است.

P06-DEN-126 — Numeric Closeness بدون Dataset/Tolerance/Domain/Uncertainty معتبر نیست.

P06-DEN-127 — Tolerance Post-hoc یا Result-specific ممنوع است.

P06-DEN-128 — One successful reproduction نباید Accuracy/Independence/Qualification نامیده شود.

P06-DEN-129 — `EQ-BEHAVIORAL` نباید Scientific Equality خارج از Declared Tests ایجاد کند.

P06-DEN-130 — `EQ-VERIFIABLE` نباید Missing Provenance یا Unavailable Evidence را Launder کند.

P06-DEN-131 — Cross-platform Difference نباید خودکار Bug یا Equivalent اعلام شود.

P06-DEN-132 — Average Error نباید Worst-case/Boundary/Failure Population را پنهان کند.

P06-DEN-133 — Excluded Cases نباید از Denominator بدون Predeclared Rule حذف شوند.

P06-DEN-134 — Artifact Equivalence نباید Status/Approval Equivalence ایجاد کند.

P06-DEN-135 — Screenshot/Visualization Equality Scientific Equivalence نیست.

P06-DEN-136 — AI Similarity Judgment Equivalence Oracle نیست.

P06-DEN-137 — Equivalence Claim هیچ Spacecraft-command Route مجاز نمی‌کند.

P06-FAIL-077 — Equivalence Profile ناقص نتیجه `EQUIVALENCE_PROFILE_INVALID` دارد.

P06-FAIL-078 — Dataset/Denominator Unbound نتیجه `EQUIVALENCE_POPULATION_UNRESOLVED` دارد.

P06-FAIL-079 — Result خارج Tolerance نتیجه `NUMERICAL_EQUIVALENCE_FAILED` دارد.

P06-FAIL-080 — Domain Mismatch نتیجه `SCIENTIFIC_EQUIVALENCE_DOMAIN_MISMATCH` دارد.

P06-FAIL-081 — Reproduction Manifest ناقص نتیجه `REPRODUCIBILITY_NOT_ESTABLISHED` دارد.

P06-FAIL-082 — Post-hoc Oracle Change نتیجه `EQUIVALENCE_ORACLE_TAMPERING` دارد.

P06-FAIL-083 — Unknown Relation نتیجه `EQ-UNKNOWN — PROMOTION_BLOCKED` دارد.

P06-FAIL-084 — Status/Authority Inference از Equivalence نتیجه `EQUIVALENCE_SCOPE_VIOLATION` دارد.

## 19. مرز AI در علم و محاسبۀ عددی

P06-REQ-028 — AI فقط Advisory و `UNTRUSTED_DATA_ONLY` است؛ می‌تواند Evidence را توضیح، Missing Field را شناسایی، Test/Sensitivity/Discrepancy Hypothesis پیشنهاد و Source-bound Summary تولید کند، اما Truth عددی یا Authority نمی‌سازد.

P06-CON-290 — AI می‌تواند Draft Scientific Request ایجاد کند فقط اگر تمام Fieldهای پیشنهادی/مفقود Label شوند و Validator/Owner مستقل آن را Resolve کند.

P06-CON-291 — AI می‌تواند Inconsistency میان Time/Frame/Unit/Covariance/Status را Flag کند؛ Flag Finding است نه Scientific Decision.

P06-CON-292 — AI می‌تواند Validated Artifact را با Citation، Uncertainty، Counterevidence، Limitations و Validity Domain توضیح دهد.

P06-CON-293 — AI می‌تواند Candidate Test، Metamorphic Property، Sensitivity Range یا Root-cause Hypothesis پیشنهاد کند؛ P13/Domain Owner باید آن را Review/Approve کند.

P06-CON-294 — AI Output باید Model/Prompt/Corpus/Tool/Provider Version و Source Citations در حد P07 Contract قابل‌حل داشته باشد.

P06-CON-295 — AI Confidence از Physics Confidence، Data Quality، Verification Status و Risk جدا است.

P06-CON-296 — AI Summary باید Original Result Status، Units، Frame، Epoch، Uncertainty، Limitation و Discrepancy را حفظ کند.

P06-CON-297 — AI-generated Number فقط Quoted/Derived از Source-bound Artifact یا محاسبۀ Approved Numerical Method آینده می‌تواند مصرف شود؛ LLM Token Prediction Method علمی نیست.

P06-CON-298 — AI نمی‌تواند Missing Observation، State، Covariance، HBR، Force Parameter، Time Scale، Frame یا Unit را Authoritative Impute کند.

P06-CON-299 — AI نمی‌تواند Convergence، Validation، Verification، Independence، Qualification یا Scientific Promotion اعلام کند.

P06-CON-300 — AI نمی‌تواند Scientific Disagreement را با Majority، Fluent Explanation یا Model Confidence Resolve کند.

P06-CON-301 — AI Tool Proposal باید از P08/P05/P03/P04 Gates عبور کند؛ P06 هیچ Tool Execution مجاز نمی‌کند.

P06-CON-302 — AI Correction Proposal Revision جداست و Source Artifact را Silent Edit نمی‌کند.

P06-CON-303 — AI Citation باید Exact Source/Version/Digest/Section را تا حد Available حفظ کند؛ Citation Presence Truth را ثابت نمی‌کند.

P06-CON-304 — AI Explanation باید Distinguish کند: observed، estimated، propagated، assumed، simulated، disputed و unknown.

P06-CON-305 — AI نمی‌تواند `NOT_COMPUTABLE/NOT_CONVERGED/INDETERMINATE` را با Plausible Answer جایگزین کند.

P06-CON-306 — AI cannot lower Tiers، Tolerances، Verification Requirements یا Failure Severity برای پاسخ‌دادن سریع‌تر.

P06-CON-307 — AI Memory/RAG/Vector/Graph Projection متعلق به P07/P09/P10 است و هیچ‌یک Canonical Scientific Truth Store نیست.

P06-CON-308 — Human Acceptance از AI Output آن را Scientific Truth نمی‌کند؛ Evidence/Method Contract همچنان لازم است.

P06-CON-309 — AI هیچ Recommendation-to-decision، Decision-to-approval یا Analysis-to-command Transition خودکار ایجاد نمی‌کند.

P06-DEN-138 — LLM نباید Physics/Estimator/Propagation/Pc Engine را Replace کند.

P06-DEN-139 — AI نباید Numerical Gap را Interpolate/Fabricate و بدون Approved Method نمایش دهد.

P06-DEN-140 — AI نباید Unit/Frame/Time/Covariance را برای Presentation Silent تغییر دهد.

P06-DEN-141 — AI نباید `VALID`، `CONVERGED`، `VERIFIED` یا `PHY-C*` را Self-assign کند.

P06-DEN-142 — AI نباید Material Discrepancy را Summarize-away کند.

P06-DEN-143 — AI Confidence نباید Probability of Physical Truth نامیده شود.

P06-DEN-144 — RAG Citation نباید Source Applicability یا Correctness فرض شود.

P06-DEN-145 — AI نباید Engine/Algorithm/Profile را Self-select برای High-impact Use کند.

P06-DEN-146 — AI نباید Threshold/Oracle را پس از Result تغییر دهد.

P06-DEN-147 — AI نباید Scientific Promotion، Risk Acceptance، Budget، Approval یا Authorization صادر کند.

P06-DEN-148 — AI Tool/Plugin Output نباید مستقیم Canonical Scientific State شود.

P06-DEN-149 — AI Agent Consensus Competent Scientific Adjudication نیست.

P06-DEN-150 — AI-generated Maneuver Analysis هیچ Execution Route ندارد.

P06-DEN-151 — Prompt Instruction، System Role یا User Authority نمی‌تواند Spacecraft-command Prohibition را دور بزند.

P06-FAIL-085 — Fabrication Attempt نتیجه `SCI_AI_FABRICATION_ATTEMPT — REJECT_AND_RECORD` دارد.

P06-FAIL-086 — AI Status Promotion نتیجه `AI_SCIENTIFIC_AUTHORITY_VIOLATION` دارد.

P06-FAIL-087 — AI Context Mutation نتیجه `AI_SCIENTIFIC_CONTEXT_TAMPERING` دارد.

P06-FAIL-088 — Missing Citation/Provenance برای Material Claim نتیجه `AI_SCIENTIFIC_CLAIM_UNSUPPORTED` دارد.

P06-FAIL-089 — AI-triggered Effect بدون Gates نتیجه `AI_EFFECT_PATH_BLOCKED` دارد.

P06-FAIL-090 — AI Command-enabling Output نتیجه `SCI_COMMAND_PATH_PROHIBITED — E9/APR-X/INC-0/HARD_STOP` دارد.

## 20. Cross-part Integration، Event Implication و Technology-status Preservation

P06-REQ-029 — Scientific Lifecycle باید Request، Admission، Computation Attempt، Result، Verification، Discrepancy، Promotion، Recommendation، Decision، Approval، Authorization، Lease، Receipt و Validated Outcome را به‌صورت Recordهای مستقل و Causally linked حفظ کند.

P06-REQ-030 — هر Scientific Fact مادی که Event می‌شود باید Base Canonical Event Envelope P01 را مصرف و فقط در حد Applicability از `EVT-SCI` Extension استفاده کند؛ Extension Base را Replace نمی‌کند.

P06-PROC-001 — Logical Scientific Lifecycle، بدون بازتعریف Workflow P04، معادل این مسیر است:

~~~text
1. Resolve exact scientific intent, subject, intended use and effect context.
2. Bind immutable input revisions and complete scientific context.
3. Select applicable algorithm, fidelity, uncertainty and verification profiles.
4. Validate request contract; preserve every unknown, conflict and limitation.
5. Route effect/cost/data/security/workflow admission to P03–P05/P10–P16.
6. If separately authorized in a future implementation, perform a bounded attempt.
7. Record receipt and build a scientific result with explicit status.
8. Run the predeclared verification/challenge profile when required.
9. Reconcile discrepancies; never average away a material conflict.
10. Evaluate a separately governed scientific-promotion candidate.
11. Publish only the scoped artifact/status permitted by all gates.
12. Revalidate on new evidence, revision, staleness or validity-domain change.
13. Preserve immutable history, counterevidence and supersession links.
14. Never create or hand off any spacecraft-command/uplink/execution route.
~~~

P06-PROC-002 — Scientific-baseline Change، Model/Algorithm/Profile Promotion، High-impact Result Promotion یا Material Discrepancy Disposition باید Report Profile P05 را Re-resolve کند؛ Trigger `FULL` در P05 یک Documentation/Admission Obligation است، نه Approval یا Execution Authority.

P06-CON-310 — Step Completion در Lifecycle بالا Result Validity یا Permission برای Step بعد نیست.

P06-CON-311 — Request Semantics P03، Workflow Semantics P04، Authority P05 و Scientific Semantics P06 باید با Exact References پیوند بخورند و در یک Boolean `approved/valid` ادغام نشوند.

P06-CON-312 — Computation Attempt ممکن است Succeeded Transport/Runtime باشد اما Scientific Result `INVALID/NOT_CONVERGED/INDETERMINATE` بماند.

P06-CON-313 — Scientific Promotion Candidate باید Exact Result Digest، Confidence/Verification/Discrepancy، Intended Use، Effect، Approval Presentation و Decision Record References داشته باشد.

P06-CON-314 — `FULL` Report Completion Scientific Review، Approval، AuthorizationDecision یا Lease نیست.

P06-CON-315 — Scientific Evidence می‌تواند Approval Floor/Risk/Profile را سخت‌گیرانه‌تر کند؛ Approval/Risk Acceptance نمی‌تواند Scientific Failure را Valid کند.

P06-CON-316 — Event Fact Proposed/Started/Completed/Failed/Validated/Verified/Promoted/Revoked/Superseded States را جدا نگه می‌دارد.

P06-CON-317 — Scientific Event Typeهای حداقلی، در صورت Applicability، شامل این موارد‌اند:

1. `SCIENTIFIC_REQUEST_REGISTERED`؛
2. `SCIENTIFIC_CONTEXT_VALIDATED_OR_REJECTED`؛
3. `SCIENTIFIC_ATTEMPT_STARTED`؛
4. `SCIENTIFIC_RESULT_RECORDED`؛
5. `SCIENTIFIC_NON_CONVERGENCE_RECORDED`؛
6. `SCIENTIFIC_VERIFICATION_REQUESTED`؛
7. `SCIENTIFIC_VERIFICATION_RECORDED`؛
8. `SCIENTIFIC_DISCREPANCY_RECORDED`؛
9. `SCIENTIFIC_RESULT_SUPERSEDED`؛
10. `SCIENTIFIC_PROMOTION_PROPOSED_OR_DECIDED`؛
11. `CONJUNCTION_ASSESSMENT_REVISED`؛
12. `PROHIBITED_SCIENTIFIC_COMMAND_PATH_DETECTED`.

P06-CON-318 — Event Name Human-readable است؛ Semantics از Schema Version، Source Clause، Subject/Request/Result/Revision و Status می‌آید.

P06-CON-319 — `EVT-SCI` Representative Fields شامل Epoch، Time-scale Profile، Frame، Units، Covariance، Uncertainty، Algorithm/Engine/Config/Auxiliary Digests، Validity Domain و Verification Status است.

P06-CON-320 — Security/Approval/Evidence/Cost Fields فقط با Extensionهای `EVT-SEC-AUD`، `EVT-RISK-COST`، `EVT-REL-EVID` و `EVT-REL-OBS` در Applicability مربوط اضافه می‌شوند؛ P06 مالک آن‌ها نیست.

P06-CON-321 — Event Producer باید Source Artifact/Status را حفظ کند؛ Event Arrival یا Projection Success Authority/Truth ایجاد نمی‌کند.

P06-CON-322 — Event Consumer باید Idempotent، Duplicate-aware، Out-of-order-aware و Fail-closed باشد.

P06-CON-323 — Scientific Result/Discrepancy/Prohibited-path Events نباید Sample شوند اگر Sampling Evidence/Status را مخدوش می‌کند؛ Exact Policy متعلق به P12/P11 است.

P06-CON-324 — Event Replay نباید Computation، Cost، Publication، Promotion یا External Effect را دوباره اجرا کند؛ Replay Fact از Action جدا است.

P06-CON-325 — Event Payload باید Data Minimization، Tenant/Purpose، Classification و Protected References متعلق به P10/P11 را رعایت کند.

P06-CON-326 — Event Correction با New Correction/Superseding Event و حفظ Original History انجام می‌شود.

P06-CON-327 — Scientific Workflow Degraded Mode فقط Scope/Fidelity/Horizon/Resolution را در Profile مجاز کاهش می‌دهد و Truth/Authority را افزایش نمی‌دهد.

P06-CON-328 — Scientific Computation Capability در P08 باید Exact Operation، Scientific Profile Ceiling، Input/Output Schemas، Effect Graph و Prohibited-command Boundary داشته باشد.

P06-CON-329 — Persistence P09 باید Artifact/Revision/Projection را جدا کند؛ Scientific Record Immutable است و Cache/Search/Vector/Twin Projection Authoritative Truth نیست.

P06-CON-330 — Data Governance P10 باید Source Rights، Quality، Retention و Dataset Lifecycle را تعیین کند؛ P06 Presence Data را به Usage Permission تبدیل نمی‌کند.

P06-CON-331 — Security P11 می‌تواند Access/Execution را Deny کند؛ نمی‌تواند Scientific Result نامعتبر را Valid کند.

P06-CON-332 — Observability P12 باید Evidence/Metric/Denominator و Telemetry Quality را حفظ کند؛ Metric Goodness Scientific Validity نیست.

P06-CON-333 — Assurance P13 باید Test/Oracle/Equivalence/Acceptance Evidence را مالک شود؛ P06 Scientific Preconditions و Domain-specific Failure Semantics را فراهم می‌کند.

P06-CON-334 — Deployment/Release P14/P15 و Roadmap P17 فقط Consumer Scientific Gate هستند و نمی‌توانند `DOMAIN_REVIEW_REQUIRED` را حذف کنند.

P06-CON-335 — P16 Risk/Governance می‌تواند Use را محدود/منع کند؛ Scientific Truth با Risk Acceptance تغییر نمی‌کند.

P06-CON-336 — P18 فقط Source/Trace/Conflict را Compile می‌کند و P06 Scientific Definitions یا Discrepancy را Rewrite نمی‌کند.

P06-CON-337 — Technology Statusهای P01 بدون Promotion/Downgrade چنین حفظ می‌شوند:

| Technology | Status حفظ‌شده |
|---|---|
| Python، Java، TypeScript | `PROVISIONAL_SELECTION` |
| Rust | `RESEARCH_TRACK` |
| FastAPI + OpenAPI | `PROVISIONAL_SELECTION` |
| gRPC + Protobuf | `PROVISIONAL_SELECTION` |
| Redpanda | `SHORTLISTED` |
| NATS JetStream | `SHORTLISTED` |
| PostgreSQL | `PROVISIONAL_SELECTION` |
| ClickHouse | `PROVISIONAL_SELECTION_WITH_ACTIVATION_GATE` |
| S3-compatible Storage | `APPROVED_PRINCIPLE` |
| Ceph | `SHORTLISTED` |
| Apache Iceberg | `PROVISIONAL_SELECTION` |
| Qdrant | `PROVISIONAL_SELECTION` |
| Ray | `PROVISIONAL_SELECTION` |
| Kubernetes | `SHORTLISTED` |
| OCI Containers | `APPROVED_PRINCIPLE` |
| OpenTelemetry | `PROVISIONAL_SELECTION` |
| OPA | `PROVISIONAL_SELECTION` |
| SPIFFE/SPIRE | `SHORTLISTED` |
| Sigstore/Cosign | `PROVISIONAL_SELECTION` |
| vLLM | `PROVISIONAL_SELECTION` |
| Triton، Ray Serve | `SHORTLISTED` |
| MLflow | `PROVISIONAL_SELECTION` (Model Registry Contract) |

P06-DEN-152 — Scientific Validity نباید Effect/Approval/Authorization را Implied کند.

P06-DEN-153 — Event نباید Command، Approval، Verification یا Outcome را Implied کند.

P06-DEN-154 — Queue/Event/Workflow Retry نباید Scientific Attempt/Cost را بدون Fresh Gates تکرار کند.

P06-DEN-155 — Projection/Twin/Search/Cache نباید Canonical Scientific Artifact را Replace کند.

P06-DEN-156 — Scientific Event Schema نباید Base Envelope P01 را Rename یا Replace کند.

P06-DEN-157 — Report `FULL` نباید به GO/APPROVED تبدیل شود.

P06-DEN-158 — Downstream Approved Source نباید Owner P06 را Approved Launder کند.

P06-DEN-159 — P06 Technology Table انتخاب تازه، Procurement یا Architecture Freeze نیست.

P06-DEN-160 — `APPROVED_PRINCIPLE` Technology Status به Tool/Implementation/Deployment Approval تعمیم نمی‌یابد.

P06-DEN-161 — Event Replay/Backfill نباید Command-compatible Effect ایجاد کند.

P06-DEN-162 — Scientific Promotion نباید Missing P05/P13/P16 Gates را با Domain-owner Opinion دور بزند.

P06-DEN-163 — هیچ Cross-part Handoffی Spacecraft Command/Uplink/Flight-control Route ندارد.

P06-FAIL-091 — Record-role Conflation نتیجه `SCIENTIFIC_RECORD_SEPARATION_VIOLATION` دارد.

P06-FAIL-092 — Event Schema/Profile Invalid نتیجه `SCIENTIFIC_EVENT_INVALID` دارد.

P06-FAIL-093 — Critical Scientific Event Gap نتیجه `SCIENTIFIC_EVENT_EVIDENCE_GAP — RECONCILE` دارد.

P06-FAIL-094 — Out-of-order Revision Conflict نتیجه `SCIENTIFIC_REVISION_ORDER_CONFLICTED` دارد.

P06-FAIL-095 — Authority/Scientific Snapshot Non-atomic نتیجه `SCIENTIFIC_ADMISSION_SNAPSHOT_INVALID` دارد.

P06-FAIL-096 — Status Laundering از Downstream Source نتیجه `SOURCE_STATUS_PRESERVATION_VIOLATION` دارد.

P06-FAIL-097 — Technology Status Promotion نتیجه `TECHNOLOGY_STATUS_DRIFT — REWORK_REQUIRED` دارد.

P06-FAIL-098 — Event/Workflow Command Coupling نتیجه `SCI_COMMAND_PATH_PROHIBITED — INC-0/HARD_STOP` دارد.

## 21. Failure Code Registry، Unknown Handling و Graceful Degradation

P06-REQ-031 — تمام Failure/Unknown Stateها باید Explicit، Typed، Evidence-bound و Fail-closed باشند؛ هیچ Degraded Mode حق افزایش Scientific Claim، Authority، Exposure یا Scope ندارد.

P06-DEF-033 — `ScientificDegradedMode` Profile از پیش تعریف‌شده، Time/Use-bound و Evidence-producing است که فقط Scope، Horizon، Resolution، Fidelity یا Availability را کاهش می‌دهد و Result Status/Limitation را صریح نگه می‌دارد.

P06-PROC-003 — Precedence برای Result Status و Degradation:

~~~text
1. E9/command-enabling path => HARD_STOP / INC-0; no degraded continuation.
2. Invalid scientific context or unsafe numerical state => INVALID / DO_NOT_USE.
3. Missing computability precondition => NOT_COMPUTABLE.
4. Failed convergence => NOT_CONVERGED.
5. Material unresolved discrepancy => DISPUTED / promotion blocked.
6. Truth or applicability unresolved => INDETERMINATE.
7. Bounded limitation with valid evidence => VALID_WITH_LIMITATIONS.
8. VALID only when every applicable contract and validity predicate passes.
9. Scientific status never grants approval, authorization, lease or execution.
~~~

P06-PROC-004 — هر Failure باید Request/Attempt/Result Reference، Time، Source/Engine/Profile، Error Code، Context Digest، Impacted Claim/Use، Evidence، Retryability، Containment، Required Review و Final/Reconciled Status را ثبت کند.

P06-CON-338 — Source Failure Codeهای اجباری بدون تغییر معنایی عبارت‌اند از:

- `SCI_TIME_SCALE_MISSING`
- `SCI_EPOCH_INVALID`
- `SCI_FRAME_MISSING_OR_UNSUPPORTED`
- `SCI_UNIT_UNKNOWN`
- `SCI_COVARIANCE_INVALID`
- `SCI_AUXILIARY_DATA_STALE_OR_MISSING`
- `SCI_PROFILE_UNAPPROVED`
- `SCI_ENGINE_UNQUALIFIED`
- `SCI_NOT_CONVERGED`
- `SCI_NUMERICAL_INSTABILITY`
- `SCI_VALIDITY_DOMAIN_EXCEEDED`
- `SCI_VERIFICATION_MISSING`
- `SCI_MATERIAL_DISCREPANCY`
- `SCI_AI_FABRICATION_ATTEMPT`
- `SCI_COMMAND_PATH_PROHIBITED`

P06-CON-339 — Failure Registry بالا Extensionپذیر است اما Existing Code Meaning نباید Reuse/Weaken شود.

P06-CON-340 — Unknown Stateها حداقل `NOT_FOUND|UNRESOLVED|INDETERMINATE|STALE|CONFLICTED|UNVERIFIED|UNSUPPORTED|UNBOUNDED|NOT_COMPUTABLE|NOT_CONVERGED` را جدا نگه می‌دارند.

P06-CON-341 — `NOT_APPLICABLE` فقط با Predicate، Scope، Profile، Source Rule و Rationale معتبر است؛ Field خالی Not Applicable نیست.

P06-CON-342 — Missing Context به Lowest Tier/Confidence یا Default Validity تبدیل نمی‌شود.

P06-CON-343 — Retry فقط اگر Request/Inputs/Profile/Gates معتبر و Failure Retryable باشد Attempt تازه با ID/Receipt جدا است.

P06-CON-344 — Retry Count، Backoff و Aggregate Cost/Effect متعلق به P04/P05/P12 است و Scientific Evidence باید Attempts را جدا نگه دارد.

P06-CON-345 — Fallback Engine/Profile باید Mapping/Equivalence/Qualification/Gates و Result Limitation جدا داشته باشد؛ Silent Fallback ممنوع است.

P06-CON-346 — Partial Batch Success باید Successful/Failed/Unknown Memberها و Complete Denominator را ثبت کند.

P06-CON-347 — Degraded Result باید Original Requested Profile، Actual Profile، Trigger، Lost Capabilities، Validity/Use Limits و Expiry را ثبت کند.

P06-CON-348 — Degradation به Model ساده‌تر فقط برای Use پشتیبانی‌شده و با Reclassification/Disclosure مجاز آینده است.

P06-CON-349 — Stale Auxiliary Data می‌تواند Result را Limited/Not-computable کند؛ Freshness Threshold باید Profile-bound باشد.

P06-CON-350 — Material Discrepancy یا Command Path هیچ Degraded Allow Route ندارد.

P06-CON-351 — Recovery/Recompute Result Artifact تازه می‌سازد و Failure History را حفظ می‌کند.

P06-CON-352 — Numerical Warning باید به Status Rule Map شود؛ Warning Suppression بدون Evidence ممنوع است.

P06-CON-353 — NaN/Inf/Overflow/Underflow/Cancellation/Conditioning باید Detect و Contextualize شوند؛ Serialization آن‌ها Success نیست.

P06-CON-354 — Failure Message برای User باید Scientific Impact و Next Evidence Need را توضیح دهد، نه Safe/No-risk Assumption.

P06-CON-355 — System Unavailability نمی‌تواند Cached Scientific Result را Current کند؛ Staleness/Validity همچنان حاکم است.

P06-CON-356 — Human Override می‌تواند Work را Stop/Limit کند؛ نمی‌تواند Invalid Result را Valid کند.

P06-CON-357 — Error Redaction باید Security/Privacy را رعایت و Diagnostic/Evidence Integrity را با Protected Reference حفظ کند.

P06-CON-358 — Failure Metric باید Denominator/Eligibility و Per-code Population را حفظ کند؛ Unknown Cases از Denominator حذف Silent نمی‌شوند.

P06-CON-359 — Graceful Degradation باید Testable/Observable باشد اما این Part هیچ Test اجرا یا Implementation ایجاد نمی‌کند.

P06-CON-360 — Prohibited-path Detection باید Unsampled، High-priority، Evidence-preserving و `INC-0`-linked باشد.

P06-DEN-164 — Unknown به Pass/Valid/Zero/No-risk تبدیل نمی‌شود.

P06-DEN-165 — Retry نباید Last-known-good Result را Current یا Valid فرض کند.

P06-DEN-166 — Fallback نباید Tier/Verification/Engine Qualification را پنهان کند.

P06-DEN-167 — Partial Success نباید Batch Success کامل گزارش شود.

P06-DEN-168 — `NOT_COMPUTABLE` نباید `0` یا No Conjunction تفسیر شود.

P06-DEN-169 — `NOT_CONVERGED` نباید با Last Iterate Valid شود.

P06-DEN-170 — `DISPUTED` نباید با Preferred Result بسته شود.

P06-DEN-171 — `INDETERMINATE` نباید برای Deadline به `VALID_WITH_LIMITATIONS` Downgrade شود.

P06-DEN-172 — Error Suppression/Log Loss نباید Outcome را Success کند.

P06-DEN-173 — Degraded Mode نباید Scope/Exposure/Authority را افزایش دهد.

P06-DEN-174 — Cached/Stale Result نباید Fresh نمایش داده شود.

P06-DEN-175 — Recovery نباید Original Failure را حذف کند.

P06-DEN-176 — Command-path Failure هیچ Retry/Alternate Route ندارد.

P06-FAIL-099 — Unknown-to-success Conversion نتیجه `SCIENTIFIC_UNKNOWN_LAUNDERING` دارد.

P06-FAIL-100 — Partial-result Aggregation Misreport نتیجه `SCIENTIFIC_BATCH_COMPLETENESS_INVALID` دارد.

P06-FAIL-101 — Silent Fallback نتیجه `SCIENTIFIC_FALLBACK_UNDECLARED` دارد.

P06-FAIL-102 — Retry بدون Fresh Validity/Gates نتیجه `SCIENTIFIC_RETRY_INVALID` دارد.

P06-FAIL-103 — Degraded Scope Expansion نتیجه `SCIENTIFIC_DEGRADATION_SAFETY_VIOLATION` دارد.

P06-FAIL-104 — Numerical Exception پنهان نتیجه `SCI_NUMERICAL_INSTABILITY — INVALID` دارد.

P06-FAIL-105 — Stale Result Reuse نتیجه `SCIENTIFIC_RESULT_STALE` دارد.

P06-FAIL-106 — Unreconciled Failure History نتیجه `SCIENTIFIC_LIFECYCLE_INCOMPLETE` دارد.

P06-FAIL-107 — Material Discrepancy Bypass نتیجه `SCI_MATERIAL_DISCREPANCY — PROMOTION_BLOCKED` دارد.

P06-FAIL-108 — Prohibited Path نتیجه `SCI_COMMAND_PATH_PROHIBITED — E9/APR-X/INC-0/HARD_STOP` دارد.

## 22. Verification Requirements و Domain-review Gate

P06-REQ-032 — P13 باید Verification Program آینده را طوری طراحی کند که حداقل این Classها را برای P06 پوشش دهد؛ فهرست زیر Test Execution نیست:

1. Analytic و High-precision Reference Cases؛
2. Metamorphic/Property Tests؛
3. Differential Engine Tests؛
4. Time-scale/Leap-second/EOP Tests؛
5. Frame/Unit/Covariance Round-trip Tests؛
6. Boundary/Conditioning/NaN/Inf/Convergence Tests؛
7. Monte Carlo/Statistical Tests در Applicability مربوط؛
8. Sensitivity و Uncertainty-propagation Tests؛
9. Historical/Reference Dataset Tests با Provenance؛
10. Independent Implementation/Reviewer Tests؛
11. Command-path Negative Tests بدون ساخت Operational Route.

P06-REQ-033 — رفع Sentinel `DOMAIN_REVIEW_REQUIRED — NOT_NORMATIVELY_ACTIVATED` نیازمند Exact Digest، Competent Astrodynamics/Scientific-computing Review، Independent Challenge، Fresh Explicit Approval و Successor-manifest Registration است.

P06-REQ-034 — Acceptance Evidence باید Claim-to-Test-to-Oracle-to-Result-to-Reviewer-to-Disposition Trace را حفظ کند و Failed/Excluded/Unknown Population را پنهان نکند.

P06-CON-361 — Analytic Reference Cases باید Assumption/Closed-form Domain، Precision و Expected Error را مشخص کنند.

P06-CON-362 — High-precision Reference به‌تنهایی Truth نیست؛ Source/Method/Precision/Independence باید Evidence-bound باشد.

P06-CON-363 — Metamorphic Properties می‌توانند Invariance، Conservation، Reversibility/round-trip، Symmetry یا Monotonicity Applicable را تست کنند؛ Property باید Domain/Exceptions صریح داشته باشد.

P06-CON-364 — Differential Tests باید Context را Align و Independence/Common-cause را ثبت کنند.

P06-CON-365 — Time Tests باید Leap Boundary، UTC/TAI/TT/UT1 Conversion، EOP Missing/Predicted و Precision/Round-trip را پوشش دهند.

P06-CON-366 — Frame/Unit Tests باید Known Transforms، Chain/Round-trip، Jacobian/Covariance و Ambiguous Alias Rejection را پوشش دهند.

P06-CON-367 — Covariance Tests باید Ordering/Basis/Units، PSD/Conditioning، Transform، Correlation و Invalid-input Failure را پوشش دهند.

P06-CON-368 — Numerical Robustness Tests باید NaN/Inf، Extreme Scale، Cancellation، Step Failure، Ill-conditioning، Non-convergence و Boundary Domain را پوشش دهند.

P06-CON-369 — Monte Carlo/Statistical Tests باید Distribution، Seed/Stream، Sample/Stopping Rule، Coverage Metric و Confidence Interval را Predeclare کنند.

P06-CON-370 — Sensitivity Tests باید Parameter Range، Interaction، Local/Global Method، Output Metric و Decision Impact را ثبت کنند.

P06-CON-371 — Historical/Reference Dataset باید Rights، Provenance، Revision، Leakage/Bias و Ground-truth Authority را ثبت کند.

P06-CON-372 — Verification Dataset نباید فقط Happy-path یا Known-success Population باشد؛ Exclusion/Denominator قابل بازسازی لازم است.

P06-CON-373 — Command Negative Tests باید Schema/Adapter/Workflow/Export/Generic-tool/Successor Paths را Static/Formal/Isolated بررسی کنند و هیچ Credential/Endpoint/Command Payload فعال نسازند.

P06-CON-374 — Test Oracle، Tolerance و Expected Failure باید قبل از Unblinding Versioned شود.

P06-CON-375 — Test Result باید Environment/Build/Profile/Input Digest، Logs/Evidence، Outcome، Reviewer و Limitations را Bind کند.

P06-CON-376 — `PASS` فقط Exact Test/Oracle/Scope را پوشش می‌دهد؛ Requirement/Engine/Project Universal Verification نیست.

P06-CON-377 — Failed/Flaky/Skipped/Blocked/Not-run Testها Stateهای مستقل‌اند و Pass نمی‌شوند.

P06-CON-378 — Coverage Claim نیازمند Denominator Contract P12 و Orphan/Trace Contract P13 است.

P06-CON-379 — Competent Reviewer Criteria، Identities و Conflict/Independence Evidence باید توسط Governance Sources تعیین شوند؛ این Part آن‌ها را جعل نمی‌کند.

P06-CON-380 — Domain Review باید Scientific Assumptions، Failure Semantics، Validity Domains، Uncertainty، Engine Mapping، Independence و Anti-command Boundary را Challenge کند.

P06-CON-381 — Independent Challenge باید Dissent/Counterevidence را Immutable ثبت و Resolution را Source-bound کند.

P06-CON-382 — Fresh Approval باید Exact Artifact Digest/Version/Status/Scope و Remaining Limitations را Bind کند؛ Approval Inheritance ممنوع است.

P06-CON-383 — Manifest Registration پس از Approval یک Gate جداست و خود Approval یا Scientific Correctness نیست.

P06-CON-384 — این P06 هیچ Numerical Calculation، Validation Run، Verification Run، Benchmark، Monte Carlo، Engine Comparison یا Domain Approval اجرا نکرده است.

P06-DEN-177 — Test Plan Presence Test Execution یا Pass نیست.

P06-DEN-178 — Unit Test/Static Review به‌تنهایی Scientific Validation/Qualification نیست.

P06-DEN-179 — Green Pipeline نباید Competent Domain Review را Replace کند.

P06-DEN-180 — Test Cases پس از Failure نباید بدون Controlled Revision حذف/تضعیف شوند.

P06-DEN-181 — Coverage Percentage بدون Denominator معتبر نیست.

P06-DEN-182 — Reviewer Count/Seniority Independence/Competence را ثابت نمی‌کند.

P06-DEN-183 — Fresh Approval نباید از Prior/Historical/Missing Stage ارث برده شود.

P06-DEN-184 — Manifest Registration Normative Activation نیست مگر تمام Gates صریح تکمیل شوند.

P06-DEN-185 — P13 Approved Source Status به P06 Owner یا این Prompt Part منتقل نمی‌شود.

P06-DEN-186 — Negative Test نباید Command Route، Credential یا Operational Payload بسازد.

P06-DEN-187 — Internal Prompt Audit Scientific Review نیست.

P06-FAIL-109 — Missing Oracle/Denominator نتیجه `SCIENTIFIC_ASSURANCE_ORACLE_INCOMPLETE` دارد.

P06-FAIL-110 — Test Status Laundering نتیجه `SCIENTIFIC_TEST_STATUS_INVALID` دارد.

P06-FAIL-111 — Domain Reviewer/Competence Unresolved نتیجه `DOMAIN_REVIEW_NOT_SATISFIED` دارد.

P06-FAIL-112 — Independent Challenge Missing نتیجه `INDEPENDENT_CHALLENGE_NOT_SATISFIED` دارد.

P06-FAIL-113 — Fresh Digest-bound Approval Missing نتیجه `SCIENTIFIC_SUCCESSOR_NOT_NORMATIVELY_ACTIVATED` دارد.

P06-FAIL-114 — Manifest Binding Missing نتیجه `SCIENTIFIC_SUCCESSOR_REGISTRATION_INCOMPLETE` دارد.

P06-FAIL-115 — Command Negative-test Unsafe Design نتیجه `SCI_COMMAND_PATH_PROHIBITED` دارد.

P06-FAIL-116 — Unsupported Verification/Validation Claim نتیجه `SCIENTIFIC_ASSURANCE_CLAIM_UNSUPPORTED` دارد.

## 23. Traceability، Source Binding، Compression و Orphan Detection

P06-REQ-035 — هر Clause مادی P06 باید Owner، Requirement/Decision ID، Source Identity، Supporting Bindings، Upstream Clause، Consumer، Enforcement، Evidence، Verification Owner، Acceptance Test، Conflict، Compression/Reconstitution، Implementation Status، Limitation و Open Issue قابل‌حل داشته باشد.

P06-REQ-036 — P06 از یک Canonical Trace Schema مشترک و بدون Alias رقیب استفاده می‌کند؛ `prompt_clause_id` و `requirement_or_decision_id` دو هویت مستقل‌اند و هرگز Merge یا Copy نمی‌شوند.

P06-REQ-037 — Semantic Compression فقط `DIRECT|PARAPHRASED_LOSSLESS|REFERENCED|DEDUPLICATED` است و نباید Normative Force، Scope، Status، Exception، Failure، Scientific Caveat، Uncertainty، Anti-claim یا Source Binding را حذف کند.

P06-PROC-005 — Required Trace Record Projection برای Clauseهای P06:

~~~yaml
trace_schema_id: CSIP-EO-FMSP-TRACE-RECORD
trace_schema_version: 1
prompt_clause_id:
requirement_or_decision_id:
statement:
normative_keyword:
owner_part_id: CSIP-EO-FMSP-P06
semantic_owner_artifact_id: CSIP-EO-RS-STAGE-20
semantic_owner_version: 0.1.0-reconstituted-draft
semantic_owner_sha256: 8e12aa3c7d1c9c03d8d20fcc9cf556a0e8a2e1462d1a9698c7d689d45c6bb8a4
semantic_owner_status: RECONSTITUTED_DRAFT — REVIEW_READY — DOMAIN_REVIEW_REQUIRED — NOT_APPROVED — NOT_FROZEN
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
mapped_stage: 20
mapped_control:
requirement_owner_role:
enforcement_reference:
evidence_reference:
verification_owner: P13_AND_COMPETENT_SCIENTIFIC_REVIEW
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

P06-CON-385 — `prompt_clause_id` باید Pattern `P06-{INV|REQ|DEF|CON|PROC|DEN|FAIL|DEC|OI}-nnn` داشته باشد؛ `requirement_or_decision_id` می‌تواند `RS20-DEC-*`، `CGR-REQ-*`، `CGR-DEC-*` یا `NOT_APPLICABLE_WITH_RATIONALE` باشد.

P06-CON-386 — Owner Part و چهار Field Semantic Owner مستقل از پنج Field Primary Source Binding هستند؛ هیچ‌کدام جای دیگری نیست.

P06-CON-387 — `supporting_source_bindings` آرایۀ Structured، Ordered، Version/Digest/Status-bound است؛ List Filename یا نام مبهم کافی نیست.

P06-CON-388 — `upstream_clause_references` از Source Binding و Consumer Mapping مستقل است.

P06-CON-389 — `compression_operation` برای Record مادی خالی نمی‌ماند؛ Losslessness باید قابل Audit باشد.

P06-CON-390 — `reconstitution_operation` مستقل است و باید `NONE` یا شرح Source-bound دقیق باشد. برای P06 Prompt Derivation مجاز: `PROMPT_DERIVATION_FROM_DIGEST_BOUND_RECONSTITUTED_SUCCESSOR; NO_HISTORICAL_BYTE_RECOVERY_CLAIM`.

P06-CON-391 — Inline/Memory Payload غیر Byte-addressable نباید Digest یا Byte-equality جعلی دریافت کند؛ Limitation `INLINE_PAYLOAD_BYTES_NOT_ADDRESSABLE` در صورت Applicability ثبت می‌شود.

P06-CON-392 — Enforcement، Evidence، Verification Owner و Acceptance Test چهار Concern مستقل‌اند و در فیلد مبهم ادغام نمی‌شوند.

P06-CON-393 — Aliasهای Legacy پیش از Serialization به Canonical Field Normalize می‌شوند و در Record نهایی Schema دوم نمی‌سازند.

| Legacy/Source label | Canonical field |
|---|---|
| `p06_clause_id` | `prompt_clause_id` |
| `requirement_id` | `requirement_or_decision_id` |
| `semantic_owner_part` | `owner_part_id` |
| `semantic_owner_digest` | `semantic_owner_sha256` |
| `source_document` | `source_artifact_id` |
| `source_digest` | `source_sha256` |
| `supporting_sources` | `supporting_source_bindings` |
| `owner_role_or_future_owner` | `requirement_owner_role` |
| `enforcement_point_or_future_boundary` | `enforcement_reference` |
| `evidence_type` | `evidence_reference` |
| `acceptance_test` | `acceptance_test_reference` |
| `compression_or_reconstitution_operation` | دو Field مستقل Canonical |
| `parent_requirements` | `parent_requirement_or_decision_ids` |
| `derived_requirements` | `derived_requirement_or_decision_ids` |
| `open_issue_reference` | `open_issue_references` |

P06-CON-394 — Exact Source Identity Registry:

| نقش | Artifact ID / Version | SHA-256 | Status حفظ‌شده |
|---|---|---|---|
| Semantic Owner | `CSIP-EO-RS-STAGE-20 / 0.1.0-reconstituted-draft` | `8e12aa3c7d1c9c03d8d20fcc9cf556a0e8a2e1462d1a9698c7d689d45c6bb8a4` | `RECONSTITUTED_DRAFT — REVIEW_READY — DOMAIN_REVIEW_REQUIRED — NOT_APPROVED — NOT_FROZEN` |
| Harmonization Overlay | `CSIP-EO-AUDIT-GAP-02 / 0.1.0-candidate` | `fa400334a69702bf56e8588210449590573bccd3120d7c2cebd6ba9cc8fc161f` | `CANDIDATE — REVIEW_READY — NON_NORMATIVE_UNTIL_DIGEST_BOUND_APPROVAL` |
| Enterprise Mandate | `ENTERPRISE-TRUST-RISK-COST-EVIDENCE-REPRODUCIBILITY-MANDATE / verified-input-2026-07-28` | `1b5e7884a343589312d62259f181bd48f1a12b51e2613685c0d58c747a08dab4` | `PRESENT_VERIFIED_BYTES / SUPPLEMENTAL_CROSS_CUTTING_INPUT` |
| Assembly Contract | `CSIP-EO-PROMPT-ARCH-18P-C1 / 0.1.0-design-candidate` | `a4c80b938fccaab5d3d85c780351a41ee3444b4c6712920af45b493afbacb09b` | `DESIGN_CANDIDATE — REVIEW_READY — NOT_APPROVED — NOT_FROZEN` |
| Candidate Manifest | `CSIP-EO-GAP-RESOLUTION-MANIFEST-C1 / 0.1.0-candidate` | `349b590df9fad00c2e0ec317f4bd0b7ad747a5e22a1fead0f66f28c98e955216` | `REVIEW_READY_NOT_APPROVED` |

P06-CON-395 — Digestهای Deprecated/غیرمجاز `e9789e4163470a15f914d4e82a868169396d5f3206fc71cae91ff01d178c72a7`، `9dd808f9c0dbd7a9fe5ca150d94a032dd788e9e1f7fb3cb149b43148a5e5ade2` و `fd74eabab248717a6a160a8eb11a51d14455b852515d95c5f47f8316a72f4072` نباید جای Sourceهای Registry بالا مصرف شوند.

P06-CON-396 — Upstream Part Binding Registry:

| Part | Semantic Owner SHA-256 | Clause/Boundary مصرف‌شده | Operation |
|---|---|---|---|
| `CSIP-EO-FMSP-P01` | `a33bf602b5a5e5c8518b709b5dde7ab6b96617cc76ac86c66d2c795271422c50` | Project/Scope/Invariant؛ TemporalStamp؛ Base Event؛ Technology Status | `REFERENCE_ONLY` |
| `CSIP-EO-FMSP-P02` | `b0ffc9a74b3bac68ee6f74176f732fdf3ea60277697546c9b009b54e5ab4cb6b` | Stage/Gate/Handoff؛ Lifecycle Independence؛ Stage-20 Review Gate | `REFERENCE_ONLY` |
| `CSIP-EO-FMSP-P03` | `3f16593a323f3024550a4515a1c48118872e53bfdbb60d3d7ae47385ab4ff249` | Request/Command/Event/Approval/Authorization/Lease/Receipt/Outcome Separation | `REFERENCE_ONLY` |
| `CSIP-EO-FMSP-P04` | `98c58b2fc8fe56e0d84f39c901421642d8b8b525c18979b9a1b2aaee25c5d75b` | Workflow/Step/Human Checkpoint/Retry/Recovery/Scientific Context Reference | `REFERENCE_ONLY` |
| `CSIP-EO-FMSP-P05` | `30525213394593910a4bb0406ba3eb2ee784ddae05170933cea1a033654d8731` | `P05-CON-443..449`؛ Effect/Approval/Permission/Autonomy/Profile Boundary | `REFERENCE_ONLY` |

P06-CON-397 — Accepted P05 Payload Binding برای Chain Integrity: `CSIP-EO_FMSP_P05_v0.9.0-draft.txt / SHA-256 52243c8f77614940f00b56b39b3408083af2e795163b6de3063f3bba82fe9a9a / PART_ACCEPTED_FOR_ASSEMBLY`؛ این Status Source P05 را Promote نمی‌کند.

P06-CON-398 — P06 مالک اصلی `CGR-REQ-003`، `CGR-REQ-004` و `CGR-REQ-005` است:

| Requirement | P06 Mapping | Consumerها | Implementation Status حفظ‌شده |
|---|---|---|---|
| `CGR-REQ-003` | P06-REQ-004، P06-REQ-007، P06-REQ-028 و `INV/CON/DEN/FAIL` مرتبط | P01، P07، P13 | `DESIGNED_NOT_IMPLEMENTED` |
| `CGR-REQ-004` | P06-REQ-008..010 و Time/Frame/Unit Clauses | P01، P09، P10، P13 | `DESIGNED_NOT_IMPLEMENTED` |
| `CGR-REQ-005` | P06-REQ-016..018، P06-REQ-024..027 و Verification Clauses | P13 | `DESIGNED_NOT_IMPLEMENTED` |

P06-CON-399 — Clause-range Source Mapping:

| P06 range | Primary binding | Operation |
|---|---|---|
| `REQ-001..003` | Assembly Contract §§8، 10؛ P05 Handoff | faithful reception envelope |
| `REQ-004..007` | RS20 §§0–3؛ Assembly §6.6؛ `CGR-REQ-003` | owned objective/truth boundary |
| `REQ-008..010` | RS20 §§4–6؛ `CGR-REQ-004` | owned scientific context/time/frame/unit |
| `REQ-011..012` | RS20 §§7–8 | owned scientific request/result payloads |
| `REQ-013` | RS20 §3؛ P01 status registry | engine-neutral mapping; status preserved |
| `REQ-014..015` | RS20 §9 | propagation fidelity tiers |
| `REQ-016..018` | RS20 §11؛ `CGR-REQ-005` | OD/covariance semantics |
| `REQ-019` | RS20 §§2، 4، 8 | ephemeris/twin scientific state |
| `REQ-020..021` | RS20 §12 | conjunction/HBR/Pc |
| `REQ-022` | RS20 §§2، 12، 18 | analysis-only scenario boundary |
| `REQ-023` | RS20 §10 | physics confidence |
| `REQ-024..025` | RS20 §13 | independence/discrepancy |
| `REQ-026..027` | RS20 §14؛ Gap02 §8؛ P13 ownership | scientific equivalence application |
| `REQ-028` | RS20 §15؛ `CGR-REQ-003` | AI scientific boundary |
| `REQ-029..031` | RS20 §16؛ P01–P05 integration | lifecycle/event/failure implications |
| `REQ-032..034` | RS20 §§17، 19؛ P02/P13 gates | verification/domain-review contract |
| `REQ-035..037` | Assembly §13؛ Gap02 §5؛ P05 canonical trace contract | trace/compression conformance projection |

P06-CON-400 — `DIRECT` فقط برای Statement مادی مستقیم با Binding دقیق؛ `PARAPHRASED_LOSSLESS` فقط با حفظ تمام Force/Status/Caveat؛ `REFERENCED` فقط با Upstream Clause دقیق؛ و `DEDUPLICATED` فقط با Link به Clause Canonical باقی‌مانده مجاز است.

P06-CON-401 — Derived Definitionهای این Part مانند `ScientificContext`، `TimeConversionRecord`، `PhysicsConfidenceRecord` یا Mapping دقیق فقط Design Candidate در Owner Status فعلی‌اند و Approved/Implemented نیستند.

P06-CON-402 — Source/Requirement Conflict باید `CONFLICTED — FAIL_CLOSED` بماند؛ Scientific Conflict برای Competent Domain Adjudication و Package Conflict برای P18/P16 Route می‌شود.

P06-CON-403 — Part Order، Newer File، Longer Text، Retrieval Rank یا Approved Downstream Source Precedence علمی ایجاد نمی‌کند.

P06-CON-404 — Orphan شامل Missing Source/Owner/Digest/Status، Missing Consumer/Enforcement، Missing Verification/Evidence، Competing Owner، Claim قوی‌تر از Source، Status Promotion، Test بدون Requirement/Oracle و Open Issue بدون Disposition است.

P06-CON-405 — Full Machine-readable Trace Graph برای تمام P06 Clauses و تمام Consumer Parts هنوز Future Work است؛ Human Projection حاضر Completion آن را ادعا نمی‌کند.

P06-CON-406 — Trace Edge تولیدشده توسط AI/Rule تا Validation معتبر `CANDIDATE` است و Orphan را Closed نمی‌کند.

P06-CON-407 — Alias حل‌نشده، Invalid Compression، Missing Canonical Field یا Reconstitution بدون Source Binding Required Trace Coverage را Fail می‌کند.

P06-CON-408 — Supporting Source Status به Semantic Owner Status و Semantic Owner Status به Prompt/Package Status منتقل نمی‌شود.

P06-CON-409 — P13 Assurance Ownership با P06 Scientific Ownership تعارض ندارد: P06 Truth/Input/Result/Failure Semantics را تعریف می‌کند؛ P13 Oracle/Test/Acceptance/Equivalence Governance را مالک است.

P06-CON-410 — `DOMAIN_REVIEW_REQUIRED` باید در Header، Source Registry، Decision/Open Issue، Audit و Handoff Visible بماند.

P06-CON-411 — Unsupported Claim Scan باید `APPROVED|NORMATIVE|FROZEN|IMPLEMENTED|VERIFIED|VALIDATED|QUALIFIED|RELEASED|DEPLOYED|PRODUCTION_READY|COMPLIANT` را Contextually بررسی و فقط Source-bound scoped use را مجاز کند.

P06-CON-412 — Owner-boundary Scan باید Competing API/Workflow/Authority/AI/Capability/Persistence/Data/Security/Observability/Test/Deployment/Governance/Compilation Definitions را Block کند.

P06-CON-413 — Clause ID Scan باید Duplicate و Sequence Gap در هر Prefix استفاده‌شده را Blocking بداند.

P06-CON-414 — Anchor/Fence/YAML Scan باید Anchorهای یکتا، Fenceهای زوج، Parse-valid YAML و Visible End Anchor را تأیید کند.

P06-CON-415 — Status/Digest Scan باید پنج Source Identity و سه Deprecated Digest را دقیق بررسی کند.

P06-CON-416 — Compression Audit باید تفکیک Clause/Requirement، چهار Operation مجاز و Reconstitution مستقل را تأیید کند.

P06-DEN-188 — Requirement بدون Source/Owner نباید با Best Practice یا Model Knowledge Normative شود.

P06-DEN-189 — Filename/Memory/Summary Source Identity نیست.

P06-DEN-190 — Trace Matrix ناقص نباید با Percentage بدون Denominator Complete گزارش شود.

P06-DEN-191 — Orphan با حذف/Informative کردن Requirement پنهان نمی‌شود.

P06-DEN-192 — Supporting Source Status Owner را Promote نمی‌کند.

P06-DEN-193 — Machine Scan Pass Domain Review/Fresh Approval نیست.

P06-DEN-194 — P06 نباید P07 Content یا AI/RAG/Memory Taxonomy را بسازد؛ فقط Handoff Pointer مجاز است.

P06-DEN-195 — Semantic Compression نباید Scientific Caveat/Uncertainty/Failure را حذف کند.

P06-DEN-196 — Legacy Alias نباید به Field دوم/Competing Schema تبدیل شود.

P06-DEN-197 — `prompt_clause_id` نباید از `requirement_or_decision_id` Copy شود.

P06-DEN-198 — Historical Byte Recovery نباید از Prompt Derivation استنتاج شود.

P06-DEN-199 — Digest Fixity Scientific Correctness/Approval نیست.

P06-DEN-200 — Package Compiler نباید Conflict/Discrepancy را Summary-away کند.

P06-DEN-201 — P13 Verification Ownership نباید Scientific Truth P06 را Override کند.

P06-DEN-202 — P06 Scientific Ownership نباید P13 Test Oracle را تصاحب کند.

P06-FAIL-117 — Trace Join ناقص نتیجه `TRACE_SOURCE_DIGEST_UNRESOLVED` دارد.

P06-FAIL-118 — Orphan Requirement نتیجه `ORPHAN_REQUIREMENT — REWORK_REQUIRED` دارد.

P06-FAIL-119 — Unsupported Claim نتیجه `UNSUPPORTED_SCIENTIFIC_CLAIM — PART_NOT_ACCEPTED` دارد.

P06-FAIL-120 — Owner Collision نتیجه `SEMANTIC_OWNER_CONFLICT — FAIL_CLOSED` دارد.

P06-FAIL-121 — Status Drift نتیجه `STATUS_LAUNDERING_VIOLATION — REWORK_REQUIRED` دارد.

P06-FAIL-122 — Invalid Compression/Reconstitution نتیجه `TRACE_SEMANTIC_COMPRESSION_INVALID` دارد.

P06-FAIL-123 — Duplicate/Gap Clause ID نتیجه `CLAUSE_ID_INTEGRITY_FAILED` دارد.

P06-FAIL-124 — Fence/YAML/Anchor Failure نتیجه `PART_STRUCTURAL_INTEGRITY_FAILED` دارد.

P06-FAIL-125 — Deprecated Source Digest Use نتیجه `SOURCE_BINDING_CONFLICTED` دارد.

P06-FAIL-126 — P07 Content Intrusion نتیجه `PART_BOUNDARY_VIOLATION — REWORK_REQUIRED` دارد.

## 24. Decision Projection، Limitations و Open Issueها

Decisionهای زیر Projection مستقیم مالک معنایی‌اند و همگی فقط `PROPOSED` باقی می‌مانند:

P06-DEC-001 — `RS20-DEC-001`: Physics/Evidence بر AI و Governance Preference مقدم‌اند — Status: `PROPOSED`.

P06-DEC-002 — `RS20-DEC-002`: Canonical Boundary از Contractهای Engine-agnostic و Versioned استفاده می‌کند — Status: `PROPOSED`.

P06-DEC-003 — `RS20-DEC-003`: Time/Frame/Unit/Covariance/Provenance Context غیرOptional است — Status: `PROPOSED`.

P06-DEC-004 — `RS20-DEC-004`: Orekit Primary Candidate؛ GMAT Independent Candidate؛ Tudat Research؛ Basilisk 6-DOF — Status: `PROPOSED`.

P06-DEC-005 — `RS20-DEC-005`: `T0..T4` Scoped Fidelity Profiles هستند، نه Universal Guarantee — Status: `PROPOSED`.

P06-DEC-006 — `RS20-DEC-006`: `PHY-C0..C5` Evidence Maturity است، نه Authority — Status: `PROPOSED`.

P06-DEC-007 — `RS20-DEC-007`: High-impact Output به Independent Verification و Discrepancy Handling نیاز دارد — Status: `PROPOSED`.

P06-DEC-008 — `RS20-DEC-008`: Non-computable/Non-converged/Disputed Stateها صریح می‌مانند — Status: `PROPOSED`.

P06-DEC-009 — `RS20-DEC-009`: AI هیچ Numerical Truth یا Scientific Promotion ایجاد نمی‌کند — Status: `PROPOSED`.

P06-DEC-010 — `RS20-DEC-010`: Maneuver فقط Analysis است؛ Command/Uplink/Execution ممنوع — Status: `PROPOSED`.

P06-DEC-011 — `CGR-DEC-023`: هر Timestamp علمی Time-scale Explicit است — Status: `PROPOSED`.

P06-DEC-012 — `CGR-DEC-028`: Reproducibility Acceptance Artifact-class-specific و تحت مالکیت P13 است — Status: `PROPOSED`.

P06-CON-417 — وجود Decision Projection Approval، Historical Recovery، Normative Activation، Engine Qualification، Implementation یا Freeze ایجاد نمی‌کند.

### 24.1 محدودیت‌های اجباری

P06-CON-418 — Historical Bytes، Clauseها، Decision Provenance و Approval State دقیق `CSIP-EO-STAGE-20` بازیابی نشده‌اند.

P06-CON-419 — Successor Candidate حاضر Newly Authored است و فقط Digest آن Fixity Bytes Candidate را نشان می‌دهد.

P06-CON-420 — هیچ Numerical Computation، Scientific Validation، Verification Run، Benchmark، Simulation یا Independent Challenge توسط این Part اجرا نشده است.

P06-CON-421 — هیچ Engine Version/Build/Profile، Dataset، Force Model، Estimator، Time/Frame/Unit Convention، Auxiliary Source، HBR/Pc Method یا Tolerance توسط این Part Approved/Qualified نشده است.

P06-CON-422 — هیچ Scientific Reviewer/Approver Identity، Organizational Competence Matrix، Risk Threshold، Cost Ceiling، Environment، SLO یا Runtime Fact Source-bound در این Part موجود نیست.

P06-CON-423 — `CSIP-EO-RS-STAGE-20` و P06 همچنان `DOMAIN_REVIEW_REQUIRED — NOT_NORMATIVELY_ACTIVATED` باقی می‌مانند.

### 24.2 Open Issueهای اجباری

P06-OI-001 — Historical Bytes و Approval Provenance Stage 20 `NOT_FOUND` و غیرقابل‌جعل‌اند.

P06-OI-002 — Exact Digest Successor باید Competent Domain Review، Independent Challenge، Fresh Approval و Manifest Registration دریافت کند؛ انجام نشده است.

P06-OI-003 — Competence Criteria، Reviewer Identities، Independence/Conflict Rules و Domain Approver `NOT_FOUND` هستند.

P06-OI-004 — Canonical Validation/Reference Datasetها، Oracles، Denominatorها و Acceptance Thresholdها انتخاب یا Approve نشده‌اند.

P06-OI-005 — Exact Engine Versions/Builds/Dependencies/Platforms و Qualification Profiles تعیین/اجرا نشده‌اند.

P06-OI-006 — Force-model، Propagation، Estimator، Integrator، Tolerance و Validity Profiles Adopt/Validate نشده‌اند.

P06-OI-007 — Canonical Time-scale، Leap/EOP، Frame Realization، Unit، Convention و Constant Profiles Approve نشده‌اند.

P06-OI-008 — Auxiliary-data Sources، Freshness/Prediction/Quality Policies و Snapshot Registry نهایی نشده‌اند.

P06-OI-009 — OD Observation Association، Weight/Bias/Reject، Conditioning و Covariance Health/Repair Policies نهایی نشده‌اند.

P06-OI-010 — Conjunction Screening، TCA، HBR، `Pc` Method، Sensitivity و High-impact Threshold/Profileها نهایی نشده‌اند.

P06-OI-011 — Independence Profiles، Common-cause Rules، Engine Mappings و Discrepancy Materiality Thresholdها Qualify نشده‌اند.

P06-OI-012 — Full Machine-readable Trace Graph برای تمام P06 Clauses/Consumer Parts Populate/Validate نشده است.

P06-OI-013 — `EVT-SCI` Scientific Event Types/Schemas هنوز Registry/Compatibility/Implementation/Verification ندارند.

P06-OI-014 — Technology/Runtime/Operational Owners، Workloads، Capacity، Cost و Environment Facts همچنان `UNKNOWN/NOT_FOUND` هستند.

P06-OI-015 — Command-path Negative Assurance Evidence اجرا نشده؛ Permanent Prohibition از P01/P05 پابرجاست و هیچ Test Route نباید ایجاد شود.

P06-OI-016 — Stage 32 همچنان `PROPOSED` است و Project Specification Freeze اجرا نشده است.

P06-CON-424 — Open Issue فقط با Closure Record تازه، Exact Evidence/Source/Digest، Competent Owner، Decision Status، Impacted Clause/Consumer و Residual Limitation قابل بسته‌شدن است.

P06-CON-425 — Summary، Part Acceptance، Model Output، Internal Audit یا Absence of Objection هیچ Open Issue را نمی‌بندد.

P06-CON-426 — New Evidence می‌تواند Open Issue را Refine یا Scope را Narrow کند؛ History/Counterevidence حذف نمی‌شود.

P06-CON-427 — `DOMAIN_REVIEW_REQUIRED` تا Closure معتبر P06-OI-002 و تمام Preconditions Applicable باقی می‌ماند.

P06-CON-428 — P07، P13، P16 یا P18 نمی‌توانند به‌تنهایی P06 Scientific Review Gate را بدون Competent Evidence ببندند.

P06-CON-429 — Approved Status Sourceهای P08–P17 به Prompt Part/Owner P06، Package، Implementation یا Production منتقل نمی‌شود.

P06-CON-430 — Historical Gap با Successor Similarity یا Decision Projection بسته نمی‌شود.

P06-DEN-203 — `PROPOSED` Decision نباید Approved نمایش داده شود.

P06-DEN-204 — Open Issue به‌دلیل Time/Token/Reviewer Absence حذف یا `NOT_APPLICABLE` نمی‌شود.

P06-DEN-205 — Missing Historical Source نباید Recovered Claim دریافت کند.

P06-DEN-206 — Internal Audit نباید P06-OI-002 را Closed کند.

P06-DEN-207 — Approved Downstream Stage Status Scientific Review P06 نیست.

P06-DEN-208 — Domain Review بدون Exact Digest/Fresh Approval Gate کافی نیست.

P06-DEN-209 — Engine Candidate Role Procurement/Qualification Decision نیست.

P06-DEN-210 — Open Issue Closure بدون Residual Limitation/Counterevidence Invalid است.

P06-FAIL-127 — Historical-recovery Claim نتیجه `HISTORICAL_STATUS_VIOLATION — REWORK_REQUIRED` دارد.

P06-FAIL-128 — Silent Open-issue Closure نتیجه `OPEN_ISSUE_DISPOSITION_INVALID` دارد.

P06-FAIL-129 — Decision Status Drift نتیجه `DECISION_STATUS_LAUNDERING` دارد.

P06-FAIL-130 — Domain-review Sentinel Removal نتیجه `SCIENTIFIC_REVIEW_GATE_VIOLATION — PART_NOT_ACCEPTED` دارد.

## 25. Part-level Acceptance، Audit و Anti-claimها

P06-REQ-038 — P06 فقط وقتی برای Assembly قابل‌پیشنهاد است که Header/Anchor/Footer/Pointer، Owner/Source Digest/Status، Required Sentinel، Owner Boundary، Scientific Domains، Trace Schema، Decision/Open Issue، Handoff و No-command Boundary کامل و سازگار باشند.

P06-REQ-039 — Audit داخلی باید بر Bytes واقعی Final File انجام شود و حداقل Clause ID، Sequence، Fence، YAML، Anchor، Source Digest، Status، Required-section، Owner-boundary، Trace-contract، Unsupported-claim، P07 Intrusion و Truncation را کنترل کند.

P06-REQ-040 — عبور از Structural/Semantic Audit فقط `PART_AUDITED — READY_FOR_USER_REVIEW` ایجاد می‌کند؛ Scientific Verification، Approval، Normative Activation یا Runtime Readiness نیست.

P06-PROC-006 — Checklist اجباری Part-level:

1. Filename `CSIP-EO_FMSP_P06_v0.9.0-draft.txt`؛
2. Package ID/Version و Part ID/Index/Count/Title دقیق؛
3. Start/End Anchor هرکدام دقیقاً یک‌بار؛
4. Prior `P05` و Next `P07`؛
5. Semantic Owner ID/Version/Digest/Status دقیق؛
6. Supporting Source Bindings/Digests/Statuses دقیق؛
7. Sentinel `DOMAIN_REVIEW_REQUIRED — NOT_NORMATIVELY_ACTIVATED`؛
8. Global Invariant Capsule؛
9. تمام ۱۱ موضوع Mandatory Assembly Contract §6.6؛
10. `CGR-REQ-003..005` Coverage؛
11. Unique/Gapless Clause IDs در هر Prefix؛
12. Balanced `~~~` Fences و Parse-valid YAML؛
13. Canonical Trace Field Coverage و No competing schema؛
14. Source Status Preservation و No Laundering؛
15. No Scientific Approval/Executed Validation/Operational Fitness Claim؛
16. No P07 Content Beyond Pointer؛
17. No Command/Uplink/Execution Path؛
18. Fixed Receiver Acknowledgment؛
19. Footer Fields و Visible End Anchor؛
20. Actual Line/Byte/SHA-256 Computation در External Manifest؛
21. No Truncation یا Payload بعد از End Anchor.

P06-CON-431 — Required-section Coverage باید Scientific Truth Hierarchy، Envelopes، Context، Engine Roles، Tiers/Confidence، OD/Covariance، Conjunction/Pc، Independence/Discrepancy، Equivalence/Reproducibility، AI Boundary و Maneuver No-command Boundary را Map کند.

P06-CON-432 — Clause Scan Pattern دقیق `P06-{INV|REQ|DEF|CON|PROC|DEN|FAIL|DEC|OI}-nnn` است.

P06-CON-433 — Duplicate Clause ID یا Gap در Sequence هر Prefix استفاده‌شده Blocking است.

P06-CON-434 — Fence Scan باید هر `~~~text`/`~~~yaml` را با Fence دقیق `~~~` ببندد.

P06-CON-435 — YAML Parse باید تمام YAML Blocks را با Parser واقعی بررسی کند؛ Model Confidence کافی نیست.

P06-CON-436 — Source Digest Scan باید Bytes/Digest Registry را با منابع Materialized معتبر تطبیق دهد؛ Digest جعلی ممنوع است.

P06-CON-437 — Deprecated Digest Scan باید عدم مصرف سه Digest غیرمجاز را به‌جز Denylist Documentation بررسی کند.

P06-CON-438 — Status Scan باید `NOT_APPROVED`، `NOT_FROZEN`، `DOMAIN_REVIEW_REQUIRED` و `NOT_NORMATIVELY_ACTIVATED` را حفظ کند.

P06-CON-439 — Unsupported-claim Scan باید Scoped Definition/Requirement را از Claim اجراشده جدا کند.

P06-CON-440 — Owner-boundary Scan باید P13 Equivalence/Assurance و P05 Authority Ownership را حفظ کند.

P06-CON-441 — Trace Audit باید ۳۵ Canonical Top-level Field، Clause/Requirement Separation، چهار Compression Operation و مستقل‌بودن Reconstitution را بررسی کند.

P06-CON-442 — Handoff Audit فقط `P07` را Next معرفی و AI/RAG/Memory Content را تولید نمی‌کند.

P06-CON-443 — Truncation Audit باید Fixed ACK، Footer و End Anchor را در انتهای Payload ببیند.

P06-CON-444 — Audit Numbers، Line Count، Byte Count و SHA-256 فقط از Final Bytes محاسبه می‌شوند و داخل Self-hashed Payload جعل نمی‌شوند.

P06-CON-445 — File Digest در External Manifest ثبت می‌شود؛ Header Field `PART_PAYLOAD_SHA256` با Pointer خارجی از Self-hash Cycle جلوگیری می‌کند.

P06-CON-446 — Internal Audit Correctness علمی، Legal/Security/Privacy/Cost/Operational Fitness یا Domain Approval را اثبات نمی‌کند.

P06-CON-447 — User Acceptance فقط Assembly Scope و Exact Delivered Part را پوشش می‌دهد.

P06-CON-448 — هر Post-acceptance Edit Revision/Digest/Audit تازه می‌خواهد و Prior Bytes/Status حفظ می‌شود.

P06-CON-449 — تمام Future Implementation/Test/Qualification/Release/Deployment/Operation/Freeze Gates مستقل باقی می‌مانند.

P06-CON-450 — P06 Complete Text هیچ Action Authority ایجاد نمی‌کند.

P06-CON-451 — Global Project State پس از دریافت تمام ۱۸ Part فقط `CONTEXT_ASSEMBLED — AWAITING_EXPLICIT_TASK` می‌تواند باشد.

P06-CON-452 — `CONTEXT_ASSEMBLED` نیز Project Freeze، Implementation Authorization، Runtime Verification، Deployment یا Production نیست.

P06-CON-453 — Part Acceptance نمی‌تواند Required Status Sentinel را حذف کند.

P06-CON-454 — P06 Audit Failure باید پیش از Delivery اصلاح شود و Failed Candidate برای Assembly ارسال نشود.

P06-DEN-211 — متن کامل یا Audit Pass Scientific Approval نیست.

P06-DEN-212 — Part Acceptance Normative Activation نیست.

P06-DEN-213 — Part Digest Runtime Verification نیست.

P06-DEN-214 — YAML/Structure Pass Domain Correctness نیست.

P06-DEN-215 — No Finding به معنی No Risk/No Defect نیست.

P06-DEN-216 — `PART_DECLARED_COMPLETE` Project/Package Complete نیست.

P06-DEN-217 — `PART_ACCEPTED_FOR_ASSEMBLY` Source Approved نیست.

P06-DEN-218 — `CONTEXT_ASSEMBLED` Implementation/Production Ready نیست.

P06-DEN-219 — P06 نباید همراه P07 تحویل یا تولید شود.

P06-DEN-220 — Audit/Delivery هیچ Spacecraft-command Path مجاز نمی‌کند.

P06-FAIL-131 — Missing Required Section نتیجه `P06_REQUIRED_COVERAGE_FAILED — REWORK_REQUIRED` دارد.

P06-FAIL-132 — Structural/Trace Audit Failure نتیجه `PART_NOT_ACCEPTED` دارد.

P06-FAIL-133 — Unsupported Approval/Validation Claim نتیجه `P06_STATUS_HONESTY_FAILED` دارد.

P06-FAIL-134 — P07 Intrusion نتیجه `PART_BOUNDARY_VIOLATION` دارد.

P06-FAIL-135 — Truncated End/ACK/Footer نتیجه `PART_TRUNCATED — CONTEXT_NOT_ACTIVATED` دارد.

P06-FAIL-136 — Command/Uplink Path نتیجه `E9/APR-X/INC-0/HARD_STOP` دارد.

### 25.1 Anti-claimهای صریح

این Part، تدوین، Audit، Delivery، Review یا پذیرش آن برای Assembly هیچ‌یک از ادعاها یا مجوزهای زیر را ایجاد نمی‌کند:

- Historical Stage 20 Recovery؛
- Approval، Ratification، Normative Activation یا Freeze مالک `CSIP-EO-RS-STAGE-20`؛
- Competent Scientific Review یا Independent Challenge؛
- اجرای Numerical Computation، Simulation، Propagation، OD، Conjunction Screening، `Pc` یا Monte Carlo؛
- Validation، Verification، Qualification یا Operational Fitness هیچ Engine/Profile/Result؛
- Approved بودن `T0..T4`، `PHY-C0..C5`، Scientific Envelopes یا Derived Definitions؛
- انتخاب Final Algorithm، Force Model، Estimator، Dataset، Tolerance، HBR یا `Pc` Method؛
- ایجاد Code، Dependency، Repository، Database، Event Schema، Service، Tool، Plugin، Infrastructure یا Credential؛
- ایجاد Approval، AuthorizationDecision، ExecutionLease، Risk Acceptance، Budget Authorization یا Spend؛
- Build، Release، Deployment، Pilot، Production، Operation یا Project Freeze؛
- Legal Compliance، Security/Privacy Certification، Safety Guarantee یا Mission Assurance؛
- Recommendation، Maneuver Decision، Command، Telecommand، Uplink، Flight Control یا Autonomous Maneuver Execution.

## 26. تحویل کنترل‌شده به Part 07

P06-CON-455 — P07 باید AI Advisory، Model Gateway، RAG، Knowledge، Memory و AI Confidence را در مالکیت خود تعریف و Physics-before-AI، Scientific Context، Result Status، Uncertainty، Evidence، Counterevidence و No-fabrication Contract P06 را Reference کند.

P06-CON-456 — P06 هیچ Model Gateway، AI Output Schema، Retrieval Rank، Knowledge Class، Memory Lifecycle یا AI Confidence Taxonomy متعلق به P07 را تعریف یا پیش‌تصویب نمی‌کند.

P06-CON-457 — P07 نباید AI/RAG/Memory Output را Canonical Scientific Truth، Physics Engine، Verification Evidence، Approval یا Execution Authority معرفی کند.

P06-CON-458 — P07 باید `NOT_COMPUTABLE|NOT_CONVERGED|DISPUTED|INDETERMINATE|INVALID` و Uncertainty/Limitation P06 را بدون Semantic Compression حفظ کند.

P06-CON-459 — P07 می‌تواند Scientific Artifact را توضیح/بازیابی کند اما هیچ Time/Frame/Unit/Covariance/Status/Confidence Level را Silent Change نمی‌دهد.

P06-CON-460 — `CSIP-EO-RS-STAGE-20` پس از Handoff نیز `DOMAIN_REVIEW_REQUIRED — NOT_NORMATIVELY_ACTIVATED` باقی می‌ماند.

P06-CON-461 — Part بعدی فقط Pointer زیر است:

- Part ID: `CSIP-EO-FMSP-P07`
- Part Index: `07 of 18`
- Title: `AI Advisory, RAG, Knowledge and Memory Boundary | مرز AI Advisory، RAG، Knowledge و Memory`
- Semantic Owner: `CSIP-EO-RS-STAGE-21`
- Receive Mode: `CONTEXT_ONLY`
- Action Authority: `NONE`

P06-CON-462 — P06 هیچ Clause یا Payload محتوایی P07 را در این Part تولید نمی‌کند.

P06-REQ-041 — P07 باید فقط در پیام/فایل جداگانه و پس از پذیرش صریح P06 و مجوز روشن کاربر آغاز شود؛ سکوت، تکمیل P06، عنوان/Owner/Digest معلوم یا وجود Candidate مجوز نیست.

P06-REQ-042 — پس از دریافت سالم این قسمت، تنها پاسخ مجاز متن ثابت زیر است و هیچ عبارت دیگری نباید قبل یا بعد از آن قرار گیرد:

~~~text
قسمت ۰۶ از ۱۸ ابرپرامپت نهایی CSIP-EO با موفقیت دریافت و ثبت شد.
هیچ تحلیل، طراحی جدید، پیاده‌سازی یا اقدام اجرایی آغاز نمی‌شود.
منتظر قسمت ۰۷ هستم.
~~~

P06-DEN-221 — Receiver نباید پس از P06 تحلیل یکپارچه، P07 Generation، Implementation یا Action را خودکار آغاز کند.

P06-DEN-222 — ACK دریافت Approval علمی، Source Approval، Package Approval یا Project Freeze نیست.

P06-DEN-223 — Handoff Pointer P07 محتوای P07 یا مجوز تولید آن نیست.

P06-DEN-224 — هیچ Handoff، ACK یا Future Part مسیر Spacecraft Command/Uplink/Execution ایجاد نمی‌کند.

RECEIVER_MUST_WAIT_FOR_NEXT_PART: TRUE
PART_DECLARED_COMPLETE: TRUE
NEXT_EXPECTED_PART: P07
RECEPTION_ACTION: ACK_ONLY
<<<CSIP-EO-FMSP-18P|0.9.0-draft|P06|END>>>
