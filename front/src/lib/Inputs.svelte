<script>
	export let birth;
	export let sex;
	export let countries;
	export let country;
</script>

<div>
	<label for="birth-date">Birth:</label>
	<input
		id="birth-date"
		type="date"
		bind:value={birth}
		min="1900-01-01"
		max={new Date().toISOString().split('T')[0]}
	/>
</div>

<div>
	<label for="sex">Sex:</label>
	<select bind:value={sex}>
		<option value="Male">Male</option>
		<option value="Female">Female</option>
	</select>
</div>

<div>
	<label for="country-name">Country of birth:</label>
	<select name="country" id="country-name" bind:value={country}>
		{#each countries as cnt}
			<option value={cnt}>{cnt}</option>
		{/each}
	</select>
</div>
