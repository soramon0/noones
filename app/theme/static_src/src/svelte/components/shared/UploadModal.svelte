<script lang="ts">
  import { scale, fade, fly } from 'svelte/transition';
  import { createEventDispatcher } from 'svelte';
  import { UIStore, UpdatesStore, PhotoStore } from '../../store/index';
  import Breadcrumb from './Breadcrumb.svelte';
  import SaveButton from './SaveButton.svelte';
  import CancelButton from './CancelButton.svelte';
  import SuccessNotifier from './SuccessNotifier.svelte';
  import ErrorNotifier from './ErrorNotifier.svelte';

  export let title: string;
  export let multiple: boolean = false;
  export let errorKey: string;

  $: updatesData = $UpdatesStore;
  $: photoData = $PhotoStore;
  $: UIData = $UIStore;

  const dispatch = createEventDispatcher();

  const toggleShow = () => {
    dispatch('show');
  };

  const onFileChange = ({ target }) => {
    const files = target.files;
    const file = files[0];

    // if multiple is false and we have a file dispatch file
    if (file && !multiple) {
      dispatch('file', file);
    }

    // if multiple is true and we have at laest one file dispatch files
    if (file && multiple) {
      dispatch('file', files);
    }
  };
</script>

<!-- Backdrop -->
<div
  transition:fade
  on:click={toggleShow}
  class="fixed inset-0 bg-black z-10 opacity-50" />

<!-- Upload Modal -->
<div
  transition:scale={{ delay: 150 }}
  class="max-w-2xl w-4/5 h-500 m-auto shadow-md fixed inset-0 bg-white z-30
  rounded-lg sm:1/2 "
  data-simplebar>

  <!-- Progress indicator -->
  <div
    class="border-4 border-indigo-400 overflow-hidden transform
    transition-transform duration-500 ease-out"
    style="transform: translateX({UIData.fileUploadPercentage === 0 ? -100 : 0}%)" />

  <div class="text-center py-4 border-b-2 border-gray-200">
    <p class="font-semibold sm:text-2xl">{title}</p>
  </div>

  <!-- Error Handling -->
  <ErrorNotifier
    errors={updatesData.errors}
    {errorKey}
    on:clearErrors={UpdatesStore.clearErrors.bind(this, errorKey)} />

  <div
    class="p-4 flex justify-center items-center bg-white border-b-2
    border-gray-200 ">
    <CancelButton on:click={toggleShow} fetching={UIData.fetching} />

    <input
      type="file"
      id="uploadFile"
      accept="image/*"
      class="ml-2 w-1 h-1 opacity-0 invisible"
      on:change={onFileChange}
      {multiple} />

    <SaveButton
      fetching={UIData.fetching}
      text="Upload New Photo"
      on:click={() => document.getElementById('uploadFile').click()} />
  </div>

  <div class="p-4">
    <p class="text-lg font-semibold">From Gallery</p>
    <div class="mt-4 flex flex-wrap justify-center sm:justify-start">
      {#each photoData.photos as photo, i}
        <div
          class="h-32 w-32 bg-gray-300 cursor-pointer mb-2 mr-2 border
          border-gray-300 hover:border-indigo-400 overflow-hidden">
          <img
            src={photo.image}
            class="w-full h-full object-cover hover:scale-125 transform
            transition-all duration-500 ease-out"
            alt="model gallery {i}" />
        </div>
      {:else}
        <p>Gallery Is Empty</p>
      {/each}
    </div>

    <!-- {#if showConfirmPictureUpload}
        <div
          transition:scale
          class="w-56 h-24 p-4 m-auto flex justify-evenly items-center fixed
          inset-0 bg-white z-40 rounded-lg shadow-md">
          <CancelButton on:click={toggleConfirmPictureUpload} />
          <SaveButton fetching={UIData.fetching} />
        </div>
      {/if} -->

  </div>
</div>
