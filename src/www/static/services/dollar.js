import 'https://unpkg.com/axios@1.7.8/dist/axios.min.js'

export async function getDollarValue() {
    return await axios.get('/api/v1/dollar', {
        params: {
            page: 'bcv',
            monitor: 'usd'
        }
    })
        .then(response => {
            return response.data
        })
        .catch(error => {
            return {}
        })
}