import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
  input: 'src/main.js',
  output: {
      sourcemap: true,
      format: 'iife',
      name: 'app',
      file: 'bundle.js',
  },
  plugins: [
      svelte(),
  ],
})
