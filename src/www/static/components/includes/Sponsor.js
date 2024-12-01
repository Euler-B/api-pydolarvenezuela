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
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold text-center">Sponsors</h1>
      <p class="text-center w-full mt-2 mb-4">Este proyecto es posible gracias a nuestros patrocinadores:</p>
      <div class="flex flex-wrap justify-center items-center">
        <transition-group name="fade" tag="div" class="flex flex-wrap justify-center items-center w-full">
          <div v-for="(sponsor, index) in sponsors" v-show="index < 3" :key="index" class="m-4 p-4 text-black shadow-lg flex items-center justify-center w-24 h-24 animate-fade-in">
              <a :href="sponsor.url" target="_blank" class="flex flex-col items-center">
                <img :src="sponsor.logo" :alt="sponsor.name" class="w-full h-full mb-2 object-contain">
              </a>
          </div>
        </transition-group>
        <p v-if="sponsors.length > 3" class="text-white mt-4">
          <a href="https://github.com/fcoagz/api-pydolarvenezuela#sponsors" class="underline">Ver más...</a>
        </p>
      </div>
    </div>
  </section>
    `
}