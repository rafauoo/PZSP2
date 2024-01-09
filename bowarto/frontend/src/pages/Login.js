import Button from 'react-bootstrap/Button';
import axios from 'axios';
import Form from 'react-bootstrap/Form';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [username, setUsername] = useState()
  const [password, setPassword] = useState()
  const [userData, setUserData] = useState()
  const [loginError, setLoginError] = useState(true);
  const [loginErrorMessage, setLoginErrorMessage] = useState('');
  // const [postData, setPostData] = useState()
  const navigate = useNavigate();


  const handleLogin = (event) => {
    event.preventDefault();

    const postData = {
      email: username,
      password: password,
    };
    axios.post("http://20.108.53.69/api/login/", postData, {
    })
      .then(response => {
        setLoginError(false);
        const responseData = response.data;
        const token = responseData.access;
        sessionStorage.setItem('access', token);

        const headers = {
          'Authorization': 'Bearer ' + token, // Add any authorization token if needed
        };
        // NOTE: store role of logged in user in the sessionStorage
        axios.get(`http://20.108.53.69/api/me/`, { headers })
          .then(res => {
            const userData = res.data;
            setLoginError(false);
            setUserData(userData)
            sessionStorage.setItem('role', userData.group.name);
            console.log(sessionStorage.getItem('role'))
            console.log(sessionStorage.getItem('access'))
            navigate('/');
          })
          .catch((error) => {
            setLoginError(true);
            console.log("Error fetching data:", error);
          });
      })
      .catch(error => {
        console.log('Login failed:', error.message);
        setLoginError(true);
        setLoginErrorMessage(JSON.stringify(error.response.data, null, 2));
        alert('Niepoprawne dane logowania');
      });
  };

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
    <>
      <div className="d-flex justify-content-center">
        <h1>Witamy na platformie konkursowej BoWarto!</h1>
      </div>
      <div className="d-flex justify-content-center vh-100">
        <Form onSubmit={handleLogin}>
          <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>Nazwa użytkownika</Form.Label>
            <Form.Control type="text" style={{ width: '300px' }} placeholder="Podaj nazwę użytkownika" value={username} onChange={(e) => setUsername(e.target.value)} />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicPassword">
            <Form.Label>Hasło</Form.Label>
            <Form.Control type="password" placeholder="Podaj hasło" value={password} onChange={(e) => setPassword(e.target.value)} />
          </Form.Group>
          <div className="d-flex justify-content-center">

            {/* NOTE: this console.log("ERROR") should be changed */}
            <button style={buttonStyle} variant="success" type="submit" >
              {/* <Button variant="success" type="submit" onClick={loginError ? console.log("ERROR") : () => handleBack()}> */}
              Zaloguj
            </button>
          </div>
        </Form>
      </div >
    </>
  );
}

export default Login;
