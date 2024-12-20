import { getAmountStars } from '../../services/github.js';

export default {
    name: 'HeaderComponent',
    setup() {
        const stars = Vue.ref(0);
        const token = Vue.ref('');
        const menuOpen = Vue.ref(false);
        const setStars = async () => {
            const starsValue = await getAmountStars();
            localStorage.setItem('stars', `${starsValue};${new Date().getTime()}`);
            
            return starsValue;
        };

        const toggleMenu = () => { menuOpen.value = !menuOpen.value; };

        const inicialize = async () => {
            if (localStorage.getItem('stars')) {
                const [starsValue, date] = localStorage.getItem('stars').split(';');
                if (new Date().getTime() - date < 86400000) {
                    stars.value = starsValue;
                } else {
                    stars.value = await setStars();
                }
            } else {
                stars.value = await setStars();
            }

            if (localStorage.getItem('token')) {
                token.value = localStorage.getItem('token');
            }
        };

        inicialize();

        return { stars, menuOpen, toggleMenu, token };
  },
  template: `
  <header class="bg-gray-100 font-bold p-4 shadow-lg">
    <div class="max-w-4xl mx-auto flex flex-wrap justify-between items-center">
      <div class="flex w-full sm:w-auto justify-between items-center mb-2 sm:mb-0">
        <h1 class="text-2xl font-bold text-center sm:text-left">API pyDolarVenezuela</h1>
        <button @click="toggleMenu" class="sm:hidden text-black focus:outline-none ml-4">
          <i class="fa fa-bars text-2xl"></i>
        </button>
      </div>
      <nav :class="{'block': menuOpen, 'hidden': !menuOpen}" class="w-full sm:w-auto mt-2 sm:mt-0 sm:flex sm:items-center">
        <ul class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-6 items-center">
          <li><a class="text-blue-600 hover:text-blue-800 transition duration-300" href="/">Inicio</a></li>
          <li><a class="text-blue-600 hover:text-blue-800 transition duration-300" href="/pricing">Planes</a></li>
        </ul>
      </nav>

      <div class="w-full sm:w-auto mt-2 sm:mt-0 flex justify-center sm:justify-start items-center bg-blue-600 px-3 py-2 rounded-lg hover:bg-blue-800 transition duration-300">
        <a v-if="!token" href="/login" class="flex items-center text-white">
          <i class="fa fa-key text-2xl mr-2"></i>
          <p class="mb-0">Login</p>
        </a>
        <a v-else href="/dashboard" class="flex items-center text-white">
          <i class="fa fa-tachometer-alt text-2xl mr-2"></i>
          <p class="mb-0">Dashboard</p>
        </a>
      </div>

      <div class="w-full sm:w-auto mt-2 sm:mt-0 flex justify-center sm:justify-start items-center bg-blue-600 px-3 py-2 rounded-lg hover:bg-blue-800 transition duration-300">
        <a href="https://github.com/fcoagz/api-pydolarvenezuela" target="_blank" class="flex items-center text-white">
          <i class="fa-brands fa-github text-2xl mr-2"></i>
          <p class="mb-0">Stars: {{ stars }}</p>
        </a>
      </div>
    </div>
  </header>
  `
};
