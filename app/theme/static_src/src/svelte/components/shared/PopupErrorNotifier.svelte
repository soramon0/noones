<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { fade, scale } from 'svelte/transition';
  import CancelButton from './CancelButton.svelte';

  export let errors: any = {};
  export let errorKey: string | null = null;

  const dispatch = createEventDispatcher();

  const hideErrorNotifier = () => {
    errors = {};
    dispatch('clearErrors');
  };
</script>

{#if errors.hasOwnProperty(errorKey)}
  <div
    transition:scale
    class="p-4 w-11/12 fixed z-40 bg-white border-l-2 border-red-500 rounded-lg
    shadow-md sm:w-1/2">
    {#each errors[errorKey] as err}
      <p class="text-gray-600">{err}</p>
    {/each}
    <div class="mt-2 text-right">
      <CancelButton text="Close" on:click={hideErrorNotifier} />
    </div>
  </div>
{/if}
