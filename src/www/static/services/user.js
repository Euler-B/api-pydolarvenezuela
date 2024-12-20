import 'https://unpkg.com/axios@1.7.8/dist/axios.min.js'

export async function getUser() {
    return await axios.get('/api/user/get-user',
        { headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
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
  return await axios.put('/api/user/change-name',
    { name: user },
    {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
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
    return await axios.post('/api/user/validate-token', {}, { headers: {
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
    return await axios.get('/api/user/hourly-totals-24h',
        { headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        }})
        .then(response => {
            return response.data
        })
        .catch(error => {
            return error
        })
}
export async function getDaily7() {
    return await axios.get('/api/user/daily-totals-7d',
        { headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        }})
        .then(response => {
            return response.data
        })
        .catch(error => {
            return error
        })
}

export async function getDaily30() {
    return await axios.get('/api/user/daily-totals-30d',
        { headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        }})
        .then(response => {
            return response.data
        })
        .catch(error => {
            return error
        })
}
