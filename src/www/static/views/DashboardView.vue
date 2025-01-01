<script>
import { RouterLink, RouterView } from 'vue-router';
import Cookies from 'js-cookie';

export default {
    data() {
        return {
            menuOpen: false
        };
    },
    methods: {
        toggleMenu() {
            this.menuOpen = !this.menuOpen;
        },
        logout() {
            Cookies.remove('token');
            this.$router.push('/');
        },
        isActive(route) {
            return this.$route.path === route;
        }
    },
    mounted() { 
        this.$router.push('/dashboard/usage'); 
    }
}
</script>
<template>
    <div class="flex bg-gray-50 p-4 min-h-screen">
        <div class="bg-white shadow-lg rounded-lg overflow-hidden flex flex-col md:flex-row w-full">
            <aside class="w-full md:w-64 bg-blue-700 text-white flex flex-col">
            <div class="p-4 text-xl font-bold border-b border-blue-600 flex items-center justify-between">
                <span>Dashboard</span>
                <div class="md:hidden relative">
                <button @click="toggleMenu" class="focus:outline-none">
                    <i class="fas fa-bars"></i>
                </button>
                <div v-if="menuOpen" class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10">
                    <ul>
                    <li :class="{'bg-blue-600': isActive('/dashboard/usage')}" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                        <router-link to="/dashboard/usage" @click="toggleMenu">Uso</router-link>
                    </li>
                    <li :class="{'bg-blue-600': isActive('/dashboard/profile')}" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                        <router-link to="/dashboard/profile" @click="toggleMenu">Perfil</router-link>
                    </li>
                    <li class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                        <a href="#" @click.prevent="logout">Cerrar sesión</a>
                    </li>
                    <li class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                        <RouterLink to="/" @click="toggleMenu">Salir</RouterLink>
                    </li>
                    </ul>
                </div>
                </div>
            </div>
            <nav class="p-4 border-t border-blue-600 hidden md:block">
                <ul>
                <li :class="{'bg-blue-600': isActive('/dashboard/usage')}" class="py-2 px-4 hover:bg-blue-600 flex items-center">
                    <i class="fas fa-chart-line mr-2"></i>
                    <RouterLink to="/dashboard/usage" class="block text-white">Uso</RouterLink>
                </li>
                <li :class="{'bg-blue-600': isActive('/dashboard/profile')}" class="py-2 px-4 hover:bg-blue-600 flex items-center">
                    <i class="fas fa-user mr-2"></i>
                    <RouterLink to="/dashboard/profile" class="block text-white">Perfil</RouterLink>
                </li>
                </ul>
            </nav>
            <div class="mt-auto p-4 border-t border-blue-600 hidden md:block">
                <ul>
                <li class="py-2 px-4 hover:bg-blue-600 flex items-center">
                    <i class="fas fa-sign-out-alt mr-2"></i>
                    <a href="#" @click.prevent="logout" class="block text-white">Cerrar sesión</a>
                </li>
                <li class="py-2 px-4 hover:bg-blue-600 flex items-center">
                    <i class="fas fa-arrow-left mr-2"></i>
                    <RouterLink to="/" class="block text white">Salir</RouterLink>
                </li>
                </ul>
            </div>
            </aside>
            <main class="flex-1 p-6 bg-gray-100 overflow-auto">
            <RouterView />
            </main>
        </div>
    </div>
</template>