<script>
  import { createEventDispatcher } from "svelte";
  import { fly, fade } from "svelte/transition";
  import SaveButton from "../shared/SaveButton";
  import UpdateButton from "../shared/UpdateButton";
  import CancelButton from "../shared/CancelButton";
  import SuccessNotifier from "../shared/SuccessNotifier";
  import ErrorNotifier from "../shared/ErrorNotifier";
  import ChangeGalleryPicture from "./ChangeGalleryPicture";

  export let photo;
  export let index;
  export let fetching;

  const disptach = createEventDispatcher();

  const handleUpdate = (target, photoId) => {
    const file = target.files[0];

    if (file) {
      disptach("update", { file, photoId });
    }
  };

  const handleResponseTagStateUI = state => {
    if (state && Object.keys(state).length > 0) {
      if (!state.accept && !state.decline) return "bg-indigo-700";
      else if (state.accept) return "bg-green-400";
      else if (state.decline) return "bg-red-400";
    } else {
      return "bg-indigo-700";
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
  <div class="mt-2 flex w-full">
    <div class="w-1/3 h-64 rounded-lg overflow-hidden shadow-md">
      <img
        src={photo.image}
        class="w-full h-full object-cover"
        alt="model gallery {index}" />
    </div>
    <div
      class="w-4/6 h-auto ml-4 py-2 flex flex-col justify-between text-sm
      sm:text-base">
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
    <div class="">
      <CancelButton
        type="button"
        text="Remove"
        {fetching}
        on:click={() => disptach('delete', photo.id)} />
      <button
        on:click={() => document.getElementById(`photo-${index}`).click()}
        disabled={fetching}
        class="ml-2 px-8 py-3 text-xs rounded-md tracking-wider bg-black
        text-white hover:bg-gray-900 transition-transform duration-200
        ease-in-out transform hover:scale-110 sm:w-auto sm:text-sm md:text-base {fetching ? 'bg-gray-700 cursor-not-allowed' : ''}">
        Update
      </button>
      <input
        type="file"
        id="photo-{index}"
        accept="image/*"
        class="w-1 h-1 opacity-0 invisible"
        on:change={({ target }) => handleUpdate(target, photo.id)} />
    </div>
  </div>
</div>
