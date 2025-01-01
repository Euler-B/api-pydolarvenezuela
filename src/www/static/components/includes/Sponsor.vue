<script setup>
import { sponsors } from '@/utils/sponsors/small/sponsors';
</script>
<template>
  <section class="bg-blue-600 text-white p-4">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold text-center">Sponsors</h1>
      <p class="text-center mt-2 mb-4">Este proyecto es posible gracias a nuestros patrocinadores:</p>
      <div class="flex flex-wrap justify-center items-center">
        <transition-group name="fade" tag="div" class="flex flex-wrap justify-center items-center w-full">
          <div v-for="(sponsor, index) in sponsors" v-show="index < 2" :key="index" class="m-4 p-4 text-black bg-white shadow-lg flex items-center w-auto h-24 animate-fade-in transition-all duration-300 hover:shadow-xl">
            <a :href="sponsor.url" target="_blank" class="flex items-center hover:text-blue-600">
              <img :src="sponsor.logo" :alt="sponsor.name" class="w-16 h-16 object-contain mr-4">
              <span :class="{'hidden sm:block': !sponsor.description.trim()}">{{ sponsor.description }}</span>
            </a>
          </div>
        </transition-group>
        <p v-if="sponsors.length > 2" class="text-white mt-4">
          <a href="https://github.com/fcoagz/api-pydolarvenezuela#sponsors" class="underline">Ver más...</a>
        </p>
      </div>
    </div>
  </section>
</template>