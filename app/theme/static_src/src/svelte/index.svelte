<script>
  import { onMount } from 'svelte';
  import { fade } from "svelte/transition";
  import { createModelStore } from "./store/main"
  import Navbar from "./components/layout/Navbar";
  import General from "./components/General";
  import Measures from "./components/Measures";
  import Photos from "./components/Photos";
  import Settings from "./components/Settings";
  import Spinner from "./components/shared/Spinner";

  let modelStore;
  let tab = parseInt(localStorage.getItem('current_tab'));

  // check if there's a tab and 
  // tab is not greater than the pages we have
  if (!tab || tab > 3) tab = 0;

  const changeTab = ({ detail }) => {
    tab = detail;
    // Persist the current tab
    localStorage.setItem('current_tab', JSON.stringify(detail))
  };

  onMount(async () => {
    modelStore = await createModelStore()
  })
  
</script>

{#if modelStore}
  <div transition:fade={{duration: 600 }}>
    <Navbar on:changeTab={changeTab} userId={$modelStore.id} />

    {#if tab === 0}
      <General bind:modelStore />
    {:else if tab === 1}
      <Measures />
    {:else if tab === 2}
      <Photos />
    {:else if tab === 3}
      <Settings bind:modelStore />
    {/if}
  </div>
{:else}
  <Spinner />
{/if}
