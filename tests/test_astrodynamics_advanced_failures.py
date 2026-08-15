from __future__ import annotations

from types import SimpleNamespace

import pytest

from ailora.services.astrodynamics.tca import (
    TcaAnalysisError,
    TcaAnalyzer,
    TcaErrorCode,
    TcaSearchConfig,
)
from tests.test_astrodynamics_tca import EPOCH, LinearPropagation, search_request


def test_iteration_limit_reports_typed_non_convergence() -> None:
    analyzer = TcaAnalyzer(
        LinearPropagation(EPOCH),  # type: ignore[arg-type]
        TcaSearchConfig(
            coarse_intervals=20,
            max_iterations=1,
            max_evaluations=100,
            time_tolerance_seconds=1e-9,
        ),
    )
    with pytest.raises(TcaAnalysisError) as captured:
        analyzer.find(search_request())
    assert captured.value.code is TcaErrorCode.NOT_CONVERGED


def test_evaluation_budget_exhaustion_is_typed() -> None:
    analyzer = TcaAnalyzer(
        LinearPropagation(EPOCH),  # type: ignore[arg-type]
        TcaSearchConfig(
            coarse_intervals=20,
            max_iterations=64,
            max_evaluations=23,
            time_tolerance_seconds=1e-9,
        ),
    )
    with pytest.raises(TcaAnalysisError) as captured:
        analyzer.find(search_request())
    assert captured.value.code is TcaErrorCode.EVALUATION_BUDGET_EXHAUSTED


class NonfinitePropagation:
    def propagate(self, request: object) -> object:
        return SimpleNamespace(
            position_km=(float("nan"), 0.0, 0.0),
            velocity_km_s=(0.0, 0.0, 0.0),
            target_epoch=EPOCH,
        )


def test_nonfinite_state_fails_closed() -> None:
    analyzer = TcaAnalyzer(
        NonfinitePropagation(),  # type: ignore[arg-type]
        TcaSearchConfig(coarse_intervals=4, max_evaluations=20),
    )
    with pytest.raises(TcaAnalysisError) as captured:
        analyzer.find(search_request())
    assert captured.value.code is TcaErrorCode.NONFINITE_STATE
