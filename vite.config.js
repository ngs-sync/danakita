import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), 'VITE_');
  return {
    plugins: [
      {
        name: 'html-transform',
        transformIndexHtml(html) {
          return html
            .replace('VITE_SUPABASE_URL_PLACEHOLDER', env.VITE_SUPABASE_URL || '')
            .replace('VITE_SUPABASE_KEY_PLACEHOLDER', env.VITE_SUPABASE_ANON_KEY || '');
        },
      },
    ],
    build: {
      rollupOptions: {
        input: {
          main: 'index.html',
          admin: 'super-admin.html',
        },
      },
    },
  };
});
