from app.domain.response import Response
from app.speech.speech_feature_extractor import (
    speech_feature_extractor,
)


class SpeechAnalysisService:

    def analyze(
        self,
        response: Response,
    ) -> Response:

        response.speech_features = (
            speech_feature_extractor.extract(
                response.segments
            )
        )

        return response


speech_analysis_service = SpeechAnalysisService()