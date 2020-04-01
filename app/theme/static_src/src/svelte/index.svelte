<script>
  import { onMount } from "svelte";
  import { fly } from "svelte/transition";
  import { fade } from "svelte/transition";
  import userStore from "./store/main";
  import Navbar from "./components/layout/Navbar";
  import Avatar from "./components/Avatar";
  import General from "./components/General";
  import Measures from "./components/Measures";
  import Photos from "./components/Photos";
  import Settings from "./components/Settings";
  import Spinner from "./components/shared/Spinner";

  let tab = parseInt(localStorage.getItem("current_tab"));

  // check if there's a tab and
  // tab is not greater than the pages we have
  if (!tab || tab > 3) tab = 0;

  const changeTab = ({ detail }) => {
    tab = detail;
    // Persist the current tab
    localStorage.setItem("current_tab", JSON.stringify(detail));
  };

  $: userData = $userStore;

  onMount(() => {
    userStore.populate();
  });
</script>

{#if userData}
  <div class="relative flex h-screen" transition:fade={{ duration: 600 }}>

    <Navbar on:changeTab={changeTab}>
      <Avatar model={userData.model} />
    </Navbar>

    <div class="px-4 mt-4 w-full">
      {#if tab === 0}
        <div in:fly={{ x: -200, duration: 400 }} out:fade={{ duration: 100 }}>
          <General model={userData.model} />
        </div>
      {:else if tab === 1}
        <div in:fly={{ x: -200, duration: 400 }} out:fade={{ duration: 100 }}>
          <Measures />
        </div>
      {:else if tab === 2}
        <div in:fly={{ x: -200, duration: 400 }} out:fade={{ duration: 100 }}>
          <Photos
            profile={userData.model.profilePicture}
            cover={userData.model.coverPicture} />
        </div>
      {:else if tab === 3}
        <div in:fly={{ x: -200, duration: 400 }} out:fade={{ duration: 100 }}>
          <Settings model={userData.model} />
        </div>
      {/if}
    </div>
  </div>
{:else}
  <Spinner />
{/if}
