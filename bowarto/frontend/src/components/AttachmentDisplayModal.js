import React from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

function AttachmentDisplayModal({show, handleClose, attachment}) {
  const handleShowAttachment = () => {
    const attachmentUrl = attachment.url; // Załóżmy, że obiekt attachment zawiera pole 'url'
    window.open(attachmentUrl, '_blank');
  };

  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Szczegóły załącznika</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {/* Dostosuj zawartość modalu w zależności od danych załącznika */}
        <p>Nazwa załącznika: {attachment.name}</p>
        <p>Typ załącznika: {attachment.type}</p>
        {/* Dodaj więcej szczegółów w zależności od struktury danych załącznika */}
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Zamknij
        </Button>
        <Button variant="primary" onClick={handleShowAttachment}>
          Zobacz załącznik
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export default AttachmentDisplayModal;
