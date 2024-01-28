<script lang="ts">
	import { variables } from '$lib/utils/constants';
	import { locations } from '$lib/store/locationStore';

	import { userData } from '$lib/store/userStore';
	import { logOutUser } from '$lib/utils/requestUtils';
	import { onMount } from 'svelte';

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

<header class="admin__header">
	<nav class="admin__nav rt-content-mar">
		<div class="admin__nav--content">
			<ul class="bread-crumbs">
				<li class="bread-crumb-item">ADMIN</li>
				<!-- <li class="bread-crumb-item">
					<a href="#" class="bread-crumb-link">Home</a>
				</li> -->
				<!-- <li class="bread-crumb-item">
					<div class="section__selection" data-toggle-parent>
						<button class="section__select--button" data-toggle-list>
							Courses Section
							<span class="section__select--button-icon">
								<span class="material-symbols-rounded">expand_more</span>
							</span>
						</button>
						<div class="section__wrapper">
							<div class="section__list">
								<a class="section__link" href="">
									<span class="section__link--label">Hero Section</span>
								</a>
								<a class="section__link" href="">
									<span class="section__link--label"> Courses Section</span>
								</a>
								<a class="section__link" href="">
									<span class="section__link--label"> Who We Are Section</span>
								</a>
								<a class="section__link" href="">
									<span class="section__link--label"> University Section</span>
								</a>
								<a class="section__link" href="">
									<span class="section__link--label"> Extended Education Section</span>
								</a>
								<a class="section__link" href="">
									<span class="section__link--label"> Create Inovate Section</span>
								</a>
								<a class="section__link" href="">
									<span class="section__link--label"> Partners Section</span>
								</a>
								<a class="section__link" href="">
									<span class="section__link--label"> Testimonials Section</span>
								</a>
								<a class="section__link" href="">
									<span class="section__link--label"> Life at Softwarica</span>
								</a>
								<a class="section__link" href="">
									<span class="section__link--label"> Blogs Sections</span>
								</a>
								<a class="section__link" href="">
									<span class="section__link--label"> News & Announcements</span>
								</a>
								<a class="section__link" href="">
									<span class="section__link--label"> Contact Information</span>
								</a>
							</div>
						</div>
					</div>
				</li> -->
			</ul>
			<div class="admin__nav--rt--wrapper">
				{#if !$userData.phone_number}
					<div class="button-wrapper fl-row gap-2 al-center">
						<a class="btn btn--grey" href="/register">Register</a>
						<a class="btn btn--primary" href="/login">Login</a>
					</div>
				{:else}
					<button class="icon--button" on:click={logOutUser}>
						<div class="user--icon btn-icon">
							<span class="material-symbols-rounded"> logout </span>
						</div>
						<div class="user--label btn-label">Logout</div>
					</button>
					<a
						class="icon--button user--wrapper"
						href="/user/{$userData.phone_number}-{$userData.id}"
					>
						<div class="btn-icon user--icon">
							<span class="material-symbols-rounded"> face </span>
						</div>
						<div class="btn-label user--label">{$userData.phone_number}</div>
					</a>
				{/if}
			</div>
		</div>
	</nav>
</header>
