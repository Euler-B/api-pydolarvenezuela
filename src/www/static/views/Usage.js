import { getDaily30, getDaily7, getHourly24 } from "../services/user.js";

export default {
  name: 'Usage',
  data() {
    return {
      selectedChart: '24h',
      chart: null,
      chartData: null,
      totalRequests: 0
    };
  },
  methods: {
    async fetchData() {
      let response;
      try {
        if (this.selectedChart === '24h') {
          response = await getHourly24();
        } else if (this.selectedChart === '7d') {
          response = await getDaily7();
        } else if (this.selectedChart === '30d') {
          response = await getDaily30();
        }

        if (response && response.paths) {
          this.chartData = response.paths;
          this.totalRequests = response.total;  // Asignar el total de solicitudes
          this.renderChart();
        } else {
          console.error('Datos inválidos recibidos:', response);
          this.chartData = null;
          this.totalRequests = 0;
        }
      } catch (error) {
        console.error('Error al obtener los datos:', error);
        this.chartData = null;
        this.totalRequests = 0;
      }
    },
    renderChart() {
      if (!this.chartData) {
        console.error('No hay datos para renderizar');
        return;
      }

      if (this.chart) {
        this.chart.destroy();
      }

      const labels = [];
      const datasets = [];

      Object.keys(this.chartData).forEach(path => {
        const data = this.chartData[path].map(item => item.total_petitions);
        const label = path;
        const backgroundColor = this.getRandomColor();
        const borderColor = backgroundColor;

        labels.push(...this.chartData[path].map(item => this.selectedChart === '24h' ? item.time : item.date));

        datasets.push({
          label,
          data,
          backgroundColor,
          borderColor,
          fill: false
        });
      });

      const ctx = document.getElementById('usageChart').getContext('2d');
      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: [...new Set(labels)],
          datasets
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Total de Peticiones'
              }
            },
            x: {
              title: {
                display: true,
                text: this.selectedChart === '24h' ? 'Hora' : 'Fecha'
              }
            }
          },
          plugins: {
            legend: {
              display: true,
              position: 'top',
              labels: {
                color: 'black'
              }
            },
            tooltip: {
              callbacks: {
                title: function(context) {
                  return context[0].label;
                },
                label: function(context) {
                  return `Total: ${context.raw}`;
                }
              }
            }
          }
        }
      });
    },
    getRandomColor() {
      const letters = '0123456789ABCDEF';
      let color = '#';
      for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    },
    formatTotal(total) { 
      if (total >= 1000000) { 
        return (total / 1000000).toFixed(1) + 'm'; 
      } else if (total >= 1000) { 
        return (total / 1000).toFixed(1) + 'k'; 
      } 
      return total.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); 
    }
  },
  mounted() {
    this.fetchData();
  },
  template: `
    <div class="p-4">
      <h2 class="text-2xl font-bold mb-4">Estadísticas de Uso</h2>
      <p class="text-sm text-gray-500 mb-4">Se actualiza cada hora</p>
      <div class="mb-4">
        <label for="chartType" class="block text-sm font-medium text-gray-700">Selecciona el tipo de gráfica:</label>
        <select v-model="selectedChart" @change="fetchData" id="chartType" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md">
          <option value="24h">Últimas 24 Horas</option>
          <option value="7d">Últimos 7 Días</option>
          <option value="30d">Últimos 30 Días</option>
        </select>
      </div>
      <p class="text-lg font-medium mb-4">Total de Solicitudes: {{ formatTotal(totalRequests) }}</p>
      <div class="relative h-96 w-full md:w-3/4 lg:w-2/3 mx-auto">
        <canvas id="usageChart"></canvas>
      </div>
    </div>
  `
};

