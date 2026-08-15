"""Advisory-only primary astrodynamics computation boundary."""

from ailora.services.astrodynamics.adapter import Sgp4Engine
from ailora.services.astrodynamics.analysis import (
    BoundedConjunctionAssessment,
    ConjunctionAnalysisConfig,
    SafeScientificLabel,
    assess_bounded_conjunction,
)
from ailora.services.astrodynamics.config import AstrodynamicsConfig
from ailora.services.astrodynamics.covariance import CovarianceContract
from ailora.services.astrodynamics.models import PropagationRequest, PropagationResult, TLEInput
from ailora.services.astrodynamics.service import AstrodynamicsService
from ailora.services.astrodynamics.tca import (
    TcaAnalyzer,
    TcaResult,
    TcaSearchConfig,
    TcaSearchRequest,
)
from ailora.services.astrodynamics.verification import (
    DifferentialVerificationResult,
    IndependentTcaReference,
    VerificationError,
    VerificationErrorCode,
    VerificationStatus,
    VerificationTolerance,
    reference_content_digest,
    verify_tca_result,
)

__all__ = [
    "AstrodynamicsConfig",
    "AstrodynamicsService",
    "BoundedConjunctionAssessment",
    "ConjunctionAnalysisConfig",
    "CovarianceContract",
    "PropagationRequest",
    "PropagationResult",
    "Sgp4Engine",
    "SafeScientificLabel",
    "TcaAnalyzer",
    "TcaResult",
    "TcaSearchConfig",
    "TcaSearchRequest",
    "TLEInput",
    "assess_bounded_conjunction",
    "DifferentialVerificationResult",
    "IndependentTcaReference",
    "VerificationError",
    "VerificationErrorCode",
    "VerificationStatus",
    "VerificationTolerance",
    "reference_content_digest",
    "verify_tca_result",
]
