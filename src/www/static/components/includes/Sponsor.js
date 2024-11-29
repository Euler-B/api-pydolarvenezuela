import { sponsors } from '../../utils/sponsors/small/sponsors.js'

export default {
    setup() {
        return {
            sponsors
        }
    },
    name: 'SponsorComponent',
    template: `
        <section class="bg-blue-600 text-white p-4">
            <h1 class="text-3xl font-bold">Sponsors</h1>
            <div class="max-w-4xl mx-auto flex flex-wrap justify-center items-center">
                <p class="text-center w-full sm:w-auto mr-2">Este proyecto es posible gracias a nuestros patrocinadores:</p>
                <div class="w-full sm:w-auto mt-4 sm:mt-0 flex items-center">
                    <ul class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-6">
                        <li v-for="(sponsor, index) in sponsors" :key="index">
                            <a :href="sponsor.url" target="_blank" class="flex items-center text-white" v-if="index < 3">
                                <img :src="sponsor.logo" :alt="sponsor.name" class="w-16 h-16 rounded-full mr-2 bg-white"> -  {{ sponsor.description }}
                            </a>
                        </li>

                        <li v-if="sponsors.length > 3">
                            <a href="https://github.com/fcoagz/api-pydolarvenezuela#sponsors" class="text-white">Ver más...</a>
                    </ul>
                </div>
            </div>
        </section>
    `
}