<script setup>
import { getUser, updateUser } from '@/services/user';
import { onMounted, ref } from 'vue';
const profile = ref({});
const newName = ref("");

const formatDate = (dateString) => { 
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString('es-ES', options); 
}

const getProfile = async () => {
    profile.value = await getUser();
}

const saveName = async () => {
    if (newName.value.trim() !== "") {
    profile.value.name = newName.value;
    await updateUser(newName.value);
    newName.value = ""; 
    alert("Nombre actualizado exitosamente");
    } else {
    alert("El nombre no puede estar vacío");
    }
}

onMounted(async () => {
    await getProfile();
});

</script>
<template>
    <div class="p-4">
      <h1 class="text-2xl font-bold mb-4">Perfil</h1>
      <div v-if="Object.keys(profile).length" class="bg-white shadow-md rounded p-6 mb-6">
        <div class="mb-4">
          <label for="name" class="block text-sm font-medium text-gray-700">Nombre</label>
          <p class="text-gray-500 text-sm mb-2">El nombre asociado a tu cuenta</p>
          <input v-model="newName" type="text" id="name" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md" :placeholder="profile.name">
          <button @click="saveName" class="mt-2 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-700">Guardar</button>
        </div>
        <div class="mb-4">
          <label for="created_at" class="block text-sm font-medium text-gray-700">Creado</label>
          <p class="text-gray-500 text-sm mb-2">Fecha de creación de la cuenta</p>
          <p>{{ formatDate(profile.created_at) }}</p>
        </div>
        <div class="mb-4">
          <label for="token" class="block text-sm font-medium text-gray-700">Token</label>
          <p class="text-gray-500 text-sm mb-2">Token de acceso a la API</p>
          <p>{{ profile.token }}</p>
        </div>
      </div>
      <div v-else>
        <p>Cargando perfil...</p>
      </div>
    </div>
</template>