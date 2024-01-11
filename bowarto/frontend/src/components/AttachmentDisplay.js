import React, {useState} from 'react';
import axios from 'axios';
import refreshAccessToken from '../requests/refresh';


const buttonStyle = {
  backgroundColor: 'rgb(131, 203, 83)',
  borderRadius: '5px',
  color: 'black',
  padding: '5px 10px',
  border: 'none',
  cursor: 'pointer',
};

const buttonContainerStyle = {
  display: 'flex',
  justifyContent: 'center',
  gap: '10px',
};

function AttachmentDisplay({attachment, onDownload, onRemove}) {
  const handleDownloadFile = () => {
    if (onDownload) {
      // Wywołaj funkcję z komponentu nadrzędnego do pobierania załącznika
      onDownload(attachment);
    }
  };

  const handleRemoveAttachment = () => {
    if (onRemove) {
      // Wywołaj funkcję z komponentu nadrzędnego do usuwania załącznika
      onRemove(attachment);
    }
  };

  return (
    <div style={buttonContainerStyle}>
      <button style={buttonStyle} onClick={handleDownloadFile}>Pobierz</button>
      <button style={buttonStyle} onClick={handleRemoveAttachment}>Usuń</button>
    </div>
  );
}

export default AttachmentDisplay;

