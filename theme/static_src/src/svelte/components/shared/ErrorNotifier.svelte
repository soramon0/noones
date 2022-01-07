<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { fade, fly } from 'svelte/transition';

  export let errors = {};
  export let errorKey: string | null = null;

  const dispatch = createEventDispatcher();

  const hideErrorNotifier = () => {
    errors = {};
    dispatch('clearErrors');
  };
</script>

{#if errors[errorKey] && errors[errorKey].length > 0}
  <div
    in:fly={{ x: -200, duration: 400 }}
    out:fade={{ duration: 400 }}
    class="p-3 mt-2 bg-red-400 border-l-4 border-red-500 rounded-sm relative
    sm:p-4">
    {#each errors[errorKey] as error}
      <p class="mr-5 text-xs text-white sm:text-sm md:text-base">{error}</p>
    {/each}
    <button
      class="absolute right-0 top-0 mt-2 mr-2"
      on:click={hideErrorNotifier}>
      <svg viewBox="0 0 20 20" class="w-8 h-8 fill-current text-white">
        <path
          d="M12.71,7.291c-0.15-0.15-0.393-0.15-0.542,0L10,9.458L7.833,7.291c-0.15-0.15-0.392-0.15-0.542,0c-0.149,0.149-0.149,0.392,0,0.541L9.458,10l-2.168,2.167c-0.149,0.15-0.149,0.393,0,0.542c0.15,0.149,0.392,0.149,0.542,0L10,10.542l2.168,2.167c0.149,0.149,0.392,0.149,0.542,0c0.148-0.149,0.148-0.392,0-0.542L10.542,10l2.168-2.168C12.858,7.683,12.858,7.44,12.71,7.291z
          M10,1.188c-4.867,0-8.812,3.946-8.812,8.812c0,4.867,3.945,8.812,8.812,8.812s8.812-3.945,8.812-8.812C18.812,5.133,14.867,1.188,10,1.188z
          M10,18.046c-4.444,0-8.046-3.603-8.046-8.046c0-4.444,3.603-8.046,8.046-8.046c4.443,0,8.046,3.602,8.046,8.046C18.046,14.443,14.443,18.046,10,18.046z" />
      </svg>
    </button>
  </div>
{/if}
