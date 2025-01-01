<script setup>
import { getDollarValue } from '@/services/dollar';
import Cache from '@/utils/cache';
import { onMounted, ref } from 'vue';

const c = new Cache(30 * 60 * 1000);
const dollarData = ref(null);

const fetchDollarValue = async () => {
  const cachedValue = c.get("dollarValue");
  if (cachedValue) {
    dollarData.value = cachedValue;
  } else {
    dollarData.value = await getDollarValue();
    c.put("dollarValue", dollarData.value);
  }
};

onMounted(async () => {
  await fetchDollarValue();
});
</script>
<template>
    <div class="bg-black text-white p-4 rounded-lg mt-4">
        <div class="mb-2">
            <strong>Solicitud:</strong>
            <pre class="bg-gray-800 p-2 rounded whitespace-pre-wrap text-sm sm:text-base break-all sm:break-normal">GET https://pydolarve.org/api/v1/dollar?page=bcv&monitor=usd</pre>
        </div>
        <div>
            <strong>Respuesta:</strong>
            <pre class="bg-gray-800 p-2 rounded whitespace-pre-wrap text-left text-sm sm:text-base break-all sm:break-normal">{{ dollarData }}</pre>
        </div>
    </div>
</template>