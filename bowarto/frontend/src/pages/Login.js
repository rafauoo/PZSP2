import Form from 'react-bootstrap/Form';
import {useState} from 'react';
import {useNavigate} from 'react-router-dom';
import {getMe, loginUser} from "../api/requests/auth";
import { buttonSaveChanges, buttonStyle, buttonStyled, buttonSubmit } from '../styles/styles';

function Login() {
  const [username, setUsername] = useState()
  const [password, setPassword] = useState()
  const [userData, setUserData] = useState()
  const [loginError, setLoginError] = useState(true);
  const [loginErrorMessage, setLoginErrorMessage] = useState('');
  // const [postData, setPostData] = useState()
  const navigate = useNavigate();


  const handleLogin = async (event) => {
    event.preventDefault();

    const postData = {
      email: username,
      password: password,
    };
    try {
      const tokens = await loginUser(postData);
      setLoginError(false);

      const accessToken = tokens.access;
      const refreshToken = tokens.refresh;

      sessionStorage.setItem('access', accessToken);
      sessionStorage.setItem('refresh', refreshToken);
      try {
        const userData = await getMe();

        setLoginError(false);
        setUserData(userData);
        sessionStorage.setItem('role', userData.user_type);
        console.log(sessionStorage.getItem('role'))
        // NOTE: Using window.location because navigate didn't refresh the page,
        // therefore the navbar wasn't being updated
        window.location.href = '/';
      } catch (error) {
        setLoginError(true);
        console.log("Error fetching data:", error);
      }
    } catch (error) {
      console.log('Login failed:', error.message);
      setLoginError(true);
      console.log(error)
      setLoginErrorMessage(JSON.stringify(error.null, 2));
      alert('Niepoprawne dane logowania');
    }
  };

  const handleBack = () => {
    navigate("/");
  };

  return (
    <>
      <br></br>
      <div className="d-flex justify-content-center">
        <h1>Witamy na platformie konkursowej fundacji BoWarto!</h1>
      </div>
      <br></br>
      <div className="d-flex justify-content-center vh-100">
        <Form onSubmit={handleLogin}>
          <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>Nazwa użytkownika</Form.Label>
            <Form.Control type="text" style={{width: '300px'}}
                          placeholder="Podaj nazwę użytkownika" value={username}
                          onChange={(e) => setUsername(e.target.value)}/>
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicPassword">
            <Form.Label>Hasło</Form.Label>
            <Form.Control type="password" placeholder="Podaj hasło"
                          value={password}
                          onChange={(e) => setPassword(e.target.value)}/>
          </Form.Group>
          <div className="d-flex justify-content-center">

            {/* NOTE: this console.log("ERROR") should be changed */}
            <button style={buttonSubmit} variant="success" type="submit">
              {/* <Button variant="success" type="submit" onClick={loginError ? console.log("ERROR") : () => handleBack()}> */}
              Zaloguj
            </button>
          </div>
        </Form>
      </div>
    </>
  );
}

export default Login;
