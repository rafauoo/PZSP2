import {useEffect} from 'react';
import {useState} from 'react';
import Form from 'react-bootstrap/Form';
import refreshAccessToken from '../requests/refresh';
import {fetchDataFromApi} from '../requests/user_panel';
import {getSchoolList} from "../api/requests/school";
import { buttonSaveChanges, buttonStyled, buttonSubmit } from '../styles/styles';
import MessageModal from "../components/MessageModal";
import {registerUser} from "../api/requests/auth";


function Register() {
  const [showMessageModal, setShowMessageModal] = useState(false);
  const [messageText, setMessageText] = useState('');

  const [first_name, setFirstName] = useState()
  const [last_name, setLastname] = useState()
  const [email, setEmail] = useState()
  const [password, setPassword] = useState()
  const [confirmPassword, setConfirmPassword] = useState()

  const formData = {
    email,
    password,
    first_name,
    last_name,
  }


  const handleSubmit = async (event) => {
    event.preventDefault();
    if (password !== confirmPassword) {
      setMessageText("Podane hasła nie są identyczne!")
      setShowMessageModal(true)
      return;
    }
    try {
      const {success, response} = await registerUser(formData);
      if (success) {
        sessionStorage.setItem('refresh', response.refresh)
        sessionStorage.setItem('access', response.access)
        sessionStorage.setItem('role', response.user_type)
        setMessageText('Zarejestrowano użytkownika ' + response.email)
        setShowMessageModal(true)
        window.location.href = '/';

      } else {
        let messageText = '';
        if (response.email) {
          messageText += 'Istnieje użytkownik o takim emailu.\n';
        }
        if (response.password) {
          messageText += 'Hasło nie spełnia wymogów bezpieczeństwa.\n';
        }
        if (response.first_name) {
          messageText += 'Niepoprawna wartość pola imię.\n';
        }
        if (response.last_name) {
          messageText += 'Niepoprawna wartość pola nazwisko.\n';
        }
        messageText = messageText.trimEnd()
        console.log(messageText)
        setMessageText(messageText)
        setShowMessageModal(true)
      }
    } catch (error) {
      console.error("Error something went wrong: ", error);
    }
  }

  return (
    <>
      <br></br>
      <div className="d-flex justify-content-center">
        <h1>Rejestracja użytkownika</h1>
      </div>
      <br></br>
      <div className="d-flex justify-content-center vh-100">
        <Form style={{width: '50%'}} onSubmit={handleSubmit}>
          <Form.Group className="mb-3" controlId="formBasicEmail">

            <Form.Label>Imię*</Form.Label>
            <Form.Control required type="text" value={first_name}
                          onChange={(e) => setFirstName(e.target.value)}
                          placeholder="Podaj imię"/>

            <Form.Label>Nazwisko*</Form.Label>
            <Form.Control required type="text" placeholder="Podaj nazwisko"
                          value={last_name}
                          onChange={(e) => setLastname(e.target.value)}/>


            <Form.Label>E-mail*</Form.Label>
            <Form.Control required type="email" placeholder="Podaj e-mail" value={email}
                          onChange={(e) => setEmail(e.target.value)}/>

          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicPassword">
            <Form.Label>Hasło*</Form.Label>
            <Form.Control required type="password" placeholder="Podaj hasło"
                          value={password}
                          onChange={(e) => setPassword(e.target.value)}/>
          </Form.Group>
          <Form.Group className="mb-3" controlId="formBasicPassword">
            <Form.Label>Powtórz hasło*</Form.Label>
            <Form.Control required type="password" placeholder="Powtórz hasło"
                          value={confirmPassword}
                          onChange={(e) => setConfirmPassword(e.target.value)}/>
          </Form.Group>
          <div className="d-flex justify-content-center">
            <button style={buttonSubmit} variant="success" type="submit">
              Zarejestruj
            </button>
          </div>
        </Form>
      </div>
      <MessageModal
        show={showMessageModal}
        onClose={() => {
          setShowMessageModal(false);
          setMessageText('');
        }}
        message={messageText}
      />
    </>
  );
}

export default Register;
