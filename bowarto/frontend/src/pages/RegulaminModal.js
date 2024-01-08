import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

function RegulaminModal(props) {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const buttonStyle = {
    backgroundColor: 'rgb(131, 203, 83)',
    borderRadius: '5px',
    color: 'black',
    padding: '5px 10px',
    border: 'none',
    cursor: 'pointer',
    margin: '5px'
  };


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
