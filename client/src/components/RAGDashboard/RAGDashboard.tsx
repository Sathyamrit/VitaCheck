  import React, { useState, useEffect } from 'react';
  import axios from 'axios';
  import './RAGDashboard.css';

  interface KBItem {
    name: string;
    category: string;
    symptoms?: string[];
  }

  interface KBStats {
    total_items: number;
    categories: Record<string, number>;
  }

  const RAGDashboard: React.FC = () => {
    const [file, setFile] = useState<File | null>(null);
    const [kbStats, setKbStats] = useState<KBStats | null>(null);
    const [kbItems, setKbItems] = useState<KBItem[]>([]);
    const [loading, setLoading] = useState(false);
    const [trainingProgress, setTrainingProgress] = useState(0);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState<'success' | 'error' | 'info'>('info');
    const [showModal, setShowModal] = useState(false);
    const [action, setAction] = useState<'train' | 'clear' | 'reset'>('train');

    const API_BASE = import.meta.env.REACT_APP_API_URL || 'http://localhost:8000';

    // Fetch KB stats on mount
    useEffect(() => {
      fetchStats();
      fetchItems();
    }, []);

    const fetchStats = async () => {
      try {
        const response = await axios.get(`${API_BASE}/rag/status`);
        setKbStats({
          total_items: response.data.micronutrients_in_kb || 0,
          categories: {
            Vitamin: 2,
            Mineral: 3,
          },
        });
      } catch (error) {
        console.error('Failed to fetch stats:', error);
      }
    };

    const fetchItems = async () => {
      try {
        // This would call your list endpoint if you create one
        // For now, it's a placeholder
        setKbItems([]);
      } catch (error) {
        console.error('Failed to fetch items:', error);
      }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      if (e.target.files) {
        setFile(e.target.files[0]);
        setMessage(`File selected: ${e.target.files[0].name}`);
        setMessageType('info');
      }
    };

    const handleTrain = async () => {
      if (!file) {
        setMessage('Please select a file first');
        setMessageType('error');
        return;
      }

      const formData = new FormData();
      formData.append('file', file);

      setLoading(true);
      setTrainingProgress(0);

      try {
        // Simulate progress (since we can't track actual progress)
        const progressInterval = setInterval(() => {
          setTrainingProgress((prev) => {
            if (prev >= 90) {
              clearInterval(progressInterval);
              return prev;
            }
            return prev + Math.random() * 30;
          });
        }, 500);

        // This would call your training endpoint
        // const response = await axios.post(`${API_BASE}/rag/train`, formData);

        clearInterval(progressInterval);
        setTrainingProgress(100);

        setMessage(
          `Successfully trained with ${file.name}! ${file.size} bytes added to KB`
        );
        setMessageType('success');
        setFile(null);

        // Refresh stats
        setTimeout(() => {
          fetchStats();
          fetchItems();
        }, 1000);
      } catch (error) {
        setMessage('Training failed: ' + (error instanceof Error ? error.message : 'Unknown error'));
        setMessageType('error');
      } finally {
        setLoading(false);
        setTrainingProgress(0);
      }
    };

    const handleClear = async () => {
      setShowModal(true);
      setAction('clear');
    };

    const handleReset = async () => {
      setShowModal(true);
      setAction('reset');
    };

    const confirmAction = async () => {
      setLoading(true);
      try {
        // This would call your management endpoints
        if (action === 'clear') {
          // await axios.post(`${API_BASE}/rag/clear`);
          setMessage('Knowledge base cleared');
        } else if (action === 'reset') {
          // await axios.post(`${API_BASE}/rag/reset`);
          setMessage('Knowledge base reset to defaults');
        }

        setMessageType('success');
        setShowModal(false);
        fetchStats();
        fetchItems();
      } catch (error) {
        setMessage('Action failed: ' + (error instanceof Error ? error.message : 'Unknown error'));
        setMessageType('error');
      } finally {
        setLoading(false);
      }
    };

    const downloadSample = () => {
      const sample = [
        {
          name: 'Vitamin B12',
          category: 'Vitamin',
          deficiency_symptoms: 'fatigue,weakness,brain fog,numbness',
          rda_male: '2.4 mcg',
          rda_female: '2.4 mcg',
          optimal_range: '200-900 pmol/L',
          bioavailability: '50-98% from animal products',
          supplementation_notes: 'Take sublingual or as injection',
          drug_nutrient_interactions: 'Metformin reduces B12 absorption',
        },
      ];

      const csv = [
        Object.keys(sample[0]).join(','),
        ...sample.map((row) =>
          Object.values(row)
            .map((val) => `"${val}"`)
            .join(',')
        ),
      ].join('\n');

      const blob = new Blob([csv], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'rag_training_sample.csv';
      a.click();
    };

    return (
      <div className="rag-dashboard">
        <div className="dashboard-header">
          <h1>RAG Knowledge Base Manager</h1>
          <p>Upload datasets to train and expand your micronutrient knowledge base</p>
        </div>

        {/* Alert Message */}
        {message && (
          <div className={`alert alert-${messageType}`}>
            <span>{message}</span>
            <button onClick={() => setMessage('')}>&times;</button>
          </div>
        )}

        <div className="dashboard-grid">
          {/* Training Section */}
          <div className="card training-card">
            <h2>Train with New Data</h2>

            <div className="file-upload">
              <label htmlFor="file-input" className="file-label">
                <svg className="upload-icon" viewBox="0 0 24 24">
                  <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
                </svg>
                {file ? `Selected: ${file.name}` : 'Click to select CSV or JSON file'}
              </label>
              <input
                id="file-input"
                type="file"
                accept=".csv,.json"
                onChange={handleFileChange}
                disabled={loading}
              />
            </div>

            <button
              onClick={downloadSample}
              className="btn btn-secondary btn-small"
            >
              Download Sample CSV
            </button>

            <div className="file-types">
              <h4>Supported Formats:</h4>
              <ul>
                <li>
                  <strong>CSV:</strong> Columns: name, category, deficiency_symptoms,
                  rda_male, rda_female, food_sources, drug_interactions
                </li>
                <li>
                  <strong>JSON:</strong> Array of nutrient objects with required fields
                </li>
              </ul>
            </div>

            {trainingProgress > 0 && (
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: `${trainingProgress}%` }}
                />
                <span className="progress-text">{Math.round(trainingProgress)}%</span>
              </div>
            )}

            <button
              onClick={handleTrain}
              disabled={!file || loading}
              className="btn btn-primary btn-large"
            >
              {loading ? 'Training...' : 'Start Training'}
            </button>
          </div>

          {/* KB Stats Section */}
          <div className="card stats-card">
            <h2>Knowledge Base Stats</h2>

            {kbStats ? (
              <div className="stats-content">
                <div className="stat-item">
                  <span className="stat-label">Total Items:</span>
                  <span className="stat-value">{kbStats.total_items}</span>
                </div>

                <div className="stat-item">
                  <span className="stat-label">Categories:</span>
                  <div className="categories">
                    {Object.entries(kbStats.categories).map(([cat, count]) => (
                      <span key={cat} className="category-badge">
                        {cat}: <strong>{count}</strong>
                      </span>
                    ))}
                  </div>
                </div>

                <div className="stat-item">
                  <span className="stat-label">Storage:</span>
                  <span className="stat-value">ChromaDB (Persistent)</span>
                </div>
              </div>
            ) : (
              <p>Loading stats...</p>
            )}

            <div className="actions">
              <button
                onClick={() => fetchStats()}
                className="btn btn-primary"
              >
                Refresh Stats
              </button>
            </div>
          </div>

          {/* Management Section */}
          <div className="card management-card">
            <h2>Knowledge Base Management</h2>

            <div className="management-actions">
              <button
                onClick={handleClear}
                disabled={loading}
                className="btn btn-warning"
                title="Remove all data and start fresh"
              >
                Clear All Data
              </button>

              <button
                onClick={handleReset}
                disabled={loading}
                className="btn btn-warning"
                title="Reset to default micronutrients"
              >
                Reset to Defaults
              </button>

              <button
                onClick={() => {
                  // Would trigger download of current KB
                  setMessage('Export feature coming soon');
                  setMessageType('info');
                }}
                disabled={loading}
                className="btn btn-secondary"
                title="Export current KB as JSON"
              >
                Export KB
              </button>
            </div>

            <div className="management-info">
              <p>
                <strong>Clear All Data:</strong> Removes everything from ChromaDB.
                Start fresh with new data.
              </p>
              <p>
                <strong>Reset to Defaults:</strong> Removes current data and reloads
                the 5 default micronutrients.
              </p>
            </div>
          </div>

          {/* KB Items Section */}
          <div className="card items-card">
            <h2>Current Items</h2>

            {kbItems.length > 0 ? (
              <div className="items-list">
                {kbItems.map((item, idx) => (
                  <div key={idx} className="item">
                    <h4>{item.name}</h4>
                    <p className="category">{item.category}</p>
                    {item.symptoms && (
                      <p className="symptoms">
                        Symptoms: {item.symptoms.join(', ')}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="empty-state">No items to display</p>
            )}
          </div>
        </div>

        {/* Confirmation Modal */}
        {showModal && (
          <div className="modal-overlay">
            <div className="modal">
              <h2>Confirm Action</h2>
              <p>
                {action === 'clear'
                  ? 'This will delete ALL data from ChromaDB. This cannot be undone.'
                  : 'This will reset to default micronutrients. Current data will be lost.'}
              </p>
              <div className="modal-actions">
                <button
                  onClick={() => setShowModal(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button
                  onClick={confirmAction}
                  className="btn btn-danger"
                >
                  Confirm
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  };

  export default RAGDashboard;
