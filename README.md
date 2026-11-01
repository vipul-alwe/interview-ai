# Interview AI

### Evidence-Based Interview Intelligence & Candidate Assessment

Interview AI is an AI-powered interview assessment system designed to transform recorded interviews into structured, evidence-backed candidate evaluations.

Rather than attempting real-time interview analysis, the system processes complete interview recordings, builds a contextual transcript and uses Large Language Models (LLMs) to evaluate candidate responses across 25 defined competencies.

The focus is on contextual understanding, traceable evidence and consistent candidate assessment rather than superficial keyword matching.

## Overview

Traditional interview assessments depend heavily on interviewer interpretation, manual note-taking and subjective evaluation.

Interview AI aims to introduce a structured, evidence-driven assessment workflow by combining speech processing, speaker attribution, information extraction and LLM-based reasoning.

The system analyses the complete interview before generating competency assessments, allowing the model to evaluate responses in their conversational context.

## Core Pipeline

```text
       Interview Recording
                |
                v
        Audio Processing
                |
                v
          Transcription
          (Whisper)
                |
                v
       Speaker Attribution
         (Diarization)
                |
                v
       Speaker-Aligned
           Transcript
                |
                v
       Candidate Evidence
          Extraction
                |
                v
        Evidence Atoms
     (Timestamped Statements)
                |
                v
       Evidence Normalization
                |
                v
        LLM Assessment
                |
                v
       25 Competency Scores
                |
                v
       Evidence Verification
                |
                v
       Structured Assessment
```

## Key Capabilities

### 1. Audio Transcription

Processes complete interview recordings and converts spoken conversations into timestamped transcript segments.

- Whisper-based speech recognition.
- Segment-level timestamps.
- Full-interview transcription.
- Structured transcript representation.

### 2. Speaker Attribution

Uses speaker diarization to distinguish conversational participants and associate transcript segments with speakers.

The assessment pipeline uses speaker attribution to identify candidate responses and isolate relevant interview evidence.

### 3. Evidence Extraction

Extracts meaningful statements from candidate responses and converts them into structured behavioural evidence.

Each evidence item is designed to retain:

- Original candidate quotation.
- Timestamp reference.
- Relevant actions and decisions.
- Context surrounding the response.

The objective is to preserve what the candidate actually said rather than generate generic competency descriptions.

### 4. Competency Assessment

Evaluates candidates against a predefined framework of 25 competencies.

Instead of evaluating isolated keywords, the LLM considers the complete interview context and available behavioural evidence.

The assessment pipeline connects extracted evidence to relevant competencies and produces structured evaluations.

### 5. Evidence Verification

Assessment outputs are designed to remain traceable to the original interview.

The verification stage helps ensure that competency rationales are supported by actual candidate statements rather than invented achievements, assumptions or generic descriptions.

## Assessment Architecture

The evidence processing pipeline follows a structured sequence:

```text
Candidate Responses
        |
        v
Evidence Extraction
        |
        v
Evidence Normalization
        |
        v
Competency Mapping
        |
        v
Contextual Assessment
        |
        v
Evidence Verification
```

This separation allows evidence extraction, normalization and assessment to be developed and evaluated independently.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| Speech Recognition | Faster-Whisper |
| Speaker Diarization | pyannote.audio |
| LLM | Qwen 2.5 7B Instruct |
| Model Format | GGUF, Q4_K_M |
| Inference Runtime | llama.cpp |
| Audio Processing | SoundDevice, SoundFile |
| AI Processing | Python-based modular services |

## Local LLM Inference

Interview AI explores locally hosted LLM inference for contextual interview assessment.

The current model configuration includes:

- Qwen 2.5 7B Instruct.
- Q4_K_M quantisation.
- GGUF model format.
- llama.cpp inference runtime.

Using local inference provides an opportunity to experiment with model performance, computational constraints and structured reasoning without depending entirely on external inference APIs.

## Engineering Principles

The system is built around several important design principles:

- **Context over keywords:** Evaluate responses in the context of the complete interview.
- **Evidence before scoring:** Extract and normalise behavioural evidence before competency assessment.
- **Traceability:** Connect assessment rationales to actual candidate statements.
- **Modularity:** Keep transcription, evidence extraction and assessment as independent processing stages.
- **Structured outputs:** Generate consistent, machine-readable assessment results.
- **Local inference:** Explore privacy-conscious, hardware-efficient LLM deployment.

## Project Objectives

Interview AI explores how AI systems can make interview evaluation more structured, consistent and explainable.

The broader engineering challenges include speech processing, speaker attribution, long-context reasoning, evidence extraction, LLM orchestration and reliable evaluation pipelines.

## Developer

**Vipul Alwe**

AI & Automation Engineer | Generative AI | LLM Engineering | Python

[GitHub Profile](https://github.com/vipul-alwe)

---

*Interview AI — Turning interview conversations into structured, evidence-backed intelligence.*
