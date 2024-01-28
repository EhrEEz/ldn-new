import { variables } from '$lib/utils/constants';
import type { MainVehicle } from '$lib/interfaces/vehicles.interface';
import { error } from '@sveltejs/kit';
/** @type {import('./$types').PageLoad} */
export const load = async ({ fetch, params }): Promise<MainVehicle> => {
	const slug = params.slug;
	const data = await fetch(`${variables.BASE_MAIN_URI}/v/vehicle/${slug}/`);
	if (data.ok) {
		return data.json();
	} else {
		throw error(500, 'Server Error');
	}
};
