import { getAmountStars } from '../../services/github.js';

export default {
    name: 'HeaderComponent',
    setup() {
        const stars = Vue.ref(0);

        if (localStorage.getItem('stars')) {
            const [starsValue, date] = localStorage.getItem('stars').split(';');
            if (new Date().getTime() - date < 86400000) {
                stars.value = starsValue;
            }
        } else {
            getAmountStars().then(starsValue => {
            stars.value = starsValue;
            localStorage.setItem('stars', `${starsValue};${new Date().getTime()}`);
        });
        }

        return { stars };
  },
  template: `
    <header class="bg-gray-800 text-white p-4 shadow-lg">
      <div class="max-w-4xl mx-auto flex flex-wrap justify-between items-center">
        <h1 class="text-2xl font-bold w-full sm:w-auto">API pyDolarVenezuela</h1>
        <nav class="w-full sm:w-auto mt-2 sm:mt-0">
          <ul class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-6">
            <li><a class="text-blue-400 hover:text-blue-600 transition duration-300" href="/">Inicio</a></li>
            <li><a class="text-blue-400 hover:text-blue-600 transition duration-300" href="/pricing">Planes</a></li>
          </ul>
        </nav>
        <div class="w-full sm:w-auto mt-2 sm:mt-0 flex items-center bg-blue-600 px-3 py-2 rounded-lg hover:bg-blue-800 transition duration-300">
          <a href="https://github.com/fcoagz/api-pydolarvenezuela" target="_blank" class="flex items-center text-white">
            <i class="fa-brands fa-github text-2xl mr-2"></i>
            <p class="mb-0">Stars: {{ stars }}</p>
          </a>
        </div>
      </div>
    </header>
  `
};
