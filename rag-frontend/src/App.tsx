import { useState } from "react";
import { uploadFile, askQuestion } from "./api";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);

  const handleUpload = async () => {
    if (!file) return;
    setUploadStatus("Uploading & embedding...");
    try {
      const res = await uploadFile(file);
      setUploadStatus(`Uploaded: ${res.filename}`);
    } catch (err) {
      setUploadStatus("Upload failed");
      console.error(err);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setAnswer("");
    try {
      const res = await askQuestion(question);
      setAnswer(res.answer);
    } catch (err) {
      setAnswer("Something went wrong");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ maxWidth: 800, margin: "0 auto", padding: "2rem" }}>
      <h1>📦 Supply Chain AI Assistant</h1>

      {/* File upload */}
      <section style={{ marginTop: "1.5rem" }}>
        <h2>1️⃣ Upload a document</h2>
        <input
          type="file"
          accept=".xlsx,.xls,.pdf,.doc,.docx"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        />
        <button onClick={handleUpload} disabled={!file}>
          Upload & Embed
        </button>
        {uploadStatus && <p>{uploadStatus}</p>}
      </section>

      {/* Chat */}
      <section style={{ marginTop: "2rem" }}>
        <h2>2️⃣ Ask a question</h2>
        <textarea
          rows={3}
          style={{ width: "100%", marginBottom: "0.5rem" }}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about inventory, suppliers, orders, forecasts..."
        />
        <button onClick={handleAsk} disabled={loading}>
          {loading ? "Thinking..." : "Ask"}
        </button>

        {answer && (
          <div style={{ marginTop: "1rem", padding: "1rem", border: "1px solid #ddd" }}>
            <strong>Answer:</strong>
            <p>{answer}</p>
          </div>
        )}
      </section>
    </main>
  );
}

export default App;
