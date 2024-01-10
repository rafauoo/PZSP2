// EditParticipantModal.js
import React, {useState, useEffect} from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

function EditParticipantModal({
                                show,
                                handleClose,
                                onEditParticipant,
                                editedParticipant,
                              }) {
  const [editedData, setEditedData] = useState({
    first_name: '',
    last_name: '',
    email: '',
  });

  useEffect(() => {
    // Aktualizacja stanu po zmianie edytowanego uczestnika
    setEditedData({
      first_name: editedParticipant.first_name,
      last_name: editedParticipant.last_name,
      email: editedParticipant.email,
    });
  }, [editedParticipant]);

  const handleInputChange = (e) => {
    const {name, value} = e.target;
    setEditedData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleEditParticipant = async () => {
    console.log(editedData);
    onEditParticipant(editedParticipant.id, editedData);
    handleClose();
  };

  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Edytuj uczestnika</Modal.Title>
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
              value={editedData.first_name}
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
              value={editedData.last_name}
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
              value={editedData.email}
              onChange={handleInputChange}
            />
          </div>
        </form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Zamknij
        </Button>
        <Button variant="primary" onClick={handleEditParticipant}>
          Zapisz zmiany
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export default EditParticipantModal;
