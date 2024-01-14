import React, {useState} from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import { buttonSaveChanges } from '../styles/styles';

function AttachmentModal({show, handleClose, onAddAttachment, participantId}) {
  const [newAttachment, setNewAttachment] = useState(null);

  const handleAttachmentChange = (e) => {
    // Handle file attachment change
    const file = e.target.files[0];
    setNewAttachment(file);
  };

  const handleUploadClick = async () => {
    console.log(participantId, newAttachment);
    onAddAttachment(participantId, newAttachment);
    // Reset new attachment and close the modal after upload
    setNewAttachment(null);
    handleClose();
  };

  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Załącz pracę</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <form>
          <div>
            <label>Wybierz załącznik:</label>
            <br></br>
            <input type="file" onChange={handleAttachmentChange}/>
          </div>
        </form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Zamknij
        </Button>
        <Button style={buttonSaveChanges} onClick={handleUploadClick}>
          Prześlij plik
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export default AttachmentModal;
