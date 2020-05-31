<script>
  import { createEventDispatcher } from "svelte";

  export let currentTab = 0;
  export let tabs = [];

  const dispatch = createEventDispatcher();
  const currentTabStyles = "text-black border-b-2 border-black";

  const setTab = newTab => {
    currentTab = newTab;
    dispatch("change", currentTab);
  };
</script>

<div class="flex px-4 my-2 ml-4 space-x-6 border-b sm:ml-0">
  {#each tabs as tab, i}
    {#if tab.show}
      <button
        class="px-2 {i === currentTab ? currentTabStyles : 'text-gray-500'}"
        on:click={() => setTab(i)}>
        {tab.name}
      </button>
    {/if}
  {/each}
</div>
