<script lang="ts">
	import { fly } from 'svelte/transition';
	import { goto } from '$app/navigation';
	import { variables } from '$lib/utils/constants';
	import { notificationData } from '$lib/store/notificationStore';
	import { post } from '$lib/utils/requestUtils';
	import type { CustomError } from '$lib/interfaces/error.interface';
	import type { UserResponse } from '$lib/interfaces/user.interface';
	import { changeText } from '$lib/helpers/buttonText';
	import '../../sass/app.scss';
	import { redirect } from '@sveltejs/kit';

	let email: string,
		fullName: string,
		bio: string,
		phone_number: string,
		password: string,
		confirmPassword: string,
		errors: object;
		const submitForm = async () => {
		const [jsonRes, err] = await post(fetch, `${variables.BASE_API_URI}/register/`, {
			user: {
				email: email,
				phone_number: phone_number,
				password: password,
				bio: bio,
				full_name: fullName
			}
		});
		const response: UserResponse = jsonRes;

		if (err) {
			errors = err;
		} else if (response.user) {
			notificationData.update(() => 'Registration successful. Login now...');
			await redirect(301, '/login');
		}
	};
	const passwordConfirm = () => (password !== confirmPassword ? false : true);
</script>

<svelte:head>
	<title>LDN Login</title>
</svelte:head>

<div class="login--main">
	<div
		class="center-block large"
		in:fly={{ y: -100, duration: 500, delay: 500 }}
		out:fly={{ duration: 500 }}
	>
		<div class="login-wrapper p-ms">
			<h1 class="heading-4">Register to LDN</h1>

			<form on:submit|preventDefault={submitForm} class="login-form py-sm">
				<div class="row">
					<div class="col-5">
						<div
							class="form-group {typeof errors === 'object' && 'phone_number' in errors
								? 'error'
								: ''}"
						>
							<label for="phoneNumber">Phone Number</label>
							<input
								bind:value={phone_number}
								id="phoneNumber"
								type="text"
								aria-label="Phone Number"
								placeholder="Phone Number"
								class="form-control"
								required
							/>
							{#if typeof errors === 'object' && 'phone_number' in errors}
								<small class="error-text">
									{#each errors.phone_number as err}
										{err} <br />
									{/each}
								</small>
							{/if}
						</div>
					</div>
					<div class="col-5">
						<div class="form-group">
							<label for="fullName">Full Name</label>
							<input
								bind:value={fullName}
								type="text"
								class="form-control"
								id="fullName"
								aria-label="Full name"
								placeholder="Full name"
								required
							/>
							{#if typeof errors === 'object' && 'full_name' in errors}
								<small class="error-text">
									{#each errors.full_name as err}
										{err} <br />
									{/each}
								</small>
							{/if}
						</div>
					</div>
					<div class="col-8">
						<div class="form-group">
							<label for="email">Email Address</label>
							<input
								bind:value={email}
								type="email"
								class="form-control"
								id="email"
								aria-label="Email address"
								placeholder="Email address"
								required
							/>
							{#if typeof errors === 'object' && 'email' in errors}
								<small class="error-text">
									{#each errors.email as err}
										{err} <br />
									{/each}
								</small>
							{/if}
						</div>
					</div>

					<div class="col-8">
						<div class="form-group">
							<label for="bio">Bio</label>
							<textarea
								bind:value={bio}
								class="form-control"
								id="bio"
								rows="5"
								aria-label="Brief bio"
								placeholder="Tell us about yourself..."
								required
							/>
							{#if typeof errors === 'object' && 'email' in errors}
								<small class="error-text">
									{#each errors.bio as err}
										{err} <br />
									{/each}
								</small>
							{/if}
						</div>
					</div>
					<div class="col-5">
						<div class="form-group">
							<label for="password">Password</label>
							<input
								bind:value={password}
								id="password"
								type="password"
								class="form-control"
								name="password"
								aria-label="password"
								placeholder="password"
								required
							/>
						</div>
					</div>
					<div class="col-5">
						<div class="form-group">
							<label for="confirmPassword">Password</label>
							<input
								bind:value={confirmPassword}
								type="password"
								name="confirmPassword"
								class="form-control"
								id="confirmPassword"
								aria-label="Confirm password"
								placeholder="Confirm password"
								required
							/>
						</div>
					</div>
				</div>

				<div class="button-group fl-row al-center jc-center gap-2">
					<a class="btn btn-global btn--secondary" href="/login"> Login </a>
					{#if confirmPassword}
						<button
							class="btn btn-global btn--primary"
							type="submit"
							on:click={(e) => changeText(e, 'Registering...')}
						>
							Register
						</button>
					{:else}
						<button class="btn btn-global btn--primary" type="submit" disabled>Register</button>
					{/if}
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
