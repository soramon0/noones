<script>
  import { createEventDispatcher } from "svelte";

  export let tabs = [];
  export let tabName = tabs[0].name || "";
  const currentTabStyles = "text-black border-b-2 border-black";

  const dispatch = createEventDispatcher();

  const setTab = newTab => {
    tabName = newTab;
    dispatch("change", tabName);
  };
</script>

<div class="px-4 my-2 ml-4 border-b whitespace-no-wrap sm:ml-0" data-simplebar>
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
