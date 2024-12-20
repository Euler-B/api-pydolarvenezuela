// Components
import Home from './components/Home.js';
import Plans from './components/Plans.js';
import Login from './components/LoginToken.js';
import App from './templates/App.js';
import Dashboard from './templates/Dashboard.js';

const routes = [
    {
        path: '/', component: Home
    },
    {
        path: '/pricing', component: Plans
    }
]

const router = VueRouter.createRouter({
    history: VueRouter.createWebHistory(),
    routes
});

if (location.pathname === '/' || location.pathname === '/pricing') {
    Vue.createApp(App).use(router).mount('#app');
} else if (location.pathname === '/login' && !localStorage.getItem('token')) {
    Vue.createApp(Login).mount('#app');
} else if (location.pathname === '/dashboard' && localStorage.getItem('token')) {
    Vue.createApp(Dashboard).mount('#app');
} else {
    window.location.href = '/';
}