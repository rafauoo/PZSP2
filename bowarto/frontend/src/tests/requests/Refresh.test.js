import {refreshAccessToken} from "../../api/requests/auth";
import {refreshUrl} from "../../api/urls";

describe('Auth endpoints', () => {
  // Mocking fetch for the tests
  global.fetch = jest.fn(() =>
    Promise.resolve({
      ok: true,
      json: () => Promise.resolve({}),
    })
  );

  afterEach(() => {
    fetch.mockClear();
  });

  describe('refreshAccessToken', () => {
    it('should refresh the access token successfully', async () => {
      // Arrange
      const mockRefreshToken = 'mockRefreshToken';

      // Act
      await expect(refreshAccessToken(mockRefreshToken)).resolves.toEqual(undefined);

      // Assert
      expect(fetch).toHaveBeenCalledWith(refreshUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          refresh: mockRefreshToken,
        }),
      });
    });

    it('should handle refresh token failure', async () => {
      // Arrange
      const mockRefreshToken = 'mockRefreshToken';
      const errorMessage = 'Invalid refresh token';

      // Act
      fetch.mockImplementationOnce(() =>
        Promise.resolve({
          ok: false,
          status: 401,
          json: () => Promise.resolve({detail: errorMessage}),
        })
      );

      // Assert
      await expect(refreshAccessToken(mockRefreshToken)).rejects.toThrow(`Failed to refresh access token: 401 - ${errorMessage}`);
    });

    it('should handle network error during refresh', async () => {
      // Arrange
      const mockRefreshToken = 'mockRefreshToken';
      const networkErrorMessage = 'Network error';

      // Act
      fetch.mockImplementationOnce(() =>
        Promise.reject(new Error(networkErrorMessage))
      );

      // Assert
      await expect(refreshAccessToken(mockRefreshToken)).rejects.toThrow(`Error refreshing access token: ${networkErrorMessage}`);
    });
  });
});
