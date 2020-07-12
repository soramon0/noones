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
  class="max-w-4xl mt-4 pb-4 border-b">
  <ErrorNotifier
    errors={photo.errors}
    errorKey="image"
    on:clearErrors={() => disptach('clearErrors')} />
  <div class="mt-2 flex w-full h-64">
    <div class="w-1/3 h-full rounded-lg overflow-hidden shadow-md">
      <img
        src={photo.image}
        class="w-full h-full object-cover"
        alt="model gallery {index}" />
    </div>
    <div
      class="w-4/6 h-full px-4 py-2 flex flex-col justify-between text-xs
      sm:text-sm">
      <p class="text-gray-700">
        {#if photo.message}
          {photo.message}
        {:else}
          You can change this picture for the next 24 hours after that it will
          be either approved to declined by a stuff member. In case it was
          declined, we will inform you why that is the case.
        {/if}
      </p>
      <div class="flex justify-between items-center">
        <span
          class="py-2 px-4 tracking-wide text-white rounded-lg {handleResponseTagStateUI(photo)}">
          {#if !photo.accept && !photo.decline}
            Pending
          {:else if photo.accept}Approved{:else if photo.decline}Declined{/if}
        </span>
        <div class="space-x-4">
          <CancelButton
            type="button"
            text="Remove"
            {fetching}
            on:click={() => disptach('delete', photo.id)} />
          <UpdateButton
            type="button"
            {fetching}
            on:click={() => document
                .getElementById(`photo-${index}`)
                .click()} />
          <input
            type="file"
            id="photo-{index}"
            accept="image/*"
            class="w-1 h-1 opacity-0 invisible"
            on:change={({ target }) => handleUpdate(target, photo.id)} />
        </div>
      </div>
    </div>
  </div>
</div>
