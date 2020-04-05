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
  let loaded = false;

  // Subscribe to the store
  $: userData = $userStore;

  // check if there's a tab and
  // tab is not greater than the pages we have
  if (!tab || tab > 3) tab = 0;

  const changeTab = ({ detail }) => {
    tab = detail;
    // Persist the current tab
    localStorage.setItem("current_tab", JSON.stringify(detail));
  };

  onMount(async () => {
    await userStore.populate();
    loaded = true;
  });

  $: console.log(userData);
</script>

{#if loaded}
  {#if userData.errors.detail}
    <div
      transition:fly={{ x: -200, duration: 500 }}
      class="px-4 py-6 bg-red-500 text-white">
      <p>{userData.errors.detail}</p>
    </div>
  {/if}

  <div class="relative flex" transition:fade={{ duration: 600 }}>
    <Navbar on:changeTab={changeTab}>
      <Avatar profile={userData.profile} id={userData.model.id} />
    </Navbar>

    <div class="px-4 mt-4 w-full mb-8">
      {#if tab === 0}
        <div in:fly={{ x: -200, duration: 400 }} out:fade={{ duration: 100 }}>
          <General model={userData.model} errors={userData.errors} />
        </div>
      {:else if tab === 1}
        <div in:fly={{ x: -200, duration: 400 }} out:fade={{ duration: 100 }}>
          <Measures measures={userData.measures} errors={userData.errors} />
        </div>
      {:else if tab === 2}
        <div in:fly={{ x: -200, duration: 400 }} out:fade={{ duration: 100 }}>
          <Photos profile={userData.profile} cover={userData.cover} />
        </div>
      {:else if tab === 3}
        <div in:fly={{ x: -200, duration: 400 }} out:fade={{ duration: 100 }}>
          <Settings email={userData.email} />
        </div>
      {/if}
    </div>
  </div>
{:else}
  <Spinner />
{/if}
