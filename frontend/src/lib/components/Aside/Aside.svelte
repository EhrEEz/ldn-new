<script lang="ts">
	import logo from './ldn-logo.svg';
</script>

<nav class="main__aside">
	<div id="navLogoWrapper" class="main__aside--logo">
		<img src={logo} alt="" />
	</div>
	<ul class="main__aside--list">
		<li class="main__aside--item">
			<a href="/seller" class="main__aside--link">
				<span class="main__aside--icon">
					<span class="material-symbols-rounded"> dashboard </span>
				</span>
				<span class="main__aside--label">Dashboard</span>
			</a>
		</li>
		<li class="main__aside--item">
			<a href="/" class="main__aside--link">
				<span class="main__aside--icon">
					<span class="material-symbols-rounded"> home </span>
				</span>
				<span class="main__aside--label">Home</span>
			</a>
		</li>
		<li class="main__aside--item" data-toggle-parent="">
			<button class="main__aside--link sub__link" data-toggle-list="">
				<span class="main__aside--icon">
					<span class="material-symbols-rounded"> account_balance </span>
				</span>
				<span class="main__aside--label">About</span>
			</button>
			<ul class="main__aside--sub--list">
				<li class="main__aside--sub--item active">
					<a href="#" class="main__aside--sub--link">About Us </a>
				</li>
				<li class="main__aside--sub--item inner active">
					<a href="#" class="main__aside--sub--link">About Us </a>
				</li>
				<li class="main__aside--sub--item inner">
					<a href="#" class="main__aside--sub--link">About Us </a>
				</li>
				<li class="main__aside--sub--item">
					<a href="#" class="main__aside--sub--link">Coventry University</a>
				</li>
				<li class="main__aside--sub--item">
					<a href="#" class="main__aside--sub--link">Message from Director</a>
				</li>
			</ul>
		</li>
		<li class="main__aside--item">
			<a href="#" class="main__aside--link">
				<span class="main__aside--icon">
					<span class="material-symbols-rounded"> book </span>
				</span>
				<span class="main__aside--label">Courses</span>
			</a>
		</li>
		<li class="main__aside--item">
			<a href="#" class="main__aside--link">
				<span class="main__aside--icon">
					<span class="material-symbols-rounded"> group </span>
				</span>
				<span class="main__aside--label">Students Center</span>
			</a>
		</li>
		<li class="main__aside--item">
			<a href="#" class="main__aside--link">
				<span class="main__aside--icon">
					<span class="material-symbols-rounded"> contacts </span>
				</span>
				<span class="main__aside--label">Contact</span>
			</a>
		</li>
	</ul>
	<div class="main__aside--footer">
		<div class="muted regular-10">From Capital Eye Nepal</div>
	</div>
</nav>
