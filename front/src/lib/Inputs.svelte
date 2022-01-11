<script>
	export let birth;
	export let sex;
	export let countries;
	export let country;
</script>

<div>
	<label for="birth-date">Birth:</label>
	<input id="birth-date" type="date" bind:value={birth} />
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
