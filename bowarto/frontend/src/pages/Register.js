import {useEffect} from 'react';
import {useState} from 'react';
import Form from 'react-bootstrap/Form';
import refreshAccessToken from '../requests/refresh';
import {fetchDataFromApi} from '../requests/user_panel';
import {getSchoolList} from "../api/requests/school";

const buttonStyle = {
  backgroundColor: 'rgb(131, 203, 83)',
  borderRadius: '5px',
  color: 'black',
  padding: '5px 10px',
  border: 'none',
  cursor: 'pointer',
  margin: '5px'
};

function Register() {
  const [first_name, setFirstName] = useState()
  const [last_name, setLastname] = useState()
  const [town, setTown] = useState()
  const [school, setSchoolName] = useState()
  const [email, setEmail] = useState()
  const [password, setPassword] = useState()
  const [schoolsData, setSchoolsData] = useState([])

  const formData = {
    email,
    password,
    first_name,
    last_name,
    school,
  }

  useEffect(() => {
    const getSchools = async () => {
      try {
        const schoolsData = await getSchoolList();
        console.log(schoolsData)
        setSchoolsData(schoolsData);
      } catch (error) {
        console.log(error)
      }
    };
    getSchools();
  }, [])

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await refreshAccessToken();
      const token = sessionStorage.getItem('access')
      const apiUrl = 'http://20.108.53.69/api/register/'
      const createUserResponse = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(formData)
      })
      console.log(JSON.stringify(formData))
      console.log(createUserResponse.json())
    } catch (error) {
      console.error("Error something went wrong: ", error);
    }
  }

  return (
    <>
      <div className="d-flex justify-content-center">
        <h1>Rejestracja użytkownika</h1>
      </div>
      <div className="d-flex justify-content-center vh-100">
        <Form style={{width: '50%'}} onSubmit={handleSubmit}>
          <Form.Group className="mb-3" controlId="formBasicEmail">

            <Form.Label>Imię</Form.Label>
            <Form.Control type="text" value={first_name}
                          onChange={(e) => setFirstName(e.target.value)}
                          placeholder="Podaj imię"/>

            <Form.Label>Nazwisko</Form.Label>
            <Form.Control type="text" placeholder="Podaj nazwisko"
                          value={last_name}
                          onChange={(e) => setLastname(e.target.value)}/>

            <Form.Label>Szkoła</Form.Label>
            <Form.Select aria-label="Szkoła"
                         onChange={(e) => setSchoolName(e.target.value)}>
              <option value="" disable selected hidden></option>
              {schoolsData.map((school) => (
                <option value={school.id}>{school.name}</option>
              ))}
            </Form.Select>

            <Form.Label>Miasto</Form.Label>
            <Form.Control type="text" placeholder="Podaj miasto" value={town}
                          onChange={(e) => setTown(e.target.value)}/>

            <Form.Label>Email</Form.Label>
            <Form.Control type="email" placeholder="Podaj email" value={email}
                          onChange={(e) => setEmail(e.target.value)}/>

          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicPassword">
            <Form.Label>Hasło</Form.Label>
            <Form.Control type="password" placeholder="Podaj hasło"
                          value={password}
                          onChange={(e) => setPassword(e.target.value)}/>
          </Form.Group>
          <div className="d-flex justify-content-center">
            <button style={buttonStyle} variant="success" type="submit">
              Rejestruj
            </button>
          </div>
        </Form>
      </div>
    </>
  );
}

export default Register;
