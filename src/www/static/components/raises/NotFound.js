export default {
    setup() {
        return {
            message: Vue.ref('404 - Page not found')
        }
    },
    name: 'NotFound',
    template: `
        <div>
            <h1>{{ message }}</h1>
        </div>
    `
};