<script lang="ts">
  import { onMount } from 'svelte';
  import { fly } from 'svelte/transition';
  import { fade } from 'svelte/transition';
  import { UserStore } from './store/index';
  import Navbar from './components/layout/Navbar.svelte';
  import Sidebar from './components/layout/Sidebar.svelte';
  import General from './components/General/General.svelte';
  import Measures from './components/Measures/Measures.svelte';
  import Photos from './components/Photos/Photos.svelte';
  import Settings from './components/Settings/Settings.svelte';
  import Spinner from './components/shared/Spinner.svelte';

  let promise = UserStore.populate();

  let tab = parseInt(localStorage.getItem('current_tab'), 10) || 0;

  // Subscribe to the store
  $: userData = $UserStore;

  // check if there's a tab and
  // tab is not greater than the pages we have
  if (!tab || tab > 3) tab = 0;

  const changeTab = ({ detail }) => {
    tab = detail;
    // Persist the current tab
    localStorage.setItem('current_tab', JSON.stringify(detail));
  };
</script>

{#await promise}
  <div class="h-full flex justify-center items-center">
    <Spinner />
  </div>
{:then _}
  <div class="relative h-screen" transition:fade={{ duration: 600 }}>
    <!-- Top Menu -->
    <Navbar
      profilePicture={userData.profilePicture}
      modelId={userData.model.id}
      fullname={`${userData.model.first_name} ${userData.model.last_name}`} />

    <div class="min-h-full flex bg-gray-100">

      <Sidebar on:changeTab={changeTab} />

      <main class="w-full mb-4 px-4 py-2 sm:mt-4">
        {#if userData.errors.detail}
          <div
            transition:fly={{ x: -200, duration: 500 }}
            class="px-4 py-2 rounded bg-red-400 text-white">
            <p>{userData.errors.detail}</p>
          </div>
        {/if}

        {#if tab === 0}
          <div in:fly={{ x: 200, duration: 200 }} out:fade={{ duration: 100 }}>
            <General model={userData.model} errors={userData.errors} />
          </div>
        {:else if tab === 1}
          <div in:fly={{ x: 200, duration: 200 }} out:fade={{ duration: 100 }}>
            <Measures measures={userData.measures} />
          </div>
        {:else if tab === 2}
          <div in:fly={{ x: 200, duration: 200 }} out:fade={{ duration: 100 }}>
            <Photos
              profilePicture={userData.profilePicture}
              coverPicture={userData.coverPicture} />
          </div>
        {:else if tab === 3}
          <div in:fly={{ x: 200, duration: 200 }} out:fade={{ duration: 100 }}>
            <Settings email={userData.email} />
          </div>
        {/if}
      </main>
    </div>
  </div>
{:catch error}
  <div class="h-full text-center mt-10">
    <p class="text-lg">Something went wrong! Please try again later.</p>
    <p>Status: {error.status}</p>
  </div>
{/await}
