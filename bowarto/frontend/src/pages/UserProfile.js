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
      await getMe()
      .then(data => {
        this.setState({ 
          userInfo: data,
          pendingSchool: data.school 
        });
      })
      .catch(_ => {});

      await this.refreshAcccess();
      await getSchoolList()
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
      await createSchool(newSchool).then(data => {
        window.alert('Pomyślnie dodano szkołę!');
        this.setState({ pendingSchool: data.id }, () => {
          getSchoolList().then(data => {
            this.setState({ schools: data });
          }).catch(_ => {});
        });
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

    handleUserSubmit = async (event) => {
      event.preventDefault();

      console.log("Changing user data...");

      const {userInfo} = this.state;

      await this.refreshAcccess();
      await editUser(userInfo.id, userInfo).then(_ => {
        window.alert('Dane zostały pomyślnie zaktualizowane!');
      })
      .catch(error => {
        if(error.message && error.message.includes('400')) {
          window.alert('Email jest już używany przez innego użytkownika. Proszę podać inny email.');
        } else {
          window.alert('Edycja użytkownika nie powiodła się. Spróbuj ponownie.');
        }
      });
    }

    handleSchoolSubmit = async (event) => {
      event.preventDefault();

      console.log("Changing user school...");

      const {userInfo, pendingSchool} = this.state;

      const pendingApproval = {
        user: userInfo.id,
        school: pendingSchool
      };
      await this.refreshAcccess();
      await  createPendingApproval(pendingApproval).then(_ => {
        window.alert('Wysłano prośbę o zmianę szkoły!');
        window.location.reload();
      })
      .catch(error => {
        if(error.message && error.message.includes('400')) {
          window.alert('Już jest rozpatrywana jedna proźba o zmianę szkoły!');
        } else {
          window.alert('Wysłanie prośby o zmianę szkoły nie powiodło się!');
        }
      });
    }
  
    render() {
      const { userInfo, schools, pendingSchool, showPopup } = this.state;

      if (!userInfo) {
        return <div>Ładowanie...</div>;
      }

      const { first_name, last_name, email } = userInfo;

      return (
        <>
          <br />
          <div className="d-flex justify-content-center">
            <h1>Profil użytkownika</h1>
          </div>
          <br />
          <div className="d-flex flex-column align-items-center vh-100">
            <div>
              <Form onSubmit={this.handleUserSubmit}>
                <FormGroup className="mb-3">
                  <Form.Label>Imię</Form.Label>
                  <Form.Control type="text" id='first_name' defaultValue={`${first_name}`} onChange={this.handleChangeDefault}/>
        
                  <Form.Label>Nazwisko</Form.Label>
                  <Form.Control type="text" id='last_name' defaultValue={`${last_name}`} onChange={this.handleChangeDefault}/>
        
                  <Form.Label>Email</Form.Label>
                  <Form.Control type="text" id='email' defaultValue={`${email}`} onChange={this.handleChangeDefault}/>
        
                  <div className="d-flex justify-content-center">
                    <button style={buttonSubmit} type="submit">
                      Zapisz zmiany
                    </button>
                  </div>
                </FormGroup>
              </Form>
            </div>
            <div>
              <Form onSubmit={this.handleSchoolSubmit}>
                <FormGroup className="mb-3">
                  <Form.Label>Szkoła</Form.Label>
                  <div className="d-flex">
                    <Form.Select aria-label="Szkoła" id='school' onChange={this.handleSchoolChange}>
                      <option key={null} value={null} hidden selected={pendingSchool == null}>Brak</option>
                      {schools.map((school) => (
                        <option key={school.id} value={school.id} selected={pendingSchool === school.id}> 
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
                      Zmień szkołę
                    </button>
                  </div>
                </FormGroup>
              </Form>
            </div>
          </div>
        </>
      );
    }
}

export default UserProfile;