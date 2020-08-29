<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { fly, fade } from 'svelte/transition';
  import UpdateButton from '../shared/UpdateButton.svelte';
  import CancelButton from '../shared/CancelButton.svelte';
  import SuccessNotifier from '../shared/SuccessNotifier.svelte';
  import ErrorNotifier from '../shared/ErrorNotifier.svelte';
  import ChangeGalleryPicture from './ChangeGalleryPicture.svelte';

  export let photo;
  export let index: number;
  export let fetching: boolean;

  const disptach = createEventDispatcher();

  const handleUpdate = (target, photoId) => {
    const file = target.files[0];

    if (file) {
      disptach('update', { file, photoId });
    }
  };

  const handleResponseTagStateUI = (state) => {
    if (state && Object.keys(state).length > 0) {
      if (!state.accept && !state.decline) return 'bg-indigo-700';
      else if (state.accept) return 'bg-green-400';
      else if (state.decline) return 'bg-red-400';
    } else {
      return 'bg-indigo-700';
    }
  };
</script>

<div
  in:fly={{ x: 200, delay: index * 500 }}
  out:fade
  class="max-w-4xl mt-4 px-4 py-2 bg-white rounded-md">
  <ErrorNotifier
    errors={photo.errors}
    errorKey="image"
    on:clearErrors={() => disptach('clearErrors')} />
  <div class="mt-2 sm:flex">
    <div class="w-full h-64 rounded-lg overflow-hidden shadow-md sm:w-1/3">
      <img
        src={photo.image}
        class="w-full h-full object-cover"
        alt="model gallery {index}" />
    </div>
    <div class="w-full h-auto py-2 text-sm sm:text-base sm:w-4/6 sm:ml-4">
      <p class="text-gray-600">
        {#if photo.message}
          {photo.message}
        {:else}
          You can change this picture for the next 24 hours after that it will
          be either approved to declined by a stuff member. In case it was
          declined, we will inform you why that is the case.
        {/if}
      </p>
    </div>
  </div>

  <div class="mt-2 flex justify-between items-center">
    <span
      class="text-sm py-2 px-4 tracking-wide text-white rounded-lg sm:text-base {handleResponseTagStateUI(photo)}">
      {#if !photo.accept && !photo.decline}
        Pending
      {:else if photo.accept}Approved{:else if photo.decline}Declined{/if}
    </span>
    <div class="flex">
      <CancelButton
        text="Remove"
        {fetching}
        on:click={() => disptach('delete', photo.id)} />
      <UpdateButton
        {fetching}
        on:click={() => document.getElementById(`photo-${index}`).click()} />
      <input
        type="file"
        id="photo-{index}"
        accept="image/*"
        class="w-1 h-1 opacity-0 invisible"
        on:change={({ target }) => handleUpdate(target, photo.id)} />
    </div>
  </div>
</div>
