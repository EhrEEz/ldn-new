<script lang="ts">
	import { onMount } from 'svelte';
	import { handleGetRequestsWithPermissions } from '$lib/utils/requestUtils';
	import { variables } from '$lib/utils/constants';
	import type { CustomError } from '$lib/interfaces/error.interface';
	import { loading } from '$lib/store/loadingStore';
	let vehicleList: Promise<object[]> = Promise.resolve([]);

	async function fetchVehicles() {
		const [res, err]: [object[], Array<CustomError>] = await handleGetRequestsWithPermissions(
			fetch,
			`${variables.BASE_MAIN_URI}/vehicles/user-vehicles/`
		);
		return res;
		// if (err.length) {
		// } else {
		// 	throw new Error('Something went Wrong');
		// }
	}
	onMount(() => {
		document.body.classList.add('overflow-hidden');
		vehicleList = fetchVehicles();
	});
</script>

<h1 class="med-30 mb-xs">Your Vehicles</h1>
{#await vehicleList}
	loading...
{:then vehicles}
	<div class="row align-items-stretch">
		{#each vehicles as vehicle}
			<div class="col-lg-6">
				<div class="vehicle__card">
					<div class="vehicle__title--wrapper">
						{#if vehicle.on_trip}
							<span class="vehicle__trip vehicle-tag tag--primary">On Trip</span>
						{:else}
							<span class="vehicle__trip vehicle-tag tag--green">Available</span>
						{/if}
						<div class="top">
							<div class="vehicle__info">
								<h2 class="med-14 muted mb-0">{vehicle.name}</h2>
							</div>
							<div class="vehicle__info--main">
								<h3 class="med-24 mb-1">{vehicle.model_manufacturer} {vehicle.model_name}</h3>
								<div class="med-16 primary">{vehicle.reg_no}</div>
							</div>
							<div class="spec--item vehicle-spec mt-2 mb-1">
								<span class="material-symbols-rounded">location_pin</span>
								{vehicle.vehicle_location}, {vehicle.vehicle_city}
							</div>
							<div class="vehicle__spec--grid">
								<div class="spec--item vehicle-spec">
									<span class="material-symbols-rounded">chair</span>
									{vehicle.seats}
								</div>

								<div class="spec--item vehicle-spec">
									{#if vehicle.fuel_type === 'EV'}
										<span class="material-symbols-rounded"> battery_charging_50 </span>
									{:else}
										<span class="material-symbols-rounded"> local_gas_station </span>
									{/if}
									{vehicle.mileage}
									{vehicle.fuel_type === 'EV' ? `KM/C` : 'KM/L'}
								</div>
							</div>
						</div>
						<div class="button--row fl-row gap-2 al-center pt-sm">
							<a
								href="/seller/vehicles/{vehicle.slug}"
								class="btn icon--button btn--primary btn-slim"
							>
								<span class="btn-icon">
									<span class="material-symbols-rounded"> analytics </span>
								</span><span class="btn-text">View Details</span>
							</a>
							<a href="/seller/vehicles/{vehicle.slug}" class="btn icon--button btn--grey btn-slim"
								><span class="btn-icon">
									<span class="material-symbols-rounded"> edit </span>
								</span><span class="btn-text">Edit</span></a
							>
						</div>
					</div>
					<div class="vehicle__image--wrapper">
						<div class="df-image-wrapper">
							<img src={vehicle.vehicle_image} alt={vehicle.name} />
						</div>
					</div>
				</div>
			</div>
		{/each}
	</div>
{/await}
