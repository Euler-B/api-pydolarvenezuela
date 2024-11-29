export default {
    name: 'Plans',
    template: `
      <section class="bg-white text-gray-800 p-8">
        <div class="max-w-4xl mx-auto text-center">
          <h2 class="text-3xl font-bold mb-6">Planes de la API pyDolarVenezuela</h2>
          <p class="text-lg mb-6">
            Si deseas conocer características interesantes de la API de por vida, considera hacer una donación o suscribirte a través de Ko-fi. Tu apoyo contribuirá al continuo desarrollo del proyecto y al mantenimiento de los servicios en los que está alojado.
          </p>
          <div class="flex flex-wrap justify-center space-x-4">
            <!-- Plan Gratis -->
            <div class="bg-gray-100 p-6 rounded-lg shadow-lg w-full sm:w-80 mb-6">
              <h3 class="text-2xl font-bold mb-4">Gratis</h3>
              <ul class="text-left space-y-2">
                <li><strong>Solicitudes API:</strong> 500/hora</li>
                <li><strong>Historial de precios:</strong> No</li>
                <li><strong>Webhooks:</strong> No</li>
              </ul>
            </div>
            <!-- Plan de Por Vida -->
            <div class="bg-blue-600 text-white p-6 rounded-lg shadow-lg w-full sm:w-80 mb-6">
              <h3 class="text-2xl font-bold mb-4">Token</h3>
              <ul class="text-left space-y-2">
                <li><strong>Solicitudes API:</strong> ∞</li>
                <li><strong>Historial de precios:</strong> Sí</li>
                <li><strong>Webhooks:</strong> Sí</li>
              </ul>
              <a href="https://ko-fi.com/fcoagz" target="_blank" class="block mt-4 bg-white text-blue-600 px-4 py-2 rounded-lg hover:bg-gray-200 transition duration-300">
                Suscribirse en Ko-fi
              </a>
            </div>
          </div>
        </div>
      </section>
    `
  };
  