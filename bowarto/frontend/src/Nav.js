import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Image from 'react-bootstrap/Image';
import { useState, useEffect } from 'react';
import logout from './requests/logout';

function NavbarExample() {
  const [role, setRole] = useState(sessionStorage.getItem('role'))
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  useEffect(() => {
    // Check if 'access' item is in sessionStorage
    const token = sessionStorage.getItem('access');

    // Update isLoggedIn based on the presence of 'access' item
    setIsLoggedIn(!!token);
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
              <Nav.Link href="/konkursy">Konkursy</Nav.Link>
              {role === 'admin' ? (
                <>
                  <Nav.Link href="/createCompetition">Stwórz konkurs</Nav.Link>
                  <Nav.Link href="/participants">Uczestnicy</Nav.Link>
                </>
              ) : null}
              {role === 'user' ? (
                <>
                  <Nav.Link href="/user_panel">Moje aplikacje</Nav.Link>
                </>
              ) : null}

              {isLoggedIn ? (
                <>
                <Nav.Link onClick={logout}>Wyloguj</Nav.Link>
                 <Nav.Link href="/profile">Profil</Nav.Link>
                </>
              ) : (
                <>
                <Nav.Link href="/login">Logowanie</Nav.Link>
                <Nav.Link href="/register">Rejestracja</Nav.Link>
                </>
              )}

            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  );
}

export default NavbarExample;
