import React, { useState } from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import { buttonSaveChanges } from '../../../styles/styles';
import { useEffect } from 'react';
import { getCompetitionTypes } from '../../../api/requests/competitionType'
import { editCompetition } from '../../../api/requests/competition'
import DatePicker from 'react-datepicker'
import Form from 'react-bootstrap/Form';


const EditCompetitionModal = ({ show, handleClose, competition }) => {

  const [competitionsTypes, setCompetitionTypes] = useState([]);
  const [newCompetitionData, setNewCompetitionData] = useState({
    title: competition.title,
    start_at: new Date(competition.start_at),
    end_at: new Date(competition.end_at),
    type: competition.type,
    description: competition.description,
    attachment: null,
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setNewCompetitionData({
      ...newCompetitionData,
      [name]: value,
    });
  };

  const handleStartDateChange = (event) => {
    setNewCompetitionData(prevData => ({
      ...prevData,
      start_at: event
    }));
  };

  const handleEndDateChange = (event) => {
    setNewCompetitionData(prevData => ({
      ...prevData,
      end_at: event
    }));
  };

  const handleFileChange = (event) => {
    setNewCompetitionData({ attachment: event.target.files[0] })
  };

  const handleEditCompetition = async () => {
    const modifiedData = {
      ...newCompetitionData,
      start_at: newCompetitionData.start_at.toISOString(),
      end_at: newCompetitionData.end_at.toISOString(),
    };
    const response = await editCompetition(competition.id, modifiedData);
    window.location.reload();
    handleClose();
  };

  const fetchCompetitionTypes = async () => {
    const response = await getCompetitionTypes();
    setCompetitionTypes(response);
  }

  useEffect(() => {
    fetchCompetitionTypes();
  }, []);


  useEffect(() => {
    console.log(newCompetitionData);
  }, [newCompetitionData]);

  return (
    <Modal show={show} onHide={handleClose} >
      <Modal.Header closeButton>
        <Modal.Title>Edycja konkursu</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <form>
          <div className="mb-3">
            <label htmlFor="title" className="form-label">
              Nazwa:
            </label>
            <input
              type="text"
              className="form-control"
              id="title"
              name="title"
              value={newCompetitionData.title}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="start_at" className="form-label">
              Data rozpoczęcia:
            </label>
            <DatePicker
              name="start_at"
              selected={newCompetitionData.start_at}
              onChange={handleStartDateChange}
              dateFormat="yyyy-MM-dd HH:mm:ss"
              showTimeSelect
              timeFormat="HH:mm"
              timeIntervals={15}
              timeCaption="Time"
              required
            />
          </div>

          <div className="mb-3">
            <label htmlFor="end_at" className="form-label">
              Data zakończenia:
            </label>

            <DatePicker
              name="end_at"
              selected={newCompetitionData.end_at}
              onChange={handleEndDateChange} //NOTE: create a function to edit startdate
              dateFormat="yyyy-MM-dd HH:mm:ss"
              showTimeSelect
              timeFormat="HH:mm"
              timeIntervals={15}
              timeCaption="Time"
              required
            />
          </div>

          <div className="mb-3">
            <label htmlFor="title" className="form-label">
                Kategoria:
            </label>
            <Form.Select aria-label="Kategoria" name="type"
              value={newCompetitionData.type}
              onChange={handleInputChange}
              required>
              <option value="Kategoria" disable selected hidden>Wybierz
                kategorię
              </option>
              {competitionsTypes.map(element => (
                <option value={element.id}>{element.name}</option>
              ))}
            </Form.Select>
          </div>

          <div className="mb-3">
            <label htmlFor="description" className="form-label">
              Opis:
            </label>
            <input
              type="text"
              className="form-control"
              id="description"
              name="description"
              value={newCompetitionData.description}
              onChange={handleInputChange}
            />
          </div>

          <div className="mb-3">
            <label htmlFor="email" className="form-label">
              Załącznik:
            </label>
            <br></br>
            <input
              type="file"
              name="attachment"
              onChange={handleFileChange}
              required
            />
          </div>
        </form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Zamknij
        </Button>
        <Button style={buttonSaveChanges} onClick={handleEditCompetition}>
          Zapisz zmiany
        </Button>
      </Modal.Footer>
    </Modal >
  );
}
export default EditCompetitionModal;
