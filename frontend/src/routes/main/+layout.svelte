<script lang="ts">
	import { userData } from '$lib/store/userStore';
	import { navigating } from '$app/stores';
	import { loading } from '$lib/store/loadingStore';
	import { notificationData } from '$lib/store/notificationStore';
	import { fly } from 'svelte/transition';
	import { afterUpdate, onMount } from 'svelte';

	import Header from '$lib/components/Header/Header.svelte';
	import Loader from '$lib/components/Loader/Loader.svelte';

	import '../../../node_modules/bootstrap/dist/css/bootstrap.min.css';
	import '../../sass/app.scss';
	$: loading.setNavigate(!!$navigating);
	$: loading.setLoading(!!$navigating, 'Loading, please wait...');

	import { getCurrentUser, browserGet } from '$lib/utils/requestUtils';
	import { variables } from '$lib/utils/constants';

	export let start_date, end_date;

	onMount(async () => {
		if (browserGet('refreshToken')) {
			const [response, errs] = await getCurrentUser(
				fetch,
				`${variables.BASE_API_URI}/token/refresh/`,
				`${variables.BASE_API_URI}/user/`
			);
			if (errs.length <= 0) {
				userData.set(response);
			}
		}
	});

	afterUpdate(async () => {
		const notifyEl = document.getElementById('notification') as HTMLElement;
		// const notifyEl = document.getElementsByClassName('notification');
		if (notifyEl && $notificationData !== '') {
			setTimeout(() => {
				notifyEl.classList.add('disappear');
				notificationData.set('');
			}, 3000);
		}
		if (browserGet('refreshToken')) {
			const [response, _] = await getCurrentUser(
				fetch,
				`${variables.BASE_API_URI}/token/refresh/`,
				`${variables.BASE_API_URI}/user/`
			);
			userData.update(() => response);
		}
	});
</script>

<svelte:head>
	<link
		rel="stylesheet"
		href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
	/>
</svelte:head>
<form method="get" action="/main">
	<Header start_date={start_date} end_date={end_date} />

	<Loader />
	<slot />
</form>
