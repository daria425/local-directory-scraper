let api_base = import.meta.env.VITE_DEV_API_BASE;
if (import.meta.env.PROD) {
  api_base = import.meta.env.VITE_PROD_API_BASE;
}

export { api_base };
