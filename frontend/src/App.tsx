import { useRef, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

type NextQuestion = {
  question_id: string;
  competency_id: string;
  question: string;
  intent?: string;
  context?: string;
  follow_up_to?: string | null;
};

type AnalysisMessage = {
  type: "analysis" | "error";
  response_id?: string;
  question_id?: string;
  transcript?: string;
  evidence?: unknown[];
  competencies?: Record<string, unknown>;
  next_question?: NextQuestion;
  message?: string;
};

function App() {
  const [interviewId, setInterviewId] = useState<string | null>(null);
  const [question, setQuestion] = useState("");
  const [transcript, setTranscript] = useState("");
  const [status, setStatus] = useState<
    "idle" | "starting" | "connecting" | "listening" | "processing" | "error" | "stopped"
  >("idle");

  const websocketRef = useRef<WebSocket | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const processorRef = useRef<ScriptProcessorNode | null>(null);
  const sourceRef = useRef<MediaStreamAudioSourceNode | null>(null);

  async function startInterview() {
    if (interviewId) {
      return;
    }

    setStatus("starting");
    setTranscript("");

    try {
      const response = await fetch(
        `${API_URL}/interview/start`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        const text = await response.text();

        throw new Error(
          `Backend returned ${response.status}: ${text}`
        );
      }

      const data = await response.json();

      console.log(
        "[INTERVIEW] Started:",
        data
      );

      setInterviewId(data.interview_id);

      if (data.initial_question) {
        setQuestion(
          typeof data.initial_question === "string"
            ? data.initial_question
            : data.initial_question.question
        );
      }

      setStatus("connecting");

      connectWebSocket(
        data.interview_id
      );
    } catch (error) {
      console.error(
        "[INTERVIEW] Start failed:",
        error
      );

      setStatus("error");
    }
  }

  function connectWebSocket(id: string) {
    const websocket = new WebSocket(
      `ws://127.0.0.1:8000/ws/audio/${id}`
    );

    websocket.binaryType = "arraybuffer";

    websocket.onopen = async () => {
      console.log(
        "[WS] Connected."
      );

      websocketRef.current = websocket;

      try {
        await startMicrophone();

        setStatus("listening");
      } catch (error) {
        console.error(
          "[MIC] Failed:",
          error
        );

        setStatus("error");

        websocket.close();
      }
    };

    websocket.onmessage = (
      event
    ) => {
      try {
        const message: AnalysisMessage =
          JSON.parse(event.data);

        console.log(
          "[WS] Message:",
          message
        );

        if (
          message.type === "analysis"
        ) {
          if (message.transcript) {
            setTranscript(
              message.transcript
            );
          }

          if (
            message.next_question
          ) {
            setQuestion(
              message.next_question.question
            );
          }

          setStatus("listening");
        }

        if (
          message.type === "error"
        ) {
          console.error(
            "[BACKEND ERROR]",
            message.message
          );

          setStatus("error");
        }
      } catch (error) {
        console.error(
          "[WS] Invalid message:",
          error
        );
      }
    };

    websocket.onerror = (
      error
    ) => {
      console.error(
        "[WS] Error:",
        error
      );

      setStatus("error");
    };

    websocket.onclose = (
      event
    ) => {
      console.log(
        "[WS] Closed:",
        event.code,
        event.reason
      );

      websocketRef.current = null;

      stopMicrophone();

      if (
        status !== "stopped"
      ) {
        setStatus("stopped");
      }
    };
  }

  async function startMicrophone() {
    const stream =
      await navigator.mediaDevices.getUserMedia(
        {
          audio: {
            channelCount: 1,
            sampleRate: 16000,

            // Browser-level processing.
            echoCancellation: true,
            noiseSuppression: true,
            autoGainControl: true,
          },
        }
      );

    streamRef.current = stream;

    const audioContext =
      new AudioContext({
        sampleRate: 16000,
      });

    audioContextRef.current =
      audioContext;

    if (
      audioContext.state ===
      "suspended"
    ) {
      await audioContext.resume();
    }

    const source =
      audioContext.createMediaStreamSource(
        stream
      );

    sourceRef.current = source;

    /*
     * We keep the existing PCM pipeline because
     * the backend expects raw PCM audio.
     */
    const processor =
      audioContext.createScriptProcessor(
        4096,
        1,
        1
      );

    processorRef.current =
      processor;

    processor.onaudioprocess = (
      event
    ) => {
      const websocket =
        websocketRef.current;

      if (
        !websocket ||
        websocket.readyState !==
          WebSocket.OPEN
      ) {
        return;
      }

      const input =
        event.inputBuffer.getChannelData(
          0
        );

      /*
       * Convert Float32 [-1, 1]
       * to signed 16-bit PCM.
       */
      const pcm =
        new Int16Array(
          input.length
        );

      for (
        let i = 0;
        i < input.length;
        i++
      ) {
        const sample =
          Math.max(
            -1,
            Math.min(
              1,
              input[i]
            )
          );

        pcm[i] =
          sample < 0
            ? sample * 32768
            : sample * 32767;
      }

      websocket.send(
        pcm.buffer
      );
    };

    source.connect(
      processor
    );

    /*
     * ScriptProcessor needs to be connected
     * to keep processing active.
     *
     * We don't want audible microphone
     * feedback, so connect through a zero-gain
     * output node.
     */
    const silentGain =
      audioContext.createGain();

    silentGain.gain.value = 0;

    processor.connect(
      silentGain
    );

    silentGain.connect(
      audioContext.destination
    );

    console.log(
      "[MIC] Microphone started."
    );
  }

  function stopMicrophone() {
    processorRef.current?.disconnect();
    sourceRef.current?.disconnect();

    processorRef.current = null;
    sourceRef.current = null;

    if (
      streamRef.current
    ) {
      streamRef.current
        .getTracks()
        .forEach(
          (track) => track.stop()
        );

      streamRef.current = null;
    }

    if (
      audioContextRef.current
    ) {
      audioContextRef.current
        .close()
        .catch(() => {});

      audioContextRef.current =
        null;
    }

    console.log(
      "[MIC] Microphone stopped."
    );
  }

  function stopInterview() {
    setStatus("stopped");

    stopMicrophone();

    const websocket =
      websocketRef.current;

    if (websocket) {
      websocket.close();

      websocketRef.current =
        null;
    }
  }

  return (
    <main
      style={{
        maxWidth: 900,
        margin: "0 auto",
        padding: 40,
        fontFamily:
          "Inter, system-ui, sans-serif",
      }}
    >
      <h1>Interview AI</h1>

      <section
        style={{
          marginTop: 40,
          padding: 32,
          border:
            "1px solid #ddd",
          borderRadius: 16,
        }}
      >
        <p
          style={{
            fontSize: 13,
            color: "#777",
            textTransform:
              "uppercase",
          }}
        >
          Interview Question
        </p>

        <h2
          style={{
            lineHeight: 1.5,
          }}
        >
          {question ||
            "Press Start Interview to begin."}
        </h2>

        <p>
          Status:{" "}
          <strong>
            {status}
          </strong>
        </p>

        {!interviewId ||
        status === "stopped" ||
        status === "error" ? (
          <button
            onClick={
              startInterview
            }
            disabled={
              status === "starting" ||
              status === "connecting"
            }
          >
            {status === "starting"
              ? "Starting..."
              : "Start Interview"}
          </button>
        ) : (
          <button
            onClick={
              stopInterview
            }
          >
            Stop Interview
          </button>
        )}
      </section>

      <section
        style={{
          marginTop: 24,
          padding: 32,
          border:
            "1px solid #ddd",
          borderRadius: 16,
        }}
      >
        <p
          style={{
            fontSize: 13,
            color: "#777",
            textTransform:
              "uppercase",
          }}
        >
          Latest Response
        </p>

        <p
          style={{
            lineHeight: 1.6,
            minHeight: 50,
          }}
        >
          {transcript ||
            "Your response will appear here."}
        </p>
      </section>
    </main>
  );
}

export default App;