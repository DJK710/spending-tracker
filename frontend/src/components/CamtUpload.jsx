import { useRef, useState } from "react";

function CamtUpload({ onUpload }) {
  const fileInputRef = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0] || null);
    setMessage("");
    setError("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!selectedFile) {
      setError("Choose a CAMT XML file first.");
      return;
    }

    setIsUploading(true);
    setMessage("");
    setError("");

    try {
      const importedCount = await onUpload(selectedFile);
      setMessage(`Imported ${importedCount} transactions from ${selectedFile.name}.`);
      setSelectedFile(null);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    } catch (uploadError) {
      const detail = uploadError.response?.data?.detail;
      setError(detail || "Could not import this CAMT file.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <form className="camt-upload" onSubmit={handleSubmit}>
      <div>
        <h2>Import CAMT File</h2>
        <p>Upload a CAMT XML export from your bank to add its transactions.</p>
      </div>

      <div className="camt-upload-controls">
        <input
          ref={fileInputRef}
          id="camt-file"
          type="file"
          accept=".xml,text/xml,application/xml"
          onChange={handleFileChange}
        />

        <label className="file-picker-button" htmlFor="camt-file">
          {selectedFile ? selectedFile.name : "Choose CAMT file"}
        </label>

        <button type="submit" disabled={isUploading}>
          {isUploading ? "Importing..." : "Upload CAMT"}
        </button>
      </div>

      {message && <p className="upload-message">{message}</p>}
      {error && <p className="error-message">{error}</p>}
    </form>
  );
}

export default CamtUpload;
