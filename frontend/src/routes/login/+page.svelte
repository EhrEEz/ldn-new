<script lang="ts">
	import { notificationData } from '$lib/store/notificationStore';
	import { post, browserSet, browserGet } from '$lib/utils/requestUtils';
	import { goto } from '$app/navigation';
	import { variables } from '$lib/utils/constants';
	import { fly } from 'svelte/transition';
	import '../../sass/app.scss';
	import type { UserResponse } from '$lib/interfaces/user.interface';
	import type { CustomError } from '$lib/interfaces/error.interface';
	import { changeText } from '$lib/helpers/buttonText';
	import { userData } from '$lib/store/userStore';
	import { onMount } from 'svelte';
	import { get } from 'svelte/store';
	import { error } from '@sveltejs/kit';

	let phone_number = '',
		password = '',
		errors: Array<CustomError>;

	let loginBtn;

	function showErrors(errors: Array<string>) {
		loginBtn.innerText = 'Login';
		notificationData.update(() => 'Login failed...');
	}

	const handleLogin = async () => {
		if (browserGet('refreshToken')) {
			localStorage.removeItem('refreshToken');
		}
		const [jsonRes, rers] = await post(fetch, `${variables.BASE_API_URI}/login/`, {
			user: {
				phone_number: phone_number,
				password: password
			}
		});

		const response: UserResponse = jsonRes;
		const err = jsonRes.user.error ? jsonRes.user.error : [];
		if (err.length > 0) {
			errors = err;
			showErrors(errors);
		} else if (response.user.tokens) {
			if (response.user.tokens && response.user.tokens.refresh) {
				browserSet('refreshToken', response.user.tokens.refresh);
			}
			notificationData.update(() => 'Login successful...');
			await goto('/');
		}
	};
	onMount(() => {
		const user = get(userData);
		if (user.id) {
			goto(`/user/${user.id}`);
		}
	});
</script>

<svelte:head>
	<title>LDN Login</title>
</svelte:head>
<div class="login--main">
	<div
		class="center-block"
		in:fly={{ y: -100, duration: 500, delay: 500 }}
		out:fly={{ duration: 500 }}
	>
		<div class="login-wrapper p-ms">
			<h1 class="heading-4">Login to LDN</h1>
			<form on:submit|preventDefault={handleLogin} class="login-form py-sm">
				{#if errors}
					<div class="error-messages">
						{#each errors as error}
							<div>{error}</div>
						{/each}
					</div>
				{/if}
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
				<!-- <div class="form-group">
					<a href="#" class="ar-link fp-link">Forgot Password?</a>
				</div> -->
				<!-- <div class="form-group">
					<label for="remember">
						<input type="checkbox" name="remember" id="remember" class="checkbox" />
						Remember Me</label
					>
				</div> -->
				<div class="button-group fl-row al-center jc-center gap-2">
					<a href="/register" class="btn btn-global btn--grey">Get started</a>
					<button
						class="btn btn-global btn--primary"
						type="submit"
						on:click={(e) => changeText(e, 'Signing in...')}
						bind:this={loginBtn}>Login</button
					>
				</div>
			</form>
		</div>
	</div>
</div>

<style>
	.login--main {
		min-height: 100vh;
		min-width: 100vw;
		background-color: #f7f7f7;
	}
</style>
