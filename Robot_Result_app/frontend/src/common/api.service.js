const axios = require('axios');

function configureAxios() {
  axios.defaults.xsrfCookieName = "csrftoken";
  axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
}

export { axios, configureAxios };