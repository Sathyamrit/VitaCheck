/**
 * Phase 1: Streaming Diagnostic Hook
 * 
 * React hook for consuming Server-Sent Events from /chat/stream endpoint.
 * Provides real-time token updates, extracted symptoms, and RAG context.
 */

import { useState, useCallback, useRef } from 'react';

export interface StreamEvent {
  type: 'status' | 'extracted' | 'rag_context' | 'token' | 'completed' | 'error';
  message?: string;
  data?: any;
  content?: string;
  retrieved?: number;
  preview?: string;
}

export interface DiagnosisState {
  status: 'idle' | 'loading' | 'streaming' | 'completed' | 'error';
  extracted: any | null;
  ragContext: string | null;
  diagnosis: string;
  currentMessage: string;
  ttft: number | null; // Time to first token (ms)
  totalTime: number | null;
  error: string | null;
}

/**
 * useStreamingDiagnosis
 * 
 * @returns {Object} State and callbacks for streaming diagnosis
 * 
 * Example:
 * ```tsx
 * const { diagnosis, status, streamDiagnosis } = useStreamingDiagnosis();
 * 
 * const handleSubmit = async (input: string) => {
 *   await streamDiagnosis(input);
 * };
 * 
 * return (
 *   <div>
 *     <input onChange={(e) => setInput(e.target.value)} />
 *     <button onClick={() => handleSubmit(input)}>Diagnose</button>
 *     <div>{status === 'streaming' && 'Loading...'}</div>
 *     <div>{diagnosis}</div>
 *   </div>
 * );
 * ```
 */
export function useStreamingDiagnosis() {
  const [state, setState] = useState<DiagnosisState>({
    status: 'idle',
    extracted: null,
    ragContext: null,
    diagnosis: '',
    currentMessage: '',
    ttft: null,
    totalTime: null,
    error: null,
  });

  const eventSourceRef = useRef<EventSource | null>(null);
  const startTimeRef = useRef<number | null>(null);
  const ttftRef = useRef<number | null>(null);

  const streamDiagnosis = useCallback(async (userInput: string, userId?: string) => {
    // Reset state
    setState({
      status: 'loading',
      extracted: null,
      ragContext: null,
      diagnosis: '',
      currentMessage: '',
      ttft: null,
      totalTime: null,
      error: null,
    });

    startTimeRef.current = Date.now();
    ttftRef.current = null;

    try {
      // Close any existing EventSource
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }

      // Create new EventSource connection with POST request
      // Note: This uses a workaround since EventSource doesn't support POST
      // We'll use fetch with ReadableStream instead
      await streamDiagnosisWithFetch(userInput, userId);
    } catch (error) {
      setState(prev => ({
        ...prev,
        status: 'error',
        error: error instanceof Error ? error.message : 'Unknown error',
      }));
    }
  }, []);

  const streamDiagnosisWithFetch = async (userInput: string, userId?: string) => {
    try {
      const response = await fetch('http://localhost:8000/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: userInput,
          user_id: userId,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('Response body is not readable');
      }

      setState(prev => ({ ...prev, status: 'streaming' }));

      // Read stream
      while (true) {
        const { done, value } = await reader.read();

        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const jsonStr = line.slice(6);
              const event: StreamEvent = JSON.parse(jsonStr);

              // Record TTFT on first token
              if (event.type === 'token' && ttftRef.current === null) {
                ttftRef.current = Date.now() - (startTimeRef.current || 0);
                setState(prev => ({
                  ...prev,
                  ttft: ttftRef.current,
                  status: 'streaming',
                }));
              }

              // Process event types
              setState(prev => {
                switch (event.type) {
                  case 'status':
                    return {
                      ...prev,
                      currentMessage: event.message || '',
                    };

                  case 'extracted':
                    return {
                      ...prev,
                      extracted: event.data,
                      currentMessage: `Symptoms extracted: ${event.data.symptoms.join(', ')}`,
                    };

                  case 'rag_context':
                    return {
                      ...prev,
                      ragContext: event.preview,
                      currentMessage: `Retrieved ${event.retrieved} bytes of medical context`,
                    };

                  case 'token':
                    return {
                      ...prev,
                      diagnosis: prev.diagnosis + (event.content || ''),
                      status: 'streaming',
                    };

                  case 'completed':
                    const totalTime = Date.now() - (startTimeRef.current || 0);
                    return {
                      ...prev,
                      status: 'completed',
                      totalTime,
                      currentMessage: `Diagnosis complete (${totalTime}ms)`,
                    };

                  case 'error':
                    return {
                      ...prev,
                      status: 'error',
                      error: event.message || 'Stream error',
                    };

                  default:
                    return prev;
                }
              });
            } catch (e) {
              console.warn('Failed to parse event:', line, e);
            }
          }
        }
      }

      // Mark as complete if not already
      setState(prev => 
        prev.status === 'streaming' 
          ? { 
              ...prev, 
              status: 'completed',
              totalTime: Date.now() - (startTimeRef.current || 0)
            }
          : prev
      );
    } catch (error) {
      setState(prev => ({
        ...prev,
        status: 'error',
        error: error instanceof Error ? error.message : 'Unknown error',
      }));
    }
  };

  const resetDiagnosis = useCallback(() => {
    setState({
      status: 'idle',
      extracted: null,
      ragContext: null,
      diagnosis: '',
      currentMessage: '',
      ttft: null,
      totalTime: null,
      error: null,
    });
  }, []);

  return {
    ...state,
    streamDiagnosis,
    resetDiagnosis,
  };
}

