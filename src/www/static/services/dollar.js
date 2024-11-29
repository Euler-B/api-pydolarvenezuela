import 'https://unpkg.com/axios@1.7.8/dist/axios.min.js'

const URL_API = 'https://pydolarve.org/api/v1/dollar'

export async function getDollarValue() {
    return await axios.get(URL_API, {
        params: {
            page: 'bcv',
            monitor: 'usd'
        }
    })
        .then(response => {
            return response.data
        })
}