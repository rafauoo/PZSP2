import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Image from 'react-bootstrap/Image';
import { useState, useEffect } from 'react';

function NavbarExample() {
  // WARNING: Now displayed link change after a page reload, not when the role is changed, idk why
  const [role, setRole] = useState(sessionStorage.getItem('role'));

  // Update the role state when the session storage changes
  useEffect(() => {
    setRole(sessionStorage.getItem('role'));
  }, []);
  return (
    <>
      <Navbar expand="lg" className="bg-body-tertiary">
        <Container>
          <Navbar.Brand href="/">
            <Image src="./images/logo.png" alt="Description" width={200} />
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto justify-content-between">
              <Nav.Link href="/">Home</Nav.Link>
              <Nav.Link href="/konkursy">Konkursy</Nav.Link>
              <Nav.Link href="/register">Rejestracja</Nav.Link>
              <Nav.Link href="/login">Logowanie</Nav.Link>
              {role === 'admin' ? (
                <>
                  <Nav.Link href="/createCompetition">Stwórz konkurs</Nav.Link>
                  <Nav.Link href="/participants">Uczestnicy</Nav.Link>
                </>
              ) : null}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  );
}

export default NavbarExample;
