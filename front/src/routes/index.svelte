<script>
	import { dev } from '$app/env';
	import Clock from '$lib/Clock.svelte';
	import Inputs from '$lib/Inputs.svelte';
	import { onMount } from 'svelte';

	let apiUrl = dev ? 'http://localhost:8000' : 'https://deathclock.fly.dev';

	let currentAge = 40;
	let country = 'France';
	let sex = 'Female';
	let birth = '1981-07-13';
	let countries = [];
	$: birthNumber = Date.parse(birth);
	let remaining = 40;
	$: getRemaining(country, sex, currentAge).then((rem) => (remaining = rem));
	$: getCountries().then((data) => (countries = data));

	function ageFromBirth(birthNb) {
		return (Date.now() - birthNb) / (1000 * 60 * 60 * 24 * 365);
	}

	function updateAge() {
		currentAge = ageFromBirth(birthNumber);
		setTimeout(updateAge, 1000);
	}

	async function getCountries() {
		const res = await fetch(`${apiUrl}/countries/`);
		const countries = await res.json();

		if (res.ok) {
			return countries;
		} else {
			throw new Error(countries);
		}
	}

	async function getRemaining(country, sex, currentAge) {
		const res = await fetch(
			`${apiUrl}/remaining/?country=${country}&sex=${sex}&current=${currentAge}&year=2019`
		);
		const remaining = await res.json();

		if (res.ok) {
			return remaining;
		} else {
			throw new Error(remaining);
		}
	}

	onMount(() => {
		updateAge();
	});
</script>

<main>
	<div class="inputs">
		<Inputs bind:birth bind:sex {countries} bind:country />
	</div>

	<div class="hourglass" />

	<div class="outputs">
		<div>
			<p>Current Age: {currentAge.toFixed(1)} years</p>
			<p>Remaining life expectancy: <strong>{remaining.toFixed(1)}</strong> years.</p>
			<p>
				That is
				<strong>{((100 * remaining) / (currentAge + remaining)).toFixed(1)}%</strong> of your life remaining.
			</p>
		</div>
		<p>
			<strong>
				{(remaining * 24 * 60 * 60 * 365).toLocaleString('en-US')}
			</strong> seconds remaining.
		</p>
	</div>
	<div class="clock"><Clock /></div>
	<footer>
		<div class="source">
			<p>
				<a
					href="https://www.who.int/data/gho/data/indicators/indicator-details/GHO/gho-ghe-life-tables-by-country"
					target="_blank">Source: World Health Organisation</a
				>
			</p>
		</div>
	</footer>
</main>

<style>
	* {
		margin: 0;
		padding: 0;
	}

	main {
		background-color: black;
	}

	footer {
		background-color: steelblue;
		color: white;
		padding: 10px;
	}

	footer a {
		color: white;
	}

	footer a:hover {
		color: orange;
	}

	footer a:focus {
		color: yellow;
	}

	.source {
		margin: 0 auto;
		max-width: 500px;
		text-align: center;
	}

	.clock {
		max-width: 500px;
		margin: 0 auto;
	}

	.outputs {
		margin: 10px auto;
		max-width: 500px;
		text-align: center;
		padding: 10px;
		color: white;
	}

	p {
		font-size: 20px;
		margin: 8px;
		font-family: sans-serif;
	}

	.inputs {
		background-color: steelblue;
		color: white;
		font-size: 20px;
	}
</style>
