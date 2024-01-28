<script lang="ts">
	import logo from './ldn-logo.svg';
	import { variables } from '$lib/utils/constants';
	import { locations } from '$lib/store/locationStore';
	import { browserGet } from '$lib/utils/requestUtils';
	import { userData } from '$lib/store/userStore';
	import { logOutUser } from '$lib/utils/requestUtils';
	import { onMount } from 'svelte';
	import moment from 'moment';
	const now = moment().format('YYYY-MM-DD');
	$: later = moment(start_date, 'YYYY-MM-DD').add(1, 'd').format('YYYY-MM-DD');
	const attributes1 = { min: now };
	const attributes2 = { required: false };
	export let start_date;
	export let end_date;
	
	function handleResetEnd() {
		end_date = '';
	}
	let locationList: Array<any>;
	let locationPromise: Promise<any> = Promise.resolve([]);
	async function fetchLocations(): Promise<any[]> {
		const res = await self.fetch(`${variables.BASE_MAIN_URI}/vehicles/locations/`);
		if (res.ok) {
			return res.json();
		} else {
			throw new Error('Something went wrong');
		}
	}
	onMount(() => {
		locationPromise = fetchLocations();
		locationPromise.then((data) => {
			locations.set(data);
			locations.subscribe((value) => {
				locationList = value;
			});
		});
	});
</script>

<header>
	<nav class="nav nav__main">
		<div class="nav-logo-wrapper">
			<a href="/">
				<img src={logo} alt="" style="max-height:2rem;" />
			</a>
		</div>
		<div class="nav__search--wrapper">
			<div class="form-group select location">
				<i class="icon ti ti-map-pin" />
				<select name="location" id="location" class="form-control">
					{#await locationPromise}
						<option value="">Loading...</option>
					{:then}
						<option value="">Everywhere</option>
						{#each locationList as location}
							<option value={location.city}>{location.city}</option>
						{/each}
					{:catch}
						<option value="">Select Location</option>
					{/await}
					<!-- {#each locationList as location}
							<option value={location}>{location.toUpperCase()}</option>
						{/each} -->
				</select>
			</div>
			<div class="form-group">
				<input type="date" name="startDate" id="startDate" class="form-control"										min={attributes1.min}
				{...attributes2}
				bind:value={start_date}
				on:change={handleResetEnd} />
			</div>
			<div class="form-group">
				<input type="date" name="endDate" id="endDate" class="form-control" min={later}
				{...attributes2}
				bind:value={end_date} />
			</div>
			<div class="button-group">
				<button class="btn btn-global btn--primary">Search</button>
			</div>
		</div>
		<div class="nav__rt-wrapper fl-row gap-2 al-center">
			<div class="nav__notification-group notification-main">
				<a href="/main/bookings" class="btn btn-round-md btn--grey notification-base">
					<i class="ti ti-bell" />
				</a>
				<div class="notification-drop">
					<ul class="notification-list" />
				</div>
			</div>
			{#if browserGet('refreshToken')}
				<button class="btn btn-round-md btn--grey notification-base" on:click={logOutUser}>
					<i class="ti ti-logout" />
				</button>

				<a href="/user/{$userData.phone_number}-{$userData.id}">
					<div class="nav__user--group user__main dropdown-main">
						<div class="nav__user--dropdown user__base dropdown-base">
							<div class="user__base--image dropdown-base--image">
								<!-- <img src="images/user.png" alt="User" /> -->
							</div>
							<div class="user__base--text dropdown-base--text">{$userData.phone_number}</div>
							<div class="user__base--icon dropdown-base--icon">
								<i class="ti ti-chevron-down" />
							</div>
						</div>
						<!-- <div class="user__drop dropdown-drop active">
						<ul class="user__options dropdown-options">
							<li class="user__option--item dropdown-option--item">
								<a href="/" class="user__option--link dropdown-option--link">
									<span class="user__option--text dropdown-option--text">Settings</span>
									<span class="user__option--icon dropdown-option--icon"
										><i class="ti ti-settings" /></span
									>
								</a>
							</li>
							<li class="user__option--item dropdown-option--item">
								<a
									href="/"
									class="user__option--link dropdown-option--link"
									on:click={logOutUser}
								>
									<span class="user__option--text dropdown-option--text">Logout</span>
									<span class="user__option--icon dropdown-option--icon"
										><i class="ti ti-logout" /></span
									>
								</a>
							</li>
						</ul>
					</div> -->
					</div>
				</a>
			{:else}
				<div class="button-wrapper fl-row gap-2 al-center">
					<a class="btn btn-global btn--grey" href="/register">Register</a>
					<a class="btn btn-global btn--primary" href="/login">Login</a>
				</div>
			{/if}
		</div>
	</nav>
</header>
