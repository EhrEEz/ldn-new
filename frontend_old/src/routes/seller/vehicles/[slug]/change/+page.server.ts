// import { superValidate } from 'sveltekit-superforms/server';
// import { fail } from '@sveltejs/kit';
// import { z } from 'zod';
import { variables } from '$lib/utils/constants';
import type { MainVehicle } from '$lib/interfaces/vehicles.interface';
// import type { Actions } from '@sveltejs/kit';
import { error } from '@sveltejs/kit';

// const schema = z.object({
// 	name: z.string().default('Hello world!'),
// 	email: z.string().email()
// });
/** @type {import('./$types').PageLoad} */
export const load = async ({ fetch, params }): Promise<MainVehicle> => {
	const slug = params.slug;
	const data = await fetch(`${variables.BASE_MAIN_URI}/v/vehicle/${slug}/`);
	if (data.ok) {
		return data.json();
		// const form = await superValidate(data.json(), schema);
	} else {
		throw error(500, 'Server Error');
	}
};
