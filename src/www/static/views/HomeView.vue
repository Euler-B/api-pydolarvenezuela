<script setup>
import Console from '@/components/Console.vue';
import Sponsor from '@/components/includes/Sponsor.vue';
</script>
<template>
    <Sponsor />
        <section class="bg-white text-gray-800 p-8">
        <div class="max-w-4xl mx-auto text-center">
            <h2 class="text-3xl font-bold mb-4">Bienvenido a la API pyDolarVenezuela</h2>
            <p class="text-lg mb-6 text-justify">
            La API pyDolarVenezuela proporciona datos actualizados sobre el valor del dólar en Venezuela. Es una herramienta esencial para desarrolladores que necesitan información precisa y actualizada sobre el valor del dólar en Venezuela.
            </p>
            <div class="flex justify-center space-x-4">
                <a href="https://github.com/fcoagz/api-pydolarvenezuela" target="_blank" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-800 transition duration-300">
                    Ver Repositorio
                </a>
                <a href="https://docs.pydolarve.org" class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-800 transition duration-300">
                    Ir a la Documentación
                </a>
            </div>
            <Console />
        </div>
    </section>
</template>