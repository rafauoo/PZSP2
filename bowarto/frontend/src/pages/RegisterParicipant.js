import React, {useState} from "react";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import refreshAccessToken from "../requests/refresh";
import { buttonSaveChanges } from "../styles/styles";

const RegisterParticipantTable = (competitionId) => {
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    phoneNumber: "",
    agreement: false,
    attachment: null // File attachment
  });

  const handleInputChange = (event) => {
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;

    setFormData({
      ...formData,
      [name]: value
    });
  }

  const handleFileChange = (event) => {
    setFormData({
      ...formData,
      attachment: event.target.files[0]
    });
  }

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Create form data
    const formDataToSend = new FormData();
    formDataToSend.append('first_name', formData.firstName);
    formDataToSend.append('last_name', formData.lastName);
    formDataToSend.append('email', formData.email);
    // Add other form data as needed
    // ...

    await refreshAccessToken();
    const token = sessionStorage.getItem('access')

    try {
      // Step 1: Try to fetch existing applications for the given competitionId
      const apiUrl = `http://20.108.53.69/api/applications/?competition=${competitionId}`;
      const response = await fetch(apiUrl, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        }
      });
      const existingApplications = await response.json();

      // Step 2: Check if the list is empty
      if (existingApplications.length === 0) {
        // If the list is empty, create a new application object
        const newApplication = {competition: competitionId};

        // Send a POST request to create a new application
        const createApplicationResponse = await fetch('http://20.108.53.69/api/applications/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify(newApplication),
        });

        const createdApplicationData = await createApplicationResponse.json();
        const createdApplicationId = createdApplicationData.id;

        // Add the applicationId to the formData
        formData.application = createdApplicationId;
      } else {
        // If the list is not empty, use the first applicationId from the list
        const existingApplicationId = existingApplications[0].id;

        // Add the existing applicationId to the formData
        formData.applicationId = existingApplicationId;
      }

      // Step 3: Now you can send the extended formData to another endpoint or perform any other actions
      console.log('Extended formData:', formData);

      // Example: Send the extended formData to another API endpoint
      const submitResponse = await fetch('http://20.108.53.69/api/participants/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      const submitResult = await submitResponse.json();
      console.log('Submit result:', submitResult);
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  }

  return (
    <div className="d-flex justify-content-center">
      <div style={{width: '60%'}}>
        <h1 className="text-left">Formularz zgłoszeniowy</h1>
        <div className="d-flex justify-content-start vh-100">
          <Form style={{width: '100%'}} onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Imię*</Form.Label>
              <Form.Control
                type="text"
                placeholder="Podaj imię"
                name="firstName"
                value={formData.firstName}
                onChange={handleInputChange}
                required
              />

              <Form.Label>Nazwisko*</Form.Label>
              <Form.Control
                type="text"
                placeholder="Podaj nazwisko"
                name="lastName"
                value={formData.lastName}
                onChange={handleInputChange}
                required
              />

              <Form.Label>E-mail*</Form.Label>
              <Form.Control
                type="text"
                placeholder="Podaj e-mail"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                required
              />

              <Form.Label>Numer telefonu*</Form.Label>
              <Form.Control
                type="text"
                placeholder="Podaj numer telefonu"
                name="phoneNumber"
                value={formData.phoneNumber}
                onChange={handleInputChange}
                required
              />

              <Form.Label>Dodaj załącznik (praca w formacie .pdf, .docx)</Form.Label>
              <Form.Control
                type="file"
                name="attachment"
                onChange={handleFileChange}
              />

              <Form.Check
                type="checkbox"
                id="custom-checkbox"
                label="Wyrażam zgodę na przetwarzanie moich danych osobowych {...}"
                name="agreement"
                checked={formData.agreement}
                onChange={handleInputChange}
                required
              />
            </Form.Group>

            <div className="d-flex justify-content-left">
              <Button style={buttonSaveChanges} type="submit">
                Weź udział
              </Button>
            </div>
          </Form>
        </div>
      </div>
    </div>
  );
}

export default RegisterParticipantTable;
