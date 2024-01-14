import React, {useState} from 'react';
import axios from 'axios';
import refreshAccessToken from '../requests/refresh';
import { iconButtonStyle, buttonStyleDelete, buttonStyleEdit, buttonContainerStyleAttachment } from '../styles/styles';


function AttachmentDisplay({attachment, participant, onDownload, onRemove}) {
  const handleDownloadFile = () => {
    if (onDownload) {
      // Wywołaj funkcję z komponentu nadrzędnego do pobierania załącznika
      onDownload(attachment);
    }
  };

  const handleRemoveAttachment = () => {
    if (onRemove) {
      // Wywołaj funkcję z komponentu nadrzędnego do usuwania załącznika
      onRemove(participant);
    }
  };

  return (
    <div style={buttonContainerStyleAttachment}>
      <button style={buttonStyleEdit} onClick={handleDownloadFile}>
        <img src={require('../images/download.png')} alt="Pobierz" style={iconButtonStyle}/>
        Pobierz
      </button>
      <button style={buttonStyleDelete} onClick={handleRemoveAttachment}>
        <img src={require('../images/delete.png')} alt="Usuń" style={iconButtonStyle}/>
        Usuń
      </button>
    </div>
  );
}

export default AttachmentDisplay;

