<script lang="ts">
	import '../../sass/app.scss';

	import { notificationData } from '$lib/store/notificationStore';
	import { post, browserSet, browserGet } from '$lib/utils/requestUtils';
	import { goto } from '$app/navigation';
	import { variables } from '$lib/utils/constants';
	import { fly } from 'svelte/transition';

	import type { UserResponse } from '$lib/interfaces/user.interface';
	import type { CustomError } from '$lib/interfaces/error.interface';
	import { changeText } from '$lib/helpers/buttonText';

	/** @type {import('./$types').ActionData} */
	export let form;

	let phone_number = '',
		password = '',
		errors: Array<CustomError>;

	if (form) {
		if (!form.success) {
			errors = form.data;
			notificationData.update(() => `${errors[0]}`);
		}
	}
</script>

<svelte:head>
	<title>LDN Login</title>
</svelte:head>
<div
	class="center-block"
	in:fly={{ x: -100, duration: 500, delay: 500 }}
	out:fly={{ duration: 500 }}
>
	<div class="login-wrapper p-ms">
		<h1 class="heading-4">Login to LDN</h1>
		<form action="?/handleLogin" class="login-form py-sm" method="post">
			<div class="form-group">
				<label for="phoneNumber">Phone Number</label>
				<input
					bind:value={phone_number}
					name="phone_number"
					type="text"
					aria-label="Phone Number"
					placeholder="Phone Number"
					required
					class="form-control"
				/>
			</div>
			<div class="form-group">
				<label for="password">Password</label>
				<input
					bind:value={password}
					name="password"
					type="password"
					aria-label="password"
					placeholder="password"
					required
					class="form-control"
				/>
			</div>
			<div class="form-group">
				<!-- <a href="#" class="ar-link fp-link">Forgot Password?</a> -->
			</div>
			<div class="form-group">
				<label for="remember">
					<input type="checkbox" name="remember" id="remember" class="checkbox" />
					Remember Me</label
				>
			</div>
			<div class="button-group fl-row al-center jc-center gap-2">
				<a class="btn btn-global btn--secondary" href="/register">Get started</a>
				<button class="btn btn-global btn--primary">Login</button>
			</div>
		</form>
	</div>
</div>
