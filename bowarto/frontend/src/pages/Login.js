import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

function Login() {
  return (
    <>
      <div className="d-flex justify-content-center">
        <h1>Witamy na platformie konkursowej BoWarto!</h1>
      </div>
      <div className="d-flex justify-content-center vh-100">
        <Form>
          <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>Nazwa użytkownika</Form.Label>
            <Form.Control type="text" style={{ width: '300px' }} placeholder="Podaj nazwę użytkownika" />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicPassword">
            <Form.Label>Hasło</Form.Label>
            <Form.Control type="password" placeholder="Podaj hasło" />
          </Form.Group>
          <div className="d-flex justify-content-center">
            <Button variant="success" type="submit">
              Rejestruj
            </Button>
          </div>
        </Form>
      </div>
    </>
  );
}

export default Login;
