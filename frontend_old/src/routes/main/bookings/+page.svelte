<script lang="ts">
	import { onMount } from 'svelte';
	import { notificationData } from '$lib/store/notificationStore';
	import {
		handleGetRequestsWithPermissions,
		handlePostRequestsWithPermissions
	} from '$lib/utils/requestUtils';
	import { variables } from '$lib/utils/constants';
	import type { CustomError } from '$lib/interfaces/error.interface';
	import moment from 'moment';

	interface Readings {
		[key: string]: number;
	}

	let booking_list: Promise<object[]> = Promise.resolve([]);
	let inactive_booking_list: Promise<object[]> = Promise.resolve([]);
	let final_odometer_readings: Readings = {};
	async function fetchActiveBookings() {
		const [res, err]: [object[], Array<CustomError>] = await handleGetRequestsWithPermissions(
			fetch,
			`${variables.BASE_MAIN_URI}/vehicles/user/bookings/`
		);
		return res;
	}
	async function fetchInActiveBookings() {
		const [res, err]: [object[], Array<CustomError>] = await handleGetRequestsWithPermissions(
			fetch,
			`${variables.BASE_MAIN_URI}/vehicles/user/terminated-bookings/`
		);
		return res;
	}
	async function cancelBooking(booking: string) {
		const [res, err]: [object, Array<CustomError>] = await handlePostRequestsWithPermissions(
			fetch,
			`${variables.BASE_MAIN_URI}/vehicles/booking/cancel/`,
			{
				booking: booking
			}
		);
		if (res) {
			notificationData.update(() => 'Booking Cancelled...');
			booking_list = fetchActiveBookings();
			inactive_booking_list = fetchInActiveBookings();
		}
		return res;
	}
	async function finishBooking(booking: string, amount: number, id: keyof Readings) {
		const imID = final_odometer_readings[id];

		const [res, err]: [object, Array<CustomError>] = await handlePostRequestsWithPermissions(
			fetch,
			`${variables.BASE_MAIN_URI}/vehicles/booking/payment-create/`,
			{
				booking: booking,
				amount: amount,
				final_odometer_reading: imID
			}
		);
		if (res) {
			notificationData.update(() => 'Booking Payment Created...');
			booking_list = fetchActiveBookings();
			inactive_booking_list = fetchInActiveBookings();
		}
		return res;
	}
	onMount(() => {
		document.body.classList.add('overflow-hidden');
		booking_list = fetchActiveBookings();
		inactive_booking_list = fetchInActiveBookings();
	});
</script>

