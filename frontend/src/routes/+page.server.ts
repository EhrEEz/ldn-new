import { redirect } from '@sveltejs/kit';
import { userData } from '$lib/store/userStore';

export function load() {
	throw redirect(308, '/main');
}
