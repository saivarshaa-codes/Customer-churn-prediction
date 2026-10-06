import { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const ASSISTANT_API_URL = import.meta.env.VITE_ASSISTANT_API_URL || 'http://localhost:8001/assistant/chat';

export default function AssistantPage() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I am your Retention AI Assistant. You can ask me about individual customer profiles, high-risk churn candidates, aggregate churn summaries, or what-if predictions.',
      toolsCalled: []
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastUserMessage, setLastUserMessage] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (messageToSend = inputMessage) => {
    const text = messageToSend.trim();
    if (!text || loading) return;

    setError(null);
    setLastUserMessage(text);
    setInputMessage('');

    // Append user message
    const updatedMessages = [...messages, { role: 'user', content: text }];
    setMessages(updatedMessages);
    setLoading(true);

    // Prepare bounded history (last 8 turns)
    const historyPayload = updatedMessages.slice(-8).map(m => ({
      role: m.role,
      content: m.content
    }));

    try {
      const response = await axios.post(ASSISTANT_API_URL, {
        message: text,
        history: historyPayload
      });

      const data = response.data;
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: data.reply,
          toolsCalled: data.tools_called || [],
          usage: data.usage
        }
      ]);
    } catch (err) {
      console.error('Error invoking Assistant API:', err);
      setError(err.response?.data?.detail || 'Failed to reach the Retention AI Assistant. Please check if the service is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = () => {
    if (lastUserMessage) {
      handleSend(lastUserMessage);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '24px', fontFamily: 'sans-serif' }}>
      <header style={{ marginBottom: '20px', borderBottom: '1px solid #e2e8f0', paddingBottom: '12px' }}>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 'bold', color: '#1a202c', margin: '0 0 8px 0' }}>
          Telecom Retention AI Assistant
        </h1>
        <p style={{ color: '#4a5568', margin: 0 }}>
          Grounded insights powered by Claude API, Decision Tree inference, and verified database tools.
        </p>
      </header>

      {/* Chat Window */}
      <div style={{
        height: '520px',
        overflowY: 'auto',
        border: '1px solid #cbd5e0',
        borderRadius: '8px',
        padding: '16px',
        backgroundColor: '#f7fafc',
        display: 'flex',
        flexDirection: 'column',
        gap: '14px'
      }}>
        {messages.map((m, idx) => (
          <div
            key={idx}
            style={{
              alignSelf: m.role === 'user' ? 'flex-end' : 'flex-start',
              maxWidth: '80%',
              display: 'flex',
              flexDirection: 'column',
              gap: '6px'
            }}
          >
            <div style={{
              padding: '12px 16px',
              borderRadius: '8px',
              backgroundColor: m.role === 'user' ? '#3182ce' : '#ffffff',
              color: m.role === 'user' ? '#ffffff' : '#2d3748',
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
              lineHeight: '1.5',
              whiteSpace: 'pre-wrap'
            }}>
              {m.content}
            </div>

            {/* Tool Calls Trail Badge */}
            {m.toolsCalled && m.toolsCalled.length > 0 && (
              <div style={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: '6px',
                fontSize: '0.75rem',
                color: '#718096'
              }}>
                <span style={{ fontWeight: '600' }}>Tools Executed:</span>
                {m.toolsCalled.map((t, tIdx) => (
                  <span
                    key={tIdx}
                    style={{
                      backgroundColor: '#edf2f7',
                      border: '1px solid #e2e8f0',
                      borderRadius: '4px',
                      padding: '2px 8px',
                      color: '#2b6cb0',
                      fontFamily: 'monospace'
                    }}
                  >
                    {t.tool} {t.args && Object.keys(t.args).length > 0 ? `(${JSON.stringify(t.args)})` : '()'}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div style={{ alignSelf: 'flex-start', color: '#718096', fontStyle: 'italic', padding: '8px 12px' }}>
            Assistant is consulting retention tools...
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Error & Retry Alert */}
      {error && (
        <div style={{
          marginTop: '12px',
          padding: '12px 16px',
          backgroundColor: '#fff5f5',
          border: '1px solid #feb2b2',
          borderRadius: '6px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          color: '#c53030'
        }}>
          <span>{error}</span>
          <button
            onClick={handleRetry}
            style={{
              backgroundColor: '#e53e3e',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              padding: '6px 12px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
          >
            Retry Request
          </button>
        </div>
      )}

      {/* Input Box */}
      <div style={{ marginTop: '16px', display: 'flex', gap: '8px' }}>
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question (e.g. 'Show profile for 7590-VHVEG' or 'What is our churn rate?')"
          disabled={loading}
          style={{
            flex: 1,
            padding: '12px',
            borderRadius: '6px',
            border: '1px solid #cbd5e0',
            fontSize: '1rem',
            outline: 'none'
          }}
        />
        <button
          onClick={() => handleSend()}
          disabled={loading || !inputMessage.trim()}
          style={{
            padding: '12px 24px',
            backgroundColor: loading || !inputMessage.trim() ? '#a0aec0' : '#3182ce',
            color: '#ffffff',
            border: 'none',
            borderRadius: '6px',
            fontWeight: '600',
            cursor: loading || !inputMessage.trim() ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>

      {/* Suggested Quick Prompts */}
      <div style={{ marginTop: '12px', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
        <button
          onClick={() => handleSend('What is the current overall churn rate and summary?')}
          style={{ padding: '4px 10px', fontSize: '0.85rem', borderRadius: '4px', border: '1px solid #cbd5e0', background: '#fff', cursor: 'pointer' }}
        >
          "What is our overall churn summary?"
        </button>
        <button
          onClick={() => handleSend('Look up customer profile for 7590-VHVEG')}
          style={{ padding: '4px 10px', fontSize: '0.85rem', borderRadius: '4px', border: '1px solid #cbd5e0', background: '#fff', cursor: 'pointer' }}
        >
          "Look up customer 7590-VHVEG"
        </button>
        <button
          onClick={() => handleSend('Predict churn risk for a customer with 2 months tenure, $85 monthly charges, month-to-month contract, and 1 service')}
          style={{ padding: '4px 10px', fontSize: '0.85rem', borderRadius: '4px', border: '1px solid #cbd5e0', background: '#fff', cursor: 'pointer' }}
        >
          "Predict what-if scenario"
        </button>
      </div>
    </div>
  );
}
