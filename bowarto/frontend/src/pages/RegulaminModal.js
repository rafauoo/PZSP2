import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { buttonStyle } from '../styles/styles';

function RegulaminModal(props) {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  return (
    <>
      <button style={buttonStyle} onClick={handleShow}>
        Regulamin
      </button>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>{props.title}</Modal.Title>
        </Modal.Header>
        <Modal.Body>{props.description}</Modal.Body>
        <Modal.Footer>
          <button style={buttonStyle} onClick={handleClose}>
            Zamknij
          </button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default RegulaminModal;
