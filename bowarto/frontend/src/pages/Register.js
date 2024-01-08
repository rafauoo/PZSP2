import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';


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
  return (
    <>
      <div className="d-flex justify-content-center">
        <h1>Witamy na platformie konkursowej BoWarto!</h1>
      </div>
      <div className="d-flex justify-content-center vh-100">
        <Form>
          <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>Imię</Form.Label>
            <Form.Control type="text" placeholder="Podaj imię" style={{ width: '300px' }} />

            <Form.Label>Nazwisko</Form.Label>
            <Form.Control type="text" placeholder="Podaj nazwisko" />


            <Form.Label>Etap nauczania</Form.Label>
            <Form.Select aria-label="Etap nauczania">
              <option value="" disable selected hidden></option>
              <option value="1">Podstawowy</option>
              <option value="2">Ponadpodstawowy</option>
              <option value="3">Wyższy</option>
            </Form.Select>

            <Form.Label>Miasto</Form.Label>
            <Form.Control type="text" placeholder="Podaj miasto" />

            <Form.Label>Pełna nazwa jednoski</Form.Label>
            <Form.Control type="text" placeholder="Podaj pełną nazwę jednoski" />

            <Form.Label>Telefon</Form.Label>
            <Form.Control type="text" placeholder="Podaj telefon" />

            <Form.Label>Email</Form.Label>
            <Form.Control type="email" placeholder="Podaj email" />

            <Form.Label>Nazwa użytkownika</Form.Label>
            <Form.Control type="text" placeholder="Podaj nazwę użytkownika" />
          </Form.Group>


          <Form.Group className="mb-3" controlId="formBasicPassword">
            <Form.Label>Hasło</Form.Label>
            <Form.Control type="password" placeholder="Podaj hasło" />
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
