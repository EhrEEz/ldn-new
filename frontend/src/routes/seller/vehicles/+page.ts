// import { error } from '@sveltejs/kit';
// import { handleGetRequestsWithPermissions } from '$lib/utils/requestUtils';
// import { variables } from '$lib/utils/constants';

// export const load = async () => {
// 	const [vehicles, errors] = await handleGetRequestsWithPermissions(
// 		fetch,
// 		`${variables.BASE_MAIN_URI}/vehicles/user-vehicles/`
// 	);
// 	if (errors.length) {
// 		throw error(500, 'Errors');
// 	} else {
// 		return vehicles;
// 	}
// };
