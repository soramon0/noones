<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  type tabOptions = {
    name: string;
  };

  export let tabs: tabOptions[] = [];
  export let tabName: string = tabs[0].name || '';
  const currentTabStyles = 'text-black border-b-2 border-black';

  const dispatch = createEventDispatcher();

  const setTab = (newTab: string) => {
    tabName = newTab;
    dispatch('change', tabName);
  };
</script>

<div class="px-4 my-2 ml-4 whitespace-no-wrap sm:ml-0" data-simplebar>
  <div class="space-x-4">
    {#each tabs as tab}
      <button
        class="tab p-3 rounded-sm focus:outline-none focus:bg-gray-200
        hover:bg-gray-200 {tab.name === tabName ? currentTabStyles : 'text-gray-500'}"
        on:click={() => setTab(tab.name)}>
        {tab.name}
      </button>
    {/each}
  </div>
</div>
<slot />
