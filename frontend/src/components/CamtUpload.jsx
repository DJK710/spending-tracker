import { useRef, useState } from "react";

function CamtUpload({ onUpload }) {
  const fileInputRef = useRef(null);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const xmlFiles = Array.from(event.target.files || []).filter((file) =>
      file.name.toLowerCase().endsWith(".xml")
    );

    setSelectedFiles(xmlFiles);
    setMessage("");
    setError("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (selectedFiles.length === 0) {
      setError("Choose a folder that contains CAMT XML files first.");
      return;
    }

    setIsUploading(true);
    setMessage("");
    setError("");

    try {
      const importedCount = await onUpload(selectedFiles);
      const fileLabel = selectedFiles.length === 1 ? "file" : "files";
      setMessage(`Imported ${importedCount} transactions from ${selectedFiles.length} ${fileLabel}.`);
      setSelectedFiles([]);

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
        <h2>Import CAMT Folder</h2>
        <p>Upload a folder of CAMT XML exports from your bank to add its transactions.</p>
      </div>

      <div className="camt-upload-controls">
        <input
          ref={fileInputRef}
          id="camt-file"
          type="file"
          accept=".xml,text/xml,application/xml"
          multiple
          directory=""
          webkitdirectory=""
          onChange={handleFileChange}
        />

        <label className="file-picker-button" htmlFor="camt-file">
          {selectedFiles.length > 0
            ? `${selectedFiles.length} CAMT files selected`
            : "Choose CAMT folder"}
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
