# Interview AI

### Real-Time AI Interview Assistant

Interview AI is an AI-powered application designed to process interview conversations in real time, extract meaningful information from spoken responses and generate structured insights using local Large Language Models (LLMs).

The project explores the intersection of speech processing, real-time communication, feature extraction and on-device AI inference.

## Overview

Traditional interview analysis often requires manually reviewing recordings, identifying important responses and extracting relevant candidate information.

Interview AI aims to streamline this process through an automated audio processing pipeline that converts spoken conversations into structured, AI-generated insights.

The system uses a WebSocket-based communication layer to receive audio chunks and process them through a modular backend pipeline.

## Key Capabilities

- Real-time audio chunk ingestion.
- WebSocket-based audio communication.
- Audio processing and transcription pipeline.
- Automated feature extraction from interview conversations.
- Local LLM inference.
- Modular backend architecture separating transcription and analysis services.

## Technical Architecture

The application follows a modular backend architecture built around asynchronous audio processing.

```text
          Audio Input
               |
               v
       Audio Capture Layer
               |
               v
        WebSocket Server
               |
               v
       Audio Processing
          Pipeline
               |
         +-----+-----+
         |           |
         v           v
   Transcription  Feature
     Service      Extraction
         |           |
         +-----+-----+
               |
               v
        LLM Processing
               |
               v
      Structured Insights
```

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| Communication | WebSockets |
| Audio Processing | SoundDevice, SoundFile |
| AI Inference | Local LLMs |
| Model Runtime | llama.cpp / GGUF ecosystem |
| Model | Qwen 2.5 7B Instruct (4-bit quantised) |

## Backend Architecture

The backend is organised into modular components:

- **Interview API:** Handles interview-related application endpoints.
- **WebSocket API:** Manages real-time audio communication through `/ws/audio`.
- **Transcript Service:** Handles transcription-related processing.
- **Feature Extraction Service:** Extracts relevant information from interview conversations.
- **Audio Pipeline:** Processes incoming audio chunks and coordinates downstream services.

## Local AI Inference

Interview AI experiments with locally hosted language models to reduce reliance on external inference APIs.

The development environment includes:

- Qwen 2.5 7B Instruct.
- GGUF quantisation (Q4_K_M).
- Local model inference.
- Hardware-conscious model deployment.

This approach explores the practical trade-offs between model size, inference performance and available computing resources.

## Project Structure

```text
interview-ai/
│
├── app/
│   ├── api/
│   │   ├── interview/
│   │   └── websocket/
│   │
│   ├── services/
│   │   ├── transcript_service/
│   │   └── feature_extraction_service/
│   │
│   └── ...
│
├── models/
│   └── llm/
│
├── ...
│
└── README.md
```

*The structure above illustrates the primary architectural components; the complete repository structure may differ.*

## Engineering Focus

This project explores several engineering challenges:

- Designing low-latency audio ingestion pipelines.
- Handling continuous audio streams through WebSockets.
- Separating transcription and feature extraction into independent services.
- Running quantised LLMs on local hardware.
- Building modular AI applications that combine multiple processing stages.

## Project Status

An experimental AI engineering project focused on real-time audio processing and LLM-powered interview analysis.

## Developer

**Vipul Alwe**

AI & Automation Engineer | Generative AI | Python | LLM Engineering

[GitHub](https://github.com/vipul-alwe)

---

*Exploring practical applications of local AI inference and real-time intelligent systems.*
