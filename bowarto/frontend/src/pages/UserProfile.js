import React, { Component } from 'react';
import AddSchoolModal from '../components/AddSchoolModal';
import Form from 'react-bootstrap/Form';
import FormGroup from 'react-bootstrap/esm/FormGroup';
import { editUser, getUserMe } from '../api/requests/user';
import { getSchoolList, createSchool } from '../api/requests/school';
import { createPendingApproval } from '../api/requests/pendingApproval';

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
        pendingSchool: null, 
        schools: [],
        showPopup: false
      };
    }

    async componentDidMount() {
      getUserMe()
      .then(data => {
        this.setState({ userInfo: data });
      });

      getSchoolList()
      .then(data => {
        this.setState({ schools: data });
      });
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
      createSchool(newSchool).then(_ => {
        // const updatedUser = {
        //   ...this.state.userInfo,
        //   school: data.id,
        // };
        // this.setState({ userInfo: updatedUser });

        getSchoolList()
        .then(data => {
          this.setState({ schools: data });
        });
      });
    }

    handleChangeDefault = (event) => {
      const { id, value } = event.target;
  
      this.setState({
        userInfo: {
          ...this.state.userInfo,
          [id]: value,
        },
      });
    }

    handleSchoolChange = (event) => {
      const { value } = event.target;
  
      this.setState({
        pendingSchool: value,
      });
    }

    handleSubmit = async (event) => {
      event.preventDefault();

      console.log("Form submitted");

      const {userInfo, pendingSchool} = this.state;

      editUser(userInfo.id, userInfo).then(data => {
        console.log(data);
        window.alert('Dane zostały pomyślnie zaktualizowane!');
      });
      if(pendingSchool) {
        const pendingApproval = {
          user: userInfo.id,
          school: pendingSchool
        };

        createPendingApproval(pendingApproval).then(data => {
          console.log(data);
          window.alert('Wysłano prośbę o zmianę szkoły!');
        });
      }
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
                <Form.Control type="text" id='first_name' defaultValue={`${first_name}`} onChange={this.handleChangeDefault}/>
  
                <Form.Label>Nazwisko</Form.Label>
                <Form.Control type="text" id='last_name' defaultValue={`${last_name}`} onChange={this.handleChangeDefault}/>
  
                <Form.Label>Email</Form.Label>
                <Form.Control type="text" id='email' defaultValue={`${email}`} onChange={this.handleChangeDefault}/>
  
                <Form.Label>Szkoła</Form.Label>
                <div className="d-flex">
                  <Form.Select aria-label="Szkoła" id='school' defaultValue={schoolID} onChange={this.handleSchoolChange}>
                    <option key={null} value={null} selected={schoolID == null}>Brak</option>
                    {schools.map((school) => (
                      <option key={school.id} value={school.id} selected={school.id === schoolID}>
                        {school.name}, {school.postcode} {school.city}
                      </option>
                    ))}
                  </Form.Select>
                  <button style={buttonStyle} type="button" onClick={this.togglePopup}>
                    Inna
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