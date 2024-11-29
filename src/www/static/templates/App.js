import HeaderComponent from "../components/includes/MainHeader.js"

export default {
    name: 'App',
    components: {
        HeaderComponent
    },
    template: `
        <div>
            <HeaderComponent />
            <router-view />
        </div>
    `
}