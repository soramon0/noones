<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { fade } from 'svelte/transition';

  const dispatch = createEventDispatcher();
  export let value: string | number = '';
  export let type = 'text';
  export let name: string;
  export let label: string | undefined;
  export let errors = [];
  export let selectOptions = [];
  let selected = value;
  $: isErrorsEmpty = !errors || errors.length === 0;

  const valueChanged = (e) => {
    if (type === 'select') {
      dispatch('valueChanged', { name, value: selected });
    } else {
      value = e.target.value;
      value = type === 'number' ? +value : value;
      dispatch('valueChanged', { name, value });
    }
  };
</script>

<label for={name} class="block my-1 text-sm text-gray-700 font-semibold">
  {label}
</label>

{#if type === 'textarea'}
  <textarea
    id={name}
    {value}
    on:change={valueChanged}
    class="form-textarea h-32 w-full text-gray-800 font-mono transition-colors
    duration-300 ease-in-out {!isErrorsEmpty ? 'border border-red-500' : ''}" />
{:else if type === 'select'}
  <select class="form-select" bind:value={selected} on:blur={valueChanged}>
    {#each selectOptions as option}
      <option value={option}>{option.toUpperCase()}</option>
    {/each}
  </select>
{:else}
  <input
    id={name}
    {type}
    {value}
    step={type === 'number' ? '.01' : null}
    on:change={valueChanged}
    class="form-input text-gray-800 font-mono transition-colors duration-300
    ease-in-out {!isErrorsEmpty ? 'border border-red-500' : ''}" />
{/if}

{#if !isErrorsEmpty}
  <div transition:fade>
    {#each errors as error}
      <p class="text-sm my-1 text-red-400">{error}</p>
    {/each}
  </div>
{/if}
