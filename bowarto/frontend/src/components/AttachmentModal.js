// AttachmentModal.js
import {useState} from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

function AttachmentModal({show, handleClose, handleAttachmentUpload}) {
  const [newAttachment, setNewAttachment] = useState(null);

  const handleAttachmentChange = (e) => {
    // Handle file attachment change
    const file = e.target.files[0];
    setNewAttachment(file);
  };

  const handleUploadClick = () => {
    // Implement file upload logic here
    handleAttachmentUpload(newAttachment);
    // Reset new attachment and close the modal after upload
    setNewAttachment(null);
    handleClose();
  };

  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Attachment Form</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <form>
          <div>
            <label>Select New Attachment:</label>
            <input type="file" onChange={handleAttachmentChange}/>
          </div>
        </form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
        <Button variant="primary" onClick={handleUploadClick}>
          Upload
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export default AttachmentModal;
