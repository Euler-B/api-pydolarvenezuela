import { defineConfig } from 'vitepress'
import { useSidebar } from 'vitepress-openapi'
import spec from '../public/openapi.json' assert { type: 'json' }

const sidebar = useSidebar({ spec })

export default defineConfig({
  title: "PyDolarVenezuela API Docs",
  description: "Documentación de la API de pyDolarVenezuela",
  themeConfig: {
    sidebar: [
      ...sidebar.generateSidebarGroups(),
    ],
    nav: [
      {
        text: 'API',
        link: 'https://pydolarve.org/'
      },
    ],
    socialLinks: [
      {
        icon: 'github',
        link: 'https://github.com/fcoagz/api-pydolarvenezuela'
      },
    ],
  },
})
