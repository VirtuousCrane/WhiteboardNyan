import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

const { resolve } = require('path');

// https://vitejs.dev/config/
// export default defineConfig({
//  input: 'src/main.js',
//  plugins: [
//      svelte(),
//  ],
// })
export default {
    build: {
        manifest: true,
        rollupOptions: {
            input: [
                resolve(__dirname, './src/main.js'),
            ]
        },
        outDir: 'static',
        assetsDir: 'theme',
    },
    plugins: [svelte(),],
    server: {
        port: 3001,
        open: false,
    }
};
