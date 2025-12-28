import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'

export default defineConfig({
  plugins: [
    vue(),
    createSvgIconsPlugin({
      iconDirs: [path.resolve(__dirname, 'src/icons/svg')],
      symbolId: 'icon-[name]'
    })
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      'echarts/theme/halloween$': path.resolve(__dirname, './src/theme/halloween.js')
    }
  },
  css: {
    preprocessorOptions: {
      scss: {
        // Silence dart-sass legacy API warning; safe to remove once deps migrate.
        silenceDeprecations: ['legacy-js-api']
      }
    }
  },
  server: {
    port: 5173
  }
})