<section class="main-content py-ms">
	<div class="container">
		<div class="row">
			<div class="col-lg-12">
				<h1 class="heading-3 mb-sm">Active Bookings</h1>
			</div>
			<div class="col-lg-12">
				{#await booking_list}
					getting_data..
				{:then data}
					<div class="row align-items-stretch">
						{#each data as item}
							<div class="col-lg-8 mb-4">
								<div class="gr--card">
									<div class="row">
										<div class="col-12">
											<div class="pb-sm">
												<h3 class="med-24 mb-1">
													{item.vehicle.model_manufacturer}
													{item.vehicle.model_name}
												</h3>
												<div class="med-16 primary">{item.vehicle.reg_no}</div>
											</div>
										</div>
										<div class="col-8">
											<div class="card--label">Booking ID</div>
											<div class="card--value primary med-16">{item.id}</div>
										</div>
										<div class="col-4">
											<div class="card--label">Booking Date</div>
											<div class="card--value">
												{moment(item.creation_date).format('MMMM Do, YYYY')}
											</div>
										</div>

										<div class="col-6">
											<div class="pt-sm">
												<div class="card--label">Location</div>
												<div class="card--value">
													{item.vehicle.vehicle_location}, {item.vehicle.vehicle_city}
												</div>
											</div>
										</div>
										<div class="col-4">
											<div class="pt-sm">
												<div class="card--label">Confirmation</div>
												<div class="card--value">{item.is_confirmed ? 'Confirmed' : 'Pending'}</div>
											</div>
										</div>
									</div>
								</div>
							</div>
							<div class="col-lg-4 mb-4">
								<div class="gr--card">
									<div class="row">
										<div class="col-12">
											<div class="">
												<h3 class="med-24 mb-1 primary">Rs. {item.total_cost}</h3>
											</div>
										</div>
										<div class="col-6">
											<div class="pt-sm">
												<div class="card--label">From</div>
												<div class="card--value">
													{moment(item.booking_start_date).format('MMMM Do, YYYY')}
												</div>
											</div>
										</div>
										<div class="col-6">
											<div class="pt-sm">
												<div class="card--label">To</div>
												<div class="card--value">
													{moment(item.booking_end_date).format('MMMM Do, YYYY')}
												</div>
											</div>
										</div>
										<div class="col-12">
											<div class="fl-row al-center gap-2 pt-ms fl-wrap">
												{#if !item.is_confirmed}
													<button
														class="btn btn--grey btn-global"
														on:click={() => {
															cancelBooking(item.id);
														}}>Cancel Booking</button
													>
												{:else if !item.is_terminated}
													<div class="form-group">
														<label for="foa-{item.id}"
															>Final Odometer Reading (min: {item.booking_details_set
																.odometer_reading_before})</label
														>
														<input
															type="number"
															class="form-control"
															name="foa-{item.id}"
															id="foa-{item.id}"
															min={item.booking_details_set.odometer_reading_before}
															bind:value={final_odometer_readings[`${item.id}`]}
														/>
													</div>
													<button
														class="btn btn--success btn-global"
														on:click={() => {
															finishBooking(item.id, item.total_cost, `${item.id}`);
														}}>Finish Booking</button
													>
												{/if}
											</div>
										</div>
									</div>
								</div>
							</div>
						{/each}
					</div>
				{/await}
			</div>
		</div>
		<div class="row" style="padding-top: 1em; border-top: 1px solid #efefef;">
			<div class="col-lg-12">
				<h1 class="heading-3 mb-sm">Terminated Bookings</h1>
			</div>
			<div class="col-lg-12">
				{#await inactive_booking_list}
					getting_data..
				{:then data}
					<div class="row align-items-stretch">
						{#each data as item}
							<div
								class="col-lg-8 mb-4
							"
							>
								<div class="gr--card">
									<div class="row">
										<div class="col-12">
											<div class="pb-sm">
												<h3 class="med-24 mb-1">
													{item.vehicle.model_manufacturer}
													{item.vehicle.model_name}
												</h3>
												<div class="med-16 primary">{item.vehicle.reg_no}</div>
											</div>
										</div>
										<div class="col-8">
											<div class="card--label">Booking ID</div>
											<div class="card--value primary med-16">{item.id}</div>
										</div>
										<div class="col-4">
											<div class="card--label">Booking Date</div>
											<div class="card--value">
												{moment(item.creation_date).format('MMMM Do, YYYY')}
											</div>
										</div>

										<div class="col-6">
											<div class="pt-sm">
												<div class="card--label">Location</div>
												<div class="card--value">
													{item.vehicle.vehicle_location}, {item.vehicle.vehicle_city}
												</div>
											</div>
										</div>
										<div class="col-4">
											<div class="pt-sm">
												<div class="card--label">Status</div>
												<div class="card--value">
													{item.is_terminated
														? item.terminate_bookings_set.end_type === 332
															? 'Finished'
															: 'Cancelled'
														: item.is_confirmed
														? 'Confirmed'
														: 'Pending'}
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
							<div class="col-lg-4 mb-4">
								<div class="gr--card">
									<div class="row">
										<div class="col-12">
											<div class="">
												<h3
													class="med-24 mb-1 primary {item.terminate_bookings_set.end_type === 232
														? 'strike'
														: ''}"
												>
													Rs. {item.total_cost}
												</h3>
											</div>
										</div>
										<div class="col-6">
											<div class="pt-sm">
												<div class="card--label">From</div>
												<div class="card--value">
													{moment(item.booking_start_date).format('MMMM Do, YYYY')}
												</div>
											</div>
										</div>
										<div class="col-6">
											<div class="pt-sm">
												<div class="card--label">To</div>
												<div class="card--value">
													{moment(item.booking_end_date).format('MMMM Do, YYYY')}
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
						{/each}
					</div>
				{/await}
			</div>
		</div>
	</div>
</section>
