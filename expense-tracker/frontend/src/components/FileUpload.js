import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { uploadFile } from '../services/api';
import './FileUpload.css';

const FileUpload = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    setUploading(true);
    setMessage('');

    try {
      const result = await uploadFile(file);
      setMessage(`✓ Success! Processed ${result.count} expenses for ${result.person}`);

      // Call parent callback to refresh data
      if (onUploadSuccess) {
        setTimeout(() => {
          onUploadSuccess();
        }, 1000);
      }
    } catch (error) {
      const errorMsg = error.response?.data?.error || error.message;
      setMessage(`✗ Error: ${errorMsg}`);
    } finally {
      setUploading(false);
    }
  }, [onUploadSuccess]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls']
    },
    multiple: false,
    disabled: uploading
  });

  return (
    <div className="file-upload-container">
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'active' : ''} ${uploading ? 'uploading' : ''}`}
      >
        <input {...getInputProps()} />
        {uploading ? (
          <div className="upload-message">
            <div className="spinner"></div>
            <p>Processing file...</p>
          </div>
        ) : isDragActive ? (
          <p>Drop the file here...</p>
        ) : (
          <div className="upload-prompt">
            <p className="upload-title">📁 Drop your expense file here</p>
            <p className="upload-subtitle">or click to browse</p>
            <p className="upload-formats">Supports CSV, PDF, XLSX</p>
          </div>
        )}
      </div>
      {message && (
        <div className={`message ${message.includes('✓') ? 'success' : 'error'}`}>
          {message}
        </div>
      )}
    </div>
  );
};

export default FileUpload;
