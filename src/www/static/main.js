// Components
import Home from './components/Home.js';
import Plans from './components/Plans.js';
import App from './templates/App.js';

// Error handling
import NotFound from './components/raises/NotFound.js';

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

if (!routes.map(r => r.path).includes(location.pathname)) {
    Vue.createApp(NotFound).mount('#app');
} else {
    Vue.createApp(App).use(router).mount('#app');
}