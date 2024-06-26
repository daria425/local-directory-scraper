let api_url = import.meta.env.VITE_DEV_API_URL;
if (import.meta.env.PROD) {
  api_url = import.meta.env.VITE_PROD_API_URL;
}

export { api_url };
