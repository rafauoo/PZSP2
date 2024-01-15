import React, { Component } from 'react';
import AddSchoolModal from '../components/AddSchoolModal';
import Form from 'react-bootstrap/Form';
import FormGroup from 'react-bootstrap/esm/FormGroup';
import { editUser } from '../api/requests/user';
import { getSchoolList, createSchool } from '../api/requests/school';
import { createPendingApproval } from '../api/requests/pendingApproval';
import { getMe, refreshAccessToken } from '../api/requests/auth';
import { buttonStyle, buttonStyled, buttonSubmit } from '../styles/styles';


class UserProfile extends Component {
    constructor(props) {
      super(props);
      this.state = {
        userInfo: null,
        oldPendingSchool: null,
        pendingSchool: null, 
        schools: [],
        showPopup: false
      };
    }

    async refreshAcccess() {
      const accessToken = await refreshAccessToken(sessionStorage.getItem('refresh'));
      sessionStorage.setItem('access', accessToken);
    }

    async componentDidMount() {
      await this.refreshAcccess();
      getMe()
      .then(data => {
        this.setState({ 
          userInfo: data, 
          oldPendingSchool: data.school, 
          pendingSchool: data.school 
        });
      })
      .catch(_ => {});

      await this.refreshAcccess();
      getSchoolList()
      .then(data => {
        this.setState({ schools: data });
      })
      .catch(_ => {});
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
      await this.refreshAcccess();
      createSchool(newSchool).then(_ => {
        getSchoolList()
        .then(data => {
          this.setState({ schools: data });
        })
        .catch(_ => {});
      })
      .catch(_ => {
        window.alert('Szkoła nie została dodana!');
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

      const {userInfo, oldPendingSchool, pendingSchool} = this.state;

      await this.refreshAcccess();
      editUser(userInfo.id, userInfo).then(data => {
        console.log(data);
        window.alert('Dane zostały pomyślnie zaktualizowane!');
      })
      .catch(error => {
        if(error.message && error.message.includes('400')) {
          window.alert('Email jest już używany przez innego użytkownika. Proszę podać inny email.');
        } else {
          window.alert('Edycja użytkownika nie powiodła się. Spróbuj ponownie.');
        }
      });

      if(oldPendingSchool !== pendingSchool) {
        const pendingApproval = {
          user: userInfo.id,
          school: pendingSchool
        };
        await this.refreshAcccess();
        createPendingApproval(pendingApproval).then(data => {
          console.log(data);
          window.alert('Wysłano prośbę o zmianę szkoły!');
        })
        .catch(_ => {
          window.alert('Wysłanie prośby o zmianę szkoły nie powiodło się!');
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
          <br></br>
          <div className="d-flex justify-content-center">
            <h1>Profil użytkownika</h1>
          </div>
          <br></br>
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
                    <option key={null} value={null} hidden>Brak</option>
                    {schools.map((school) => (
                      <option key={school.id} value={school.id}> 
                        {school.name}, {school.postcode} {school.city}
                      </option>
                    ))}
                  </Form.Select>
                  <button style={buttonStyled} type="button" onClick={this.togglePopup}>
                    inna...
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
                  <button style={buttonSubmit} type="submit">
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