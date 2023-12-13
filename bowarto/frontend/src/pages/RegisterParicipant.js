import React, { Component } from "react";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Table from 'react-bootstrap/Table';

class RegisterParticipantTable extends Component {
  constructor(props) {
    super(props);
    this.state = {
      firstName: "",
      lastName: "",
      email: "",
      phoneNumber: "",
      agreement: false,
      attachment: null // File attachment
    };
  }

  handleInputChange = (event) => {
      const target = event.target;
      const value = target.type === 'checkbox' ? target.checked : target.value;
      const name = target.name;
  
      this.setState({
        [name]: value
      });
    }

  handleFileChange = (event) => {
      this.setState({
        attachment: event.target.files[0]
      });
  }

  handleSubmit = (event) => {
    event.preventDefault();
  
    // Create form data
    const formData = new FormData();
    formData.append('first_name', this.state.firstName);
    formData.append('last_name', this.state.lastName);
    formData.append('email', this.state.email);
    // formData.append('phone_number', this.state.phoneNumber);
    // formData.append('agreement', this.state.agreement);
    // formData.append('attachment', this.state.attachment);
    console.log('firstName:', this.state.firstName);
    console.log('lastName:', this.state.lastName);
    console.log('email:', this.state.email);
    console.log('phoneNumber:', this.state.phoneNumber);
    console.log('agreement:', this.state.agreement);
    console.log('attachment:', this.state.attachment);
  
    fetch('http://20.108.53.69/api/participants', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }

  render() {
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
        <div className="d-flex justify-content-center">
          <div style={{ width: '60%' }}>
            <h1 className="text-left">Formularz zgłoszeniowy</h1>
            <div className="d-flex justify-content-start vh-100">
              <Form style={{ width: '100%' }} onSubmit={this.handleSubmit}>
                <Form.Group className="mb-3" controlId="formBasicEmail">
                  <Form.Label>Imię</Form.Label>
                  <Form.Control 
                    type="text" 
                    placeholder="Podaj imię" 
                    name="firstName" 
                    value={this.state.firstName}
                    onChange={this.handleInputChange}
                  />
      
                  <Form.Label>Nazwisko</Form.Label>
                  <Form.Control 
                    type="text" 
                    placeholder="Podaj nazwisko" 
                    name="lastName" 
                    value={this.state.lastName}
                    onChange={this.handleInputChange}
                  />
      
                  <Form.Label>Email</Form.Label>
                  <Form.Control 
                    type="text" 
                    placeholder="Podaj email" 
                    name="email" 
                    value={this.state.email}
                    onChange={this.handleInputChange}
                  />
      
                  <Form.Label>Numer telefonu*</Form.Label>
                  <Form.Control 
                    type="text" 
                    placeholder="Podaj numer telefonu" 
                    name="phoneNumber" 
                    value={this.state.phoneNumber}
                    onChange={this.handleInputChange}
                  />
  
                  <Form.Label>Dodaj załącznik (praca w formacie .pdf, .docx)</Form.Label>
                  <Form.Control 
                    type="file" 
                    name="attachment"
                    onChange={this.handleFileChange} 
                  />
  
                  <Form.Check
                    type="checkbox"
                    id="custom-checkbox"
                    label="Wyrażam zgodę na przetwarzanie moich danych osobowych {...}"
                    name="agreement" 
                    checked={this.state.agreement}
                    onChange={this.handleInputChange}
                  />
                </Form.Group>
    
                <div className="d-flex justify-content-left">
                  <Button style={buttonStyle} type="submit">
                    Weź udział
                  </Button>
                </div>
              </Form>
            </div>
          </div>
        </div>
      );
  }
}

export default RegisterParticipantTable;