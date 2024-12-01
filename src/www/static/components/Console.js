import { getDollarValue } from "../services/dollar.js";

export default {
    name: 'ConsoleComponent',
    setup() {
        const request = Vue.ref('GET https://pydolarve.org/api/v1/dollar?page=bcv&monitor=usd');
        const response = Vue.ref('');

        const setDollarValue = async () => {
            const dollarValue = await getDollarValue();
            const JSONDollarValue = JSON.stringify(dollarValue, null, 2);
            localStorage.setItem('dollar', `${JSONDollarValue};${new Date().getTime()}`);
            
            return JSONDollarValue;
        };

        const inicialize = async () => {
            if (localStorage.getItem('dollar')) {
                const [dollarValue, date] = localStorage.getItem('dollar').split(';');
                if (new Date().getTime() - date < 1800000) {
                    response.value = dollarValue;
                } else {
                    response.value = await setDollarValue();
                }
            } else {
                response.value = await setDollarValue();
            }
        };

        inicialize();

        return { request, response };
  },
  template: `
    <div class="bg-black text-white p-4 rounded-lg mt-4">
        <div class="mb-2">
            <strong>Solicitud:</strong>
            <pre class="bg-gray-800 p-2 rounded whitespace-pre-wrap text-sm sm:text-base break-all sm:break-normal">{{ request }}</pre>
        </div>
        <div>
            <strong>Respuesta:</strong>
            <pre class="bg-gray-800 p-2 rounded whitespace-pre-wrap text-left text-sm sm:text-base break-all sm:break-normal">{{ response }}</pre>
        </div>
    </div>
  `
};
