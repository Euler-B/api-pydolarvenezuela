import HeaderComponent from "../components/includes/MainHeader.js"

export default {
    name: 'App',
    components: {
        HeaderComponent
    },
    computed: {
        isDashboardRoute() {
            return this.$route.path.startsWith('/dashboard');
        },
        isLoginRoute() {
            return this.$route.path === '/login';
        }
    },
    template: `
        <div>
            <HeaderComponent v-if="!isDashboardRoute && !isLoginRoute" />
            <router-view />
        </div>
    `
}
