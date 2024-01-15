import React, {useState} from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import {buttonSaveChanges} from '../styles/styles';

function AttachmentModal({show, handleClose, onAddAttachment, participantId}) {
  const [newAttachment, setNewAttachment] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  const handleAttachmentChange = (e) => {
    // Handle file attachment change
    const file = e.target.files[0];
    setNewAttachment(file);
    setErrorMessage(''); // Clear error message when a new file is selected
  };

  const isFileValid = () => {
    // Check if a file is selected and its size is less than or equal to 10MB
    return newAttachment && newAttachment.size <= 10 * 1024 * 1024;
  };

  const handleCloseModal = async () => {
    setErrorMessage('')
    setNewAttachment(null)
    handleClose()
  }
  const handleUploadClick = async () => {
    if (isFileValid()) {
      onAddAttachment(participantId, newAttachment);
      // Reset new attachment and close the modal after upload
      setNewAttachment(null);
      handleClose();
    } else {
      // Show an error message if the file is not valid
      if (!newAttachment) {
        setErrorMessage('Wybierz plik przed przesłaniem.');
      } else if (newAttachment.size > 10 * 1024 * 1024) {
        setErrorMessage('Przekroczono limit przesyłania załącznika. Wybierz mniejszy plik.');
      }

      // Uncomment the line below to log additional error information
      // console.error('Invalid file. Please select a file less than or equal to 10MB.');
    }
  };

  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Załącz pracę</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <form>
          <div>
            <label>Wybierz załącznik (max 10MB):</label>
            <br></br>
            <input type="file" onChange={handleAttachmentChange}/>
            {errorMessage && <p style={{color: 'red'}}>{errorMessage}</p>}
          </div>
        </form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleCloseModal}>
          Zamknij
        </Button>
        <Button
          style={buttonSaveChanges}
          onClick={handleUploadClick}
          // disabled={!isFileValid()}
        >
          Prześlij plik
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export default AttachmentModal;
