const token = localStorage.getItem("token");
const BASE_URL = "http://localhost:5005";

const defalutOptions = token 
  ? {
    // Copy from the specification: 3.4. Making a fetch request
    method: 'GET',
    headers: {
      'Content-type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
  } : {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
};

function get(url) {
  return fetch(`${BASE_URL}${url}`, {
    ...defalutOptions,
  })
    .then((res) => res.json())
    .then((data) => data)
    .catch((err) => {
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: err,
      });
    });
}

function post(url, data) {
  return fetch(`${BASE_URL}${url}`, {
    ...defalutOptions,
    method: "POST",
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.error) {
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: data.error,
        })
        return;
      }
      return data;
    })
    .catch((err) => {
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: err,
      })
  });
}

const http = {
  get,
  post,
};

export default http;