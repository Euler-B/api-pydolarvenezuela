import axios from "axios"

const URL_API = 'https://api.github.com/repos/fcoagz/api-pydolarvenezuela'

export async function getAmountStars() {
    return await axios.get(URL_API)
        .then(response => {
            return response.data.stargazers_count
        })
}