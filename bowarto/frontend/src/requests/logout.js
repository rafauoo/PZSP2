import MyToast from "../components/Toast";

async function logout() {
  const updateSession = () => {
    sessionStorage.removeItem('access');
    sessionStorage.removeItem('role');
    window.location.href = '/'
    alert("Wylogowano")
  }
  try {
    const refreshToken = sessionStorage.getItem('refresh');

    const response = await fetch('http://20.108.53.69/api/logout/', {
      method: 'POST', headers: {
        'Content-Type': 'application/json',
      }, body: JSON.stringify({
        refresh: refreshToken,
      }),
    });

    updateSession();
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
  } catch (error) {
    console.error('Error loggin out :', error);
  }
}

export default logout;
