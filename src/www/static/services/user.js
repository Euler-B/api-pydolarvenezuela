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