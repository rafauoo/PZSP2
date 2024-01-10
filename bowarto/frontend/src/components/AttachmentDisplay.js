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

function AttachmentDisplay({attachment, onRemoveAttachment}) {
  const handleDownloadFile = async () => {
    try {
      // Pobierz plik i zapisz na dysku
      await downloadFile(attachment);
    } catch (error) {
      console.error('Error downloading file:', error);
    }
  };

  const handleRemoveAttachment = async () => {
    try {
      // Usuń załącznik
      await removeAttachment(attachment);
      // Wywołaj funkcję przekazaną jako prop do aktualizacji widoku
      if (onRemoveAttachment) {
        onRemoveAttachment(attachment);
      }
    } catch (error) {
      console.error('Error removing attachment:', error);
    }
  };

  const downloadFile = async (attachmentId) => {
    try {
      await refreshAccessToken();
      const token = sessionStorage.getItem('access');

      // Pobierz plik z serwera
      const response = await axios({
        url: `http://127.0.0.1:8000/api/files/${attachmentId}/`,
        method: 'GET',
        responseType: 'arraybuffer',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const contentDisposition = response.headers['content-disposition'];
      const filename = parseFilenameFromContentDisposition(contentDisposition);

      console.log(filename);
      saveFile(response.data, filename);
    } catch (error) {
      console.error('Error downloading file:', error);
      throw error;
    }
  };

  const removeAttachment = async (attachmentId) => {
    // Implementuj logikę usuwania załącznika
    // Możesz użyć odpowiedniego zapytania do API lub innej metody usuwania
    console.log('Removing attachment:', attachmentId);
  };

  const saveFile = (data, filename) => {
    const blob = new Blob([data], {type: 'application/octet-stream'});
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const parseFilenameFromContentDisposition = (contentDisposition) => {
    const match = /filename\*=utf-8''(.+)/.exec(contentDisposition);
    return match ? decodeURIComponent(match[1]) : 'downloaded_file';
  };

  return (
    <div style={buttonContainerStyle}>
      <button style={buttonStyle} onClick={handleDownloadFile}>
        Pobierz
      </button>
      <button style={buttonStyle} onClick={handleRemoveAttachment}>
        Usuń
      </button>
    </div>
  );
}

export default AttachmentDisplay;
