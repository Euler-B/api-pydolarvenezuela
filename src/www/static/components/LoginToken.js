import { loginToken } from "../services/user.js";

export default {
    name: 'Login',
    setup() {
        const token = Vue.ref('');

        return {
            token
        };
    },
    methods: {
        async login() {
            const response = await loginToken(this.token);
            if (response.success) {
                localStorage.setItem('token', this.token);
                window.location.href = '/dashboard';
            } else {
                alert('Token inválido');
            }
        }
    },
    template: `
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-md">
      <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <h2 class="text-center text-2xl font-bold mb-4">Login with Access Token</h2>
        <form @submit.prevent="login">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="token">
              Token de acceso
            </label>
            <input v-model="token" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="token" type="text" placeholder="Ingrese su token de acceso" required>
          </div>
          <div class="flex items-center justify-between">
            <button class="bg-blue-600 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="submit">
              Login
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
    `
};