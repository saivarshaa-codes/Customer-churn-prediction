import { useState } from 'react';
import CustomerSearch from './pages/CustomerSearch.jsx';
import ChurnPrediction from './pages/ChurnPrediction.jsx';
import ChurnSummary from './pages/ChurnSummary.jsx';
import HighRiskCustomers from './pages/HighRiskCustomers.jsx';
import AssistantPage from './pages/AssistantPage.jsx';

import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('summary');

  const tabs = [
    { id: 'summary', label: '📊 Churn Analytics' },
    { id: 'search', label: '🔍 Customer Search' },
    { id: 'high-risk', label: '⚠️ High-Risk Queue' },
    { id: 'prediction', label: '🔮 ML Churn Predictor' },
    { id: 'assistant', label: '🤖 Retention AI Assistant' },
  ];

  return (
    <div className="app-container" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <header style={{
        background: '#1a202c',
        color: '#ffffff',
        padding: '16px 32px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
        alignItems: 'center',
        gap: '16px'
      }}>
        <div>
          <h1 style={{ margin: 0, fontSize: '1.4rem', fontWeight: '700', color: '#ffffff' }}>
            Customer Retention Intelligence System
          </h1>
          <p style={{ margin: '4px 0 0 0', fontSize: '0.85rem', color: '#a0aec0' }}>
            Enterprise Telecom Analytics · Machine Learning · AI Assistant
          </p>
        </div>

        <nav style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                padding: '8px 16px',
                borderRadius: '6px',
                border: 'none',
                fontWeight: activeTab === tab.id ? '700' : '500',
                fontSize: '0.9rem',
                cursor: 'pointer',
                backgroundColor: activeTab === tab.id ? '#3182ce' : '#2d3748',
                color: activeTab === tab.id ? '#ffffff' : '#cbd5e0',
                transition: 'all 0.2s ease',
              }}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </header>

      <main style={{ flex: 1, padding: '24px 16px', maxWidth: '1200px', margin: '0 auto', width: '100%', boxSizing: 'border-box' }}>
        {activeTab === 'summary' && (
          <section>
            <ChurnSummary />
          </section>
        )}

        {activeTab === 'search' && (
          <section>
            <h1 style={{ textAlign: 'center' }}>Customer Profile Search</h1>
            <CustomerSearch />
          </section>
        )}

        {activeTab === 'high-risk' && (
          <section>
            <h1 style={{ textAlign: 'center' }}>High-Risk Customer Queue</h1>
            <HighRiskCustomers />
          </section>
        )}

        {activeTab === 'prediction' && (
          <section>
            <h1 style={{ textAlign: 'center' }}>Machine Learning Churn Predictor</h1>
            <ChurnPrediction />
          </section>
        )}

        {activeTab === 'assistant' && (
          <section>
            <AssistantPage />
          </section>
        )}
      </main>

      <footer style={{
        textAlign: 'center',
        padding: '16px',
        fontSize: '0.8rem',
        color: '#718096',
        borderTop: '1px solid #e2e8f0',
        marginTop: 'auto'
      }}>
        Customer Retention Intelligence Platform · Enterprise Telecom Analytics & AI Assistant
      </footer>
    </div>
  );
}

export default App;
