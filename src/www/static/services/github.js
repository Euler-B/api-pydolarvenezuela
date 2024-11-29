import 'https://unpkg.com/axios@1.7.8/dist/axios.min.js'

const URL_API = 'https://api.github.com/repos/fcoagz/api-pydolarvenezuela'

export async function getAmountStars() {
    return await axios.get(URL_API)
        .then(response => {
            return response.data.stargazers_count
        })
}