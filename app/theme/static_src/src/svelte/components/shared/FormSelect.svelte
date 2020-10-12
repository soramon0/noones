<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { fade } from 'svelte/transition';

	const dispatch = createEventDispatcher();
	export let label: string;
	export let value: string;
	export let name: string;
	export let optionText: string;
	export let optionValue: string;
	export let selectOptions = [];
	export let errors = [];

	$: isErrorsEmpty = !errors || errors.length === 0;

	const valueChanged = (e: Event) => {
		const { options, selectedIndex } = e.target as HTMLSelectElement;
		const countryName = options[selectedIndex].text;
		dispatch('valueChanged', { name, value: countryName });
	};
</script>

<label for={name} class="block my-1 text-sm text-gray-700 font-semibold">
	{label}
</label>
<select id={name} class="form-select" bind:value on:blur={valueChanged}>
	{#each selectOptions as option}
		{#if option[optionText] === value}
			<option value={option[optionValue]} selected>{option[optionText]}</option>
		{:else}
			<option value={option[optionValue]}>{option[optionText]}</option>
		{/if}
	{/each}
</select>

{#if !isErrorsEmpty}
	<div transition:fade>
		{#each errors as error}
			<p class="text-sm my-1 text-red-400">{error}</p>
		{/each}
	</div>
{/if}
