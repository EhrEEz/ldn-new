import { variables } from '$lib/utils/constants';
import { userData } from '$lib/store/userStore';
import { get } from 'svelte/store';
import { redirect } from '@sveltejs/kit';
import type { MainVehicle } from '$lib/interfaces/vehicles.interface';
import { error } from '@sveltejs/kit';
/** @type {import('./$types').PageLoad} */
export const load = async ({ fetch, params }): Promise<MainVehicle> => {
	const user = get(userData);
	console.log(user);
	// if (!user.phone_number) {
	// 	throw redirect(307, '/login');
	// }
	const slug = params.slug;
	const data = await fetch(`${variables.BASE_MAIN_URI}/v/vehicle/${slug}/`);
	if (data.ok) {
		return data.json();
	} else {
		throw error(500, 'Server Error');
	}
};
