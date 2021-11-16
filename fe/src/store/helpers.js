let serverUrl = "";

class ApiError extends Error {
  constructor(message, response) {
    super(message);
    this.response = response;
  }

  toString() {
    if(this.response && this.response.message) {
      return this.response.message;
    } else {
      return this.message;
    }
  }
}

export const setUrl = (url) => {
  serverUrl = url + (url.endsWith('/') ? '' : '/');
}

export const get = async (url) => {
  try {
    const res = await fetch(`${serverUrl}${url}`, {
      method: 'GET',
      credentials: 'include',
    })
    if (res.status >= 400) {
      return res.json().then((json) => {
        throw new ApiError(`Error code ${res.status}`, json);
      })

    } else
      return res;
  } catch (err) {
    throw new ApiError(`Error`, { message: "network_error" });
  }
};

export const post = async (url, { body }) => {
  try {
    const res = await fetch(`${serverUrl}${url}`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    });

    if (res.status >= 400) {
      return res.json().then((json) => {
        throw new ApiError(`Error code ${res.status}`, json);
      })

    } else
      return res;
  } catch (err) {
    throw new ApiError(`Error`, { message: "network_error" });
  }
}

