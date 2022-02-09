<script>
	import Clock from '$lib/Clock.svelte';
	import Inputs from '$lib/Inputs.svelte';
	import * as aq from 'arquero';
	import { op } from 'arquero';
	import { onMount } from 'svelte';

	let expectancy = null;
	let expectancy_localized = null;

	aq.loadArrow(`/expectancy.arrow`)
		.then((table) => {
			expectancy = table;
			// console.log(expectancy.print());
		})
		.catch((err) => console.log(err));

	let currentAge = 40;
	let country = 'France';
	let sex = 'Female';
	let birth = '1980-01-13';
	let countries = [country];
	$: birthNumber = Date.parse(birth);
	let remaining = 40;
	$: expectancy ? (remaining = getRemaining(expectancy_localized, currentAge)) : null;
	$: expectancy
		? (expectancy_localized = expectancy
				.filter(aq.escape((d) => (d.location == country) & (d.sex == sex) & (d.period[0] == 2019)))
				.derive({ mid: (d) => (d.lower + d.upper + 1) / 2 })
				.derive({
					lagged_remaining: op.lag('remaining'),
					lagged_mid: op.lag('mid'),
					lead_remaining: op.lead('remaining'),
					lead_mid: op.lead('mid')
				})
				.impute({ lagged_mid: () => 0 })
				.impute({ lead_mid: () => 150 }))
		: null;

	$: expectancy
		? (countries = expectancy.rollup({ c: op.array_agg_distinct('location') }).get('c', 0))
		: null;
	// $: (expectancy != null) & (country != null) ? console.log(remaining) : null;

	// $: console.log(expectancy_localized?.print(20));

	function ageFromBirth(birthNb) {
		return (Date.now() - birthNb) / (1000 * 60 * 60 * 24 * 365);
	}

	function updateAge() {
		currentAge = ageFromBirth(birthNumber);
		setTimeout(updateAge, 1000);
	}
	function interp(low_mid, up_mid, low_rem, up_rem) {
		let coef = (up_rem - low_rem) / (up_mid - low_mid);
		return low_rem + coef * (currentAge - low_mid);
	}
	function getRemaining(expectancy_localized, currentAge) {
		// console.log(currentAge);
		const basis = expectancy_localized.filter(
			aq.escape((d) => d.lower <= currentAge && d.upper + 1 > currentAge)
		);

		const obj = basis.reify().objects()[0];

		// console.log(obj);

		let interp_low = interp(obj.lagged_mid, obj.mid, obj.lagged_remaining, obj.remaining);

		let interp_up = interp(obj.mid, obj.lead_mid, obj.remaining, obj.lead_remaining);

		if (interp_low && isFinite(interp_up)) {
			return (interp_low + interp_up) / 2;
		} else if (isFinite(interp_up)) {
			return interp_up;
		} else if (interp_low) {
			return obj.lagged_remaining * Math.exp(-(currentAge - obj.lagged_mid) / 11);
		} else {
			throw new Error('Unknown');
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
		margin: 20px 0;
		align-items: center;
		display: flex;
		justify-content: center;
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
