<script>
  import { onMount } from "svelte";
  import photoStore from "../../store/photo";

  export let modelId;
  export let fullname = "";
  export let profilePicture;

  // Subscribe to the store
  $: photoData = $photoStore;

  let showPopup = false;

  onMount(() => {
    document.addEventListener("keyup", e => {
      if (e.key == "Escape") {
        showPopup = false;
      }
    });
  });

  const togglePopup = () => (showPopup = !showPopup);
</script>

<div
  class="h-16 px-4 flex items-center justify-between bg-white border-b shadow-sm">

  <div class="flex justify-center items-center">
    <div class="h-10">
      <a href="/">
        <img class="h-full" alt="logo" src="/static/icons/logo-noc.png" />
      </a>
    </div>

    <div class="ml-2 sm:ml-6">
      <a href="/models/" class="text-xs text-gray-800 px-2 sm:text-sm">
        Nos models
      </a>
      <a href="/contact/" class="text-xs text-gray-800 px-2 sm:text-sm">
        Contact
      </a>
    </div>
  </div>

  <div class="space-x-2 flex items-center">
    <div class="relative">
      <svg
        on:click={togglePopup}
        class="h-5 w-5 cursor-pointer"
        viewBox="0 0 20 20">
        <path
          d="M13.962,8.885l-3.736,3.739c-0.086,0.086-0.201,0.13-0.314,0.13S9.686,12.71,9.6,12.624l-3.562-3.56C5.863,8.892,5.863,8.611,6.036,8.438c0.175-0.173,0.454-0.173,0.626,0l3.25,3.247l3.426-3.424c0.173-0.172,0.451-0.172,0.624,0C14.137,8.434,14.137,8.712,13.962,8.885
          M18.406,10c0,4.644-3.763,8.406-8.406,8.406S1.594,14.644,1.594,10S5.356,1.594,10,1.594S18.406,5.356,18.406,10
          M17.521,10c0-4.148-3.373-7.521-7.521-7.521c-4.148,0-7.521,3.374-7.521,7.521c0,4.147,3.374,7.521,7.521,7.521C14.148,17.521,17.521,14.147,17.521,10" />
      </svg>
      {#if showPopup}
        <div class="bg-transparent fixed inset-0 z-30" on:click={togglePopup} />
        <div
          class="absolute z-30 ml-3 mt-1 py-2 w-32 border divide-y shadow-sm
          rounded-md bg-white transform -translate-x-full">
          <a
            class="block px-4 py-1 text-gray-600 hover:bg-gray-200"
            href="/models/{modelId}">
            Profile
          </a>
          <a
            class="block px-4 py-1 text-gray-600 hover:bg-gray-200"
            href="/accounts/signout">
            Sign out
          </a>
        </div>
      {/if}
    </div>

    <div
      class="w-10 h-10 flex items-center justify-center shadow-md border-2
      border-indigo-500 rounded-full overflow-hidden">
      {#if profilePicture.image}
        <img
          src={profilePicture.image}
          alt="model profile"
          class="h-full w-full object-cover" />
      {:else}
        <svg class="fill-current text-gray-700 w-6 h-6" viewBox="0 0 20 20">
          <path
            d="M10,10.9c2.373,0,4.303-1.932,4.303-4.306c0-2.372-1.93-4.302-4.303-4.302S5.696,4.223,5.696,6.594C5.696,8.969,7.627,10.9,10,10.9z
            M10,3.331c1.801,0,3.266,1.463,3.266,3.263c0,1.802-1.465,3.267-3.266,3.267c-1.8,0-3.265-1.465-3.265-3.267C6.735,4.794,8.2,3.331,10,3.331z" />
          <path
            d="M10,12.503c-4.418,0-7.878,2.058-7.878,4.685c0,0.288,0.231,0.52,0.52,0.52c0.287,0,0.519-0.231,0.519-0.52c0-1.976,3.132-3.646,6.84-3.646c3.707,0,6.838,1.671,6.838,3.646c0,0.288,0.234,0.52,0.521,0.52s0.52-0.231,0.52-0.52C17.879,14.561,14.418,12.503,10,12.503z" />
        </svg>
      {/if}
    </div>
    <span class="text-xs capitalize sm:text-sm">{fullname}</span>
  </div>

</div>
