import type { Variables } from '$lib/interfaces/variables.interface';
const BASE_API_URI: string = import.meta.env.DEV
	? 'http://127.0.0.1:8000/api'
	: import.meta.env.VITE_BASE_API_URI_PROD;

const BASE_MAIN_URI: string = 'http://127.0.0.1:8000';

export const variables: Variables = { BASE_API_URI: BASE_API_URI, BASE_MAIN_URI: BASE_MAIN_URI };
