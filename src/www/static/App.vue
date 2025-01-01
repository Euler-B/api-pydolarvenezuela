<script setup>
import { RouterView, useRoute } from 'vue-router';
import MainHeader from './components/includes/MainHeader.vue';
import { computed } from 'vue';

const route = useRoute();

const isDashboardRoute = computed(() => route.path.startsWith('/dashboard'));
const isLoginRoute = computed(() => route.path === '/login');
</script>

<template>
  <div>
    <MainHeader v-if="!isDashboardRoute && !isLoginRoute" />
    <RouterView />
  </div>
</template>