import axios from "axios";

const getAccessToken = () => {
    const val = localStorage.getItem('access_token');
    console.log("get access token value",val)
    return val;
}

const axiosWithContentType = (contentType) => {
    const token = getAccessToken();
    const axiosInstance = axios.create({
        baseURL: 'http://127.0.0.1:8000/url-shortener',
        headers: {
          'Authorization': `bearer ${token}`,
          'Content-Type': contentType
        }
      });

      axiosInstance.interceptors.request.use(
        (config) => {
          const user = localStorage.getItem("access_token");
          if (user) {
            config.headers.Authorization = `bearer ${user}`;
          }
          console.log("request config", config);
          return config;
        },
        (error) => {
          return Promise.reject(error);
        }
      );

    return axiosInstance
}

export const apiJSONType = axiosWithContentType('application/json');
export const apiFormType = axiosWithContentType('application/x-www-form-urlencoded')