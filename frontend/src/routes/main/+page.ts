import type { VehicleSmall } from '$lib/interfaces/vehicles.interface';
import { variables } from '$lib/utils/constants';
export async function load({ url, fetch }) {
	const ref = url.searchParams.toString();
	let vehicleList: Promise<VehicleSmall[]>;
	console.log(url.searchParams.size)
	if (url.searchParams.size <= 0) {
		const res = await fetch(`${variables.BASE_MAIN_URI}/vehicles/open-vehicles/`);
		if (res.ok) {
			console.log("Un-filtered search")
			vehicleList = await res.json();
		} else {
			throw new Error('Something went Wrong');
		}
	} else {
		const res = await fetch(`${variables.BASE_MAIN_URI}/vehicles/open-vehicles/?${ref}`);
		if (res.ok) {
			vehicleList = await res.json();
			console.log("filtered search")
			console.log(vehicleList)
		} else {
			throw new Error('Something went Wrong');
		}
	}

	return {
		props: {
			ref,
			vehicleList
		}
	};
}
