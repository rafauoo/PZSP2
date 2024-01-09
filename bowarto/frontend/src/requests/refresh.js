async function refreshAccessToken() {
  try {
    const refreshToken = sessionStorage.getItem('refresh');

    const response = await fetch('http://20.108.53.69/api/refresh/', {
      method: 'POST', headers: {
        'Content-Type': 'application/json',
      }, body: JSON.stringify({
        refresh: refreshToken,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    sessionStorage.setItem('access', data.access);
    // console.log('Access token refreshed successfully:', data.access);
  } catch (error) {
    console.error('Error refreshing access token:', error);
  }
}

export default refreshAccessToken;
