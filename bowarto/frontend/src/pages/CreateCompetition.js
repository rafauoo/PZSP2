import React, {Component} from "react";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Table from 'react-bootstrap/Table';
import DatePicker from 'react-datepicker';
import axios from 'axios';
import 'react-datepicker/dist/react-datepicker.css';
import refreshAccessToken from "../requests/refresh";

class CreateCompetition extends Component {
  constructor(props) {
    super(props);
    this.state = {
      competitionName: "",
      startDate: "",
      endDate: "",
      category: "",
      description: "",
      // agreement: false,
      competitionsTypes: [],
      attachment: null // File attachment
    };
  }

  componentDidMount() {
    axios.get("http://20.108.53.69/api/competition_types/")
      .then((response) => {
        const competitionsTypes = response.data;
        console.log(competitionsTypes)
        this.setState({
          competitionsTypes: competitionsTypes
        })
      })
      .catch((error) => {
        console.log("Error fetching data:", error);
      });
  }

  handleInputChange = (event) => {
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;

    this.setState({
      [name]: value
    });
  }

  handleStartDateChange = (event) => {
    this.setState({
      startDate: event
    })
  }

  handleEndDateChange = (event) => {
    this.setState({
      endDate: event
    })
  }

  handleFileChange = (event) => {
    this.setState({
      attachment: event.target.files[0]
    });
  }

  handleSubmit = async (event) => {
    event.preventDefault();

    // Create form data
    const formData = new FormData();
    formData.append('title', this.state.competitionName);
    formData.append('description', this.state.description);
    formData.append('type', this.state.category);
    formData.append('start_at', this.state.startDate.toISOString());
    formData.append('end_at', this.state.endDate.toISOString());
    // WARNING: right now there is no attachment sent

    // console.log(formData)
    const token = sessionStorage.getItem('access');
    await refreshAccessToken();

    fetch('http://20.108.53.69/api/competitions/', {
      method: 'POST',
      body: formData,
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);

        this.setState({
          competitionName: "",
          startDate: "",
          endDate: "",
          category: "",
          description: "",
          // agreement: false,
          competitionsTypes: [],
          attachment: null // File attachment

        });
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
        <div style={{width: '60%'}}>
          <h1 className="text-left">Formularz Konkursowy</h1>
          <div className="d-flex justify-content-start vh-100">
            <Form style={{width: '100%'}} onSubmit={this.handleSubmit}>
              <Form.Group className="mb-3" controlId="formBasicEmail">

                <Form.Label>Nazwa konkursu*</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Podaj Nazwę"
                  name="competitionName"
                  value={this.state.competitionName}
                  onChange={this.handleInputChange}
                />

                <div className="row">
                  <div className="col-md-6">
                    <Form.Label>Data rozpoczęcia*</Form.Label>
                    <DatePicker
                      name="startDate"
                      selected={this.state.startDate}
                      onChange={this.handleStartDateChange}
                      dateFormat="yyyy-MM-dd HH:mm:ss"
                      showTimeSelect
                      timeFormat="HH:mm"
                      timeIntervals={15}
                      timeCaption="Time"

                    />
                  </div>

                  <div className="col-md-6">
                    <Form.Label>Data zakończenia*</Form.Label>
                    <DatePicker
                      name="endDate"
                      selected={this.state.endDate}
                      onChange={this.handleEndDateChange}
                      dateFormat="yyyy-MM-dd HH:mm:ss"
                      showTimeSelect
                      timeFormat="HH:mm"
                      timeIntervals={15}
                      timeCaption="Time"
                    />
                  </div>
                </div>

                <Form.Label>Kategoria*</Form.Label>
                <Form.Select aria-label="Kategoria" name="category"
                             value={this.state.category}
                             onChange={this.handleInputChange}>
                  <option value="Kategoria" disable selected hidden>Wybierz
                    kategorię
                  </option>
                  {this.state.competitionsTypes.map(element => {
                    return <option value={element.id}>{element.name}</option>
                  })}
                </Form.Select>


                <Form.Label>Opis konkursu*</Form.Label>
                <Form.Control
                  as="textarea"
                  type="text"
                  placeholder="Opis konkursu"
                  name="description"
                  value={this.state.description}
                  onChange={this.handleInputChange}
                  // style={{ height: '100px' }}  // Adjust the height value as needed
                  rows={7}  // Adjust the height value as needed

                />

                <div className="row">
                  <div className="col-md-6">
                    <Form.Label>Dodaj regulamin (regulamin w formacie .pdf,
                      .docx)</Form.Label>
                    <Form.Control
                      type="file"
                      name="attachment"
                      onChange={this.handleFileChange}
                    />
                  </div>

                  <div className="col-md-6">
                    <Form.Label>Dodaj plakat (plakat w formacie .png,
                      .jpg)</Form.Label>
                    <Form.Control
                      type="file"
                      name="attachment"
                      onChange={this.handleFileChange}
                    />
                  </div>
                </div>
              </Form.Group>

              <div className="d-flex justify-content-left">
                <Button style={buttonStyle} type="submit">
                  Swtórz konkurs
                </Button>
              </div>
            </Form>
          </div>
        </div>
      </div>
    );
  }
}

export default CreateCompetition;
