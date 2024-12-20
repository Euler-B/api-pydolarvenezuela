// Components
import Home from './components/Home.js';
import Plans from './components/Plans.js';
import Login from './components/LoginToken.js';
import App from './templates/App.js';
import Dashboard from './templates/Dashboard.js';
import Usage from './views/Usage.js';
import Profile from './views/Profile.js';

// Definir las rutas
const routes = [
    {
        path: '/', component: Home
    },
    {
        path: '/pricing', component: Plans
    },
    {
        path: '/login', component: Login
    },
    {
        path: '/dashboard', component: Dashboard,
        children: [
            {
                path: 'usage', component: Usage
            },
            {
                path: 'profile', component: Profile
            }
        ],
        // Redirigir a login si no hay token
        beforeEnter: (to, from, next) => {
            if (!localStorage.getItem('token')) {
                next('/login');
            } else {
                next();
            }
        }
    }
];

const router = VueRouter.createRouter({
    history: VueRouter.createWebHistory(),
    routes
});

Vue.createApp(App).use(router).mount('#app');