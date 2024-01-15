import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import Modal from 'react-bootstrap/Modal';
import { buttonStyle } from '../styles/styles';

function ErrorModal(props) {
  const [show, setShow] = useState(true);

  const handleClose = () => setShow(false);
  const navigate = useNavigate();
  // const handleShow = () => setShow(true);
  // TODO: add closable, if closable true then add closing button to modal

  const handleButtonClick = () => {
    // Use the history object to navigate to another page
    // handleClose()
    navigate('/' + props.link);
  };

  const token = sessionStorage.getItem('access');
  return (
    <>
      {!token ? (
        <Modal show={show} >
          <Modal.Header >
            <Modal.Title>{props.title}</Modal.Title>
          </Modal.Header>
          <Modal.Body>{props.description}</Modal.Body>
          <Modal.Footer>
            <button style={buttonStyle} onClick={handleButtonClick}>
              {props.link_title}
            </button>
          </Modal.Footer>
        </Modal>
      ) : null}
    </>
  )
}

export default ErrorModal;
