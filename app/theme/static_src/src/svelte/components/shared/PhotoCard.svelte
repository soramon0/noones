<script>
  import { scale } from "svelte/transition";
  import { createEventDispatcher } from "svelte";
  import SaveButton from "./SaveButton";
  import CancelButton from "./CancelButton";

  export let photo;
  export let markText = "Mark as Profile Picture";
  let showConfirm = false;
  let showDropdown = false;
  const dispatch = createEventDispatcher();

  function toggleConfirm() {
    showConfirm = !showConfirm;
  }

  function toggleDropdown() {
    showDropdown = !showDropdown;
  }

  function onRemove(id) {
    dispatch("delete", id);
    toggleConfirm();
  }
</script>

<div class="px-1 mb-2 w-full h-64 sm:w-1/2 md:w-1/3 lg:w-1/4 sm:h-56">
  <div class="relative w-full h-full rounded-md ">
    <div
      on:click={toggleDropdown}
      class="absolute right-0 p-2 mt-2 mr-2 w-8 h-8 rounded-md bg-white
      cursor-pointer">
      <svg class="w-full h-full fill-current text-gray-600" viewBox="0 0 20 20">
        <path
          d="M19.404,6.65l-5.998-5.996c-0.292-0.292-0.765-0.292-1.056,0l-2.22,2.22l-8.311,8.313l-0.003,0.001v0.003l-0.161,0.161c-0.114,0.112-0.187,0.258-0.21,0.417l-1.059,7.051c-0.035,0.233,0.044,0.47,0.21,0.639c0.143,0.14,0.333,0.219,0.528,0.219c0.038,0,0.073-0.003,0.111-0.009l7.054-1.055c0.158-0.025,0.306-0.098,0.417-0.211l8.478-8.476l2.22-2.22C19.695,7.414,19.695,6.941,19.404,6.65z
          M8.341,16.656l-0.989-0.99l7.258-7.258l0.989,0.99L8.341,16.656z
          M2.332,15.919l0.411-2.748l4.143,4.143l-2.748,0.41L2.332,15.919z
          M13.554,7.351L6.296,14.61l-0.849-0.848l7.259-7.258l0.423,0.424L13.554,7.351zM10.658,4.457l0.992,0.99l-7.259,7.258L3.4,11.715L10.658,4.457z
          M16.656,8.342l-1.517-1.517V6.823h-0.003l-0.951-0.951l-2.471-2.471l1.164-1.164l4.942,4.94L16.656,8.342z" />
      </svg>

      {#if showDropdown}
        <div
          class="absolute z-20 right-0 mt-3 py-2 border divide-y shadow-sm
          rounded-md bg-white">
          <div
            on:click={toggleConfirm}
            class="flex items-center space-x-2 py-2 pl-2 pr-4 hover:bg-gray-200">
            <svg class="w-6 h-6 fill-current text-gray-600" viewBox="0 0 20 20">
              <path
                d="M16.471,5.962c-0.365-0.066-0.709,0.176-0.774,0.538l-1.843,10.217H6.096L4.255,6.5c-0.066-0.362-0.42-0.603-0.775-0.538C3.117,6.027,2.876,6.375,2.942,6.737l1.94,10.765c0.058,0.318,0.334,0.549,0.657,0.549h8.872c0.323,0,0.6-0.23,0.656-0.549l1.941-10.765C17.074,6.375,16.833,6.027,16.471,5.962z" />
              <path
                d="M16.594,3.804H3.406c-0.369,0-0.667,0.298-0.667,0.667s0.299,0.667,0.667,0.667h13.188c0.369,0,0.667-0.298,0.667-0.667S16.963,3.804,16.594,3.804z" />
              <path
                d="M9.25,3.284h1.501c0.368,0,0.667-0.298,0.667-0.667c0-0.369-0.299-0.667-0.667-0.667H9.25c-0.369,0-0.667,0.298-0.667,0.667C8.583,2.985,8.882,3.284,9.25,3.284z" />
            </svg>
            <span class="whitespace-no-wrap text-gray-600">Remove</span>
          </div>
          {#if !photo.inUse}
            <div
              class="flex items-center space-x-2 p-2 hover:bg-gray-200"
              on:click={() => dispatch('mark', photo.id)}>
              <svg
                class="w-6 h-6 fill-current text-gray-600"
                viewBox="0 0 20 20">
                <path
                  d="M10,10.9c2.373,0,4.303-1.932,4.303-4.306c0-2.372-1.93-4.302-4.303-4.302S5.696,4.223,5.696,6.594C5.696,8.969,7.627,10.9,10,10.9z
                  M10,3.331c1.801,0,3.266,1.463,3.266,3.263c0,1.802-1.465,3.267-3.266,3.267c-1.8,0-3.265-1.465-3.265-3.267C6.735,4.794,8.2,3.331,10,3.331z" />
                <path
                  d="M10,12.503c-4.418,0-7.878,2.058-7.878,4.685c0,0.288,0.231,0.52,0.52,0.52c0.287,0,0.519-0.231,0.519-0.52c0-1.976,3.132-3.646,6.84-3.646c3.707,0,6.838,1.671,6.838,3.646c0,0.288,0.234,0.52,0.521,0.52s0.52-0.231,0.52-0.52C17.879,14.561,14.418,12.503,10,12.503z" />
              </svg>
              <span class="whitespace-no-wrap text-gray-600">{markText}</span>
            </div>
          {/if}
        </div>
      {/if}

    </div>
    <img
      class="h-full w-full object-cover rounded-md"
      src={photo.image}
      alt="profile {photo.id}" />

    {#if showConfirm}
      <div
        transition:scale
        class="w-64 top-0 p-4 absolute z-40 bg-white rounded-lg shadow-md">
        <p class="text-gray-600">Are you sure?</p>
        <div class="mt-2 flex justify-between items-center">
          <CancelButton on:click={toggleConfirm} />
          <SaveButton text="Remove" on:click={() => onRemove(photo.id)} />
        </div>
      </div>
    {/if}
  </div>

</div>
