// AddSchoolModal.js
import React, {useState} from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import { buttonSaveChanges } from '../styles/styles';

function AddSchoolModal({show, handleClose, onAddSchool}) {
  const [newSchool, setNewSchool] = useState({
    name: '',
    phone_number: '',
    fax_number: '',
    email: '',
    website: '',
    city: '',
    street: '',
    building_number: '',
    apartment_number: '',
    postcode: ''
  });

  const handleInputChange = (e) => {
    const {name, value} = e.target;
    setNewSchool((prevSchool) => ({
      ...prevSchool,
      [name]: value
    }));
  };

  const handleAddSchool = async () => {
    console.log(newSchool);
    onAddSchool(newSchool);
    handleClose();
  };

  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Dodaj szkołę</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <form>
          <div className="mb-3">
            <label htmlFor="name" className="form-label">
              Nazwa szkoły<span style={{ color: 'red' }}>*</span>:
            </label>
            <input
              type="text"
              className="form-control"
              id="name"
              name="name"
              value={newSchool.name}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="phone_number" className="form-label">
              Numer telefonu<span style={{ color: 'red' }}>*</span>:
            </label>
            <input
              type="text"
              className="form-control"
              id="phone_number"
              name="phone_number"
              value={newSchool.phone_number}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="fax_number" className="form-label">
              Numer fax:
            </label>
            <input
              type="text"
              className="form-control"
              id="fax_number"
              name="fax_number"
              value={newSchool.fax_number}
              onChange={handleInputChange}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="email" className="form-label">
              Adres e-mail<span style={{ color: 'red' }}>*</span>:
            </label>
            <input
              type="email"
              className="form-control"
              id="email"
              name="email"
              value={newSchool.email}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="website" className="form-label">
              Strona internetowa:
            </label>
            <input
              type="text"
              className="form-control"
              id="website"
              name="website"
              value={newSchool.website}
              onChange={handleInputChange}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="city" className="form-label">
              Miasto<span style={{ color: 'red' }}>*</span>:
            </label>
            <input
              type="text"
              className="form-control"
              id="city"
              name="city"
              value={newSchool.city}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="street" className="form-label">
              Ulica<span style={{ color: 'red' }}>*</span>:
            </label>
            <input
              type="text"
              className="form-control"
              id="street"
              name="street"
              value={newSchool.street}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="building_number" className="form-label">
              Numer budynku<span style={{ color: 'red' }}>*</span>:
            </label>
            <input
              type="text"
              className="form-control"
              id="building_number"
              name="building_number"
              value={newSchool.building_number}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="apartment_number" className="form-label">
              Numer mieszkania:
            </label>
            <input
              type="text"
              className="form-control"
              id="apartment_number"
              name="apartment_number"
              value={newSchool.apartment_number}
              onChange={handleInputChange}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="postcode" className="form-label">
              Kod pocztowy<span style={{ color: 'red' }}>*</span>:
            </label>
            <input
              type="text"
              className="form-control"
              id="postcode"
              name="postcode"
              value={newSchool.postcode}
              onChange={handleInputChange}
              required
            />
          </div>
        </form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" type="button" onClick={handleClose}>
          Zamknij
        </Button>
        <Button style={buttonSaveChanges} type="button" onClick={handleAddSchool}>
          Dodaj szkołę
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export default AddSchoolModal;