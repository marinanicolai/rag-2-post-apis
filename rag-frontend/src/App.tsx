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
    <main
      style={{
        maxWidth: 900,
        margin: "0 auto",
        padding: "2rem",
        fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
        color: "#f5f5f5",
        backgroundColor: "#111827",
        minHeight: "100vh",
      }}
    >
      <header style={{ marginBottom: "2rem", display: "flex", alignItems: "center", gap: "0.75rem" }}>
        <span
          style={{
            fontSize: "2rem",
          }}
        >
          📦
        </span>
        <h1 style={{ fontSize: "2.2rem", fontWeight: 700, margin: 0 }}>
          Supply Chain AI Assistant
        </h1>
      </header>

      {/* Upload section */}
      <section
        style={{
          padding: "1.5rem",
          borderRadius: "0.75rem",
          backgroundColor: "#1f2937",
          marginBottom: "1.5rem",
        }}
      >
        <h2 style={{ marginTop: 0, marginBottom: "0.75rem", fontSize: "1.25rem" }}>
          1️⃣ Upload a document
        </h2>
        <p style={{ marginTop: 0, marginBottom: "0.75rem", fontSize: "0.9rem", color: "#9ca3af" }}>
          Upload Excel, PDF, or Word files containing inventory, supplier, or
          order data.
        </p>

        <div style={{ display: "flex", gap: "0.75rem", alignItems: "center", flexWrap: "wrap" }}>
          <input
            type="file"
            accept=".xlsx,.xls,.pdf,.doc,.docx"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            style={{ color: "#e5e7eb" }}
          />
          <button
            type="button"
            onClick={handleUpload}
            disabled={!file || isUploading}
            style={{
              padding: "0.5rem 1rem",
              borderRadius: "999px",
              border: "none",
              cursor: !file || isUploading ? "not-allowed" : "pointer",
              backgroundColor: !file || isUploading ? "#4b5563" : "#10b981",
              color: "white",
              fontWeight: 600,
            }}
          >
            {isUploading ? "Uploading..." : "Upload & Embed"}
          </button>
        </div>

        {uploadStatus && (
          <p style={{ marginTop: "0.75rem", fontSize: "0.9rem", color: "#a7f3d0" }}>
            {uploadStatus}
          </p>
        )}
      </section>

      {/* Ask a question section */}
      <section
        style={{
          padding: "1.5rem",
          borderRadius: "0.75rem",
          backgroundColor: "#1f2937",
        }}
      >
        <h2 style={{ marginTop: 0, marginBottom: "0.75rem", fontSize: "1.25rem" }}>
          2️⃣ Ask a question
        </h2>
        <p style={{ marginTop: 0, marginBottom: "0.75rem", fontSize: "0.9rem", color: "#9ca3af" }}>
          Ask about fairness, suppliers, lead times, order quantities, stock levels,
          or any content inside your uploaded documents.
        </p>

        <textarea
          rows={3}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Example: What is fairness in this policy? or Which supplier has the longest lead time?"
          style={{
            width: "100%",
            padding: "0.75rem",
            borderRadius: "0.5rem",
            border: "1px solid #4b5563",
            backgroundColor: "#111827",
            color: "#e5e7eb",
            resize: "vertical",
            marginBottom: "0.75rem",
          }}
        />

        <button
          type="button"
          onClick={handleAsk}
          disabled={isAsking || !question.trim()}
          style={{
            padding: "0.5rem 1.25rem",
            borderRadius: "999px",
            border: "none",
            cursor: isAsking || !question.trim() ? "not-allowed" : "pointer",
            backgroundColor: isAsking || !question.trim() ? "#4b5563" : "#3b82f6",
            color: "white",
            fontWeight: 600,
          }}
        >
          {isAsking ? "Thinking..." : "Ask"}
        </button>

        {/* Error */}
        {error && (
          <div
            style={{
              marginTop: "1rem",
              padding: "0.75rem 1rem",
              borderRadius: "0.5rem",
              backgroundColor: "#7f1d1d",
              color: "#fee2e2",
              fontSize: "0.9rem",
            }}
          >
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Answer */}
        {answer && (
          <div
            style={{
              marginTop: "1rem",
              padding: "1rem",
              borderRadius: "0.5rem",
              backgroundColor: "#030712",
              border: "1px solid #374151",
            }}
          >
            <strong style={{ display: "block", marginBottom: "0.5rem" }}>Answer:</strong>
            <p style={{ margin: 0, whiteSpace: "pre-wrap" }}>{answer}</p>
          </div>
        )}
      </section>
    </main>
  );
};

export default App;
