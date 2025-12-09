// src/App.tsx
import React, { useState } from "react";
import { uploadFile, askQuestion } from "./api";

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [error, setError] = useState("");
  const [uploadStatus, setUploadStatus] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [isAsking, setIsAsking] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setError("");
    setAnswer("");
    setUploadStatus("Uploading & embedding...");
    setIsUploading(true);

    try {
      const res = await uploadFile(file);
      setUploadStatus(res.message);
    } catch (err: unknown) {
      console.error("Upload error:", err);
      const message =
        err instanceof Error ? err.message : "Upload failed. Please try again.";
      setError(message);
    } finally {
      setIsUploading(false);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) return;
    setError("");
    setAnswer("");
    setIsAsking(true);

    try {
      const res = await askQuestion(question);
      setAnswer(res.answer);
    } catch (err: unknown) {
      console.error("Ask error:", err);
      const message =
        err instanceof Error ? err.message : "Something went wrong.";
      setError(message);
    } finally {
      setIsAsking(false);
    }
  };

  return (
    <div className="app">
      {/* HEADER */}
      <header className="app-header">
        <div className="app-logo">📦</div>
        <div>
          <p className="app-eyebrow">AI-powered supply chain insights</p>
          <h1 className="app-title">Supply Chain AI Assistant</h1>
          <p className="app-subtitle">
            Upload policy documents or supplier data and ask natural language
            questions about fairness, inventory and lead times.
          </p>
        </div>
      </header>

      <main className="app-main">
        {/* UPLOAD CARD */}
        <section className="card">
          <div className="card-header">
            <span className="card-pill">1</span>
            <div>
              <h2 className="card-title">Upload a document</h2>
              <p className="card-description">
                Upload Excel, PDF, or Word files containing inventory, supplier,
                or order data. The assistant will index them with vector
                embeddings.
              </p>
            </div>
          </div>

          <div className="card-body">
            <div className="upload-row">
              <input
                type="file"
                accept=".xlsx,.xls,.pdf,.doc,.docx"
                onChange={(e) => setFile(e.target.files?.[0] ?? null)}
                className="file-input"
              />

              <button
                type="button"
                onClick={handleUpload}
                disabled={!file || isUploading}
                className={`btn btn-primary ${
                  (!file || isUploading) && "btn-disabled"
                }`}
              >
                {isUploading ? "Uploading…" : "Upload & Embed"}
              </button>
            </div>

            {uploadStatus && (
              <p className="status-text status-success">{uploadStatus}</p>
            )}
          </div>
        </section>

        {/* QUESTION CARD */}
        <section className="card">
          <div className="card-header">
            <span className="card-pill">2</span>
            <div>
              <h2 className="card-title">Ask a question</h2>
              <p className="card-description">
                Ask about fairness, suppliers, lead times, order quantities or
                stock levels. The model will retrieve relevant chunks and answer
                based on your uploaded data.
              </p>
            </div>
          </div>

          <div className="card-body">
            <textarea
              rows={3}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Example: Which supplier has the longest lead time in this policy?"
              className="question-textarea"
            />

            <button
              type="button"
              onClick={handleAsk}
              disabled={isAsking || !question.trim()}
              className={`btn btn-secondary ${
                (isAsking || !question.trim()) && "btn-disabled"
              }`}
            >
              {isAsking ? "Thinking…" : "Ask"}
            </button>

            {/* Error */}
            {error && (
              <div className="alert alert-error">
                <strong>Error:</strong> {error}
              </div>
            )}

            {/* Answer */}
            {answer && (
              <div className="answer-panel">
                <div className="answer-label">Answer</div>
                <p className="answer-text">{answer}</p>
              </div>
            )}
          </div>
        </section>
      </main>

      <footer className="app-footer">
        <span>Built with FAISS, SentenceTransformers &amp; Groq LLaMA&nbsp;3.3</span>
      </footer>
    </div>
  );
};

export default App;
