<script lang="ts">
	

	import { notificationData } from '$lib/store/notificationStore';

	import '../../node_modules/bootstrap/dist/css/bootstrap.min.css';
	import { fly } from 'svelte/transition';

	// onMount(async () => {
	// 	if (browserGet('refreshToken')) {
	// 		const [response, errs] = await getCurrentUser(
	// 			fetch,
	// 			`${variables.BASE_API_URI}/token/refresh/`,
	// 			`${variables.BASE_API_URI}/user/`
	// 		);
	// 		if (errs.length <= 0) {
	// 			userData.set(response);
	// 		}
	// 	}
	// });
</script>

<svelte:head>
	<link
		rel="stylesheet"
		href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
	/>
</svelte:head>

{#if $notificationData}
	<p
		class="notification"
		id="notification"
		in:fly={{ y: -100, duration: 500, delay: 500 }}
		out:fly={{ y: 100, duration: 500 }}
	>
		{$notificationData}
	</p>
{/if}
<main>
	<slot />
</main>
