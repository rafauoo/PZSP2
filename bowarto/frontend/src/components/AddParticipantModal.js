// AddParticipantModal.js
import React, {useState} from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

function AddParticipantModal({show, handleClose, onAddParticipant, applicationId}) {
  const [newParticipant, setNewParticipant] = useState({
    first_name: '',
    last_name: '',
    email: ''
  });

  const handleInputChange = (e) => {
    const {name, value} = e.target;
    setNewParticipant((prevParticipant) => ({
      ...prevParticipant,
      [name]: value
    }));
  };

  const handleAddParticipant = () => {
    onAddParticipant(applicationId, newParticipant);
    handleClose();
  };

  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Dodaj uczestnika</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <form>
          <div className="mb-3">
            <label htmlFor="first_name" className="form-label">
              Imię:
            </label>
            <input
              type="text"
              className="form-control"
              id="first_name"
              name="first_name"
              value={newParticipant.first_name}
              onChange={handleInputChange}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="last_name" className="form-label">
              Nazwisko:
            </label>
            <input
              type="text"
              className="form-control"
              id="last_name"
              name="last_name"
              value={newParticipant.last_name}
              onChange={handleInputChange}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="email" className="form-label">
              Email:
            </label>
            <input
              type="email"
              className="form-control"
              id="email"
              name="email"
              value={newParticipant.email}
              onChange={handleInputChange}
            />
          </div>
        </form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Zamknij
        </Button>
        <Button variant="primary" onClick={handleAddParticipant}>
          Dodaj uczestnika
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export default AddParticipantModal;
