import React from 'react';
import Modal from 'react-bootstrap/Modal';
import {buttonStyle} from "../styles/styles";

const MessageModal = ({title, onClose, show, message}) => {
  return (
    <Modal show={show} onHide={onClose}>
      <Modal.Header closeButton>
        <Modal.Title>{title || 'Wiadomość'}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {message.split('\n').map((line, index) => (
          <div key={index}>{line}</div>
        ))}
      </Modal.Body>
      <Modal.Footer>
        <button style={buttonStyle} onClick={onClose}>
          Zamknij
        </button>
      </Modal.Footer>
    </Modal>
  );
};

export default MessageModal;
