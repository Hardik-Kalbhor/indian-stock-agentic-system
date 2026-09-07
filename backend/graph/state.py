from typing import Any, TypedDict

from typing_extensions import NotRequired

from backend.agents.schemas import (
    Step1Output,
    Step2Output,
    Step3Output,
    Step4Output,
    Step5Output,
    Step6Output,
)


class PipelineGraphState(TypedDict, total=False):
    # Initial state (provided by the user)
    user_sector_name: NotRequired[str | None]
    user_compare_tickers: NotRequired[list[str] | None]
    user_target_ticker: NotRequired[str | None]

    # Pipeline decisions
    selected_sector: NotRequired[str | None]
    shortlisted_tickers: NotRequired[list[str] | None]
    winning_ticker: NotRequired[str | None]

    # Step results (to be returned to the client)
    step1_result: NotRequired[Step1Output | dict[str, Any] | None]
    step2_result: NotRequired[Step2Output | dict[str, Any] | None]
    step3_result: NotRequired[Step3Output | dict[str, Any] | None]
    step4_result: NotRequired[Step4Output | dict[str, Any] | None]
    step5_result: NotRequired[Step5Output | dict[str, Any] | None]
    step6_result: NotRequired[Step6Output | dict[str, Any] | None]

