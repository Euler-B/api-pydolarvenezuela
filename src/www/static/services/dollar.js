import axios from "axios"

export async function getDollarValue() {
    return await axios.get('https://pydolarve.org/api/v1/dollar', {
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