/**
 * useStreamingDiagnosisSSE
 * 
 * Alternative implementation using EventSource (requires GET endpoint).
 * Currently commented out because we're using fetch for POST support.
 */
export function useStreamingDiagnosisSSE() {
  const [state, setState] = useState<DiagnosisState>({
    status: 'idle',
    extracted: null,
    ragContext: null,
    diagnosis: '',
    currentMessage: '',
    ttft: null,
    totalTime: null,
    error: null,
  });

  const eventSourceRef = useRef<EventSource | null>(null);

  const streamDiagnosis = useCallback(async (userInput: string) => {
    setState(prev => ({ ...prev, status: 'loading' }));

    // Encode input for URL (if using GET endpoint)
    const encodedInput = encodeURIComponent(userInput);

    try {
      eventSourceRef.current = new EventSource(`/chat/stream?input=${encodedInput}`);

      eventSourceRef.current.onmessage = (event) => {
        try {
          const data: StreamEvent = JSON.parse(event.data);

          setState(prev => {
            switch (data.type) {
              case 'status':
                return { ...prev, currentMessage: data.message || '' };
              case 'token':
                return { ...prev, diagnosis: prev.diagnosis + (data.content || '') };
              case 'completed':
                return { ...prev, status: 'completed' };
              case 'error':
                return { ...prev, status: 'error', error: data.message };
              default:
                return prev;
            }
          });
        } catch (e) {
          console.error('Parse error:', e);
        }
      };

      eventSourceRef.current.onerror = () => {
        setState(prev => ({
          ...prev,
          status: 'error',
          error: 'Connection lost',
        }));
        if (eventSourceRef.current) {
          eventSourceRef.current.close();
        }
      };
    } catch (error) {
      setState(prev => ({
        ...prev,
        status: 'error',
        error: error instanceof Error ? error.message : 'Connection failed',
      }));
    }
  }, []);

  const closeStream = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
  }, []);

  return {
    ...state,
    streamDiagnosis,
    closeStream,
  };
}

/**
 * useDiagnosisDisplay
 * 
 * Helper hook for rendering streaming diagnosis with formatting.
 */
export interface DisplayOptions {
  showThinking?: boolean;
  showExtracted?: boolean;
  showContext?: boolean;
}


// export function useDiagnosisDisplay(diagnosis: string, options: DisplayOptions = {}) {
//   const {
//     showThinking = true,
//     showExtracted = true,
//     showContext = true,
//   } = options;

//   // Extract <think> blocks if present
//   const thinkingRegex = /<think>([\s\S]*?)<\/think>/g;
//   const thinking = showThinking ? (diagnosis.match(thinkingRegex) || []).join('\n') : '';
//   const response = diagnosis.replace(thinkingRegex, '').trim();

//   return {
//     thinking,
//     response,
//     hasThinking: thinking.length > 0,
//     formatted: {
//       thinking: thinking.replace(/<\/?think>/g, ''),
//       response,
//     },
//   };
// }

export function useDiagnosisDisplay(diagnosis: string, options: DisplayOptions = {}) {
  const { showThinking = true } = options;

  const thinkStartTag = '<think>';
  const thinkEndTag = '</think>';

  const startIndex = diagnosis.indexOf(thinkStartTag);
  const endIndex = diagnosis.indexOf(thinkEndTag);

  let thinking = '';
  let response = diagnosis;

  const hasThinkingStarted = startIndex !== -1;

  if (hasThinkingStarted && showThinking) {
    if (endIndex !== -1) {
      // Thought is complete: extract the middle
      thinking = diagnosis.substring(startIndex + thinkStartTag.length, endIndex);
      // Remove thought tags and content from the main response
      response = (diagnosis.substring(0, startIndex) + diagnosis.substring(endIndex + thinkEndTag.length)).trim();
    } else {
      // Thought is still streaming: everything after <think> is thinking
      thinking = diagnosis.substring(startIndex + thinkStartTag.length);
      // Response is only what came BEFORE the thinking tag
      response = diagnosis.substring(0, startIndex).trim();
    }
  }

  return {
    thinking,
    response,
    hasThinking: hasThinkingStarted,
    formatted: {
      thinking: thinking.trim(),
      response: response.trim(),
    },
  };
}