<script lang="ts">
	import type { MainVehicle } from '$lib/interfaces/vehicles.interface';
	import {
		post,
		browserSet,
		browserGet,
		handlePostRequestsWithPermissions
	} from '$lib/utils/requestUtils';
	import { goto } from '$app/navigation';
	import { get } from 'svelte/store';
	import { userData } from '$lib/store/userStore';
	import { variables } from '$lib/utils/constants';

	import moment from 'moment';
	import { onMount } from 'svelte';
	import { redirect } from '@sveltejs/kit';
	onMount(() => {
		const reqToken = browserGet('refreshToken');
		if (!reqToken) {
			goto('/login');
		}
	});
	export let data;
	$: submitting = false;
	const now = moment().format('YYYY-MM-DD');
	$: later = moment(booking_start_date, 'YYYY-MM-DD').add(1, 'd').format('YYYY-MM-DD');
	const attributes1 = { min: now };
	const attributes2 = { required: true };
	let booking_start_date = '';
	let booking_end_date = '';
	$: duration =
		booking_start_date && booking_end_date
			? moment
					.duration(
						moment(booking_end_date, 'YYYY-MM-DD').diff(moment(booking_start_date, 'YYYY-MM-DD'))
					)
					.asDays()
			: 0;
	function handleResetEnd() {
		booking_end_date = '';
		duration = 0;
	}
	const errorState = false;

	const handleBookingSubmit = async () => {
		const [res, err] = await handlePostRequestsWithPermissions(
			fetch,
			`${variables.BASE_MAIN_URI}/vehicles/booking/create/`,
			{
				vehicle: data.id,
				booking_start_date: booking_start_date,
				booking_end_date: booking_end_date
			}
		);
		if (err.length === 0) {
			return res;
		} else {
			throw new Error('Something went Wrong');
		}
	};
	let submission: Promise<any> = Promise.resolve();
	const handleSubmit = () => {
		submitting = true;
		submission = handleBookingSubmit();
	};
</script>

<svelte:head>
	<title>Book Vehicle</title>
</svelte:head>

{#if !submitting}
	<section class="book__vehicle--secrtion py-ms">
		<div class="con mx-lg">
			<div class="row">
				<div class="col-lg-7">
					<div class="heading__description--wrapper">
						<h1 class="heading-3">
							Book this
							{data.model_manufacturer}
							{data.model_name}
						</h1>
						<div class="vehicle__card--text-wrapper mb-ms">
							<div class="vehicle__number primary heading-5 py-xs">
								{data.reg_no.toUpperCase()}
							</div>
							<div class="vehicle__bound">
								{data.vehicle_location}, {data.vehicle_city}
							</div>
						</div>
					</div>
					<form action="#" on:submit|preventDefault={handleSubmit}>
						<div class="row">
							<div class="col-lg-5">
								<div class="form-group">
									<label for="booking_start_date">Booking Start Date</label>
									<input
										type="date"
										class="form-control"
										name="booking_start_date"
										min={attributes1.min}
										{...attributes2}
										bind:value={booking_start_date}
										on:change={handleResetEnd}
									/>
								</div>
							</div>
							<div class="col-lg-5">
								<div class="form-group">
									<label for="booking_end_date">Booking End Date</label>
									<input
										type="date"
										class="form-control"
										name="booking_end_date"
										min={later}
										{...attributes2}
										bind:value={booking_end_date}
									/>
								</div>
							</div>
							<div class="col-lg-3 d-none">
								<div class="form-group">
									<label for="duration">Duration</label>
									<input
										type="number"
										class="form-control"
										name="duration"
										readonly
										disabled
										bind:value={duration}
									/>
								</div>
							</div>
							<div class="col-lg-3 py-sm">
								<div class="label mb-1">Duration</div>
								<h3 class="heading-4">
									{duration} Days
								</h3>
							</div>
							<div class="col-lg-6 py-sm">
								<div class="label mb-1">Total Price</div>
								<h3 class="heading-3 primary">
									Rs.{data.vehicle_daily_price * duration}
								</h3>
							</div>
							<div class="col-lg-5">
								<div class="form-group">
									<label for="agreement">
										<input type="checkbox" name="agreement" id="agreement" {...attributes2} />
										I agree to follow the terms & conditions.
									</label>
								</div>
							</div>
							<div class="col-lg-12">
								<div class="button--wrapper fl-row gap-2 py-ms">
									<button class="btn btn-global btn--primary">Book Now</button>
								</div>
							</div>
						</div>
					</form>
				</div>
				<div class="col-lg-4">
					<div class="vehicle__information--wrapper">
						<div class="vehicle__cover--wrapper">
							<img src={data.vehicle_image} alt={data.vehicle_name} />
						</div>
					</div>
					<div class="vehicle__card--spec-grid py-xs">
						<div class="spec-group group-row">
							<div class="spec-title">Color:</div>
							<div class="spec-value">
								<div class="color-value">
									<div class="color-circle" style="--color: #{data.color_code}" />
									{data.color_name}
								</div>
							</div>
						</div>
						<div class="spec-group group-row">
							<div class="spec-title">Seats <i class="ti ti-users" /></div>
							<div class="spec-value">{data.seats} Seats</div>
						</div>
						<div class="spec-group group-row">
							<div class="spec-title">Transmission <i class="ti ti-hexagon" /></div>
							<div class="spec-value">{data.transmission}</div>
						</div>
						<div class="spec-group group-row">
							<div class="spec-title">Mileage <i class="ti ti-hexagon" /></div>
							<div class="spec-value">{data.mileage}</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</section>
{:else}
	{#await submission}
		Submitting...
	{:then res}
		<section class="booking__result--section py-lg">
			<div class="con">
				<div class="row justify-content-center align-items-stretch">
					<div class="col-lg-6">
						<div class="card confirmation__card">
							<h2 class="confirmation--title mb-sm">Your Booking has been submitted</h2>
							<div class="fl-row fl-wrap gap-2">
								<div class="info--wrapper">
									<div class="info--label">Booking ID</div>
									<div class="info--value">{res.main.id}</div>
								</div>
								<div class="info--wrapper">
									<div class="info--label">Booking Date</div>
									<div class="info--value">
										{moment(res.main.creation_date).format('YYYY-MM-DD')}
									</div>
								</div>
								<div class="info--wrapper">
									<div class="info--label">Booking Start Date</div>
									<div class="info--value">{res.main.booking_start_date}</div>
								</div>
								<div class="info--wrapper">
									<div class="info--label">Booking End Date</div>
									<div class="info--value">{res.main.booking_end_date}</div>
								</div>
								<div class="info--wrapper">
									<div class="info--label">Duration</div>
									<div class="info--value">
										<h3 class="heading-">{res.main.booking_total_days}</h3>
									</div>
								</div>
								<div class="info--wrapper">
									<div class="info--label">Price of Booking</div>
									<div class="info--value"><h3 class="heading-">Rs. {res.main.total_cost}</h3></div>
								</div>
								<div class="button--wrapper">
									<a href="/main/bookings/" class="btn btn-global btn--primary"
										>View Booking Details</a
									>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</section>
	{/await}
{/if}
