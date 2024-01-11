import React, { Component } from 'react';
import refreshAccessToken from "../requests/refresh";
import AddSchoolModal from '../components/AddSchoolModal';
import Form from 'react-bootstrap/Form';
import FormGroup from 'react-bootstrap/esm/FormGroup';

const buttonStyle = {
  backgroundColor: "rgb(131, 203, 83)",
  borderRadius: "5px",
  color: "black",
  padding: "5px 10px",
  border: "none",
  cursor: "pointer",
  margin: "5px", 
};

class UserProfile extends Component {
    constructor(props) {
      super(props);
      this.state = {
        userInfo: null,
        schools: [],
        showPopup: false
      };
    }

    async fetchData(url) {
      await refreshAccessToken();
      const token = sessionStorage.getItem('access');
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        }
      });
      return await response.json();
    }

    async componentDidMount() {
      const dataUser = await this.fetchData('http://20.108.53.69/api/me/');
      this.setState({ userInfo: dataUser });

      const dataSchools = await this.fetchData('http://20.108.53.69/api/schools/');
      this.setState({ schools: dataSchools });
    }

    togglePopup = () => {
        this.setState((prevState) => ({
          showPopup: !prevState.showPopup
        }));
      };

    closePopup = () => {
      this.setState({ showPopup: false });
    };

    onAddSchool = async (newSchool) => {
      await refreshAccessToken();
      const token = sessionStorage.getItem('access');
      const responseSchool = await fetch('http://20.108.53.69/api/schools/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(newSchool),
      });

      if(responseSchool.ok) {
        const newSchool = await responseSchool.json();
        const updatedUser = {
          ...this.state.userInfo,
          school: newSchool.id,
        };
        this.setState({ userInfo: updatedUser });

        const dataSchools = await this.fetchData('http://20.108.53.69/api/schools/');
        this.setState({ schools: dataSchools });
      }
    }

    handleChange = (event) => {
      const { id, value } = event.target;
  
      this.setState({
        userInfo: {
          ...this.state.userInfo,
          [id]: value,
        },
      });
    }

    handleSubmit = async (event) => {
      event.preventDefault();

      console.log("Form submitted");

      const {userInfo} = this.state;

      await refreshAccessToken();
      const token = sessionStorage.getItem('access');
      const responseSchool = await fetch(`http://20.108.53.69/api/users/${this.state.userInfo.id}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(userInfo),
      });
      if(!responseSchool.ok) {
        console.log("failed to patch user");
      }
      console.log(await responseSchool.json())
    }
  
    render() {
      const { userInfo, schools, showPopup } = this.state;

      if (!userInfo) {
        return <div>Ładowanie...</div>;
      }

      const { first_name, last_name, email } = userInfo;
      const schoolID = userInfo.school;

      return (
        <>
          <div className="d-flex justify-content-center">
            <h1>Profil użytkownika</h1>
          </div>
          <div className="d-flex justify-content-center vh-100">
            <Form onSubmit={this.handleSubmit}>
              <FormGroup className="mb-3">
                <Form.Label>Imię</Form.Label>
                <Form.Control type="text" id='first_name' defaultValue={`${first_name}`} onChange={this.handleChange}/>
  
                <Form.Label>Nazwisko</Form.Label>
                <Form.Control type="text" id='last_name' defaultValue={`${last_name}`} onChange={this.handleChange}/>
  
                <Form.Label>Email</Form.Label>
                <Form.Control type="text" id='email' defaultValue={`${email}`} onChange={this.handleChange}/>
  
                <Form.Label>Szkoła</Form.Label>
                <div className="d-flex">
                  <Form.Select aria-label="Szkoła" id='school' defaultValue={schoolID} onChange={this.handleChange}>
                    <option value="" disabled hidden></option>
                    {schools.map((school) => (
                      <option key={school.id} value={school.id} selected={school.id === schoolID}>
                        {school.name}
                      </option>
                    ))}
                  </Form.Select>
                  <button style={buttonStyle} type="button" onClick={this.togglePopup}>
                    Dodaj
                  </button>
                  {showPopup && (
                    <AddSchoolModal
                      show={showPopup}
                      handleClose={this.closePopup}
                      onAddSchool={this.onAddSchool}
                    />
                  )}
                </div>
                <div className="d-flex justify-content-center">
                  <button style={buttonStyle} type="submit">
                      Zapisz zmiany
                  </button>
                </div>
              </FormGroup>
            </Form>
          </div>
          </>
      );
    }
}

export default UserProfile;