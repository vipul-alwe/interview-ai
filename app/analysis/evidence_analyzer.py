from app.llm.client import llm_client
from app.llm.parser import LLMParser


class EvidenceAnalyzer:

    def _build_prompt(
        self,
        candidate_segments,
    ) -> str:

        transcript = "\n\n".join(
            (
                f"SEGMENT {index}\n"
                f"TIME: "
                f"{segment.start_time:.2f}-"
                f"{segment.end_time:.2f}\n"
                f"{segment.text}"
            )
            for index, segment in enumerate(
                candidate_segments,
                start=1,
            )
        )

        return f"""
You are a behavioral evidence extraction engine
for a professional interview.

The following transcript contains ONLY the
candidate's speech.

Extract EVERY distinct behavioral evidence atom
from the candidate's answers.

Do NOT score competencies.
Do NOT map competencies.
Do NOT infer behavior.

A single answer may contain MANY atoms.

Each atom must represent ONE observable behavior.

Examples:

- identifying a customer problem
- gathering feedback
- analyzing data
- researching competitors
- collaborating with another team
- making a decision
- persuading stakeholders
- executing an action
- measuring an outcome
- learning from an outcome

Do NOT combine unrelated behaviors.

IMPORTANT:

Only extract behavior supported by the candidate's
actual words.

Do not turn a business result into a behavior.

For example:

"Sales increased 50%"

is not itself a behavioral atom.

But:

"I proposed a small test before changing the
entire strategy"

is a behavioral atom.

Do not invent behavior.

Do not include interviewer speech.

Preserve the exact source timestamps.

Every atom must contain an exact quote from
the candidate.

Do not invent quotations.

If reasoning is not explicitly stated, use "".

If an outcome is not explicitly stated, use "".

SOURCE TIMESTAMPS:

Use the timestamps of the source segments containing
the evidence.

If an atom spans multiple consecutive segments,
use the earliest start time and latest end time.

Return ONLY valid JSON.

FORMAT:

{{
  "behavioral_atoms": [
    {{
      "id": "A001",
      "source_event": "SEGMENT 1",
      "source_start": 10.2,
      "source_end": 20.5,
      "behavior": "Candidate analyzed performance metrics to determine upcoming product assortments.",
      "decision_reasoning": "Used performance data to guide product selection.",
      "result": "",
      "quote": "analyze performance metrics, and then use that to essentially come up with upcoming product assortments"
    }}
  ]
}}

CANDIDATE TRANSCRIPT:

{transcript}
"""

    def analyze(
        self,
        candidate_segments,
    ) -> dict:

        if not candidate_segments:
            raise ValueError(
                "No candidate transcript segments available."
            )

        prompt = self._build_prompt(
            candidate_segments
        )

        print(
            "[EVIDENCE] Extracting behavioral atoms..."
        )

        raw = llm_client.generate_json(
            prompt=prompt,
            schema={
                "type": "object",
                "properties": {
                    "behavioral_atoms": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string"
                                },
                                "source_event": {
                                    "type": "string"
                                },
                                "source_start": {
                                    "type": "number"
                                },
                                "source_end": {
                                    "type": "number"
                                },
                                "behavior": {
                                    "type": "string"
                                },
                                "decision_reasoning": {
                                    "type": "string"
                                },
                                "result": {
                                    "type": "string"
                                },
                                "quote": {
                                    "type": "string"
                                },
                            },
                            "required": [
                                "id",
                                "source_event",
                                "source_start",
                                "source_end",
                                "behavior",
                                "decision_reasoning",
                                "result",
                                "quote",
                            ],
                        },
                    }
                },
                "required": [
                    "behavioral_atoms"
                ],
            },
        )

        data = LLMParser.parse_json(raw)

        atoms = data.get(
            "behavioral_atoms",
            [],
        )

        print(
            "[EVIDENCE] Behavioral atoms: "
            f"{len(atoms)}"
        )

        return {
            "behavioral_atoms": atoms
        }


evidence_analyzer = EvidenceAnalyzer()