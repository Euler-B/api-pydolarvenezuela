import axios from "axios";
import Cookies from "js-cookie";

export async function getUser() {
    return await axios.get('https://pydolarve.org/api/user/get-user',
        { headers: {
            'Authorization': `Bearer ${Cookies.get('token')}`
        }}
    )
        .then(response => {
            return response.data
        })
        .catch(error => {
            return error
        })
}

export async function updateUser(user) {
  return await axios.put('https://pydolarve.org/api/user/change-name',
    { name: user },
    {
      headers: {
        'Authorization': `Bearer ${Cookies.get('token')}`
      }
    }
  )
    .then(response => {
      return response.data;
    })
    .catch(error => {
      console.error('Error actualizando el nombre:', error);
      throw error;  // Asegura que el error sea manejado adecuadamente
    });
}


export async function loginToken(token) {
    return await axios.post('https://pydolarve.org/api/user/validate-token', {}, { headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}` 
    }})
        .then(response => {
            return response.data
        })
        .catch(error => {
            return error
        })
}

export async function getHourly24() {
    return await axios.get('https://pydolarve.org/api/user/hourly-totals-24h',
        { headers: {
            'Authorization': `Bearer ${Cookies.get('token')}`
        }})
        .then(response => {
            return response.data
        })
        .catch(error => {
            return error
        })
}
export async function getDaily7() {
    return await axios.get('https://pydolarve.org/api/user/daily-totals-7d',
        { headers: {
            'Authorization': `Bearer ${Cookies.get('token')}`
        }})
        .then(response => {
            return response.data
        })
        .catch(error => {
            return error
        })
}

export async function getDaily30() {
    return await axios.get('https://pydolarve.org/api/user/daily-totals-30d',
        { headers: {
            'Authorization': `Bearer ${Cookies.get('token')}`
        }})
        .then(response => {
            return response.data
        })
        .catch(error => {
            return error
        })
}
