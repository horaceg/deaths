<script>
	import { onMount } from 'svelte';
	import Clock from '$lib/Clock.svelte';
	import Inputs from '$lib/Inputs.svelte';

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
		const res = await fetch(`https://deathclock.fly.dev/countries/`);
		const countries = await res.json();

		if (res.ok) {
			return countries;
		} else {
			throw new Error(countries);
		}
	}

	async function getRemaining(country, sex, currentAge) {
		const res = await fetch(
			`https://deathclock.fly.dev/remaining/?country=${country}&sex=${sex}&current=${currentAge}&year=2019`
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

<Inputs bind:birth bind:sex {countries} bind:country />

<div>
	<p>Current Age: {currentAge.toFixed(1)} years</p>
	Remaining life expectancy:<strong>{remaining.toFixed(1)}</strong> years, that is
	<strong>{((100 * remaining) / (currentAge + remaining)).toFixed(1)}%</strong> of your life remaining.
</div>
<div class="outputs">
	<div class="clock"><Clock /></div>
	<strong>
		{(remaining * 24 * 60 * 60 * 365).toLocaleString('en-US')}
	</strong> seconds remaining.
</div>

<style>
	.clock {
		height: 25%;
		width: 25%;
	}

	.outputs {
		display: flexbox;
	}
</style>
